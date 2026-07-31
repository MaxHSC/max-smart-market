# Métodos SQL específicos de Estoque (3 camadas)
import sqlite3
from typing import Dict, List, Optional
from server.database.connection import connect_database, start_database
from datetime import datetime

#region ONLY READ
def get_shelf_id(product_id: int, cursor) -> int:
    sql = '''
        SELECT id, cabinet_shelf_id
        FROM products
        WHERE product_id = ?
    '''

    try:
        cursor.execute(sql, (product_id,))
        product_line = cursor.fetchone()

        product_shelf_id = product_line[1]
            
        return product_shelf_id
    
    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO NA BUSCA DO PRODUTO: [{error}]\n")
        return False


def get_product_info(product_id: int):
    sql = '''
        SELECT product_volume,
        product_weight,
        cabinet_shelf_id
        FROM products
        WHERE id = ?
    '''

    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql, (product_id,))
        list = cursor.fetchone()

        volume = list[0]
        weight = list[1]
        shelf = list[2]

        return volume, weight, shelf

    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO NA BUSCA DO PRODUTO: [{error}]\n")
        return False, False, False

    finally:
        if cursor:
            cursor.close()
        connection.close()
    

def search_product_name(product_name: str) -> List[Dict]:
    sql = '''
        SELECT id,
        bar_code,
        product_name,
        price,
        product_batch,
        validity,
        product_weight,
        cabinet_shelf_id,
        product_volume,
        reserved_volume_amount,
        avaliable
        FROM products
        WHERE product_name LIKE ?
    '''

    
    start_database()
    connection = connect_database()
    cursor = None

    products_found_list = []

    try:
        cursor = connection.cursor()
        cursor.execute(sql, (f"%{product_name}%",))
        lines = cursor.fetchall()

        for line in lines:
            products_found_list.append(
                {
                    "id":line[0],
                    "bar_code":line[1],
                    "product_name":line[2],
                    "price":line[3],
                    "product_batch":line[4],
                    "validity":line[5],
                    "product_weight":line[6],
                    "cabinet_shelf_id":line[7],
                    "product_volume":line[8],
                    "reserved_volume_amount":line[9],
                    "avaliable":line[10]
                }
            )
            
        return products_found_list
    
    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO NA BUSCA DO PRODUTO: [{error}]\n")
        return []
    finally:
        if cursor:
            cursor.close()
        connection.close()

def list_all_products() -> List[Dict]: #RETURN LIST WITH ALL PRODUCTS TO BUY (CLIENT) OR EDIT (MANAGER/STOCKER)
    sql = '''
        SELECT id,
        bar_code,
        product_name,
        price,
        product_batch,
        validity,
        product_weight,
        cabinet_shelf_id,
        product_volume,
        reserved_volume_amount,
        avaliable
        FROM products
    '''

    start_database()
    connection = connect_database()
    cursor = None

    products_list = []

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        lines = cursor.fetchall()

        for line in lines:
            products_list.append(
                {
                    "id":line[0],
                    "bar_code":line[1],
                    "product_name":line[2],
                    "price":line[3],
                    "product_batch":line[4],
                    "validity":line[5],
                    "product_weight":line[6],
                    "cabinet_shelf_id":line[7],
                    "product_volume":line[8],
                    "reserved_volume_amount":line[9],
                    "avaliable":line[10],
                }
            )
        
        return products_list
    
    finally:
        if cursor:
            cursor.close()
        connection.close()
#endregion

#region MANAGE DATABASE
def add_new_product(bar_code: int, product_name: str, price: float, product_batch: str, validity: str, product_weight: float, cabinet_shelf_id: int, product_volume: int, shelf_new_weight: float, shelf_new_volume: int) -> bool:
    sql_product = '''
        INSERT INTO products (
        bar_code,
        product_name,
        price,
        product_batch,
        validity,
        product_weight,
        cabinet_shelf_id,
        product_volume
        )
        VALUES (?,?,?,?,?,?,?,?)
    '''

    sql_shelf = '''
        UPDATE shelfs
        SET current_weight_grams = ?,
            current_volume = ?
        WHERE id = ?
    '''

    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(sql_shelf, (shelf_new_weight,shelf_new_volume,cabinet_shelf_id))
        cursor.execute(sql_product, (bar_code,product_name,price,product_batch,validity,product_weight,cabinet_shelf_id,product_volume))

        connection.commit()
        print(f"\n[BANCO DE DADOS] PRODUTO {product_name} ADICIONADO AO CATÁLOGO COM SUCESSO!\n")
        return True
    
    except sqlite3.IntegrityError:
        connection.rollback()
        print(f"\n[BANCO DE DADOS] PESO {product_weight} OU DISPONIBILIDADE INFORMADA INCORRETAMENTE.\n\n")
        return False
    
    except sqlite3.Error as error:
        connection.rollback()
        print(f"\n[BANCO DE DADOS] PROBLEMA AO EFETUAR CADASTRO DE {product_name}: {error}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        connection.close()

def change_product_info(product_id,selected_column,new_value,command=None,shelf_id=None,shelf_new_weight=None,shelf_new_volume=None) -> bool:
    '''
    INSERIR LÓGICA QUE ALTERA INFORMAÇÕES DO PRODUTO COM BASE NO PRODUTO SELECIONADO
    PELO USUÁRIO, A PARTIR DO ID DO PRODUTO, OBTIDO NA BUSCA POR NOME OU POR LISTA
    '''
    sql_product = f'''
        UPDATE products SET {selected_column} = ? WHERE id = ?;
    '''
    sql_shelf = '''
        UPDATE shelfs
        SET current_weight_grams = ?,
            current_volume = ?
        WHERE id = ?
    '''
    
    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()

        if command:
            cursor.execute(sql_shelf, (shelf_new_weight,shelf_new_volume,shelf_id))
        cursor.execute(sql_product, (new_value, product_id))

        connection.commit()
        print(f"\n[BANCO DE DADOS] PRODUTO ATUALIZADO COM SUCESSO\n")
        return True
    
    except sqlite3.IntegrityError:
        connection.rollback()
        print(f"\n[BANCO DE DADOS] NÃO É POSSÍVEL INSERIR O VALOR INFORMADO [VALOR INVÁLIDO].\n\n")
        return False
    
    except sqlite3.Error as error:
        connection.rollback()
        print(f"\n[BANCO DE DADOS] NÃO FOI POSSÍVEL ATUALIZAR AS INFORMAÇÕES DO PRODUTO: {error}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        connection.close()

def reserve_cart(cart: list) -> bool:
    '''
    AFTER CLIENT CONFIRM THE ORDER, MODELS SEND THE CART TO SUSPEND THE AMOUNT OF PRODUCTS IN CART BY PUT IT INTO ANOTHER TABLE (RESERVED STOCK), OTHERS CLIENTES CAN KEEPING SELECTING THE LEFT PRODUCTS FROM REAL STOCK - RESERVED STOCK
    '''
    sql = '''
        INSERT INTO reservation (
        user_id,
        product_id,
        amount_reserved,
        expires_time)
        VALUES (:user_id,:id,:product_volume,:expires_time)
    '''
    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql, cart[1:])

        connection.commit()
        print(f"\n[BANCO DE DADOS RESERVA] COMPRA REGISTRADA. AGUARDANDO CONFIRMAÇÃO DE PAGAMENTO.\n")

        return True

    except sqlite3.IntegrityError:
            connection.rollback()
            print(f"\n[BANCO DE DADOS RESERVA] NÚMERO DO PEDIDO INCONSISTENTE.\n")
            return False
        
    except sqlite3.Error as error:
        connection.rollback()
        print(f"\n[BANCO DE DADOS] PROBLEMA AO EFETUAR REGISTRO DE COMPRA: {error}\n")
        return False
    
    finally:
        if cursor:
            cursor.close()
        connection.close()



def conclude_checkout_cart(cart: list, shelfs_new_values: list) -> bool:
    '''cart ALWAYS MUST TO BE RECEIVED AS A LIST OF DICT WITH ID AND VOLUME TO BE BOUGHT
    [
        {
            "id":19,
            "product_volume":3
        },
    ]
    AND SEND WITH NEW STOCK VALUES AND CART DICT
    [
        {"id":19,
        "new_product_volume":3,
        "cabinet_shelf_id":5,
        "new_shelf_weight":15.0,
        "new_shelf_volume":15
        },
    ]
    '''
    
    sql_products = '''
        UPDATE products
        SET product_volume = :new_product_volume
        WHERE id = :id
    '''

    sql_shelfs = '''
        UPDATE shelfs
        SET current_weight_grams = :new_shelf_weight,
            current_volume = :new_shelf_volume
        WHERE id = :cabinet_shelf_id
    '''

    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.executemany(sql_shelfs, shelfs_new_values)

        for prod in cart:
            cursor.execute(sql_products, prod)

            if cursor.rowcount == 0:
                connection.rollback()
                print(f"\n[BANCO DE DADOS - CHEKOUT] UM OU MAIS ITENS SEM ESTOQUE SUFICIENTE. VENDA CANCELADA. [{prod['id']}]\n")
                return False

        connection.commit()
        print(f"\n[BANCO DE DADOS - CHEKOUT] VENDA CONFIRMADA COM SUCESSO, PODE RECOLHER SEUS PRODUTOS.\n")
        return True

    except (sqlite3.Error, ValueError) as error:
        connection.rollback()
        print(f"\n[BANCO DE DADOS - CHEKOUT] VENDA NÃO EFETUADA: {error}\n")
        return False

    finally:
        if cursor:
            cursor.close()
        connection.close()

#endregion