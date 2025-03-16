import tkinter as tk
from tkinter import messagebox
from auth import register_user, verify_login,reset_password
from ui_helpers import create_entry, clear_entries, switch_frames
# Initialize Tkinter window
root = tk.Tk()
root.title("Login System")
root.geometry("300x300")

# ========== LOGIN FRAME ==========
login_frame = tk.Frame(root)

tk.Label(login_frame, text="Login", font=("Arial", 14, "bold")).pack()

login_username = create_entry(login_frame, "Username:")
login_password = create_entry(login_frame, "Password:", show_text="*")

def login():
    """Handles user login."""
    username = login_username.get()
    password = login_password.get()

    if verify_login(username, password):
        messagebox.showinfo("Login Success", f"Welcome {username}!")
        clear_entries(login_username, login_password)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

tk.Button(login_frame, text="Login", command=login).pack()
tk.Button(login_frame, text="Register", command=lambda: switch_frames(login_frame, register_frame)).pack()

login_frame.pack()

# ========== REGISTER FRAME ==========
register_frame = tk.Frame(root)

tk.Label(register_frame, text="Register", font=("Arial", 14, "bold")).pack()

reg_username = create_entry(register_frame, "Username:")
reg_password = create_entry(register_frame, "Password:", show_text="*")
reg_confirm_password = create_entry(register_frame, "Confirm Password:", show_text="*")

def register():
    """Handles user registration."""
    username = reg_username.get()
    password = reg_password.get()
    confirm_password = reg_confirm_password.get()

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    messagebox.showinfo("Registration", register_user(username, password))
    clear_entries(reg_username, reg_password, reg_confirm_password)

tk.Button(register_frame, text="Register", command=register).pack()
tk.Button(register_frame, text="Back to Login", command=lambda: switch_frames(register_frame, login_frame)).pack()

def open_reset_window():
    """Opens a new window for password reset."""
    reset_window = tk.Toplevel(root)
    reset_window.title("Reset Password")
    reset_window.geometry("300x200")

    tk.Label(reset_window, text="Enter Username:").pack()
    reset_username = tk.Entry(reset_window)
    reset_username.pack()

    tk.Label(reset_window, text="New Password:").pack()
    reset_password_entry = tk.Entry(reset_window, show="*")
    reset_password_entry.pack()

    def reset():
        """Handles password reset."""
        username = reset_username.get()
        new_password = reset_password_entry.get()
        messagebox.showinfo("Reset Password", reset_password(username, new_password))
        reset_window.destroy()

    tk.Button(reset_window, text="Reset Password", command=reset).pack()

# Add "Forgot Password?" button to login screen
tk.Button(login_frame, text="Forgot Password?", command=open_reset_window).pack()

# Start Tkinter main loop
root.mainloop()
