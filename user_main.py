import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox


def user_main(parent,user):
        
        for widget in parent.winfo_children():
            widget.destroy()

        name, email, contact, location, blood_group, medical_text = user

        #----hospital count---------#
        row_count = 0

        #--------------- window appereance------------#
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")


        # -------------------- MAIN GRID --------------------
        parent.grid_columnconfigure(1, weight=1)  # content area expands
        parent.grid_rowconfigure(0, weight=1)

        # -------------------- SIDEBAR --------------------
        sidebar = ctk.CTkFrame(parent, width=220, corner_radius=0, fg_color="#2F4156")
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_rowconfigure(6, weight=1)

        # Logo
        ctk.CTkLabel(
            sidebar,
            text="LIFESTREAM",
            font=("Arial", 20, "bold"),
            text_color="white"
        ).pack(pady=30)

        # -------------------- CONTENT FRAME --------------------
        content_frame = ctk.CTkFrame(parent, fg_color="#f4f6f8")
        content_frame.grid(row=0, column=1, sticky="nsew")


        # ----------- FUNCTION TO CLEAR CONTENT -----------
        def clear_content():
            for widget in content_frame.winfo_children():
                widget.destroy()


                                 # -------------------- PAGES --------------------#

        #------------ dashboard ----------------#
        def dashboard_page():
            clear_content()

            def show_donation_card():
                clear_content()

                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="blood_donation"
                )
                cursor = conn.cursor()

                # Get latest completed donation
                cursor.execute("""
                    SELECT hospital_name, appointment_date
                    FROM appointments
                    WHERE user_name = %s AND status = 'Completed'
                    ORDER BY appointment_date DESC
                    LIMIT 1
                """, (name,))

                result = cursor.fetchone()
                conn.close()

                if not result:
                    messagebox.showinfo("Info", "No completed donations found!")
                    return

                hospital_name, donation_date = result

            header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=30, pady=(20, 5))

            ctk.CTkLabel(
                header_frame,
                text=f"Welcome, {name}",
                font=("Segoe UI", 20, "bold")
            ).pack(anchor="w")

            ctk.CTkLabel(
                header_frame,
                text="Your contributions save lives.",
                font=("Segoe UI", 13),
                text_color="gray"
            ).pack(anchor="w", pady=(4, 0))


            
            cards_container = ctk.CTkFrame(content_frame, fg_color="transparent")
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


            
            create_card(0, "Your Blood Type", f"{blood_group}", "#d63031")
            create_card(1, "Matching Hospitals", f"{row_count}", "#0984e3")
            create_card(2, "Upcoming Appointments", "1", "#2ecc71")

            ctk.CTkButton(
                content_frame,
                text="View Donation Card",
                fg_color="darkred",
                command=show_donation_card
            ).pack(pady=10)


        #--------------- hospital page----------#
        def hospitals_page():
            clear_content()
            nonlocal row_count

            user_location = location
            user_blood = blood_group

            header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
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
                SELECT id, name,location, contact, requirement
                FROM hospitals
                WHERE location=%s AND requirement=%s
            """
            cursor.execute(query, (user_location, user_blood))
            results = cursor.fetchall()
            row_count=len(results)

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

        
            table=ctk.CTkFrame(content_frame,fg_color="grey")
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
                yscrollcommand=scrollbary.set,
                xscrollcommand=scrollbarx.set
            )
            scrollbary.config(command=tree.yview)
            scrollbarx.config(command=tree.xview)

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
            if results:
                for row in results:
                    tree.insert("", "end", values=row)
            else:
                tree.insert("", "end", values=("No hospitals found","","","",""))

            # -------- SLOT FRAME --------
            slot_frame = ctk.CTkFrame(content_frame)
            slot_frame.pack(fill="x", padx=20, pady=10)

            date_var = ctk.StringVar()
            time_var = ctk.StringVar()

            date_dropdown = ctk.CTkOptionMenu(slot_frame, variable=date_var, values=[])
            date_dropdown.pack(pady=5)

            time_dropdown = ctk.CTkOptionMenu(slot_frame, variable=time_var, values=[])
            time_dropdown.pack(pady=5)

            # -------- LOAD SLOTS --------
            def load_slots():
                selected = tree.selection()

                if not selected:
                    messagebox.showwarning("Warning", "Select hospital first!")
                    return

                hospital_data = tree.item(selected[0], "values")
                hospital_id = hospital_data[0]
                hospital_name=hospital_data[1]

                cursor.execute("""
                    SELECT DISTINCT slot_date
                    FROM hospital_slots
                    WHERE hospital_name=%s AND is_available=1
                """, (hospital_name,))
                dates = cursor.fetchall()

                date_list = [str(d[0]) for d in dates]

                if not date_list:
                    messagebox.showinfo("No Slots", "No available dates")
                    return

                date_dropdown.configure(values=date_list)
                date_var.set(date_list[0])

                # Load times automatically for first date
                load_times(date_list[0], hospital_name)

            def load_times(selected_date, hospital_name):
                cursor.execute("""
                    SELECT slot_time
                    FROM hospital_slots
                    WHERE hospital_name=%s AND slot_date=%s AND is_available=1
                """, (hospital_name, selected_date))

                times = cursor.fetchall()
                time_list = [str(t[0]) for t in times]

                time_dropdown.configure(values=time_list)

                if time_list:
                    time_var.set(time_list[0])

            # When date changes
            def on_date_change(selected_date):
                selected = tree.selection()
                if not selected:
                    return

                hospital_data = tree.item(selected[0], "values")
                hospital_name = hospital_data[1]
                load_times(selected_date, hospital_name)

            date_dropdown.configure(command=on_date_change)

            # -------- BOOK APPOINTMENT --------
            def book_appointment():
                selected = tree.selection()

                if not selected:
                    messagebox.showwarning("Warning", "Select hospital first!")
                    return

                hospital_data = tree.item(selected[0], "values")
                hospital_id = hospital_data[0]
                hospital_name = hospital_data[1]

                selected_date = date_var.get()
                selected_time = time_var.get()

                if not selected_date or not selected_time:
                    messagebox.showwarning("Warning", "Select date and time!")
                    return

                insert_query = """
                    INSERT INTO appointments 
                    (id,user_name,hospital_id, hospital_name, appointment_date, appointment_time, status)
                    VALUES (null,%s, %s, %s, %s, %s,%s)
                """

                cursor.execute(insert_query, (
                    name,
                    hospital_id,                                                                 
                    hospital_name,
                    selected_date,
                    selected_time,
                    "Pending"
                ))

                # Mark slot unavailable
                cursor.execute("""
                    UPDATE hospital_slots
                    SET is_available=0
                    WHERE hospital_name=%s AND slot_date=%s AND slot_time=%s
                """, (hospital_name, selected_date, selected_time))

                conn.commit()

                messagebox.showinfo("Success", "Appointment Booked Successfully!")

            # Buttons
            ctk.CTkButton(
                content_frame,
                text="Load Available Slots",
                command=load_slots
            ).pack(pady=5)
        

            ctk.CTkButton(content_frame,text="Get Appointments",
                        fg_color="red",
                        text_color="white",
                        anchor="center",
                        width=90,
                        height=45,
                        command=book_appointment
                        ).pack(fill="x",padx=20,pady=10) 
            

            # def book_appointment():
            #     selected = tree.selection()

            #     if not selected:
            #         messagebox.showwarning("Warning", "Please select a hospital first!")
            #         return
            # # fetching dates 
            #     hospital_data = tree.item(selected[0], "values")
            #     hospital_id = hospital_data[0]

            #     cursor.execute("""
            #         select distinct  slot_date from hospital_slots
            #         WHERE hospital_id=%s AND is_available=1
            #     """, (hospital_id,))

            #     dates = cursor.fetchall()
            #     date_list = [str(d[0]) for d in dates]

            #     date_var = ctk.StringVar()

            #     date_dropdown = ctk.CTkOptionMenu(
            #         content_frame,
            #         values=date_list,
            #         variable=date_var
            #     )
            #     date_dropdown.pack(pady=5)
            # # Time fetching
            #     def load_times(selected_date):
            #             cursor.execute("""
            #                 SELECT slot_time
            #                 FROM hospital_slots
            #                 WHERE hospital_id=%s AND slot_date=%s AND is_available=1
            #             """, (hospital_id, selected_date))

            #             times = cursor.fetchall()
            #             time_list = [t[0] for t in times]

            #             time_var = ctk.StringVar()

            #             time_dropdown = ctk.CTkOptionMenu(
            #                     content_frame,
            #                     values=time_list,
            #                     variable=time_var
            #                 )
            #             time_dropdown.pack(pady=10)

            #             time_dropdown.configure(values=time_list)

            # #connection to time with date
            #     date_dropdown.configure(command=load_times)

            # #the hospital details row fetching
               
            #     hospital_name = hospital_data[1]

            #     selected_date = date_var.get()
            #     selected_time = time_var.get()

            #     # Insert appointment
            #     insert_query = """
            #         INSERT INTO appointments (id,user_name, hospital_name, appointment_date, appointment_time, status)
            #         VALUES (null,%s, %s, %s, %s,%s)
            #     """

            #     cursor.execute(insert_query, (name, hospital_id, hospital_name,selected_date,selected_time, "Pending"))
            #     conn.commit()

            #     tk.messagebox.showinfo(
            #         "Success",
            #         f"Appointment booked at {hospital_name}"
            #     )    


#------------------------appointment page-------------------------#
        def appointments_page():
            clear_content()
            
            header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=30, pady=(20, 5))

            ctk.CTkLabel(
                header_frame,
                text="My Appointments",
                font=("Segoe UI", 20, "bold"),
                text_color="red"
            ).pack(anchor="w")

                # -------- DATABASE CONNECTION --------
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="blood_donation"
            )
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, hospital_name, appointment_date, appointment_time, status
                FROM appointments
                WHERE user_name = %s
                ORDER BY appointment_date DESC
            """, (name,))

            rows = cursor.fetchall()


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
                    yscrollcommand=scrollbary.set,
                )

                scrollbary.config(command=tree.yview)

                tree.heading("id", text="ID")
                tree.heading("Hospital", text="Hospital")
                tree.heading("Date", text="Date")
                tree.heading("time", text="time")
                tree.heading("status", text="status")


                tree.column("id", width=50, anchor="center")
                tree.column("Hospital", width=250)
                tree.column("Date", width=150)
                tree.column("time", width=120)
                tree.column("status", width=200)

                tree.pack(fill="both",expand=True)

                if rows:
                    for row in rows:
                        tree.insert("", "end", values=row)
                else:
                    tree.insert("", "end", values=("No Appointments Found", "", "", "", ""))

                conn.close()

            #----Deleting the appointments---#

                def delete_appointment():
                    selected = tree.selection()

                    if not selected:
                        messagebox.showwarning("Warning", "Select hospital first!")
                        return
                    
                    appointment_data = tree.item(selected[0], "values")

                    appointment_id = appointment_data[0]
                    hospital_name = appointment_data[1]
                    appointment_date = appointment_data[2]
                    appointment_time = appointment_data[3]

                    # mysql connection
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="root",
                        database="blood_donation"
                    )
                    cursor = conn.cursor()

                    # slots updating
                    cursor.execute("""
                        UPDATE hospital_slots
                        SET is_available = 1
                        WHERE hospital_name = %s
                        AND slot_date = %s
                        AND slot_time = %s
                    """, (hospital_name, appointment_date, appointment_time))

                    # deleting the appointment
                    cursor.execute("""
                        DELETE FROM appointments
                        WHERE id = %s
                    """, (appointment_id,))

                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Success", "Appointment Cancelled Successfully")

                ctk.CTkButton(content_frame,text='delete appointment',fg_color="red",command=delete_appointment).pack(fill="x",padx=20,pady=10)

            table_view(content_frame)



    #----------------profile page------------------#

        def profile_page():
            clear_content()

            ctk.CTkLabel(content_frame,text="Your Donor Profile",font=("Arial",28,"bold")).pack(anchor="w",padx=30,pady=20)


            details_frame=ctk.CTkFrame(content_frame,fg_color="#F9F6F6")
            details_frame.pack(fill="x",padx=(30,30),pady=25)
            def create_details(text,row):
                ctk.CTkLabel(
                            details_frame,
                            text=text,
                            font=("Segoe UI", 18 , "bold")
                        ).grid(row=row, column=0, sticky="w", padx=(30, 10), pady=10)
            

            create_details(f"Name         : {name}",0)
            create_details(f"Blood Type         :{blood_group}",1)
            create_details(f"EMAIL        :{email}",2)
            create_details(f"Contact       :{contact}",3)
            create_details(f"Location      :{location}",4)
            create_details(f"Medical history       :{medical_text}",5)



        def logout():
            parent.destroy()
            # clear_content
            # from blood_app import login
            # login()
            
            


        # -------------------- SIDEBAR BUTTONS --------------------

        def sidebar_button(text, command):
            return ctk.CTkButton(
                sidebar,
                text=text,
                height=45,
                fg_color="#34495e",
                hover_color="#3d566e",
                text_color="white",
                command=command
            )

        sidebar_button("Dashboard", dashboard_page).pack(fill="x", padx=20, pady=5)
        sidebar_button("Find Hospitals", hospitals_page).pack(fill="x", padx=20, pady=5)
        sidebar_button("My Appointments", appointments_page).pack(fill="x", padx=20, pady=5)
        sidebar_button("Profile", profile_page).pack(fill="x", padx=20, pady=5)
        sidebar_button("Logout", logout).pack(fill="x", padx=20, pady=5)

        # Load default page
        dashboard_page()


