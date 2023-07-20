from datetime import datetime
from tkcalendar import Calendar
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import os
import sqlite3

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("EVENT CALENDAR")
        self.geometry("1100x580")

        # Create a frame for the calendar
        self.calendar_frame = ctk.CTkFrame(self)
        self.calendar_frame.pack(fill=ctk.BOTH, expand=True)

        # Connect to the database
        self.conn = sqlite3.connect("user_data.db")
        self.create_reminders_table()
        self.cursor=self.conn.cursor()

        # Create a calendar widget
        self.calendar = Calendar(self.calendar_frame, selectmode='day')
        self.calendar.pack(padx=50, pady=50)

        # Create a frame for the event entry
        self.event_frame = ctk.CTkFrame(self)
        self.event_frame.pack(fill=ctk.BOTH, expand=True)

        # Create a label and entry for the event title
        self.event_title_label = ctk.CTkLabel(self.event_frame, text="Event Title:")
        self.event_title_label.pack(padx=20, pady=(20, 5))
        self.event_title_entry = ctk.CTkEntry(self.event_frame)
        self.event_title_entry.pack(padx=20, pady=5)

        # Create a label and entry for the event description
        self.event_description_label = ctk.CTkLabel(self.event_frame, text="Event Description:")
        self.event_description_label.pack(padx=20, pady=5)
        self.event_description_entry = ctk.CTkEntry(self.event_frame)
        self.event_description_entry.pack(padx=20, pady=5)

        # Create a button to add the event
        self.add_event_button = ctk.CTkButton(self.event_frame, text="Add Event", command=self.add_event)
        self.add_event_button.pack(padx=20, pady=10)
        self.back_button = ctk.CTkButton(self.event_frame, text="⬅", command=self.go_to_main)
        self.back_button.place(x=10, rely=1.0, anchor=tk.SW)

        # Load reminders from the database
        self.load_reminders()

    def create_reminders_table(self):
        """Create the reminders table in the database if it doesn't exist."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                title TEXT,
                description TEXT,
                username TEXT
            )
            """
        )
        self.conn.commit()

    def load_reminders(self):
        """Load reminders from the database and display them."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM reminders")
        reminders = cursor.fetchall()

        self.event_labels = {}

        for reminder in reminders:
            date_str, title, description = reminder[1], reminder[2], reminder[3]
            event_label = ctk.CTkLabel(self.calendar_frame, text=f"{date_str}: {title}-{description}")
            event_label.pack(padx=20, pady=5)
            self.event_labels[(date_str, title, description)] = event_label

            # Get the current date and time
            current_datetime = datetime.now()

            # Calculate the time difference between the current time and the reminder date
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time_difference = date - current_datetime.date()

            # Check if the reminder is in the future
            if time_difference.days >= 0:
                # Calculate the number of seconds until the reminder occurs
                seconds_until_reminder = time_difference.total_seconds()

                # Create a reminder using the event details and scheduled time
                self.after(int(seconds_until_reminder * 1000), self.show_reminder, reminder)

    def add_event(self):
        # Get the selected date from the calendarrs
        conn = sqlite3.connect("user_data.db")
        cursor=conn.cursor()
        selected_date = self.calendar.selection_get()
        selected_date_str = selected_date.strftime("%Y-%m-%d")

        # Get the event title and description
        event_title = self.event_title_entry.get()
        event_description = self.event_description_entry.get()

        # Insert the event into the database
        #cursor = self.conn.cursor()
        try:
            cursor.execute(f"SELECT username from status WHERE state=True")
            active_user=cursor.fetchone()[0]
        except:
            pass
        print(active_user)
        query = f"""
        INSERT INTO reminders (date, title, description, username)
        VALUES ('{selected_date_str}', '{event_title}', '{event_description}', '{active_user}')
        """

    # Execute the SQL query
        cursor.execute(query)
        conn.commit()

        # Create a label to display the event
        event_label = ctk.CTkLabel(self.calendar_frame, text=f"{selected_date_str}: {event_title}-{event_description}")
        event_label.pack(padx=20, pady=5)
        self.event_labels[(selected_date_str, event_title, event_description)] = event_label

        # Get the current date and time
        current_datetime = datetime.now()

        # Calculate the time difference between the current time and the selected event date
        time_difference = selected_date - current_datetime.date()

        # Check if the event is in the future
        if time_difference.days >= 0:
            # Calculate the number of seconds until the event occurs
            seconds_until_event = time_difference.total_seconds()

            # Create a reminder using the event details and scheduled time
            self.after(int(seconds_until_event * 1000), self.show_reminder, (selected_date_str, event_title, event_description))

        # Clear the event entry fields
        self.event_title_entry.delete(0, ctk.END)
        self.event_description_entry.delete(0, ctk.END)

    def show_reminder(self, reminder):
        # Display a message box with the event details
        date_str, event_title, event_description = reminder
        messagebox.showinfo("Event Reminder", f"Event: {event_title}\nDescription: {event_description}")

        # Remove the reminder from the database
        cursor = self.conn.cursor()
        cursor.execute(
            """
            DELETE FROM reminders
            WHERE date = ? AND title = ? AND description = ?
            """,
            (date_str, event_title, event_description)
        )
        self.conn.commit()

    def go_to_main(self):
        # Code to navigate to main.py
        self.destroy()
        os.system("python main.py")

    def __del__(self):
        # Close the database connection when the app is closed
        self.conn.close()


if __name__ == "__main__":
    app = App()
    app.mainloop()
