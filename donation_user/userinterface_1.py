import customtkinter as ctk


def user_details(parent):

    
    header_frame = ctk.CTkFrame(parent, fg_color="transparent")
    header_frame.pack(fill="x", padx=30, pady=(20, 5))

    ctk.CTkLabel(
        header_frame,
        text="Welcome, aman",
        font=("Segoe UI", 20, "bold")
    ).pack(anchor="w")

    ctk.CTkLabel(
        header_frame,
        text="Your contributions save lives.",
        font=("Segoe UI", 13),
        text_color="gray"
    ).pack(anchor="w", pady=(4, 0))


    
    cards_container = ctk.CTkFrame(parent, fg_color="transparent")
    cards_container.pack(fill="x", padx=30, pady=25)

     
    cards_container.grid_columnconfigure((0, 1, 2), weight=1)


    def create_card(col, title, value, value_color):
        card = ctk.CTkFrame(
            cards_container,
            fg_color="white",
            corner_radius=12,
            width=260,
            height=120
        )
        card.grid(row=0, column=col, padx=15, sticky="nsew")
        card.grid_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 13),
            text_color="gray"
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 24, "bold"),
            text_color=value_color
        ).pack()


    
    create_card(0, "Your Blood Type", "B+", "#d63031")
    create_card(1, "Matching Hospitals", "2", "#0984e3")
    create_card(2, "Upcoming Appointments", "1", "#2ecc71")



ctk.set_appearance_mode("light")

root = ctk.CTk()
root.title("Dashboard")
root.geometry("1000x600")
root.configure(fg_color="#f4f6f8")

user_details(root)

root.mainloop()
