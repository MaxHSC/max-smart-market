# Métodos SQL específicos de Usuários e Penalizações

import sqlite3
from typing import Dict, List, Optional
from server.database.connection import conect_database

def new_user(username: str, document: str, type_user: str) -> bool:
    '''
    INSERIR UM NOVO USUÁRIO NO BANCO DE DADOS
    '''
    sql = '''
        INSERT INTO users (username, document, type_user)
        VALUES (?, ?, ?)
    '''
    connection = conect_database()
    
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (username, document, type_user.upper()))
        connection.commit()
        print(f"\n[BANCO DE DADOS] USUÁRIO {username} CADASTRADO NO BANCO DE DADOS COM SUCESSO!\n")
        return True
    except sqlite3.IntegrityError:
        print(f"\n[BANCO DE DADOS] ERRO: CPF {document} OU TIPO DE USUÁRIO INVÁLIDO")
        return False
    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO: PROBLEMA AO EFETUAR CADASTRO DE {username}")
        return False
    finally:
        connection.close()