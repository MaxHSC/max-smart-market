# Métodos SQL específicos de Estoque (3 camadas)
import sqlite3
from typing import Dict, List, Optional
from server.database.connection import connect_database, start_database
from datetime import datetime

def get_shelf_id(product_id: int, cursor) -> int:
    sql = '''
        SELECT id, cabinet_shelf_id
        FROM products
        WHERE product_id = ?
    '''

    try:
        cursor.execute(sql, (product_id,))
        product_line = cursor.fetchone()

        product_shelf_id = product_line[7]
            
        return product_shelf_id
    
    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO NA BUSCA DO PRODUTO: [{error}]\n")
        return False
    

def search_product_name(product_name: str) -> List[Dict]:
    sql = '''
        SELECT id,
        bar_code,
        product_name,
        price,
        product_batch,
        validity,
        weight_gram_unit,
        cabinet_shelf_id,
        total_inventory_amount,
        reserved_inventory_amount,
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
                    "weight_gram_unit":line[6],
                    "cabinet_shelf_id":line[7],
                    "total_inventory_amount":line[8],
                    "reserved_inventory_amount":line[9],
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
        weight_gram_unit,
        cabinet_shelf_id,
        total_inventory_amount,
        reserved_inventory_amount,
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
                    "weight_gram_unit":line[6],
                    "cabinet_shelf_id":line[7],
                    "total_inventory_amount":line[8],
                    "reserved_inventory_amount":line[9],
                    "avaliable":line[10],
                }
            )
        
        return products_list
    
    finally:
        if cursor:
            cursor.close()
        connection.close()

def add_new_product(bar_code: int, product_name: str, price: float, product_batch: str, validity: str, weight_gram_unit: float, cabinet_shelf_id: int, total_inventory_amount: int) -> bool:
    sql_product = '''
        INSERT INTO products (
        bar_code,
        product_name,
        price,
        product_batch,
        validity,
        weight_gram_unit,
        cabinet_shelf_id,
        total_inventory_amount
        )
        VALUES (?,?,?,?,?,?,?,?)
    '''

    sql_shelf = '''
        UPDATE shelfs
        SET current_weight_grams = COALESCE(current_weight_grams, 0) + (?*?),
            current_inventory = COALESCE(current_inventory, 0) + (?)
        WHERE id = ?
            AND COALESCE(current_weight_grams, 0) + (?*?) <= weight_capacity_grams
            AND COALESCE(current_inventory, 0) + (?) <= inventory_capacity
    '''

    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql_shelf, (weight_gram_unit,total_inventory_amount,total_inventory_amount,cabinet_shelf_id,weight_gram_unit,total_inventory_amount,total_inventory_amount))

        if cursor.rowcount == 0:
            connection.rollback()
            print(f"\n[BANCO DE DADOS] NÃO FOI POSSÍVEL ADICIONAR O(S) PRODUTO(S) NA PRATELEIRA {cabinet_shelf_id}, CAPACIDADE DE PESO OU VOLUMES ATINGIU O LIMITE. TENTE OUTRA PRATELEIRA.\n")
            return False

        cursor.execute(sql_product, (bar_code,product_name,price,product_batch,validity,weight_gram_unit,cabinet_shelf_id,total_inventory_amount))
        connection.commit()
        print(f"\n[BANCO DE DADOS] PRODUTO {product_name} ADICIONADO AO CATÁLOGO COM SUCESSO!\n")
        return True
    
    except sqlite3.IntegrityError:
        connection.rollback()
        print(f"\n[BANCO DE DADOS] PESO {weight_gram_unit} OU DISPONIBILIDADE INFORMADA INCORRETAMENTE.\n\n")
        return False
    
    except sqlite3.Error as error:
        connection.rollback()
        print(f"\n[BANCO DE DADOS] PROBLEMA AO EFETUAR CADASTRO DE {product_name}: {error}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        connection.close()

def change_product_info(product_id,selected_column,new_value) -> bool:
    '''
    INSERIR LÓGICA QUE ALTERA INFORMAÇÕES DO PRODUTO COM BASE NO PRODUTO SELECIONADO
    PLO USUÁRIO, A PARTIR DO ID DO PRODUTO, OBTIDO NA BUSCA POR NOME OU POR LISTA
    '''
    sql = f'''
    UPDATE products SET {selected_column} = ? WHERE id = ?;
    '''
    
    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql, (new_value, product_id))
        connection.commit()
        print(f"\n[BANCO DE DADOS] PRODUTO ATUALIZADO COM SUCESSO\n")
        return True
    
    except sqlite3.IntegrityError:
        print(f"\n[BANCO DE DADOS] NÃO É POSSÍVEL INSERIR O VALOR INFORMADO [VALOR INVÁLIDO].\n\n")
        return False
    
    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] NÃO FOI POSSÍVEL ATUALIZAR AS INFORMAÇÕES DO PRODUTO: {error}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        connection.close()

def checkout_cart(cart: list) -> bool: #cart ALWAYS MUST TO BE A LIST OF DICT [{"id":19,"amount":3}]
    sql_products = '''
        UPDATE products
        SET total_inventory_amount = total_inventory_amount - :amount
        WHERE id = :id
        AND total_inventory_amount >= :amount
    '''

    sql_shelfs = '''
        UPDATE shelfs
        SET current_weight_grams = COALESCE(current_weight_grams, 0) - (?*?),
            current_inventory = COALESCE(current_inventory, 0) - (?)
        WHERE id = ?
            AND COALESCE(current_weight_grams, 0) - (?*?) >= 0
            AND COALESCE(current_inventory, 0) - (?) >= 0
        '''
    
    

    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()

        for prod in cart:
            shelf_id: int = get_shelf_id(prod["id"],cursor)
            prod_weight = prod["weight_gram_unit"]
            prod_amount = prod["amount"]
            cursor.execute(sql_shelfs, (prod_weight,prod_amount,prod_amount,shelf_id,prod_weight,prod_amount,prod_amount,))
            if cursor.rowcount == 0:
                connection.rollback()
                print(f"\n[BANCO DE DADOS - CHEKOUT] ERRO AO REMOVER PRODUTOS DAS PRATELEIRAS. VENDA CANCELADA.\n")
                return False

        cursor.executemany(sql_products, cart)

        if cursor.rowcount != len(cart):
            connection.rollback()
            raise ValueError("\n[BANCO DE DADOS - CHEKOUT] UM OU MAIS ITENS SEM ESTOQUE SUFICIENTE.\n")

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