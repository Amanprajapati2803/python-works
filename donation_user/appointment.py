import customtkinter as ctk
import tkinter as tk 
from tkinter import ttk


def Appointment(parent):
    header_frame = ctk.CTkFrame(parent, fg_color="transparent")
    header_frame.pack(fill="x", padx=30, pady=(20, 5))

    ctk.CTkLabel(
        header_frame,
        text="My Appointments",
        font=("Segoe UI", 20, "bold"),
        text_color="red"
    ).pack(anchor="w")

    # ctk.CTkLabel(
    #     header_frame,
    #     text="looking for specially a+ blood type :",
    #     font=("Segoe UI", 13),
    #     text_color="gray"
    # ).pack(anchor="w", pady=(4, 0))


    style = ttk.Style()
    style.theme_use("default")

    style.configure(
        "Treeview.Heading",
        font=("Arial", 18, "bold"),
        background="#e6e3dc",
        foreground="black"
    )

    style.configure(
        "MyTable.Treeview",
        rowheight=35,
        font=("Arial", 11)
    )

    def table_view(view):
        table_frame=ctk.CTkFrame(view,fg_color="grey")
        table_frame.pack(fill="both",expand="True",padx=20,pady=20)

        scrollbary = tk.Scrollbar(table_frame, orient="vertical")
        scrollbary.pack(side="right", fill="y")


        columns=("id","Hospital","Date","time","status")

        tree=ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10,
            yscrollcommand=scrollbary,
        )

        tree.heading("id", text="ID")
        tree.heading("Hospital", text="Hospital")
        tree.heading("Date", text="Time")
        tree.heading("time", text="time")
        tree.heading("status", text="status")


        tree.column("id", width=50, anchor="center")
        tree.column("Hospital", width=250)
        tree.column("Date", width=150)
        tree.column("time", width=120)
        tree.column("status", width=200)

        tree.pack(fill="both",expand=True)
    table_view(parent)

ctk.set_appearance_mode("light")

root=ctk.CTk()
root.title("Appointmets")
root.geometry("1000x1000")

Appointment(root)

root.mainloop()