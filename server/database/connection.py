# Gerenciador de conexão e transações ACID (Commit/Rollback)

import sqlite3

DATABASE_NAME = "server/database/smart_market.db"

def connect_database() -> sqlite3.Connection:
    '''
    CRIA E RETORNA UMA CONEXÃO CONFIGURADA COM O SQLITE.

    TIMEOUT=10: AGUARDA 10 SEGUNDOS SE OUTRA THREAD ESTIVER ESCREVENDO NO BANCO.
    '''

    connection = sqlite3.connect(DATABASE_NAME, timeout=10)
    connection.execute("PRAGMA foreign_keys = ON;")
    
    return connection

def start_database() -> None:
    '''
    LÊ O ARQUIVO SCHEMA.SQL E CRIA TODA A ESTRUTURA DAS TABELAS DO BANCO DE DADOS
    '''
    connection = connect_database()

    try:
        cursor = connection.cursor()
        with open("server/database/schemas.sql", "r", encoding="utf-8") as schema_file:
            script_sql = schema_file.read()
        
        cursor.executescript(script_sql)
        connection.commit()
        print(f"\n[BANCO DE DADOS] BANCO DE DADOS {DATABASE_NAME} INICIALIZADO COM SUCESSO!\n")
    
    except sqlite3.Error as error:
        print(f"\n[BANCO DE DADOS] ERRO AO INICIALIZAR BANCO DE DADOS {DATABASE_NAME}: [{error}]")
    finally:
        connection.close()