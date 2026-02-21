import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, Frame
import mysql.connector


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="vital_drop"
    )


def view_donor_table(parent, back_callback):

    for widget in parent.winfo_children():
        widget.destroy()

    def go_back():
        back_callback(parent)

    # ---------- HEADER ----------
    top_frame = ctk.CTkFrame(parent, corner_radius=10)
    top_frame.pack(fill="x", padx=20, pady=20)

    ctk.CTkLabel(
        top_frame,
        text="All Donors",
        fg_color="#2a9d8f",
        text_color="white",
        font=("Segoe UI", 18, "bold")
    ).pack(fill="x", padx=20, pady=20)

    ctk.CTkButton(
        top_frame,
        text="← Back",
        fg_color="#6c757d",
        command=go_back
    ).pack(pady=(0,10))

    
    table_container = ctk.CTkFrame(parent)
    table_container.pack(fill="both", expand=True, padx=20, pady=(0,20))

    table_frame = Frame(table_container)
    table_frame.pack(fill="both", expand=True)

    scroll_y = tk.Scrollbar(table_frame)
    scroll_y.pack(side="right", fill="y")

    donor_table = ttk.Treeview(
        table_frame,
        columns=("ID","Name","Age","Blood Group","City","Contact","Available"),
        show="headings",
        yscrollcommand=scroll_y.set
    )

    scroll_y.config(command=donor_table.yview)

    # headings
    donor_table.heading("ID", text="ID")
    donor_table.heading("Name", text="Name")
    donor_table.heading("Age", text="Age")
    donor_table.heading("Blood Group", text="Bood Group")
    donor_table.heading("City", text="City")
    donor_table.heading("Contact",text="Contact")
    donor_table.heading("Available", text="Available")

    # columns
    donor_table.column("ID", width=50, anchor="center")
    donor_table.column("Name", anchor="w", stretch=True)
    donor_table.column("Age", width=80, anchor="center")
    donor_table.column("Blood Group", anchor="w", stretch=True)
    donor_table.column("City", width=120, anchor="center")
    donor_table.column("Contact",width=80,anchor="center")
    donor_table.column("Available", width=90, anchor="center")

    donor_table.pack(fill="both", expand=True)

    # ---------- LOAD DATA ----------
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT sid, name, age, blood_group, city, contact, available FROM save_donors")

        for row in cursor.fetchall():
            donor_table.insert("", "end", values=row)

        conn.close()

    except Exception as e:
        print("DB error:", e)
