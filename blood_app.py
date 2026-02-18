import tkinter as tk
import customtkinter as ctk
from tkinter import ttk,messagebox
import mysql.connector
from user_main import user_main

app = tk.Tk()
app.title("Vital Drop")
app.geometry("600x600")
                                #-------------------login------------------#
def login():

    # for widget in root.winfo_children():
    #     widget.destroy()

    # def go_next():

    #      for widget in app.winfo_children():
    #         widget.destroy()
    #      user_main(app)

    def go_next():
        email = email_ent.get()
        password = passwrd_ent.get()

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="blood_donation"
            )
            cursor = conn.cursor()

            sql = """
            SELECT name, email, contact, location, blood_group, medical_text
            FROM registration
            WHERE email=%s AND password=%s
            """
            cursor.execute(sql, (email, password))
            user = cursor.fetchone()

            if user:
                user_main(app, user)
            else:
                messagebox.showerror("Error", "Invalid Email or Password")

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


    frame = tk.Frame(app, bg="white", padx=50, pady=60, highlightbackground="#ddd", highlightthickness=1)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame,text="VITAL DROP LOGIN",font=('Seoge UI', 20, 'bold'),fg='#C62828' , bg="white").pack(pady=(0,20))

    tk.Label(frame,text="Email",font=('Seoge UI', 14, 'bold')).pack()
    email_ent = ttk.Entry(frame,width=40)
    email_ent.pack(pady=6)

    tk.Label(frame,text="Password",font=('Seoge UI', 14, 'bold')).pack()
    passwrd_ent = ttk.Entry(frame,width=40)
    passwrd_ent.pack(pady=6)



    tk.Button(frame,text="LOGIN", bg="#E96D6D",fg="white",font=('Seoge UI', 14, 'bold'),command=go_next).pack(pady=5)
    tk.Button(frame, text="Don't have an account? Register", bg="white", border=0, command=registration).pack()

                            #--------------------Registration-------------------#

def registration():

    for widget in app.winfo_children():
        widget.destroy()

    # center frame (card)
    frame = ctk.CTkFrame(app, width=360, height=600, corner_radius=10)
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
    medical_text = ctk.CTkTextbox(frame, height=80)
    medical_text.pack(fill="x", padx=25, pady=(0, 20))

    # button frame
    btn_frame = ctk.CTkFrame(frame, fg_color="#A89A9A")
    btn_frame.pack(side="bottom")


# database workings    

    def save_donor():
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="blood_donation"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM registration WHERE email=%s",
                       (email_entry.get(),))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showerror("Error", "Email already registered!")
                return
        
        
            sql="""
            insert into registration (id,name,email,password,contact,location,blood_group,medical_text)
            values(null,%s,%s,%s,%s,%s,%s,%s)
            """
            data=(
                    name_entry.get(),
                    email_entry.get(),
                    password_entry.get(),
                    contact_entry.get(),
                    location_entry.get(),
                    blood_group.get(),
                    medical_text.get("1.0", "end-1c")
            )
            cursor.execute(sql,data)
            conn.commit()
            messagebox.showinfo("succes","registration succesful")

            for widget in app.winfo_children():
                widget.destroy()
            login()  #going bact to login

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

#---databse end----#

    ctk.CTkButton(
        btn_frame,
        text="Sign Up",
        fg_color="#d32f2f",
        hover_color="#b71c1c",
        height=40,
        command=save_donor
    ).pack(fill="x", padx=25)

    ctk.CTkButton(
        btn_frame,
        text="Back to Login",
        fg_color="transparent",
        text_color="black",
        hover=False,
        command=login
    ).pack(pady=15)



login()
app.mainloop()