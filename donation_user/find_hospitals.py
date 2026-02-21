import customtkinter as ctk
import tkinter as tk 
from tkinter import ttk
import mysql.connector

def find_hospitals(parent,user_location, user_blood):
    header_frame = ctk.CTkFrame(parent, fg_color="transparent")
    header_frame.pack(fill="x", padx=30, pady=(20, 5))

    ctk.CTkLabel(
        header_frame,
        text="Recommended Hospitals",
        font=("Segoe UI", 20, "bold"),
        text_color="red"
    ).pack(anchor="w")

    ctk.CTkLabel(
        header_frame,
        text=f"Looking for {user_blood} in {user_location}",
        font=("Segoe UI", 13),
        text_color="gray"
    ).pack(anchor="w", pady=(4, 0))

# database Fetch hospitals based on location + blood group
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="blood_donation"
    )
    cursor = conn.cursor()

    query = """
        SELECT id, name, city, contact, blood_required
        FROM hospitals
        WHERE location=%s AND requirement=%s
    """
    cursor.execute(query, (user_location, user_blood))
    results = cursor.fetchall()

    style = ttk.Style()
    style.theme_use("default")

    style.configure(
        "Treeview.Heading",
        font=("Arial", 12, "bold"),
        background="#e6e3dc",
        foreground="black"
    )

    style.configure(
        "MyTable.Treeview",
        rowheight=35,
        font=("Arial", 11)
    )

    def table_view(t_v):
        table=ctk.CTkFrame(t_v,fg_color="grey")
        table.pack(fill="both",expand="True",padx=20,pady=20)

        scrollbary = tk.Scrollbar(table, orient="vertical")
        scrollbary.pack(side="right", fill="y")

        scrollbarx = tk.Scrollbar(table, orient="horizontal")
        scrollbarx.pack(side="bottom", fill="x")

        columns=("id","name","location","contact","requirements")

        tree=ttk.Treeview(
            table,
            columns=columns,
            show="headings",
            height=10,
            yscrollcommand=scrollbary,
            xscrollcommand=scrollbarx
        )

        tree.heading("id", text="ID")
        tree.heading("name", text="Hospital Name")
        tree.heading("location", text="Location")
        tree.heading("contact", text="Contact")
        tree.heading("requirements", text="Requirements")


        tree.column("id", width=50, anchor="center")
        tree.column("name", width=250)
        tree.column("location", width=150)
        tree.column("contact", width=120)
        tree.column("requirements", width=200)

        tree.pack(fill="both",expand=True)
# giving the values to table 
        for row in results:
            tree.insert("", "end", values=row)

    table_view(parent)    

    ctk.CTkButton(parent,text="Get Appointments",
                  fg_color="red",
                  text_color="white",
                  anchor="center",
                  width=90,
                  height=45
                  ).pack(fill="x",padx=20,pady=10)    


ctk.set_appearance_mode("light")

root=ctk.CTk()
root.title("findhospitals")
root.geometry("1000x1000")
find_hospitals(root)
root.mainloop()

