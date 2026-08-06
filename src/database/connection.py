import mysql.connector
from src.config.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"[Error] Gagal terhubung ke MySQL: {err}")
        return None