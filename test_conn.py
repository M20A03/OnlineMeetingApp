# test_conn.py
import mysql.connector
from db_config import DB_CONFIG

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    print("Connected! MySQL server version:", conn.get_server_info())
    conn.close()
except Exception as e:
    print("Connection failed:", e)
