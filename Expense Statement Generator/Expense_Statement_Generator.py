import customtkinter as ctk
import tkinter.messagebox as tkmb
import sqlite3

# Setting up a database for user accounts
conn = sqlite3.connect("user_accounts.db")
cursor = conn.cursor()

# Create user table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    opening_balance REAL DEFAULT NULL,
    expenses TEXT DEFAULT '{}'
)
""")
conn.commit()

# GUI setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.cTk()
app.geometry("500x500")
app.title("Expense Statement Generator")

# Global frame setup for dynamic content display
main_frame = ctk.CTkFrame(app)
main_frame.pack(pady=20, padx=40, fill='both', expand= true)

def clear_main_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

def show_login():
    clear_main_frame()

    ctk.CTkLabel(main_frame, text='Please sign in to your account').pack(pady=12, padx=10)

    user_entry = ctk.CTkEntry(main_frame, placeholder_text="Username")
    user_entry.pack(pady=12, padx=10)

    user_pass = ctk.CTkEntry(main_frame, placeholder_text="Password", show="*")
    user_pass.pack(pady=12, padx=10)

    def login():
        username = user_entry.get()
        password = user_pass.get()
        user = cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()

        if user:
            tkmb.showinfo(title="Login Successful", message="You have logged in successfully.")
            if user[3] is None:  # Check if opening_balance is NULL
                show_first_time_setup(username)
            else:
                show_expense_manager(username)
        else:
            tkmb.showerror(title="Login Failed", message="Invalid Username or Password.")

    ctk.CTkButton(main_frame, text='Login', command=login).pack(pady=12, padx=10)

    ctk.CTkCheckBox(main_frame, text='Remember Me').pack(pady=12, padx=10)

    ctk.CTkLabel(main_frame, text="Don't have an account?", font=("Arial", 12)).pack(pady=5)

    ctk.CTkButton(main_frame, text="Sign Up", command=show_signup).pack(pady=5)

def show_signup():
    clear_main_frame()

    ctk.CTkLabel(main_frame, text="Create a New Account", font=("Arial", 20)).pack(pady=20)

    new_user_entry = ctk.CTkEntry(main_frame, placeholder_text="New Username")
    new_user_entry.pack(pady=12, padx=10)

    new_user_pass = ctk.CTkEntry(main_frame, placeholder_text="New Password", show="*")
    new_user_pass.pack(pady=12, padx=10)

    confirm_pass = ctk.CTkEntry(main_frame, placeholder_text="Confirm Password", show="*")
    confirm_pass.pack(pady=12, padx=10)

    def register_user():
        new_username = new_user_entry.get()
        new_password = new_user_pass.get()
        confirm_password = confirm_pass.get()

        if not new_username or not new_password or not confirm_password:
            tkmb.showwarning(title="Missing Information", message="Please fill out all fields.")
        elif new_password != confirm_password:
            tkmb.showerror(title="Password Mismatch", message="Passwords do not match.")
        else:
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
                conn.commit()
                tkmb.showinfo(title="Registration Successful", message="Account created successfully!")
                show_login()
            except sqlite3.IntegrityError:
                tkmb.showerror(title="Registration Failed", message="Username already exists. Please choose a different one.")

    ctk.CTkButton(main_frame, text="Register", command=register_user).pack(pady=20, padx=10)

    ctk.CTkButton(main_frame, text="Back to Login", command=show_login).pack(pady=5)

    