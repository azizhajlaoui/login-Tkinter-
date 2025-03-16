import sqlite3
import bcrypt

DB_NAME = "login_system.db"

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def register_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    hashed_password = hash_password(password)
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        return "Registration successful!"
    except sqlite3.IntegrityError:
        return "Username already exists!"

def verify_login(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
        return True
    return False
def reset_password(username, new_password):
    """Resets a user's password if the username exists."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result:
        hashed_password = hash_password(new_password)
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
        conn.commit()
        conn.close()
        return "Password reset successful!"
    else:
        conn.close()
        return "Username not found!"
