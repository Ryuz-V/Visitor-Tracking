import os
from dotenv import load_dotenv

load_dotenv()

# Database Config
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "db_tracking")

# Camera Config
CAMERA_SOURCE = os.getenv("CAMERA_SOURCE", "0")

# Pastikan CAMERA_SOURCE menjadi integer jika isinya angka (untuk Webcam)
if CAMERA_SOURCE.isdigit():
    CAMERA_SOURCE = int(CAMERA_SOURCE)