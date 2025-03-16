import sqlite3

# Connect to the database (creates file if it doesn't exist)
conn = sqlite3.connect("login_system.db")
cursor = conn.cursor()

# Create users table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")

conn.commit()
conn.close()
