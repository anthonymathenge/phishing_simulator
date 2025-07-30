import sqlite3

DB_PATH = "phishing.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id TEXT PRIMARY KEY,
            email TEXT,
            opened BOOLEAN DEFAULT 0,
            clicked BOOLEAN DEFAULT 0,
            submitted BOOLEAN DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def store_user(user_id: str, email: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO interactions (id, email) VALUES (?, ?)", (user_id, email))
    conn.commit()
    conn.close()

def update_interaction(user_id: str, column: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"UPDATE interactions SET {column} = 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
