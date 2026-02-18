import customtkinter as ctk
import tkinter as tk
import mysql.connector
from tkinter import messagebox
# from adminpage1 import admin_page1_customizatio


def admin_interface2(parent):

    # def go_back():
    #     for widget in parent.winfo_children():
    #         widget.destroy()
    #     admin_page1_customizatio(parent)

    label_font = ("Arial", 14)
    entry_width = 300

    header = ctk.CTkFrame(parent, height=50, fg_color="#d32f2f")
    header.pack(fill="x")

    ctk.CTkLabel(
        header, text="Add New Donor",
        text_color="white",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    form = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
    form.pack(pady=25)

    def make_entry(row, text):
        ctk.CTkLabel(form, text=text, font=label_font)\
            .grid(row=row, column=0, padx=15, pady=10, sticky="e")
        entry = ctk.CTkEntry(form, width=entry_width)
        entry.grid(row=row, column=1, pady=10)
        return entry

    name_entry = make_entry(0, "Name :")
    age_entry = make_entry(1, "Age :")
    contact_entry = make_entry(3, "Contact :")
    city_entry = make_entry(4, "City :")

    blood_var = tk.StringVar(value="A+")
    donate_var = tk.StringVar(value="Yes")

    ctk.CTkLabel(form, text="Blood Group :", font=label_font)\
        .grid(row=2, column=0, padx=15, pady=10, sticky="e")

    blood_menu = ctk.CTkOptionMenu(
        form,
        variable=blood_var,
        values=["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    )
    blood_menu.grid(row=2, column=1, pady=10, sticky="w")

    ctk.CTkLabel(form, text="Available :", font=label_font)\
        .grid(row=5, column=0, padx=15, pady=10, sticky="e")

    radio_frame = ctk.CTkFrame(form, fg_color="transparent")
    radio_frame.grid(row=5, column=1, sticky="w")

    ctk.CTkRadioButton(radio_frame, text="Yes", variable=donate_var, value="Yes").pack(side="left")
    ctk.CTkRadioButton(radio_frame, text="No", variable=donate_var, value="No").pack(side="left")

    def clear_form():
        for e in (name_entry, age_entry, contact_entry, city_entry):
            e.delete(0, "end")
        blood_var.set("A+")
        donate_var.set("Yes")

    def save_donor():
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="blood_donation"
            )
            cursor = conn.cursor()

            sql="""
            insert into donors (name,age,blood_group,contact,city,available)
            values(%s,%s,%s,%s,%s,%s)
            """
            data=(
                    name_entry.get(),
                    age_entry.get(),
                    blood_var.get(),
                    contact_entry.get(),
                    city_entry.get(),
                    donate_var.get()
            )
            cursor.execute(sql,data)
            conn.commit()
            messagebox.showinfo("Success", "Donor Added")
            clear_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    footer = ctk.CTkFrame(parent)
    footer.pack(pady=20)

    ctk.CTkButton(footer, text="Save",fg_color="red", command=save_donor).pack(side="left", padx=10)
    ctk.CTkButton(footer, text="Clear",fg_color="grey", command=clear_form).pack(side="left", padx=10)
    # ctk.CTkButton(footer, text="Back", command=go_back).pack(side="left", padx=10)
