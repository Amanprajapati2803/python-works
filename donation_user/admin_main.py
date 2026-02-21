import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from db import connect_db
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def admin_main(parent,logout_callback):
        

        # Clear old widgets
        for widget in parent.winfo_children():
            widget.destroy()

        # Reset grid weights
        for i in range(10):
            parent.grid_rowconfigure(i, weight=0)
            parent.grid_columnconfigure(i, weight=0)

        # Now configure fresh layout
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

   
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue") 

        # -------------------- CONTENT FRAME --------------------
        content_frame = ctk.CTkFrame(parent, fg_color="#f4f6f8")
        content_frame.grid(row=0, column=0, sticky="nsew")




        # ----------- FUNCTION TO CLEAR CONTENT -----------
        def clear_content():
            for widget in content_frame.winfo_children():
                widget.destroy()  

        #------------------ admin pages----------------------#        
        def show_pie_chart():
            clear_content()

            chart_frame = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=15)
            chart_frame.pack(fill="both", expand=True, padx=40, pady=40)

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT blood_group, COUNT(*)
                FROM registration
                GROUP BY blood_group
            """)
            data = cursor.fetchall()
            conn.close()

            if not data:
                ctk.CTkLabel(chart_frame, text="No donor data found").pack(pady=40)
                return

            labels = [row[0] for row in data]
            values = [row[1] for row in data]

            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(values, labels=labels, autopct='%1.1f%%')
            ax.set_title("Blood Group Distribution")

            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            ctk.CTkButton(
                content_frame,
                text="<- Back",
                command=Home_page,
                fg_color="darkred"
            ).pack(pady=10)
                
            #-------------- search donors---------------#

        def search_donor():
            clear_content()

                # ---------- MAIN FRAME ----------
            frame = ctk.CTkFrame(content_frame, corner_radius=10)
            frame.pack(fill="both", expand=True, padx=20, pady=20)

            blood_var = tk.StringVar(value="Any")
            city_var = tk.StringVar()

                # ---------- TITLE ----------
            ctk.CTkLabel(
                    frame,
                    text="Search Donors",
                    fg_color="#C62828",
                    text_color="white",
                    font=("Segoe UI", 18, "bold")
                ).pack(fill="x", padx=20, pady=20)

            ctk.CTkButton(
                    frame,
                    text="← Back",
                    fg_color="#6c757d",
                    hover_color="#5a6268",
                    command=Home_page
                ).pack(pady=(0, 10))

                # ---------- SEARCH BAR ----------
            search_frame = ctk.CTkFrame(frame)
            search_frame.pack(fill="x", padx=20, pady=(0,10))

            ctk.CTkLabel(search_frame, text="Blood Group").pack(side="left", padx=(10,5))

            blood_menu = ctk.CTkOptionMenu(
                    search_frame,
                    values=["Any","A+","A-","B+","B-","O+","O-","AB+","AB-"],
                    variable=blood_var,
                    width=90
                )
            blood_menu.pack(side="left", padx=(0,15))

            ctk.CTkLabel(search_frame, text="City").pack(side="left", padx=(0,5))

            city_entry = ctk.CTkEntry(search_frame, textvariable=city_var, width=150)
            city_entry.pack(side="left", padx=(0,15))

                # ---------- TABLE ----------
            table_frame = ctk.CTkFrame(frame)
            table_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))

            scroll_y = tk.Scrollbar(table_frame)
            scroll_y.pack(side="right", fill="y")

            donor_table = ttk.Treeview(
                    table_frame,
                    columns=("ID", "Name", "Age", "Blood", "City", "Contact", "Available"),
                    show="headings",
                    yscrollcommand=scroll_y.set
                )

            scroll_y.config(command=donor_table.yview)

                # headings
            donor_table.heading("ID", text="ID")
            donor_table.heading("Name", text="Name")
            donor_table.heading("Age", text="Age")
            donor_table.heading("Blood", text="Blood Group")
            donor_table.heading("City", text="City")
            donor_table.heading("Contact", text="Contact")
            donor_table.heading("Available", text="Available")

                # columns
            donor_table.column("ID", width=50, anchor="center")
            donor_table.column("Name", anchor="w", stretch=True)
            donor_table.column("Age", width=70, anchor="center")
            donor_table.column("Blood", width=90, anchor="center")
            donor_table.column("City", stretch=True)
            donor_table.column("Contact", width=110, anchor="center")
            donor_table.column("Available", width=90, anchor="center")

            donor_table.pack(fill="both", expand=True)

                # ---------- TABLE LOAD FUNCTION ----------
            def load_data(rows):
                for row in rows:
                    donor_table.insert("", "end", values=row)

                # ---------- SEARCH LOGIC ----------

            loading_label = ctk.CTkLabel(frame, text="", text_color="green", font=("Segoe UI", 12))
            loading_label.pack()    

            def perform_search():
                loading_label.configure(text="Searching...")
                frame.update()

                try:
                    conn = connect_db()
                    if not conn:
                        return
                    cursor = conn.cursor()

                    query = """
                            SELECT id, name, age, blood_group, location , contact, available
                            FROM registration
                            WHERE 1=1
                        """
                    params = []

                    if blood_var.get() != "Any":
                        query += " AND blood_group=%s"
                        params.append(blood_var.get())

                    if city_var.get().strip() != "":
                        query += " AND location LIKE %s"
                        params.append("%" + city_var.get().strip() + "%")

                    cursor.execute(query, params)
                    rows = cursor.fetchall()

                    donor_table.delete(*donor_table.get_children())

                    if not rows:
                        donor_table.delete(*donor_table.get_children())
                        messagebox.showinfo("Search Result", "No donors found!")
                    else:
                        load_data(rows)

                    cursor.close()
                    conn.close()

                except Exception as e:
                    messagebox.showerror("Error", str(e))

                finally:
                    loading_label.configure(text="") # remove the loding text    

                # ---------- SEARCH BUTTON ----------
            ctk.CTkButton(
                    search_frame,
                    text="Search",
                    fg_color="#C62828",
                    command=perform_search,
                    width=100
                ).pack(side="left")

                # ---------- AUTO LOAD ALL DONORS ----------
            perform_search()

            #-------------------- view donors--------------------# 

        def view_donor():  
            clear_content()

                # ---------- HEADER ----------
            top_frame = ctk.CTkFrame(content_frame, corner_radius=10)
            top_frame.pack(fill="x", padx=20, pady=20)

            ctk.CTkLabel(
                    top_frame,
                    text="All Donors",
                    fg_color="#2a9d8f",
                    text_color="white",
                    font=("Segoe UI", 18, "bold")
                ).pack(fill="x", padx=20, pady=20)

            ctk.CTkButton(
                    top_frame,
                    text="← Back",
                    fg_color="#6c757d",
                    command=Home_page
                ).pack(pady=(0,10))

                
            table_container = ctk.CTkFrame(content_frame)
            table_container.pack(fill="both", expand=True, padx=20, pady=(0,20))

##pakdi gai tuntun 
            table_frame = ctk.CTkFrame(table_container)
            table_frame.pack(fill="both", expand=True)

            scroll_y = tk.Scrollbar(table_frame)
            scroll_y.pack(side="right", fill="y")

            donor_table = ttk.Treeview(
                    table_frame,
                    columns=("ID","Name","Age","Blood Group","City","Contact","Available"),
                    show="headings",
                    yscrollcommand=scroll_y.set
                )

            scroll_y.config(command=donor_table.yview)

                # headings
            donor_table.heading("ID", text="ID")
            donor_table.heading("Name", text="Name")
            donor_table.heading("Age", text="Age")
            donor_table.heading("Blood Group", text="Blood Group")
            donor_table.heading("City", text="City")
            donor_table.heading("Contact",text="Contact")
            donor_table.heading("Available", text="Available")

                # columns
            donor_table.column("ID", width=50, anchor="center")
            donor_table.column("Name", anchor="w", stretch=True)
            donor_table.column("Age", width=80, anchor="center")
            donor_table.column("Blood Group", anchor="w", stretch=True)
            donor_table.column("City", width=120, anchor="center")
            donor_table.column("Contact",width=80,anchor="center")
            donor_table.column("Available", width=90, anchor="center")

            donor_table.pack(fill="both", expand=True)

                # ---------- LOAD DATA ----------
            try:
                conn = connect_db()
                if not conn :
                    return
                cursor = conn.cursor()

                cursor.execute("SELECT id, name, age, blood_group, location, contact, available FROM registration")

                for row in cursor.fetchall():
                    donor_table.insert("", "end", values=row)

                conn.close()
                cursor.close()
            except Exception as e:
                print("DB error:", e)

                    #may finally come here the code


            #----------------------update donor------------------------# 
        def update_donor():
            clear_content()
          
            def update_status():
                selected = donor_table.focus()

                if not selected:
                    messagebox.showwarning("Warning", "Please select a donor.")
                    return

                donor_id = donor_table.item(selected)["values"][0]
                new_status = availability_var.get()

                if new_status == "":
                    messagebox.showwarning("Warning", "Select availability status.")
                    return

                try:
                    conn= connect_db()
                    if not conn:
                        return
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE registration
                        SET last_donation = CURDATE(),
                            available = %s
                        WHERE id=%s
                    """, (new_status,donor_id,))

                    # also mark latest appointment completed
                    cursor.execute("""
                            UPDATE appointments
                            SET status = 'Completed'
                            WHERE user_name = (
                                SELECT name FROM registration WHERE id=%s
                            )
                            AND status='Pending'
                            ORDER BY appointment_date DESC
                            LIMIT 1
                    """, (donor_id,))
                    conn.commit()

                    messagebox.showinfo("Success", "Availability updated successfully.")
                    load_table()

                except Exception as e:
                    messagebox.showerror("Error", str(e))

                # ===== Load Table Function =====
            def load_table():
                for row in donor_table.get_children():
                    donor_table.delete(row)

                conn= connect_db()
                if not conn:
                    return
                cursor = conn.cursor()

                cursor.execute("""SELECT id, name, blood_group, location, 
                               case
                                    when available ='YES' then 'Eligible'
                                    else 'Recovery'
                               END AS availability from registration""")
                records = cursor.fetchall()

                for row in records:
                    donor_table.insert("", "end", values=row)

                cursor.close()
                conn.close()
                    
                # ===== Main Frame =====
            frame = ctk.CTkFrame(content_frame)
            frame.pack(fill="both", expand=True, padx=20, pady=20)


            ctk.CTkLabel(
                    frame, text="Update Availability",
                    text_color="white",
                    fg_color="#dc143c",
                    font=("Arial", 18, "bold")
                ).pack(fill="x",pady=10)

                # ===== Table =====
            table_frame = tk.Frame(frame)
            table_frame.pack(fill="both", expand=True)

            scroll_y = tk.Scrollbar(table_frame)
            scroll_y.pack(side="right", fill="y")

            donor_table = ttk.Treeview(
                    table_frame,
                    columns=("ID", "Name", "Blood", "City", "Availability"),
                    show="headings",
                    yscrollcommand=scroll_y.set
                )

            scroll_y.config(command=donor_table.yview)

            donor_table.heading("ID", text="ID")
            donor_table.heading("Name", text="Name")
            donor_table.heading("Blood", text="Blood Group")
            donor_table.heading("City", text="City")
            donor_table.heading("Availability", text="Availability")

            donor_table.column("ID", width=50, anchor="center")
            donor_table.column("Name", width=150)
            donor_table.column("Blood", width=100, anchor="center")
            donor_table.column("City", width=150)
            donor_table.column("Availability", width=120, anchor="center")

            donor_table.pack(fill="both", expand=True)

                # ===== Availability Selection =====
            availability_var = tk.StringVar()

            control_frame = ctk.CTkFrame(frame)
            control_frame.pack(fill="x", pady=20)

            ctk.CTkLabel(
                    control_frame,
                    text="Set Availability:"
                ).pack(side="left", padx=10)

            ctk.CTkComboBox(
                    control_frame,
                    values=["YES", "NO"],
                    variable=availability_var,
                    width=180
                ).pack(side="left", padx=10)

            ctk.CTkButton(
                    control_frame,
                    text="Update",
                    command=update_status,
                    width=120
                ).pack(side="left", padx=20)

                # ===== Back Button =====
            ctk.CTkButton(
                    frame,
                    text="Back",
                    command=Home_page,
                    width=100
                ).pack(pady=(10, 0))

            load_table()

        #---------------- main page [Home page of admin]--------------------#
        def Home_page():
            clear_content()

            # ---------------- MAIN CONTAINER ----------------
            main_container = ctk.CTkFrame(content_frame, fg_color="transparent")
            main_container.pack(fill="both", expand=True, padx=40, pady=20)

            label_font = ("Arial", 16, "italic")

            ctk.CTkLabel(main_container,text="VitalDrop",font=("segoe UI", 40, "bold"),text_color="#c1121f").pack(pady=(10, 5))

            ctk.CTkLabel(main_container,text="Connecting Donors with Lives in Need",font=("Arial", 13, "italic"),text_color="#555555").pack(pady=(0,20))

            divider = ctk.CTkFrame(main_container, height=2, fg_color="#c0c0c0")
            divider.pack(fill="x", padx=100, pady=20)

            custombtns = ctk.CTkFrame(
                main_container,
                corner_radius=15,
                # fg_color="#ffffff"
            )
            custombtns.pack(pady=20)

            # custombtns.grid_columnconfigure(0, weight=1)
            # custombtns.grid_columnconfigure(1, weight=1)

            btn_font = ("Arial", 16, "bold")

            btn1 = ctk.CTkButton(custombtns, text="view blood chart", fg_color="#d62828", width=240, height=55, font=btn_font,command=show_pie_chart)
            btn2 = ctk.CTkButton(custombtns, text="View Donors", fg_color="#2a9d8f", width=240, height=55, font=btn_font,command=view_donor)
            btn3 = ctk.CTkButton(custombtns, text="Search Blood", fg_color="#2a9d8f", width=240, height=55, font=btn_font,command=search_donor)
            btn4 = ctk.CTkButton(custombtns, text="Update Availability", fg_color="#d62828", width=240, height=55, font=btn_font,command=update_donor)

            btn1.grid(row=0, column=0, padx=20, pady=15)
            btn2.grid(row=0, column=1, padx=20, pady=15)
            btn3.grid(row=1, column=0, padx=20, pady=15)
            btn4.grid(row=1, column=1, padx=20, pady=15)


            stats = ctk.CTkFrame(main_container, fg_color="#e9ecef", corner_radius=10)
            stats.pack(pady=40 , fill="x",padx=40)
            
            stats.grid_columnconfigure((0,1,2), weight=1)

            conn=connect_db()
            cursor = conn.cursor()

            cursor.execute("select count(*) from registration")
            total=cursor.fetchone()[0]

            cursor.execute("select count(*) from registration where available='YES'")
            available = cursor.fetchone()[0]

            cursor.execute("""select count(*) from registration 
                           where blood_group in ('O+' , 'O-') 
                        """)
            rare_blood=cursor.fetchone()[0]

            ctk.CTkLabel(stats, text=f"Total Donors: {total}", font=label_font).\
                grid(row=0, column=0, pady=15)
            ctk.CTkLabel(stats, text=f"Available Donors:{available}", font=label_font, text_color="green").\
                grid(row=0, column=1)
            ctk.CTkLabel(stats, text=f"Rare Blood Types:{rare_blood} ", font=label_font, text_color="red").\
                grid(row=0, column=2)

            ctk.CTkButton(
                main_container,
                text="Logout",
                fg_color="gray",
                command=logout_callback
            ).pack(pady=10)
            ctk.CTkLabel(main_container,text="Developed by Tuntun | Blood Donation Management System",font=("Arial", 12),text_color="#666666").pack(pady=(20,5))


            conn.close()
            cursor.close()
        Home_page()