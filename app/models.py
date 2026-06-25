from app.database import get_connection


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # 👤 USERS TABLE (UPDATED)
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        balance REAL DEFAULT 0,
        is_admin INTEGER DEFAULT 0
    )
    """)

    # =========================
    # 💰 TRANSACTIONS TABLE
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        transaction_type TEXT NOT NULL,
        amount REAL NOT NULL,
        balance_after REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()