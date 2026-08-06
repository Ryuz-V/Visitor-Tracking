from datetime import date
from src.database.connection import get_connection

def catat_pengunjung(jumlah=1):
    conn = get_connection()
    if not conn:
        return
        
    try:
        cursor = conn.cursor()
        hari_ini = date.today()
        
        sql = """
            INSERT INTO log_pengunjung (tanggal, jumlah_masuk) 
            VALUES (%s, %s) 
            ON DUPLICATE KEY UPDATE jumlah_masuk = jumlah_masuk + %s
        """
        cursor.execute(sql, (hari_ini, jumlah, jumlah))
        conn.commit()
    except Exception as err:
        print(f"[Error Database] Gagal mencatat: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()