import sqlite3

def create_database():
    # Connect to SQLite database
    conn = sqlite3.connect('login_system.sqlite')
    cursor = conn.cursor()

    # Create the 'users' table for login functionality (added email)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Create the 'books' table to store book details
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    ''')

    # Insert some sample data into the 'users' table
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", ('admin', 'admin@example.com', 'password123'))
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", ('user1', 'user1@example.com', 'user123'))
    
    # Insert some sample data into the 'books' table
    cursor.execute("INSERT INTO books (title, author, genre, year) VALUES (?, ?, ?, ?)", ('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 1925))
    cursor.execute("INSERT INTO books (title, author, genre, year) VALUES (?, ?, ?, ?)", ('1984', 'George Orwell', 'Dystopian', 1949))
    cursor.execute("INSERT INTO books (title, author, genre, year) VALUES (?, ?, ?, ?)", ('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 1960))
    cursor.execute("INSERT INTO books (title, author, genre, year) VALUES (?, ?, ?, ?)", ('Moby-Dick', 'Herman Melville', 'Adventure', 1851))
    cursor.execute("INSERT INTO books (title, author, genre, year) VALUES (?, ?, ?, ?)", ('Pride and Prejudice', 'Jane Austen', 'Romance', 1813))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database and sample data created successfully!")

# Run the function to create the database and fill it with data
create_database()
