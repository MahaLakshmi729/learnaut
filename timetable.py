import tkinter as tk
import customtkinter as ctk
import os
import sqlite3

class TimetableApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("TIMETABLE")
        self.geometry("1100x580")

        # Create a frame for the timetable
        self.timetable_frame = ctk.CTkFrame(self)
        self.timetable_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create a back arrow button
        self.back_button = ctk.CTkButton(self.sidebar_frame, text="⬅", command=self.go_to_main)
        self.back_button.pack(pady=(20, 0))
        
        # Create a list of weekdays
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        # Create labels for weekdays
        for i, weekday in enumerate(weekdays):
            label = ctk.CTkLabel(self.timetable_frame, text=weekday)
            label.grid(row=0, column=i+1, padx=10, pady=10)

        # Create labels for time slots
        time_slots = ["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"]
        for i, time_slot in enumerate(time_slots):
            label = ctk.CTkLabel(self.timetable_frame, text=time_slot)
            label.grid(row=i+1, column=0, padx=10, pady=10)

        # Create entry fields for timetable slots
        self.timetable_entries = []
        for i in range(len(time_slots)):
            row_entries = []
            for j in range(len(weekdays)):
                entry = ctk.CTkEntry(self.timetable_frame)
                entry.grid(row=i+1, column=j+1, padx=10, pady=10)
                #entry.insert(0," hello")
                
                row_entries.append(entry)
            self.timetable_entries.append(row_entries)
            
        # Set the reminder interval in milliseconds (e.g., 10 minutes = 600,000 ms)
        self.reminder_interval = 600000
        self.reminder_id = None
        self.schedule_reminder()


        # Create a button to save the timetable
        self.save_button = ctk.CTkButton(self, text="Save Timetable", command=self.save_timetable)
        self.save_button.pack(pady=10)

        # Initialize the database
        self.initialize_database()

    def initialize_database(self):
        # Connect to the database or create one if it doesn't exist
        self.conn = sqlite3.connect("user_data.db")
        self.cursor = self.conn.cursor()

        # Create a table for timetable data if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS timetable (
                id INTEGER PRIMARY KEY,
                time_slot TEXT,
                weekday TEXT,
                entry_data TEXT,
                username TEXT
            )
        """)
        self.conn.commit()

    
    def save_timetable(self):
    # Get the timetable data from the entry fields
        timetable_data = []
        for i, row_entries in enumerate(self.timetable_entries):
            for j, entry in enumerate(row_entries):
                time_slot = self.timetable_frame.grid_slaves(row=i + 1, column=0)[0].cget("text")
                weekday = self.timetable_frame.grid_slaves(row=0, column=j + 1)[0].cget("text")
                entry_data = entry.get()

            # Check if the entry_data is not empty before inserting into the database
                if entry_data.strip():
                    try:
                        self.cursor.execute(f"SELECT username from status WHERE state=True")
                        active_user=self.cursor.fetchone()[0]
                    except:
                        pass# strip() removes leading and trailing whitespaces
                    timetable_data.append((time_slot, weekday, entry_data,active_user))
                

    # Insert the timetable data into the database
        self.cursor.executemany("INSERT INTO timetable (time_slot, weekday, entry_data,username) VALUES (?, ?, ?, ?)", timetable_data)
        self.conn.commit()

    # Display a success message
        ctk.messagebox.showinfo("Success", "Timetable saved successfully!")
        self.schedule_reminder()
        
    def retrieve_data(self):
        try:
            self.cursor.execute(f"SELECT username from status WHERE state=True")
            active_user=self.cursor.fetchone()[0]
        except:
            pass#
        self.cursor.execute(f"SELECT time_slot, weekday, entry_data FROM timetable WHERE username='{active_user}'")
        rows = self.cursor.fetchall()
        for row in rows:
            time_slot, weekday, entry_data = row
            for i, row_entries in enumerate(self.timetable_entries):
                for j, entry in enumerate(row_entries):
                    if (
                        self.timetable_frame.grid_slaves(row=i + 1, column=0)[0].cget("text") == time_slot
                        and self.timetable_frame.grid_slaves(row=0, column=j + 1)[0].cget("text") == weekday
                    ):
                        entry.delete(0, tk.END)  # Clear the entry field
                        entry.insert(0, entry_data)  # Insert the data from the database
        

    def schedule_reminder(self):
        # Cancel the previous reminder (if any)
        if self.reminder_id is not None:
            self.after_cancel(self.reminder_id)

        # Schedule the next reminder
        self.reminder_id = self.after(self.reminder_interval, self.show_reminder)
        
    def show_reminder(self):
        # Display the reminder message
        ctk.messagebox.showinfo("Reminder", "Don't forget to update your timetable!")

        # Schedule the next reminder
        self.schedule_reminder()

    def go_to_main(self):
        # Code to navigate to main.py
        self.destroy()
        os.system("python main.py")

    def on_close(self):
        # Close the database connection
        self.conn.close()


if __name__ == "__main__":
    app = TimetableApp()
    app.retrieve_data()
    app.mainloop()
