import customtkinter as ctk
import tkinter as tk


def edit_donor(parent):

        header = ctk.CTkFrame(parent, height=60, fg_color="#d32f2f", corner_radius=0)
        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text="Add New Donor",
            text_color="white",
            font=("Arial", 16, "bold")
        ).pack(pady=15)


        form = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=12
        )
        form.pack(pady=40)

        LABEL_FONT = ("Arial", 13)
        


        # form.grid_columnconfigure(0, weight=0)
        # form.grid_columnconfigure(1, weight=0)


        def create_field(label_text, row):
            ctk.CTkLabel(
                form,
                text=label_text,
                font=LABEL_FONT
            ).grid(row=row, column=0, sticky="w", padx=(30, 10), pady=10)

            entry = ctk.CTkEntry(form, width=340)
            entry.grid(row=row, column=1, sticky="w", pady=10)
            return entry


        name_entry   = create_field("Name :", 0)
        age_entry    = create_field("Age :", 1)

        ctk.CTkLabel(
            form,
            text="Blood Group :",
            font=LABEL_FONT
        ).grid(row=2, column=0, sticky="w", padx=(30, 10), pady=10)

        ctk.CTkOptionMenu(
            form,
            values=["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"],
            width=160
        ).grid(row=2, column=1, sticky="w", pady=10)

        number_entry = create_field("Contact Number :", 3)
        city_entry   = create_field("City :", 4)


        ctk.CTkLabel(
            form,
            text="Available to Donate :",
            font=LABEL_FONT
        ).grid(row=5, column=0, sticky="w", padx=(30, 10), pady=15)

        donate_var = tk.StringVar(value="Yes")

        radio_frame = ctk.CTkFrame(form, fg_color="transparent")
        radio_frame.grid(row=5, column=1, sticky="w")

        ctk.CTkRadioButton(
            radio_frame, text="Yes", variable=donate_var, value="Yes"
        ).pack(side="left", padx=(0, 20))

        ctk.CTkRadioButton(
            radio_frame, text="No", variable=donate_var, value="No"
        ).pack(side="left")


        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(
            btn_frame,
            text="Save Donor",
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            width=140,
            height=40
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            fg_color="#9e9e9e",
            hover_color="#7d7d7d",
            width=140,
            height=40
        ).pack(side="left", padx=10)


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Add New Donor")
root.geometry("900x600")
root.configure(fg_color="#f4f4f4")

edit_donor(root)

root.mainloop()
