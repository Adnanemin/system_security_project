import sqlite3

DB_NAME ="auction.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE
    )               
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS auctions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        commit_deadline TEXT,
        reveal_deadline TEXT,
        status TEXT
    )               
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS commits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        auction_id INTEGER,
        commitment TEXT,
        timestamp TEXT,
        UNIQUE(user_id, auction_id)
    )               
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reveals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        auction_id INTEGER,
        bid INTEGER,
        salt TEXT,
        valid INTEGER
    )               
    """)
    
    conn.commit()
    conn.close()