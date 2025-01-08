import customtkinter as ctk
import tkinter.messagebox as tkmb
import sqlite3

# Setting up a database for user accounts
conn = sqlite3.connect("user_accounts.db")
cursor = conn.cursor()

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