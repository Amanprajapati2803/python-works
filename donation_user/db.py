import mysql.connector
from tkinter import messagebox

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="blood_donation"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"{err}")
        return None