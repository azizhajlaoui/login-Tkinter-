import tkinter as tk
from tkinter import messagebox
from auth import register_user, verify_login, reset_password
from ui_helpers import create_entry, clear_entries, switch_frames
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Function to generate a random verification code
def generate_verification_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


# Function to send the verification email with the code
def send_verification_email(to_email, verification_code):
    from_email = "azizhajlaoui2@gmail.com"  # Replace with your Gmail address
    from_password = "emox xfdo nbuw ipoz"  

    subject = "Password Reset Verification Code"
    body = f"Your verification code is: {verification_code}"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print(f"Verification email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Initialize Tkinter window
root = tk.Tk()
root.title("Login System")
root.geometry("300x400")

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

# Forgot Password functionality
def open_reset_window():
    reset_window = tk.Toplevel(root)
    reset_window.title("Reset Password")
    reset_window.geometry("300x200")

    tk.Label(reset_window, text="Enter Email for Verification:").pack()
    reset_email = tk.Entry(reset_window)
    reset_email.pack()

    # Generate a random verification code
    verification_code = generate_verification_code()

    def send_code():
        """Send verification code to the email."""
        email = reset_email.get()
        send_verification_email(email, verification_code)
        tk.Label(reset_window, text="Code sent! Enter it below:").pack()

        # Verification code entry
        verification_entry = tk.Entry(reset_window)
        verification_entry.pack()

        def verify_code():
            """Verify the entered code and reset password."""
            entered_code = verification_entry.get()

            if entered_code == verification_code:
                tk.Label(reset_window, text="Code verified! Enter new password:").pack()
                new_password_entry = tk.Entry(reset_window, show="*")
                new_password_entry.pack()

                def reset_new_password():
                    """Reset the user's password."""
                    new_password = new_password_entry.get()
                    email = reset_email.get()
                    messagebox.showinfo("Password Reset", reset_password(email, new_password))
                    reset_window.destroy()

                tk.Button(reset_window, text="Reset Password", command=reset_new_password).pack()
            else:
                messagebox.showerror("Error", "Invalid verification code!")

        tk.Button(reset_window, text="Verify Code", command=verify_code).pack()

    tk.Button(reset_window, text="Send Verification Code", command=send_code).pack()

tk.Button(login_frame, text="Forgot Password?", command=open_reset_window).pack()

# Register Button
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

# Start Tkinter main loop
root.mainloop()
