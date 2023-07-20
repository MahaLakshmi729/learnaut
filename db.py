import tkinter as tk
import tkinter.messagebox
import customtkinter
from time import strftime
import os
from datetime import date
import sqlite3

# Set the appearance mode and default color theme
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


# Create the main application class
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Connect to the SQLite database
        self.connection = sqlite3.connect("your_database_file.db")
        self.cursor = self.connection.cursor()

        # Create the necessary tables if they don't exist
        self.create_tables()

        # Configure the main window
        self.title("Study_planner.py")
        self.geometry(f"{1100}x{580}")

        # ...

    def create_tables(self):
        # Create the necessary tables if they don't exist
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                )
            """
        )
        self.connection.commit()
        self.connection.close()

    def open_task_app(self):
        # Open the task.py file and pass the database connection
        os.system("python task.py {}".format(self.connection))

def add_task_app(name, description):
    connection = sqlite3.connect("your_database_file.db")
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO tasks (name, description)
        VALUES (?, ?)
        """,
        (name, description)
    )
    connection.commit()
    connection.close()
    
        
        
        


if __name__ == "__main__":
    app = App()
    app.mainloop()
