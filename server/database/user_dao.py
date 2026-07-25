# Métodos SQL específicos de Usuários e Penalizações

import sqlite3
from typing import Dict, List, Optional
from server.database.connection import connect_database

def check_document_already_exists(document: str) -> bool: #VERIFICA SE O CPF JÁ ESTÁ CADASTRADO
    sql = '''
        SELECT 1
        FROM users 
        WHERE document = ?
        LIMIT 1
    '''

    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql, (document,))
        exists = cursor.fetchone()

        if exists:
            return True
        
        return False
    
    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO NO BANCO DE DADOS: {error}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        connection.close()


def check_phone_already_exists(phone_number: str) -> bool: #VERIFICA SE O TELEFONE JÁ ESTÁ CADASTRADO
    sql = '''
        SELECT 1 
        FROM users 
        WHERE phone_number = ?
        LIMIT 1
    '''

    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql, (phone_number,))
        exists = cursor.fetchone()

        if exists:
            return True
        
        return False
    
    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO NO BANCO DE DADOS: {error}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        connection.close()


def new_user(username: str, document: str, phone_number: str, pass_key: str, type_user: str) -> bool:
    '''
    INSERIR UM NOVO USUÁRIO NO BANCO DE DADOS
    '''
    sql = '''
        INSERT INTO users (username, document, phone_number, pass_key, type_user)
        VALUES (?, ?, ?, ?, ?)
    '''
    connection = connect_database()
    cursor = None
    
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (username, document, phone_number, pass_key, type_user.upper()))
        connection.commit()
        print(f"\n[BANCO DE DADOS] USUÁRIO {username} CADASTRADO NO BANCO DE DADOS COM SUCESSO!\n")
        return True
    
    except sqlite3.IntegrityError:
        print(f"\n[BANCO DE DADOS] ERRO: CPF {document} OU TIPO DE USUÁRIO INVÁLIDO")
        return False
    
    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO: PROBLEMA AO EFETUAR CADASTRO DE {username}: {error}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        connection.close()


def search_user_document(document: str) -> Optional[Dict]:
    sql = '''
        SELECT id, username, document, phone_number, type_user, created_time, blocked_until, consecutive_cancel
        FROM users
        WHERE document = ?
    '''
    
    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql, (document,))
        line = cursor.fetchone()

        if line:
            return {
                "id": line[0],
                "username": line[1],
                "document": line[2],
                "phone_number": line[3],
                "type_user": line[4],
                "created_time": line[5],
                "blocked_until": line[6],
                "consecutive_cancel": line[7],
            }

        return None
    
    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO AO CONSULTAR USUÁRIO: {error}\n")
        return None

    finally:
        if cursor:
            cursor.close()
        connection.close()


def list_all_users() -> List[Dict]:
    sql = '''
        SELECT id, username, document, phone_number, type_user, created_time
        FROM users 
    '''

    connection = connect_database()
    cursor = None
    
    users_list = []

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        lines = cursor.fetchall()

        for line in lines:
            users_list.append(
                {
                "id": line[0],
                "username": line[1],
                "document": line[2],
                "phone_number": line[3],
                "type_user": line[4],
                "created_time": line[5],
                }
            )

        return users_list
    
    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO AO CONSULTAR USUÁRIO: {error}\n")
        return []

    finally:
        if cursor:
            cursor.close()
        connection.close()

def confirm_login_user(phone_login: str, pass_key: str):
    sql = '''
        SELECT id, username, phone_number, pass_key, type_user, blocked_until
        FROM users
        WHERE phone_number = ?
        LIMIT 1
    '''

    connection = connect_database()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql,(phone_login))
        line = cursor.fetchone()

        if line:
            if pass_key == line[3]:
                user_info = {
                    "id":line[0],
                    "username":line[1],
                    "phone_number":line[2],
                    "type_user":line[4],
                    "blocked_until":line[5]
                }
                
                return user_info
            return False

    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO AO CONSULTAR USUÁRIO: {error}\n")
        return False

    finally:
        if cursor:
            cursor.close()
        connection.close()