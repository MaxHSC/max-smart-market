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


def get_product_real_stock_info(body_payload: dict) -> dict | None:
    sql_product = '''
        SELECT id,
        bar_code,
        product_name,
        price,
        product_batch,
        validity,
        product_weight,
        shelf_id,
        product_volume,
        avaliable
        FROM products
        WHERE id = :product_id;
    '''

    start_database()
    connection = connect_database()
    cursor = None
    product_info = {}

    try:
        cursor = connection.cursor()
        cursor.execute(sql_product, body_payload)
        line = cursor.fetchone()
        
        product_info = {
            "product_id":line[0],
            "bar_code":line[1],
            "product_name":line[2],
            "price":line[3],
            "product_batch":line[4],
            "validity":line[5],
            "product_weight":line[6],
            "shelf_id":line[7],
            "product_volume":line[8],
            "avaliable":line[9]
        }

        return product_info

    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO NA BUSCA DO PRODUTO: [{error}]\n")
        return None

    finally:
        if cursor:
            cursor.close()
        connection.close()


def get_product_reserved_stock_info(body_payload: dict):
    sql_order = '''
        SELECT product_id,
            SUM(reserved_volume)
        FROM orders
        WHERE product_id = :product_id
            AND reserve_status = "PENDENTE"
        GROUP BY product_id;
    '''

    start_database()
    connection = connect_database()
    cursor = None
    reserved_info = {}

    try:
        cursor = connection.cursor()
        cursor.execute(sql_order, body_payload)
        order_line = cursor.fetchone()

        reserved_info = {
            "product_id":order_line[0],
            "reserved_volume":order_line[1],
        }

        return reserved_info

    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO NA BUSCA DO PRODUTO: [{error}]\n")
        return None

    finally:
        if cursor:
            cursor.close()
        connection.close()

def get_last_order_number() -> int:
    sql_reserve = '''
        SELECT MAX(order_number)
        FROM orders;
    '''
    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql_reserve)
        last_order = cursor.fetchone()

        if not last_order[0]:
            last_order = 0
        
        return last_order
    
    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO NA CONSULTA DE ORDENS DE COMPRAS: [{error}]\n")
        return 0
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

def list_all_products() -> tuple: #RETURN LIST WITH ALL PRODUCTS IN STOCK AND THE RESERVED PRODUTCS TO MODELS DO THE MATHS
    sql_stock = '''
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
    sql_reserved = '''
        SELECT product_id,
        SUM(amount_reserved)
        FROM orders
        WHERE reserve_status = "PENDENTE"
        GROUP BY product_id
    '''

    start_database()
    connection = connect_database()
    cursor = None

    products_stock = []
    products_reserved = {}

    try:
        cursor = connection.cursor()
        cursor.execute(sql_stock)
        lines = cursor.fetchall()

        for line in lines:
            products_stock.append(
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

        cursor.execute(sql_reserved)
        lines = cursor.fetchall()

        for line in lines:
            products_reserved[line[0]] = line[1]
        
        return products_stock, products_reserved
    
    finally:
        if cursor:
            cursor.close()
        connection.close()


def get_products_prices(products_prices_list: list) -> dict:
    sql_product = '''
        SELECT id,
        price
        FROM products
        WHERE id = :product_id
    '''

    start_database()
    connection = connect_database()
    cursor = None
    products_prices_dict = {}

    try:
        cursor = connection.cursor()
        cursor.executemany(sql_product, products_prices_list)
        lines = cursor.fetchall()

        for line in lines:
            products_prices_dict[line[0]] = line[1]
        
        return products_prices_dict
    
    
    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO NA BUSCA DO PRODUTO: [{error}]\n")
        return {}

    finally:
        if cursor:
            cursor.close()
        connection.close()



#endregion

#region MANAGE DATABASE
def add_new_product(new_product_dict: dict, update_shelf_dict: dict) -> bool:
    sql_product = '''
        INSERT INTO products (
        bar_code,
        product_name,
        price,
        product_batch,
        validity,
        product_weight,
        shelf_id,
        product_volume
        )
        VALUES (:bar_code,:product_name,:price,:product_batch,:validity,:product_weight,:shelf_id,:product_volume)
    '''

    sql_shelf = '''
        UPDATE shelfs
        SET current_weight_grams = :current_weight_grams,
            current_volume = :current_volume
        WHERE id = :id
    '''

    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(sql_shelf, update_shelf_dict)
        cursor.execute(sql_product, new_product_dict)

        connection.commit()
        print(f"\n[BANCO DE DADOS] PRODUTO {new_product_dict["product_name"]} ADICIONADO AO CATÁLOGO COM SUCESSO!\n")
        return True
    
    except sqlite3.IntegrityError:
        connection.rollback()
        print(f"\n[BANCO DE DADOS] PESO {new_product_dict["product_weight"]} OU DISPONIBILIDADE INFORMADA INCORRETAMENTE.\n\n")
        return False
    
    except sqlite3.Error as error:
        connection.rollback()
        print(f"\n[BANCO DE DADOS] PROBLEMA AO EFETUAR CADASTRO DE {new_product_dict["product_name"]}: {error}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        connection.close()

def change_product_info(update_product_dict: dict, update_shelf_dict: dict | None = None) -> bool:
    '''
    INSERIR LÓGICA QUE ALTERA INFORMAÇÕES DO PRODUTO COM BASE NO PRODUTO SELECIONADO
    PELO USUÁRIO, A PARTIR DO ID DO PRODUTO, OBTIDO NA BUSCA POR NOME OU POR LISTA
    '''
    column = update_product_dict["column_to_change"]
    sql_product = f'''
        UPDATE products
        SET product_name = :product_name,
            price = :price,
            product_volume = :product_volume,
            available = :available
        WHERE id = :product_id;
    '''
    sql_shelf = '''
        UPDATE shelfs
        SET current_weight_grams = :current_weight_grams,
            current_volume = :current_volume
        WHERE id = :id;
    '''
    
    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()

        if update_shelf_dict is not None:
            cursor.execute(sql_shelf, update_shelf_dict)
        cursor.execute(sql_product, update_product_dict)

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


def expires_order(body_payload: dict) -> bool:
    sql_expires = '''
        UPDATE orders
        SET reserve_status = "EXPIRADA"
        WHERE order_number = :order_number
    '''

    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql_expires, body_payload)

        connection.commit()
        print(f"\n[BANCO DE DADOS] PRAZO DE ORDEM DE COMPRA EXPIRADO.\n")
        return True
    
    except sqlite3.IntegrityError:
        connection.rollback()
        print(f"\n[BANCO DE DADOS] INFORMAÇÃO INVÁLIDADA AO ALTERAR STATUS DA ORDEM DE COMRPA.\n\n")
        return False
    
    except sqlite3.Error as error:
        connection.rollback()
        print(f"\n[BANCO DE DADOS] NÃO FOI POSSÍVEL CANCELAR A ORDEM DE COMPRA: {error}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        connection.close()


def cancel_order(body_payload: dict) -> bool:
    sql_cancel = '''
        UPDATE orders
        SET reserve_status = "CANCELADA"
        WHERE order_number = :order_number
    '''

    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql_cancel, body_payload)

        connection.commit()
        print(f"\n[BANCO DE DADOS] ORDEM DE COMPRA CANCELADA.\n")
        return True
    
    except sqlite3.IntegrityError:
        connection.rollback()
        print(f"\n[BANCO DE DADOS] INFORMAÇÃO INVÁLIDADA AO ALTERAR STATUS DA ORDEM DE COMRPA.\n\n")
        return False
    
    except sqlite3.Error as error:
        connection.rollback()
        print(f"\n[BANCO DE DADOS] NÃO FOI POSSÍVEL CANCELAR A ORDEM DE COMPRAS: {error}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        connection.close()


def restore_order(body_payload: dict) -> dict | None:
    '''
    AFTER GATEWAY CONFIRM THE PAYMENT, IT WILL RETURN THIS CONFIRMATION WITH THE RELATED ORDER NUMBER, MODELS WILL REQUEST FOR THE ORDER RESTAURATION TO PROCEED WITH THE SOTCK REDUCE AND WITHDRAWAL ON CABINETS
    '''
    sql_restore = '''
        SELECT total_order_price,
        product_id,
        reserved_volume,
        created_time,
        expires_time
        FROM orders
        WHERE order_number = :order_number;
    '''

    start_database()
    connection = connect_database()
    cursor = None

    products_id_list = []
    try:
        cursor = connection.cursor()
        cursor.execute(sql_restore, body_payload)
        lines = cursor.fetchall()

        for line in lines:
            products_id_list.append(
                {
                    "product_id":line[1],
                    "requested_volume":line[2],
                }
            )
        order_restored = {
            "total_order_price": lines[0][0],
            "items": products_id_list,
            "created_time": lines[0][3],
            "expires_time": lines[0][4]
        }
        
        return order_restored
    
    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO AO RECUPERAR ORDEM DE COMPRAS: [{error}]\n")
        return None
    finally:
        if cursor:
            cursor.close()
        connection.close()


def reserve_order(order: list) -> bool:
    '''
    AFTER CLIENT CONFIRM THE ORDER, MODELS SEND THE ORDER TO THE RESERVED TABLE WITH THE ORDER NUMBER THE AMOUNT OF PRODUCTS (ONE LINE FOR EACH PRODUTC) AND CLIENT ID, OTHERS CLIENTES CAN KEEPING SELECTING THE LEFT PRODUCTS FROM THE (REAL STOCK - RESERVED STOCK)
    '''
    sql = '''
        INSERT INTO orders (
        order_number,
        user_id,
        total_order_price,
        product_id,
        product_unit_price,
        product_total_price,
        reserved_volume,
        created_time,
        expires_time)
        VALUES (:order_number,:user_id,:total_order_price,:product_id,:product_unit_price,:product_total_price,:product_volume,:created_time,:expires_time)
    '''
    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.executemany(sql, order)

        connection.commit()
        print(f"\n[BANCO DE DADOS ORDEM DE COMPRA] PEDIDO REGISTRADO. AGUARDANDO CONFIRMAÇÃO DE PAGAMENTO.\n")

        return True

    except sqlite3.IntegrityError:
            connection.rollback()
            print(f"\n[BANCO DE DADOS ORDEM DE COMPRA] NÚMERO DO PEDIDO INCONSISTENTE.\n")
            return False
        
    except sqlite3.Error as error:
        connection.rollback()
        print(f"\n[BANCO DE DADOS ORDEM DE COMPRA] PROBLEMA AO EFETUAR PEDIDO DE COMPRA: {error}\n")
        return False
    
    finally:
        if cursor:
            cursor.close()
        connection.close()



def conclude_checkout_order(order_list: list[dict], new_shelfs_values: list[dict]) -> bool:
    '''order ALWAYS MUST TO BE RECEIVED AS A LIST OF DICT WITH ID AND VOLUME TO BE BOUGHT
    [
        {
            "product_id":19,
            "product_volume":3
        },
    ]
    AND SEND WITH NEW STOCK VALUES AND ORDER DICT
    [
        {"product_id":19,
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
        WHERE id = :product_id
    '''

    sql_shelfs = '''
        UPDATE shelfs
        SET current_weight_grams = :new_shelf_weight,
            current_volume = :new_shelf_volume
        WHERE id = :shelf_id
    '''
    sql_order = '''
        UPDATE orders
        SET reserve_status = "CONCLUIDA"
        WHERE order_number = :order_number
    '''

    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.executemany(sql_shelfs, new_shelfs_values)

        cursor.execute(sql_order, (order_list[0],))

        for product in order_list:
            cursor.execute(sql_products, product)

            if cursor.rowcount == 0:
                connection.rollback()
                print(f"\n[BANCO DE DADOS - CHEKOUT] UM OU MAIS ITENS SEM ESTOQUE SUFICIENTE. VENDA CANCELADA. [{product['product_id']}]\n")
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