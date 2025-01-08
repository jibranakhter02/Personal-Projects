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