import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# main window
root = ctk.CTk()
root.title("Donor Registration")
root.geometry("420x650")


# center frame (card)
frame = ctk.CTkFrame(root, width=360, height=600, corner_radius=10)
frame.pack(pady=20)


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
    entry = ctk.CTkEntry(parent,width=300, show="*" if is_password else "")
    entry.pack(fill="x", padx=25, pady=(0, 10))
    return entry


#form
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

# sign up button

btn_frame=ctk.CTkFrame(frame,fg_color="#A89A9A")
btn_frame.pack(side="bottom")
ctk.CTkButton(
    btn_frame,
    text="Sign Up",
    fg_color="#d32f2f",
    hover_color="#b71c1c",
    height=40
).pack(fill="x", padx=25)

# back to login
ctk.CTkButton(
    btn_frame,
    text="Back to Login",
    fg_color="transparent",
    text_color="black",
    hover=False
).pack(pady=15)

root.mainloop()
