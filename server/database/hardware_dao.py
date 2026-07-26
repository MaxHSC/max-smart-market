# MÉTODO SQL ESPECIFICO PARA CONFIGURAÇÃO DOS HARDWARES (CRIAÇÃO DE TABLES DE ARMÁRIOS COM CRIAÇÃO DE
# HARDWARE COM ID, CAPACIDADE DE PRATELEIRAS E QUANTIDADE DE PRATELEIRAS ATUAIS; CRIAÇÃO DE
# TABLES DE PRATELEIRAS COM CRIAÇÃO DE HARDWARE COM ID, CAPACIDADE DE PESO, CAPACIDADE DE
# VOLUME, ARMÁRIO EM QUE ESTÁ INSTALADO) APENAS PARA CONFIGURAÇÃO DO PRÓPRIO HARDWARE
# DEFINIÇÃO DE PESO E VOLUMES ATUAIS SERÁ REALIZADA POR INVENTORY_DAO, AO INSERIR OU REMOVER PRODUTOS.

import sqlite3
from typing import Dict, List, Optional
from server.database.connection import connect_database, start_database

def add_new_cabinet() -> bool:
    sql = '''
        INSERT INTO cabinets (
        current_shelf_installed
        )
        VALUES (0)
    '''

    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        print(f"\n[BANCO DE DADOS] NOVO ARMÁRIO INTELIGENTE VINCULADO COM SUCESSO.\n")
        return True
        
    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] PROBLEMA AO VINCULAR NOVO ARMÁRIO INTELIGENTE: [{error}]")
        return False

    finally:
        if cursor:
            cursor.close()
        connection.close()

def add_new_shelf(installed_cabinet_id: int) -> bool:
    sql_create_shelf = '''
        INSERT INTO shelfs (
        installed_cabinet_id
        )
        VALUES (?)
    '''

    sql_update_cabinet = '''
        UPDATE cabinets
        SET current_installed_shelf = COALESCE(current_installed_shelf, 0) + 1
        WHERE id = ?
            AND COALESCE(current_insatlled_shelf, 0) < shelf_capacity
    '''

    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql_create_shelf, (installed_cabinet_id,))
        cursor.execute(sql_update_cabinet, (installed_cabinet_id,))
        connection.commit()
        print(f"\n[BANCO DE DADOS] PRATELEIRA VINCULADA AO ARMÁRIO INTELIGENTE [{installed_cabinet_id}] COM SUCESSO.\n")
        return True
    
    except sqlite3.Error as error:
        connection.rollback()
        print(f"\n[BANCO DE DADO] NÃO FOI POSSÍVEL VINCULAR PRATELEIRA: [{error}]")
        return False

    finally:
        if cursor:
            cursor.close()
        connection.close()

def list_all_installed_shelf():
    sql = '''
        SELECT id,
        installed_cabinet_id,
        weight_capacity_grams,
        inventory_capacity,
        current_weight_grams,
        current_inventory
        FROM shelfs
    '''

    start_database()
    connection = connect_database()
    cursor = None

    installed_shelf_list = []
    
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        shelfs = cursor.fetchall()

        for shelf in shelfs:
            installed_shelf_list.append(
                {
                    "id":shelf[0],
                    "installed_cabinet_id":shelf[0],
                    "weight_capacity_grams":shelf[1],
                    "inventory_capacity":shelf[2],
                    "current_weight_grams":shelf[3],
                    "current_inventory":shelf[4],
                }
            )
        
        return installed_shelf_list

    finally:
        if cursor:
            cursor.close()
        connection.close()

def search_shelf_id(shelf_id: int) -> Dict:
    sql= '''
        SELECT id,
        installed_cabinet_id,
        weight_capacity_grams,
        inventory_capacity,
        current_weight_grams,
        current_inventory
        FROM shelfs
        WHERE id = ?
    '''

    start_database()
    connection = connect_database()
    cursor = None

    shelf_info = {}

    try:
        cursor = connection.cursor()
        cursor.execute(sql, (shelf_id,))
        shelf = cursor.fetchone

        shelf_info = {
            "id": shelf[0],
            "installed_cabinet_id": shelf[1],
            "weight_capacity_grams": shelf[2],
            "inventory_capacity": shelf[3],
            "current_weight_grams": shelf[4],
            "current_inventory": shelf[5],
        }

        return shelf_info

    finally:
        if cursor:
            cursor.close()
        connection.close()

