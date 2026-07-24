# Métodos SQL específicos de Estoque (3 camadas)
import sqlite3
from typing import Dict, List, Optional
from server.database.connection import connect_database, start_database
from datetime import datetime

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
    sql = '''
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
    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql, (bar_code,product_name,price,product_batch,validity,weight_gram_unit,cabinet_shelf_id,total_inventory_amount))
        connection.commit()
        print(f"\n[BANCO DE DADOS] PRODUTO {product_name} ADICIONADO AO CATÁLOGO COM SUCESSO!\n")
        return True
    
    except sqlite3.IntegrityError:
        print(f"\n[BANCO DE DADOS] PESO {weight_gram_unit} OU DISPONIBILIDADE INFORMADA INCORRETAMENTE.\n\n")
        return False
    
    except sqlite3.Error as error:
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