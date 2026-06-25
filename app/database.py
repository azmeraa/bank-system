import sqlite3

def get_connection():
    conn = sqlite3.connect("bank.db")
    conn.row_factory = sqlite3.Row   # ✅ IMPORTANT FIX
    return conn