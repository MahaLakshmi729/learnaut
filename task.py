import tkinter as tk
import tkinter.messagebox as messagebox
import sqlite3
from sqlite3 import Error
from tkinter import ttk
from time import strftime
import os
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import ttk
import numpy as np

# Set the appearance mode and default color theme
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


# Create the main application class
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("TASK/GOAL")
        self.geometry(f"{1100}x{580}")

        # Configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Create the sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

        # Create the input bar for getting tasks
        self.task_entry = customtkinter.CTkEntry(self, placeholder_text="Enter a task")
        self.task_entry.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Create the label for task progress
        self.progress_label = customtkinter.CTkLabel(self, text="TASK PROGRESS")
        self.progress_label.grid(row=3, column=1, padx=10, pady=(0, 10), sticky="nsew")

        # Create the progress bar
        self.progress_bar = customtkinter.CTkProgressBar(self, orientation="horizontal", mode="determinate")
        self.progress_bar.grid(row=4, column=1, padx=(10, 10), sticky="ew")
        self.progress_bar.set(0.)

        # Create the figure and canvas for the graph
        self.fig, self.ax1 = plt.subplots(figsize=(6, 4))  # Adjust the figure size here
        self.ax2 = self.ax1.twinx()  # Create a second y-axis

        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.graph_canvas.get_tk_widget().grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Create the sidebar buttons
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Add Task", command=self.add_task)
        self.sidebar_button_2.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Add Goal", command=self.add_goal)
        self.sidebar_button_3.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Complete Task",
                                                        command=self.complete_task)
        self.sidebar_button_4.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text="List Task", command=self.list_tasks)
        self.sidebar_button_5.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.sidebar_button_6 = customtkinter.CTkButton(self.sidebar_frame, text="Generate Code",
                                                        command=self.generate_code)
        self.sidebar_button_6.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Generate Graph",
                                                        command=self.generate_graph)
        self.sidebar_button_1.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        self.sidebar_button_7 = customtkinter.CTkButton(self.sidebar_frame, text="Show Progress",
                                                        command=self.show_progress)
        self.sidebar_button_7.grid(row=6, column=0, padx=20, pady=10, sticky="w")
        self.sidebar_button_8 = customtkinter.CTkButton(self.sidebar_frame, text="Save Graph", command=self.save_graph)
        self.sidebar_button_8.grid(row=7, column=0, padx=20, pady=(10, 60), sticky="w")
        # Create the back arrow button
        self.back_button = customtkinter.CTkButton(self.sidebar_frame, text="⬅", command=self.go_to_main)
        self.back_button.grid(row=8, column=0, padx=20, pady=(0, 20), sticky="w")

        # Initialize data structures
        self.tasks = []
        self.goals = []
        self.progress = 0
        self.total_tasks = 0

        self.conn = self.create_connection()
        self.create_table(self.conn)
        self.load_tasks()

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect("user_data.db")  # Create or connect to the tasks.db file
            print("Connected to SQLite database")
            return conn
        except Error as e:
            print(e)
        return conn

    def create_table(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    user TEXT NOT NULL
                )
            """)
            conn.commit()
            print("Table created successfully")
        except Error as e:
            print(e)

    def load_tasks(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT task FROM tasks")
            rows = cursor.fetchall()
            for row in rows:
                self.tasks.append(row[0])
                self.total_tasks += 1
        except Error as e:
            print(e)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT username FROM status WHERE state=True")
                username = cursor.fetchone()[0]
                print(username)
                cursor.execute("INSERT INTO tasks (task,user) VALUES (?,?)", (task,username))
                self.conn.commit()
                self.tasks.append(task)
                self.total_tasks += 1
                messagebox.showinfo("Task Added", "Task has been added successfully.")
                self.task_entry.delete(0, tk.END)
                self.progress_bar.set(0)
            except Error as e:
                print(e)
        else:
            messagebox.showwarning("Invalid Input", "Please enter a task.")

    def add_goal(self):
        goal = self.task_entry.get()
        if goal:
            self.goals.append(goal)
            messagebox.showinfo("Goal Added", "Goal has been added successfully.")
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Invalid Input", "Please enter a goal.")

    def complete_task(self):
        selected_task = self.task_entry.get()
        if selected_task:
            if selected_task in self.tasks:
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("DELETE FROM tasks WHERE task=?", (selected_task,))
                    self.conn.commit()
                    self.tasks.remove(selected_task)
                    self.progress += 1
                    self.update_progress_bar()
                    messagebox.showinfo("Task Completed", "Task has been completed and removed from the list.")
                    self.task_entry.delete(0, tk.END)
                    self.progress_bar["value"] = 0  # Reset the progress bar value to 0
                    self.progress_bar.set(1)
                except Error as e:
                    print(e)
            else:
                messagebox.showwarning("Task Not Found", "The entered task does not exist in the list.")
        else:
            messagebox.showwarning("Invalid Input", "Please enter a task.")

    def list_tasks(self):
        if self.tasks:
            task_list = "\n".join(self.tasks)
            messagebox.showinfo("Task List", f"Tasks:\n{task_list}")
        else:
            messagebox.showinfo("Task List", "No tasks found.")

    def generate_code(self):
        if self.tasks or self.goals:
            code = "# Generated code based on tasks and goals:\n"
            for index, task in enumerate(self.tasks, start=1):
                code += f"task_{index} = '{task}'\n"
            for index, goal in enumerate(self.goals, start=1):
                code += f"goal_{index} = '{goal}'\n"
            messagebox.showinfo("Generated Code", code)
        else:
            messagebox.showwarning("No Data", "No tasks or goals found. Please add tasks/goals before generating code.")

    def generate_graph(self):
        if self.tasks or self.goals:
            self.fig, self.ax1 = plt.subplots(figsize=(6, 4))  # Adjust the figure size here
            self.ax2 = self.ax1.twinx()  # Create a second y-axis

            num_tasks = len(self.tasks)
            num_goals = len(self.goals)

            x = np.linspace(0, 10, 100)
            y_tasks = np.sin(x) * 10  # Placeholder wave data for task progress
            y_goals = np.cos(x) * 20  # Placeholder wave data for goals

            self.ax1.plot(x, y_tasks, label='Task Progress', color='blue')
            self.ax2.plot(x, y_goals, label='Goals', color='orange')

            self.ax1.set_ylabel("Task Progress")
            self.ax2.set_ylabel("Goals")
            self.ax1.set_xlabel("Time")

            self.ax1.set_title("Task Progress and Goals")

            self.ax1.legend(loc='upper left')
            self.ax2.legend(loc='upper right')

            self.graph_canvas = FigureCanvasTkAgg(self.fig, master=self)
            self.graph_canvas.get_tk_widget().grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

            messagebox.showinfo("Graph", "Graph has been generated.")

        else:
            messagebox.showwarning("No Data", "No tasks or goals found. Please add tasks/goals before generating the graph.")


    def save_graph(self):
        if self.tasks or self.goals:
            file_path = tk.filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.fig.savefig(file_path)
                messagebox.showinfo("Save Graph", "Graph has been saved.")
        else:
            messagebox.showwarning("No Data",
                                   "No tasks or goals found. Please add tasks/goals before saving the graph.")

    def show_progress(self):
        if self.tasks:
            for task in self.tasks:
                messagebox.showinfo("Task Progress", f"Task: {task}\nProgress: {self.get_task_progress(task)}%")
                self.progress_bar.set(0.5)
        else:
            messagebox.showwarning("No Tasks", "No tasks found.")

    def get_task_progress(self, task):
        # Placeholder function to get the progress of a task
        # Modify this function to retrieve the actual progress of the task
        return 0

    def update_progress_bar(self):
        progress_percentage = (self.progress / self.total_tasks) * 100
        self.progress_bar["value"] = progress_percentage

        if self.progress == self.total_tasks:
            messagebox.showinfo("Progress Complete",
                                "All tasks have been completed! Don't forget to celebrate!")

    def go_to_main(self):
        # Code to navigate to main.py
        self.destroy()
        os.system("python main.py")


if __name__ == "__main__":
    app = App()
    app.mainloop()