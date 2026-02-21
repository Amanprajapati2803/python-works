import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as db # your database connection file


def update_availability_screen(parent, back_callback):

    
    connection = db.connect(
            host="localhost",
            user="root",
            password="root",
            database="vital_drop"
        )


    # Clear existing widgets
    for widget in parent.winfo_children():
        widget.destroy()

    # ===== Back Function =====
    def go_back():
        for widget in parent.winfo_children():
            widget.destroy()
        back_callback(parent)

    # ===== Update Logic =====
    def update_status():
        selected = donor_table.focus()

        if not selected:
            messagebox.showwarning("Warning", "Please select a donor.")
            return

        donor_id = donor_table.item(selected)["values"][0]
        new_status = availability_var.get()

        if new_status == "":
            messagebox.showwarning("Warning", "Select availability status.")
            return

        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE save_donors SET available = %s WHERE sid = %s",
                (new_status, donor_id)
            )
            connection.commit()

            messagebox.showinfo("Success", "Availability updated successfully.")
            load_table()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ===== Load Table Function =====
    def load_table():
        for row in donor_table.get_children():
            donor_table.delete(row)

        cursor = connection.cursor()
        cursor.execute("SELECT sid, name, blood_group, city, available FROM save_donors")
        records = cursor.fetchall()

        for row in records:
            donor_table.insert("", "end", values=row)

    # ===== Main Frame =====
    frame = ctk.CTkFrame(parent)
    frame.pack(fill="both", expand=True, padx=20, pady=20)


    ctk.CTkLabel(
        frame, text="Update Availability",
        text_color="white",
        fg_color="#dc143c",
        font=("Arial", 18, "bold")
    ).pack(fill="x",pady=10)

    # ===== Table =====
    table_frame = tk.Frame(frame)
    table_frame.pack(fill="both", expand=True)

    scroll_y = tk.Scrollbar(table_frame)
    scroll_y.pack(side="right", fill="y")

    donor_table = ttk.Treeview(
        table_frame,
        columns=("ID", "Name", "Blood", "City", "Availability"),
        show="headings",
        yscrollcommand=scroll_y.set
    )

    scroll_y.config(command=donor_table.yview)

    donor_table.heading("ID", text="ID")
    donor_table.heading("Name", text="Name")
    donor_table.heading("Blood", text="Blood Group")
    donor_table.heading("City", text="City")
    donor_table.heading("Availability", text="Availability")

    donor_table.column("ID", width=50, anchor="center")
    donor_table.column("Name", width=150)
    donor_table.column("Blood", width=100, anchor="center")
    donor_table.column("City", width=150)
    donor_table.column("Availability", width=120, anchor="center")

    donor_table.pack(fill="both", expand=True)

    # ===== Availability Selection =====
    availability_var = tk.StringVar()

    control_frame = ctk.CTkFrame(frame)
    control_frame.pack(fill="x", pady=20)

    ctk.CTkLabel(
        control_frame,
        text="Set Availability:"
    ).pack(side="left", padx=10)

    ctk.CTkComboBox(
        control_frame,
        values=["YES", "NO"],
        variable=availability_var,
        width=180
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        control_frame,
        text="Update",
        command=update_status,
        width=120
    ).pack(side="left", padx=20)

    # ===== Back Button =====
    ctk.CTkButton(
        frame,
        text="Back",
        command=go_back,
        width=100
    ).pack(pady=(10, 0))

    load_table()
