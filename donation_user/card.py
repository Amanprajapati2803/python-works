# import customtkinter as ctk

# ctk.set_appearance_mode("light")
# # ctk.set_default_color_theme("RED")

# app = ctk.CTk()
# app.geometry("500x300")
# app.title("Blood Donation Card")

# # -------------------- CARD FRAME --------------------
# card = ctk.CTkFrame(app, width=420, height=220, corner_radius=20)
# card.pack(pady=40)
# card.pack_propagate(False)

# # -------------------- HEADER --------------------
# header = ctk.CTkLabel(
#     card,
#     text="BLOOD DONATION CARD",
#     font=("Arial", 18, "bold"),
#     text_color="#de0f0f"
# )
# header.pack(pady=(15, 5))

# # -------------------- DETAILS FRAME --------------------
# details_frame = ctk.CTkFrame(card, fg_color="transparent")
# details_frame.pack(pady=10)

# def create_row(label_text, value_text):
#     row = ctk.CTkFrame(details_frame, fg_color="transparent")
#     row.pack(anchor="w", pady=3, padx=20)

#     label = ctk.CTkLabel(row, text=label_text, font=("Arial", 14, "bold"))
#     label.pack(side="left")

#     value = ctk.CTkLabel(row, text=value_text, font=("Arial", 14))
#     value.pack(side="left", padx=10)

# # -------------------- SAMPLE DATA --------------------
# create_row("Name:", "Aman Prajapati")
# create_row("Blood Group:", "O+")
# create_row("Donor ID:", "BD1025")
# create_row("Contact:", "9876543210")

# # -------------------- FOOTER --------------------
# footer = ctk.CTkLabel(
#     card,
#     text="Your Donation Saves Lives ❤️",
#     font=("Arial", 12, "italic")
# )
# footer.pack(pady=(10, 5))

# app.mainloop()

# import customtkinter as ctk
# from datetime import datetime

# ctk.set_appearance_mode("light")

# app = ctk.CTk()
# app.geometry("650x400")
# app.title("Blood Donation Record Card")

# # ---------------- MAIN CARD ----------------
# card = ctk.CTkFrame(app, width=600, height=330, corner_radius=20)
# card.pack(pady=30)
# card.pack_propagate(False)

# # ---------------- HEADER ----------------
# header = ctk.CTkLabel(
#     card,
#     text="BLOOD DONATION CERTIFICATE",
#     font=("Arial", 22, "bold"),
#     text_color="#b30000"
# )
# header.pack(pady=(15, 10))

# # ---------------- DIVIDER ----------------
# divider = ctk.CTkFrame(card, height=2, fg_color="#b30000")
# divider.pack(fill="x", padx=20, pady=5)

# # ---------------- DETAILS SECTION ----------------
# details = ctk.CTkFrame(card, fg_color="transparent")
# details.pack(pady=15, padx=20, fill="both")

# def create_row(label, value):
#     row = ctk.CTkFrame(details, fg_color="transparent")
#     row.pack(anchor="w", pady=5)

#     ctk.CTkLabel(row, text=label, font=("Arial", 14, "bold")).pack(side="left")
#     ctk.CTkLabel(row, text=value, font=("Arial", 14)).pack(side="left", padx=10)

# # Sample Data (Later you can connect this to database)
# create_row("Donor Name:", "Aman Prajapati")
# create_row("Blood Group:", "O+")
# create_row("Donor ID:", "BD1025")
# create_row("Date:", datetime.now().strftime("%d-%m-%Y"))
# create_row("Time Slot:", "10:00 AM - 11:00 AM")
# create_row("Quantity Donated:", "450 ml")
# create_row("Hospital:", "City Care Hospital")
# create_row("Location:", "Ahmedabad")

# # ---------------- FOOTER ----------------
# footer_line = ctk.CTkFrame(card, height=2, fg_color="#b30000")
# footer_line.pack(fill="x", padx=20, pady=10)

# footer = ctk.CTkLabel(
#     card,
#     text="Thank You For Saving Lives ❤️",
#     font=("Arial", 13, "italic")
# )
# footer.pack()

# app.mainloop()

import customtkinter as ctk
import qrcode
from PIL import Image, ImageTk
from datetime import datetime

ctk.set_appearance_mode("light")

app = ctk.CTk()
app.geometry("750x400")
app.title("Blood Donation Card with QR")

# ----------- Generate QR -----------
qr_data = """Donor ID: BD1025
Name: Aman Prajapati
Blood Group: O+
Date: {}
Hospital: City Care Hospital
Quantity: 450ml""".format(datetime.now().strftime("%d-%m-%Y"))

qr = qrcode.make(qr_data)
qr = qr.resize((120,120))
qr_img = ImageTk.PhotoImage(qr)

# ----------- Main Card -----------
card = ctk.CTkFrame(app, width=700, height=320, corner_radius=20)
card.pack(pady=30)
card.pack_propagate(False)

header = ctk.CTkLabel(card,
                      text="BLOOD DONATION CERTIFICATE",
                      font=("Arial",20,"bold"),
                      text_color="#b30000")
header.pack(pady=10)

body = ctk.CTkFrame(card, fg_color="transparent")
body.pack(fill="both", expand=True, padx=20, pady=10)

# ----------- Left Side (Details) -----------
details = ctk.CTkFrame(body, fg_color="transparent")
details.pack(side="left", fill="both", expand=True)

def row(label, value):
    r = ctk.CTkFrame(details, fg_color="transparent")
    r.pack(anchor="w", pady=4)
    ctk.CTkLabel(r, text=label, font=("Arial",14,"bold")).pack(side="left")
    ctk.CTkLabel(r, text=value, font=("Arial",14)).pack(side="left", padx=8)

row("Donor Name:", "Aman Prajapati")
row("Blood Group:", "O+")
row("Donor ID:", "BD1025")
row("Date:", datetime.now().strftime("%d-%m-%Y"))
row("Time Slot:", "10:00 AM - 11:00 AM")
row("Quantity:", "450 ml")
row("Hospital:", "City Care Hospital")

# ----------- Right Side (QR Code) -----------
qr_label = ctk.CTkLabel(body, image=qr_img, text="")
qr_label.pack(side="right", padx=20)

footer = ctk.CTkLabel(card,
                      text="Scan QR to Verify Donation Record",
                      font=("Arial",12,"italic"))
footer.pack(pady=5)

app.mainloop()
