from fastapi import FastAPI, HTTPException
import mysql.connector
from datetime import date

from src.config.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

app = FastAPI(
    title="People Counting API",
    description="API untuk mengambil data statistik pengunjung harian dari sistem Human Tracking.",
    version="1.0.0"
)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,       
            user=DB_USER,         
            password=DB_PASSWORD, 
            database=DB_NAME      
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error koneksi database: {err}")
        return None

@app.get("/")
def read_root():
    return {"message": "API People Counting aktif dan berjalan!"}

@app.get("/api/pengunjung/hari-ini")
def get_pengunjung_hari_ini():
    """Mengambil total pengunjung untuk hari ini."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Koneksi database gagal.")
    
    cursor = conn.cursor(dictionary=True)
    hari_ini = date.today()
    
    query = "SELECT tanggal, jumlah_masuk FROM log_pengunjung WHERE tanggal = %s"
    cursor.execute(query, (hari_ini,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if not result:
        return {"tanggal": str(hari_ini), "jumlah_masuk": 0}
        
    return result

@app.get("/api/pengunjung/riwayat")
def get_riwayat_pengunjung():
    """Mengambil seluruh riwayat data pengunjung harian (1 baris 1 hari)."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Koneksi database gagal.")
        
    cursor = conn.cursor(dictionary=True)
    
    # Mengambil data diurutkan dari tanggal terbaru
    query = "SELECT id, tanggal, jumlah_masuk FROM log_pengunjung ORDER BY tanggal DESC LIMIT 30"
    cursor.execute(query)
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return {
        "total_data": len(results),
        "data": results
    }