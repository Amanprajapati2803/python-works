import customtkinter as ctk
import tkinter as tk


def user_profile(parent):
    ctk.CTkLabel(parent,text="Your Donor Profile",font=("Arial",28,"bold")).pack(anchor="w",padx=30,pady=20)


    details_frame=ctk.CTkFrame(parent,fg_color="#F9F6F6")
    details_frame.pack(fill="x",padx=(30,30),pady=25)
    def create_details(text,row):
        ctk.CTkLabel(
                    details_frame,
                    text=text,
                    font=("Segoe UI", 18 , "bold")
                ).grid(row=row, column=0, sticky="w", padx=(30, 10), pady=10)
     

    name = create_details("Name         :",0)
    bloodtype = create_details("Blood Type         :",1)
    emial = create_details("EMAIL        :",2)
    contact = create_details("Contact       :",3)
    location = create_details("Location      :",4)
    medicalhistory = create_details("Medical history       :",5)



ctk.set_appearance_mode("light")

root=ctk.CTk()
root.title("Your Donor Profile")
root.geometry("1000x1000")

user_profile(root)
root.mainloop()