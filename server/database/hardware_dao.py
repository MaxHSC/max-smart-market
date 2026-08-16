# MÉTODO SQL ESPECIFICO PARA CONFIGURAÇÃO DOS HARDWARES (CRIAÇÃO DE TABLES DE ARMÁRIOS COM CRIAÇÃO DE
# HARDWARE COM ID, CAPACIDADE DE PRATELEIRAS E QUANTIDADE DE PRATELEIRAS ATUAIS; CRIAÇÃO DE
# TABLES DE PRATELEIRAS COM CRIAÇÃO DE HARDWARE COM ID, CAPACIDADE DE PESO, CAPACIDADE DE
# VOLUME, ARMÁRIO EM QUE ESTÁ INSTALADO) APENAS PARA CONFIGURAÇÃO DO PRÓPRIO HARDWARE
# DEFINIÇÃO DE PESO E VOLUMES ATUAIS SERÁ REALIZADA POR INVENTORY_DAO, AO INSERIR OU REMOVER PRODUTOS.

import sqlite3
from typing import Dict, List, Optional
from server.database.connection import connect_database, start_database

def add_new_cabinet(cabinet_info: dict) -> bool:
    sql = '''
        INSERT INTO cabinets (
        mac_address,
        tcp_port
        )
        VALUES (:hardware_mac_address,:hardware_tcp_port)
    '''

    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql, cabinet_info)
        connection.commit()
        print(f"\n[BANCO DE DADOS - HARDWARE] NOVO ARMÁRIO INTELIGENTE VINCULADO COM SUCESSO.\n")
        return True
    
    except sqlite3.IntegrityError:
        connection.rollback()
        print(f"\n[BANCO DE DADOS - HARDWARE] JÁ EXISTE UM ARMÁRIO INSTALADO COM O MESMO MAC.")
        return False

    except sqlite3.Error as error:
        connection.rollback()
        print(f"\n[BANCO DE DADOS - HARDWARE] PROBLEMA AO VINCULAR NOVO ARMÁRIO INTELIGENTE: [{error}]")
        return False

    finally:
        if cursor:
            cursor.close()
        connection.close()

def list_all_cabinets() -> List[Dict]:
    sql = '''
        SELECT id,
        shelf_capacity,
        current_installed_shelf,
        mac_address,
        tcp_port
        FROM cabinets
    '''

    start_database()
    connection = connect_database()
    cursor = None

    cabinet_list = []

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        cabinets = cursor.fetchall()

        for cabinet in cabinets:
            cabinet_list.append(
                {
                    "id":cabinet[0],
                    "shelf_capacity": cabinet[1],
                    "current_installed_shelf":cabinet[2],
                    "hardware_mac_address":cabinet[3],
                    "hardware_tcp_port":cabinet[4],
                }
            )
        return cabinet_list

    except sqlite3.Error as error:
        connection.rollback()
        print(f"\n[BANCO DE DADO - HARDWARE] ERRO AO BUSCAR ARMÁRIOS: [{error}]")
        return []

    finally:
        if cursor:
            cursor.close()
        connection.close()


def get_cabinet_info(cabinet_id: int) -> dict:
    sql = '''
        SELECT id,
        shelf_capacity,
        current_installed_shelf,
        mac_address,
        ip_address,
        tcp_port
        FROM cabinets
        WHERE id = ?
    '''

    start_database()
    connection = connect_database()
    cursor = None

    cabinet_info = {}

    try:
        cursor = connection.cursor()
        cursor.execute(sql, (cabinet_id,))
        cabinet = cursor.fetchone()

        cabinet_info = {
            "id": cabinet[0],
            "shelf_capacity": cabinet[1],
            "current_installed_shelf": cabinet[2],
            "hardware_mac_address":cabinet[3],
            "hardware_current_ip_address":cabinet[4],
            "hardware_tcp_port":cabinet[5],
        }

        return cabinet_info
    
    except sqlite3.Error as error:
        connection.rollback()
        print(f"\n[BANCO DE DADO] ERRO AO BUSCAR ARMÁRIO: [{error}]")
        return {}

    finally:
        if cursor:
            cursor.close()
        connection.close()


def add_new_shelf(shelf_info: dict, cabinet_id: int) -> bool:
    sql_create_shelf = '''
        INSERT INTO shelfs (
        installed_cabinet_id,
        mac_address,
        tcp_port
        )
        VALUES (:installed_cabinet_id,:hardware_mac_address,:hardware_tcp_port)
    '''

    sql_update_cabinet = '''
        UPDATE cabinets
        SET current_installed_shelf = COALESCE(current_installed_shelf, 0) + 1
        WHERE id = ?
            AND COALESCE(current_installed_shelf, 0) < shelf_capacity
    '''

    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql_update_cabinet, (cabinet_id,))

        if cursor.rowcount == 0:
            connection.rollback()
            print(f"\n[BANCO DE DADOS - HARDWARE] ARMÁRIO [{cabinet_id}] ATINGIU A CAPACIDADE MÁXIMA DE PRATELEIRAS INSTALADAS.\n")
            return False
        
        cursor.execute(sql_create_shelf, shelf_info)
        connection.commit()
        print(f"\n[BANCO DE DADOS - HARDWARE] PRATELEIRA VINCULADA AO ARMÁRIO INTELIGENTE [{cabinet_id}] COM SUCESSO.\n")
        return True

    except sqlite3.IntegrityError:
        if connection:
            connection.rollback()
        print(f"\n[BANCO DE DADOS - HARDWARE] JÁ EXISTE UMA PRATELEIRA INSTALADA COM O MESMO MAC.")
        return False

    except sqlite3.Error as error:
        if connection:
            connection.rollback()
        print(f"\n[BANCO DE DADO - HARDWARE] NÃO FOI POSSÍVEL VINCULAR PRATELEIRA: [{error}]")
        return False

    finally:
        if cursor:
            cursor.close()
        connection.close()

def list_all_installed_shelf() -> List[Dict]:
    sql = '''
        SELECT id,
        installed_cabinet_id,
        weight_capacity_grams,
        volume_capacity,
        current_weight_grams,
        current_volume,
        mac_address,
        tcp_port
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
                    "installed_cabinet_id":shelf[1],
                    "weight_capacity_grams":shelf[2],
                    "volume_capacity":shelf[3],
                    "current_weight_grams":shelf[4],
                    "current_volume":shelf[5],
                    "hardware_mac_address":shelf[6],
                    "hardware_tcp_port":shelf[7],
                }
            )
        
        return installed_shelf_list
    
    except sqlite3.Error as error:
        connection.rollback()
        print(f"\n[BANCO DE DADO - HARDWARE] ERRO AO BUSCAR PRATELEIRAS: [{error}]")
        return []

    finally:
        if cursor:
            cursor.close()
        connection.close()

def get_shelf_info(shelf_id: int) -> Dict:
    sql= '''
        SELECT id,
        installed_cabinet_id,
        weight_capacity_grams,
        volume_capacity,
        current_weight_grams,
        current_volume,
        mac_address,
        ip_address,
        tcp_port
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
        shelf = cursor.fetchone()

        shelf_info = {
            "id": shelf[0],
            "installed_cabinet_id": shelf[1],
            "weight_capacity_grams": shelf[2],
            "volume_capacity": shelf[3],
            "current_weight_grams": shelf[4],
            "current_volume": shelf[5],
            "hardware_mac_address":shelf[6],
            "hardware_current_ip_address":shelf[7],
            "hardware_tcp_port":shelf[8],
        }

        return shelf_info
    
    except sqlite3.Error as error:
        connection.rollback()
        print(f"\n[BANCO DE DADO] ERRO AO BUSCAR PRATELEIRA: [{error}]")
        return {}

    finally:
        if cursor:
            cursor.close()
        connection.close()
    

def remove_cabinet(cabinet_id: int):
    sql_cabinet = '''
        DELETE FROM cabinets
        WHERE id = ?
            AND current_installed_shelf = 0
    '''

    start_database()
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql_cabinet, (cabinet_id,))
        connection.commit()
        print("\n[BANCO DE DADOS - HARDWARE] ARMÁRIO REMOVIDO COM SUCESSO.")
        
        return True
    
    except sqlite3.IntegrityError:
        connection.rollback()
        print(f"\n[BANCO DE DADOS - HARDWARE] NÃO É POSSÍVEL REMOVER ARMÁRIO COM PRATELEIRAS INSTALADAS. REALIZE A REMOÇÃO DAS PRATELEIRAS PRIMEIRO.")

    except sqlite3.Error as error:
        connection.rollback()
        print(f"\n[BANCO DE DADOS - HARDWARE] NÃO FOI POSSIVEL REMOVER O ARMARIO: [{error}]")
        return False
    finally:
        if cursor:
            cursor.close()
        connection.close()
                

def remove_shelf(shelf_id: int, installed_cabinet_id: int, new_cabinet_installed_shelfs: int):
        sql_shelf = '''
            DELETE FROM shelfs
            WHERE id = ?
                AND current_volume = 0
        '''
        sql_cabinet = '''
            UPDATE cabinets
            SET current_installed_shelf = ?
            WHERE id = ?
        '''

        start_database()
        connection = connect_database()
        cursor = None

        try:
            cursor = connection.cursor()
            cursor.execute(sql_shelf, (shelf_id,))
            cursor.execute(sql_cabinet, (installed_cabinet_id, new_cabinet_installed_shelfs))
            connection.commit()
            print("\n[BANCO DE DADOS - HARDWARE] PRATELEIRA REMOVIDA COM SUCESSO.")
            
            return True
        
        except sqlite3.IntegrityError:
            connection.rollback()
            print(f"\n[BANCO DE DADOS - HARDWARE] NÃO É POSSÍVEL REMOVER PRATELEIRA COM PRODUTOS REGISTRADOS. REALIZE A REMOÇÃO DOS PRODUTOS PRIMEIRO.")

        except sqlite3.Error as error:
            connection.rollback()
            print(f"\n[BANCO DE DADOS - HARDWARE] NÃO FOI POSSIVEL REMOVER A PRATELEIRA: [{error}]")
            return False
        finally:
            if cursor:
                cursor.close()
            connection.close()


# def test_new_cabinet():
#     for i in range(3):
#         add_new_cabinet()

#     cabinet_list = list_all_cabinets()

#     for i in cabinet_list:
#         print(f"\n[BANCO DE DADOS TESTE] ARMÁRIO INTELIGENTE\n")
#         print(f"[BANCO DE DADOS TESTE] ID [{i["id"]}]")
#         print(f"[BANCO DE DADOS TESTE] CAPACIDADE [{i["shelf_capacity"]}]")
#         print(f"[BANCO DE DADOS TESTE] PRATELEIRAS INSTALADAS [{i["current_installed_shelf"]}]\n")

#     pass

# def test_new_shelf():
#     for i in range(4):
#         add_new_shelf(1)

#     for i in range(5):
#         add_new_shelf(2)

#     for i in range(6):
#         add_new_shelf(3)


#     shelf_list = list_all_installed_shelf()

#     for i in shelf_list:
#         print(f"\n[BANCO DE DADOS TESTE] PRATELEIRAS BALANÇA")
#         print(f"[BANCO DE DADOS TESTE] ID [{i["id"]}]")
#         print(f"[BANCO DE DADOS TESTE] INSTALADO NO ARMÁRIO ID [{i["installed_cabinet_id"]}]")
#         print(f"[BANCO DE DADOS TESTE] CAPACIDADE TOTAL DE PESO [{i["weight_capacity_grams"]}]")
#         print(f"[BANCO DE DADOS TESTE] CAPACIDADE TOTAL DE VOLUMES [{i["volume_capacity"]}]")
#         print(f"[BANCO DE DADOS TESTE] PESO ATUAL [{i["current_weight_grams"]}]")
#         print(f"[BANCO DE DADOS TESTE] VOLUME ATUAL [{i["current_volume"]}]\n")
        
#     pass

    # "id":shelf[0],
    # "installed_cabinet_id":shelf[1],
    # "weight_capacity_grams":shelf[2],
    # "volume_capacity":shelf[3],
    # "current_weight_grams":shelf[4],
    # "current_volume":shelf[5],