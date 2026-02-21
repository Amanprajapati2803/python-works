import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import admin1


def search_donor_table(parent, back_callback):

    # ---------- CLEAR PAGE ----------
    for widget in parent.winfo_children():
        widget.destroy()

    def go_back():
        for widget in parent.winfo_children():
            widget.destroy()
        back_callback(parent)

    # ---------- MAIN FRAME ----------
    frame = ctk.CTkFrame(parent, corner_radius=10)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    blood_var = tk.StringVar(value="Any")
    city_var = tk.StringVar()

    # ---------- TITLE ----------
    ctk.CTkLabel(
        frame,
        text="Search Donors",
        fg_color="#C62828",
        text_color="white",
        font=("Segoe UI", 18, "bold")
    ).pack(fill="x", padx=20, pady=20)

    ctk.CTkButton(
        frame,
        text="← Back",
        fg_color="#6c757d",
        hover_color="#5a6268",
        command=go_back
    ).pack(pady=(0, 10))

    # ---------- SEARCH BAR ----------
    search_frame = ctk.CTkFrame(frame)
    search_frame.pack(fill="x", padx=20, pady=(0,10))

    ctk.CTkLabel(search_frame, text="Blood Group").pack(side="left", padx=(10,5))

    blood_menu = ctk.CTkOptionMenu(
        search_frame,
        values=["Any","A+","A-","B+","B-","O+","O-","AB+","AB-"],
        variable=blood_var,
        width=90
    )
    blood_menu.pack(side="left", padx=(0,15))

    ctk.CTkLabel(search_frame, text="City").pack(side="left", padx=(0,5))

    city_entry = ctk.CTkEntry(search_frame, textvariable=city_var, width=150)
    city_entry.pack(side="left", padx=(0,15))

    # ---------- TABLE ----------
    table_frame = ctk.CTkFrame(frame)
    table_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))

    scroll_y = tk.Scrollbar(table_frame)
    scroll_y.pack(side="right", fill="y")

    donor_table = ttk.Treeview(
        table_frame,
        columns=("ID", "Name", "Age", "Blood", "City", "Contact", "Available"),
        show="headings",
        yscrollcommand=scroll_y.set
    )

    scroll_y.config(command=donor_table.yview)

    # headings
    donor_table.heading("ID", text="ID")
    donor_table.heading("Name", text="Name")
    donor_table.heading("Age", text="Age")
    donor_table.heading("Blood", text="Blood Group")
    donor_table.heading("City", text="City")
    donor_table.heading("Contact", text="Contact")
    donor_table.heading("Available", text="Available")

    # columns
    donor_table.column("ID", width=50, anchor="center")
    donor_table.column("Name", anchor="w", stretch=True)
    donor_table.column("Age", width=70, anchor="center")
    donor_table.column("Blood", width=90, anchor="center")
    donor_table.column("City", stretch=True)
    donor_table.column("Contact", width=110, anchor="center")
    donor_table.column("Available", width=90, anchor="center")

    donor_table.pack(fill="both", expand=True)

    # ---------- TABLE LOAD FUNCTION ----------
    def load_data(rows):
        donor_table.delete(*donor_table.get_children())
        for row in rows:
            donor_table.insert("", "end", values=row)

    # ---------- SEARCH LOGIC ----------
    def perform_search():
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="vital_drop"
            )

            cursor = conn.cursor()

            query = """
                SELECT sid, name, age, blood_group, city, contact, available
                FROM save_donors
                WHERE 1=1
            """
            params = []

            if blood_var.get() != "Any":
                query += " AND blood_group=%s"
                params.append(blood_var.get())

            if city_var.get().strip() != "":
                query += " AND city LIKE %s"
                params.append("%" + city_var.get().strip() + "%")

            cursor.execute(query, params)
            rows = cursor.fetchall()

            load_data(rows)

            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- SEARCH BUTTON ----------
    ctk.CTkButton(
        search_frame,
        text="Search",
        fg_color="#C62828",
        command=perform_search,
        width=100
    ).pack(side="left")

    # ---------- AUTO LOAD ALL DONORS ----------
    perform_search()
