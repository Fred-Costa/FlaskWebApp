import mysql.connector
from mysql.connector import connection, errorcode

configuracao_DB = {
    'user': 'root',
    'password': 'Curso123',
    'host': '127.0.0.1',
    'database': 'db_app_flask'
}

try:
    conn = connection.MySQLConnection(**configuracao_DB)
except mysql.connector.Error as erro:
    if erro.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("User ou password inválidos!")
    elif erro.errno == errorcode.ER_BAD_DB_ERROR:
        print("A base de dados não existe!")
    else:
        print(erro)

print("Ligação bem sucedida...")