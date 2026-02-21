import tkinter as tk
import customtkinter as ctk
from tkinter import ttk,messagebox
from user_main import user_main # access user file
from admin_main import admin_main # access admin file
from db import connect_db # access database file
import re


# app window
app = ctk.CTk()
app.title("Vital Drop")
app.geometry("1200x700")
ctk.set_appearance_mode("light")

                                #-------------------login------------------#
def clear_window():
    for widget in app.winfo_children():
        widget.destroy()
                                
def login():

    for widget in app.winfo_children():
        widget.destroy()


    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE registration
            SET available='Yes'
            WHERE last_donation IS NOT NULL
            AND DATEDIFF(CURDATE(), last_donation) >= 90
        """)

        conn.commit()
        cursor.close()
        conn.close()
    except:
        pass

    def go_next():
        email = email_ent.get()
        password = passwrd_ent.get()

        # admin check for login
        if email_ent.get() == "admin@gmail.com" and passwrd_ent.get() == "admin123":
            for widget in app.winfo_children():
                widget.destroy()
            clear_window()    
            admin_main(app,login)    
            return 
        
        try:
            conn = connect_db()
            cursor = conn.cursor()

            sql = """
            SELECT id,name, email, contact, location, blood_group, medical_text
            FROM registration
            WHERE email=%s AND password=%s
            """
            cursor.execute(sql, (email, password))
            user = cursor.fetchone()
        # user check for login
            if user:
                clear_window()
                user_main(app, user,login)
            else:
                messagebox.showerror("Error", "Invalid Email or Password")

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

# all login widgets
    frame = ctk.CTkFrame(app, width=450, height=450, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    frame.pack_propagate(False)

    ctk.CTkLabel(frame,text="VITAL DROP LOGIN",font=('Seoge UI', 30, 'bold'),text_color="#C62828").pack(pady=(20,20))

    ctk.CTkLabel(frame,text="Email",font=('Seoge UI', 14, 'bold')).pack()
    email_ent = ctk.CTkEntry(frame, width=320, height=40, placeholder_text="Email")
    email_ent.pack(pady=10)

    ctk.CTkLabel(frame,text="Password",font=('Seoge UI', 14, 'bold')).pack()
    passwrd_ent = ctk.CTkEntry(frame, width=320, height=40,placeholder_text="Password", show="*")
    passwrd_ent.pack(pady=10)
        
    ctk.CTkButton(
        frame,
        text="LOGIN",
        width=320,
        height=45,
        fg_color="#C62828",
        hover_color="#a31515",
        command=go_next
    ).pack(pady=20)

    ctk.CTkButton(frame, text="Don't have an account? Register",hover_color="#5A9BCA", command=registration).pack(pady=(10,20))

                            #--------------------Registration-------------------#

def registration():
    # clearing previous widgets 
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
    age_entry=create_label_entry(frame,"Age")
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

# database workings    

    def save_donor():

        name = name_entry.get().strip()
        age = age_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        contact = contact_entry.get().strip()
        location = location_entry.get().strip()
        blood = blood_group.get().strip()
        medical = medical_text.get("1.0", "end-1c").strip()

        # Check any empty entry
        if not all([name, age, email, password, contact, location, blood, medical]):
            messagebox.showerror("Error", "All fields are required!")
            return
            
        # Email format validation
        email_pattern =r'^[a-zA-Z0-9._%+-]+@(gmail|outlook)\.com$'

        if not re.match(email_pattern, email):
            messagebox.showerror("Error", "Enter a valid email address!")
            return
            
        # Contact validation
        if not contact.isdigit():
            messagebox.showerror("Error", "Contact number must contain only digits!")
            return

        if len(contact) != 10:
            messagebox.showerror("Error", "Contact number must be exactly 10 digits!")
            return
            
        # check age is number
        if not age.isdigit():
            messagebox.showerror("Error", "Age must be a number!")
            return

        age = int(age)
            
        #age criteriya
        if age < 18:
            messagebox.showerror("Error", "You must be 18 or older to register!")
            return
        

        try:
            conn=connect_db()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM registration WHERE email=%s",
                       (email_entry.get(),))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showerror("Error", "Email already registered!")
                return
        
        
            sql="""
            insert into registration (id,name,email,password,contact,location,blood_group,medical_text,age)
            values(null,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            data = (
                name,
                email,
                password,
                contact,
                location,
                blood,
                medical,
                age
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

    # button frame
    btn_frame = ctk.CTkFrame(frame, fg_color="#A89A9A")
    btn_frame.pack(side="bottom")

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



login() # calling login as a default
app.mainloop()