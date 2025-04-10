import sqlite3
import bcrypt

DB_NAME = "login_system.db"

# Connect to database
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Sample users (username: password)
users = [
    ("user1", "password123"),
    ("user2", "securepass"),
    ("admin", "adminpass"),
    ("testuser", "test1234"),
    ("azizhajlaoui5@gmail.com","azizaziz"),
]

# Function to insert users with hashed passwords
for username, password in users:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        print(f"User {username} added successfully!")
    except sqlite3.IntegrityError:
        print(f"User {username} already exists!")

conn.commit()
conn.close()
