# Métodos SQL específicos de Estoque (3 camadas)
import sqlite3
from typing import Dict, List, Optional
from server.database.connection import connect_database, start_database
import datetime

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
        reserverd_inventory_amount,
        avaliable
        FROM products
        WHERE product_name = ?
    '''

    connection = connect_database()

    products_found_list = []

    try:
        cursor = connection.cursor()
        cursor.execute(sql, (product_name))
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
                    "reserverd_inventory_amount":line[9],
                    "avaliable":line[10]
                }
            )

        return products_found_list
    finally:
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
        reserverd_inventory_amount,
        avaliable
        FROM products
    '''

    connection = connect_database()

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
                    "reserverd_inventory_amount":line[9],
                    "avaliable":line[10],
                }
            )
        
        return products_list
    finally:
        connection.close()

def add_new_product(bar_code: int, product_name: str, price: float, product_batch: str, validity: datetime.datetime, weight_gram_unit: float, cabinet_shelf_id: int, total_inventory_amount: int) -> bool:
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

    connection = connect_database()

    try:
        cursor = connection.cursor()
        cursor.execute(sql, (bar_code,product_name,price,product_batch,validity,weight_gram_unit,cabinet_shelf_id,total_inventory_amount))
        connection.commit()
        print(f"\n[BANCO DE DADOS] PRODUTO {product_name} ADICIONADO AO CATÁLOGO COM SUCESSO!\n")
        return True
    except sqlite3.IntegrityError:
        print(f"\n[BANCO DE DADOS] ERRO: PESO {weight_gram_unit} OU DISPONIBILIDADE INFORMADA INCORRETAMENTE.\n\n")
        return False
    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO: PROBLEMA AO EFETUAR CADASTRO DE {product_name}: {error}")
        return False
    finally:
        connection.close()

def change_product_info(product_id,key_change,new_value) -> bool:
    '''
    INSERIR LÓGICA QUE ALTEAR INFORMAÇÕES DO PRODUTO COM BASE NO PRODUTO SELECIONADO
    PLO USUÁRIO, A PARTIR DO ID DO PRODUTO, OBTIDO NA BUSCA POR NOME OU POR LISTA
    '''
