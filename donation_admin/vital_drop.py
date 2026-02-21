import tkinter as tk
import customtkinter as ctk
from tkinter import ttk,messagebox
import mysql.connector
import admin1 


root = tk.Tk()
root.title("Vital Drop")
root.geometry("600x700")


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

def login():

    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root, bg="white", padx=50, pady=60, highlightbackground="#ddd", highlightthickness=1)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame,text="VITAL DROP LOGIN",font=('Seoge UI', 20, 'bold'),fg='#C62828' , bg="white").pack(pady=(0,20))

    tk.Label(frame,text="Email",font=('Seoge UI', 14, 'bold'),background='white').pack()
    email_ent = ttk.Entry(frame,width=40)
    email_ent.pack(pady=6)

    tk.Label(frame,text="Password",font=('Seoge UI', 14, 'bold'),background='white').pack()
    passwrd_ent = ttk.Entry(frame,width=40)
    passwrd_ent.pack(pady=6)


    def check_login():
        connection = connect_db()

        if email_ent.get() == "admin@gmail.com" and passwrd_ent.get() == "admin123":
            for widget in root.winfo_children():
                widget.destroy()
            admin1.admin_page1_customizatio(root)
        else:
            messagebox.showerror("Error", "Invalid Admin Credentials")


    tk.Button(frame,text="LOGIN", bg="#E96D6D",fg="white",font=('Seoge UI', 14, 'bold'),command=check_login).pack(pady=5)
    tk.Button(frame, text="Don't have an account? Register", bg="white", border=0, command=registration).pack()



def registration():
    

    for widget in root.winfo_children():
        widget.destroy()

    # center frame (card)
    frame = ctk.CTkFrame(root, width=360,corner_radius=10)
    frame.pack(pady=20)
    

    ctk.set_appearance_mode("light")

    # heading
    ctk.CTkLabel(
        frame,
        text="Donor Registration",
        font=("Arial", 22, "bold"),
        text_color="#d32f2f"
    ).pack(pady=(20, 15))

    # form function
    def create_label_entry(parent, text, is_password=False):
        ctk.CTkLabel(parent, text=text, anchor="w").pack(fill="x", padx=25)
        entry = ctk.CTkEntry(parent, width=300, show="*" if is_password else "")
        entry.pack(fill="x", padx=25, pady=(0, 10))
        return entry

    # form fields
    name_entry = create_label_entry(frame, "Full Name")
    email_entry = create_label_entry(frame, "Email")
    password_entry = create_label_entry(frame, "Password", is_password=True)
    contact_entry = create_label_entry(frame, "Contact")
    location_entry = create_label_entry(frame, "Location")

    # blood type
    ctk.CTkLabel(frame, text="Blood Type", anchor="w").pack(fill="x", padx=25)
    blood_group = ctk.CTkComboBox(
        frame,
        values=["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    )
    blood_group.pack(fill="x", padx=25, pady=(0, 10))

    # medical history
    ctk.CTkLabel(frame, text="Medical History (Brief)", anchor="w").pack(fill="x", padx=25)
    medical_text = ctk.CTkTextbox(frame, height=60)
    medical_text.pack(fill="x", padx=25, pady=(0, 20))

    def insert_data():
        connection = None
        cursor = None

        try:
            connection = connect_db()
            if connection is None:
                return

            cursor = connection.cursor()

            sql = """
            INSERT INTO donors
            (name, email, password, contact, location, blood_group, medical_history)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                name_entry.get(),
                email_entry.get(),
                password_entry.get(),
                contact_entry.get(),
                location_entry.get(),
                blood_group.get(),
                medical_text.get("1.0", "end").strip()
            )

            cursor.execute(sql, values)
            connection.commit()

            messagebox.showinfo("Success", "Donor Added Successfully")
            login()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"{err}")

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    btn_frame = ctk.CTkFrame(frame)
    btn_frame.pack(fill="x", pady=10)

    ctk.CTkButton(
        btn_frame,
        text="Sign Up",
        fg_color="#d32f2f",
        hover_color="#b71c1c",
        height=40,
        command=insert_data
    ).pack(fill="x", padx=25,pady=5)

    ctk.CTkButton(
        btn_frame,
        text="Back to Login",
        fg_color="transparent",
        text_color="black",
        hover=False,
        command=login
    ).pack(pady=15)


login()
root.mainloop()