import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import *
from tkmacosx import Button

# Database connection function (SQLite3)
def connection():
    conn = sqlite3.connect('login_system.sqlite')  # Connect to the SQLite database
    return conn

# Function to refresh the Treeview (display books in the table)
def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)

    for array in read_books():
        my_tree.insert(parent='', index='end', iid=array[0], text="", values=(array), tag="orow")

    my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))
    my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=10, pady=20)

# Function to read books from the database
def read_books():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    results = cursor.fetchall()
    conn.close()
    return results

# Add a new book to the database
def add_book():
    title = str(title_entry.get())
    author = str(author_entry.get())
    genre = str(genre_entry.get())
    year = str(year_entry.get())

    if not title or not author or not genre or not year:
        messagebox.showinfo("Error", "All fields must be filled")
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO books (title, author, genre, year) VALUES (?, ?, ?, ?)",
                           (title, author, genre, year))
            conn.commit()
            conn.close()
            title_entry.delete(0, END)
            author_entry.delete(0, END)
            genre_entry.delete(0, END)
            year_entry.delete(0, END)
        except:
            messagebox.showinfo("Error", "An error occurred while adding the book.")
            return

    refreshTable()

# Update an existing book
def update_book():
    selected_item = my_tree.selection()[0]
    book_id = my_tree.item(selected_item)['values'][0]

    title = str(title_entry.get())
    author = str(author_entry.get())
    genre = str(genre_entry.get())
    year = str(year_entry.get())

    if not title or not author or not genre or not year:
        messagebox.showinfo("Error", "All fields must be filled")
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE books SET title=?, author=?, genre=?, year=? WHERE book_id=?",
                           (title, author, genre, year, book_id))
            conn.commit()
            conn.close()
            title_entry.delete(0, END)
            author_entry.delete(0, END)
            genre_entry.delete(0, END)
            year_entry.delete(0, END)
        except:
            messagebox.showinfo("Error", "An error occurred while updating the book.")
            return

    refreshTable()

# Delete a selected book
def delete_book():
    selected_item = my_tree.selection()[0]
    book_id = my_tree.item(selected_item)['values'][0]

    decision = messagebox.askquestion("Warning", "Are you sure you want to delete this book?")
    if decision != "yes":
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE book_id=?", (book_id,))
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "An error occurred while deleting the book.")
            return

    refreshTable()

# Function to open the Library Window after successful login
def open_library_window():
    global my_tree
    global title_entry, author_entry, genre_entry, year_entry

    library_frame = tk.Frame(root)

    # Labels and Entries for Book Management
    title_label = Label(library_frame, text="Title", font=('Arial', 12))
    title_label.grid(row=0, column=0, padx=10, pady=10)
    title_entry = Entry(library_frame, font=('Arial', 12))
    title_entry.grid(row=0, column=1, padx=10, pady=10)

    author_label = Label(library_frame, text="Author", font=('Arial', 12))
    author_label.grid(row=1, column=0, padx=10, pady=10)
    author_entry = Entry(library_frame, font=('Arial', 12))
    author_entry.grid(row=1, column=1, padx=10, pady=10)

    genre_label = Label(library_frame, text="Genre", font=('Arial', 12))
    genre_label.grid(row=2, column=0, padx=10, pady=10)
    genre_entry = Entry(library_frame, font=('Arial', 12))
    genre_entry.grid(row=2, column=1, padx=10, pady=10)

    year_label = Label(library_frame, text="Year", font=('Arial', 12))
    year_label.grid(row=3, column=0, padx=10, pady=10)
    year_entry = Entry(library_frame, font=('Arial', 12))
    year_entry.grid(row=3, column=1, padx=10, pady=10)

    # Buttons for CRUD operations
    add_button = Button(library_frame, text="Add Book", font=('Arial', 12), command=add_book)
    add_button.grid(row=4, column=0, padx=10, pady=10)

    update_button = Button(library_frame, text="Update Book", font=('Arial', 12), command=update_book)
    update_button.grid(row=4, column=1, padx=10, pady=10)

    delete_button = Button(library_frame, text="Delete Book", font=('Arial', 12), command=delete_book)
    delete_button.grid(row=4, column=2, padx=10, pady=10)

    # Treeview for displaying books
    my_tree = ttk.Treeview(library_frame)
    my_tree["columns"] = ("Book ID", "Title", "Author", "Genre", "Year")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Book ID", anchor=W, width=100)
    my_tree.column("Title", anchor=W, width=200)
    my_tree.column("Author", anchor=W, width=150)
    my_tree.column("Genre", anchor=W, width=100)
    my_tree.column("Year", anchor=W, width=100)

    my_tree.heading("Book ID", text="Book ID", anchor=W)
    my_tree.heading("Title", text="Title", anchor=W)
    my_tree.heading("Author", text="Author", anchor=W)
    my_tree.heading("Genre", text="Genre", anchor=W)
    my_tree.heading("Year", text="Year", anchor=W)

    my_tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    refreshTable()

    library_frame.pack(padx=20, pady=20)

# Tkinter Login Window
def login_user():
    username_or_email = username_entry.get()
    password = password_entry.get()

    conn = connection()
    cursor = conn.cursor()

    # Check if the entered value is a username or email
    cursor.execute("SELECT * FROM users WHERE username=? OR email=?", (username_or_email, username_or_email))
    result = cursor.fetchone()

    if result and result[3] == password:  # result[3] corresponds to the 'password' column
        messagebox.showinfo("Success", "Login successful!")
        login_frame.destroy()
        open_library_window()
    else:
        messagebox.showerror("Error", "Invalid username/email or password")

# Tkinter Sign-Up Window
def signup_user():
    def create_account():
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()

        if not username or not password or not email:
            messagebox.showinfo("Error", "All fields must be filled")
            return

        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Account created successfully!")
            signup_frame.destroy()
            login_frame.pack(padx=20, pady=20)
        except Exception as e:
            messagebox.showinfo("Error", f"An error occurred: {str(e)}")

    signup_frame = tk.Frame(root)
    username_label = Label(signup_frame, text="Username", font=('Arial', 12))
    username_label.grid(row=0, column=0, padx=50, pady=10)
    username_entry = Entry(signup_frame, font=('Arial', 12))
    username_entry.grid(row=0, column=1, padx=50, pady=10)

    password_label = Label(signup_frame, text="Password", font=('Arial', 12))
    password_label.grid(row=1, column=0, padx=50, pady=10)
    password_entry = Entry(signup_frame, font=('Arial', 12), show='*')
    password_entry.grid(row=1, column=1, padx=50, pady=10)

    email_label = Label(signup_frame, text="Email", font=('Arial', 12))
    email_label.grid(row=2, column=0, padx=50, pady=10)
    email_entry = Entry(signup_frame, font=('Arial', 12))
    email_entry.grid(row=2, column=1, padx=50, pady=10)

    signup_button = Button(signup_frame, text="Create Account", font=('Arial', 12), command=create_account)
    signup_button.grid(row=3, column=0, columnspan=2, pady=20)

    signup_frame.pack(padx=20, pady=20)

# Tkinter Root (Main Window)
root = tk.Tk()
root.title("Library Management System")
root.geometry("800x600")

# Login Frame
login_frame = tk.Frame(root)

login_label = Label(login_frame, text="Login", font=("Arial", 18, "bold"))
login_label.grid(row=0, column=0, padx=50, pady=20)

username_label = Label(login_frame, text="Username or Email", font=('Arial', 12))
username_label.grid(row=1, column=0, padx=50, pady=10)
username_entry = Entry(login_frame, font=('Arial', 12))
username_entry.grid(row=1, column=1, padx=50, pady=10)

password_label = Label(login_frame, text="Password", font=('Arial', 12))
password_label.grid(row=2, column=0, padx=50, pady=10)
password_entry = Entry(login_frame, font=('Arial', 12), show='*')
password_entry.grid(row=2, column=1, padx=50, pady=10)

login_button = Button(login_frame, text="Login", font=('Arial', 12), command=login_user)
login_button.grid(row=3, column=0, columnspan=2, pady=20)

signup_button = Button(login_frame, text="Sign Up", font=('Arial', 12), command=signup_user)
signup_button.grid(row=4, column=0, columnspan=2, pady=20)

login_frame.pack(padx=20, pady=20)

root.mainloop()
