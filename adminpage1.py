import customtkinter as ctk
from tkinter import messagebox
from adminpage2 import admin_interface2



def admin_page1_customizatio(parent):
        label_font = ("Arial", 16, "italic")

        ctk.CTkLabel(parent,text="HemoLink",font=("segoe UI", 40, "bold"),text_color="#c1121f").pack(pady=(20, 5))

        ctk.CTkLabel(parent,text="Connecting Donors with Lives in Need",font=("Arial", 13, "italic"),text_color="#555555").pack()

        divider = ctk.CTkFrame(parent, height=2, fg_color="#c0c0c0")
        divider.pack(fill="x", padx=100, pady=20)

        def go_next():
             for widget in parent.winfo_children():
                widget.destroy()
             admin_interface2(parent)      

        custombtns = ctk.CTkFrame(
            parent,
            corner_radius=15,
            fg_color="#ffffff"
        )
        custombtns.pack(pady=20)

        btn_font = ("Arial", 16, "bold")

        btn1 = ctk.CTkButton(custombtns, text="Add Donor", fg_color="#d62828", width=240, height=55, font=btn_font,command=go_next)
        btn2 = ctk.CTkButton(custombtns, text="View Donors", fg_color="#2a9d8f", width=240, height=55, font=btn_font)
        btn3 = ctk.CTkButton(custombtns, text="Search Blood", fg_color="#2a9d8f", width=240, height=55, font=btn_font)
        btn4 = ctk.CTkButton(custombtns, text="Update Availability", fg_color="#d62828", width=240, height=55, font=btn_font)

        btn1.grid(row=0, column=0, padx=20, pady=15)
        btn2.grid(row=0, column=1, padx=20, pady=15)
        btn3.grid(row=1, column=0, padx=20, pady=15)
        btn4.grid(row=1, column=1, padx=20, pady=15)


        stats = ctk.CTkFrame(parent, fg_color="#e9ecef", corner_radius=10)
        stats.pack(fill="x", padx=150, pady=25)

        ctk.CTkLabel(stats, text="Total Donors: ", font=label_font).pack(side="left", expand=True, padx=20, pady=10)
        ctk.CTkLabel(stats, text="Available Donors: ", font=label_font, text_color="green").pack(side="left", expand=True)
        ctk.CTkLabel(stats, text="Rare Blood Types: ", font=label_font, text_color="red").pack(side="left", expand=True)


        ctk.CTkLabel(parent,text="Developed by Tuntun | Blood Donation Management System",font=("Arial", 12),text_color="#666666").pack(pady=20)


ctk.set_appearance_mode("light")

root = ctk.CTk()
root.title("HemoLink")
root.geometry("1000x700")
root.configure(fg_color="#f2f2f2")
admin_page1_customizatio(root)

root.mainloop()
