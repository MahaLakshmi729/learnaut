import customtkinter as ctk
import webbrowser
import tkinter as tk
import tkinter
import os

class StudyPlannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("RESOURCES")
        self.geometry("1100x580")

        # Create a frame for resources
        resources_frame = ctk.CTkFrame(self)
        resources_frame.pack(pady=100, padx=100, anchor=tkinter.CENTER)

        # Add a title
        title_label = ctk.CTkLabel(resources_frame, text="Resources for Python", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=30, padx=10)

        # Create a frame for the buttons
        buttons_frame = ctk.CTkFrame(resources_frame)
        buttons_frame.pack(pady=30)

        # Define the resources
        resources = [
            {"name": "CYBERNAUT", "link": "https://cybernaut.co.in/product/trio-c-python-java/"},
            {"name": "PROGRAMIZ", "link": "https://www.programiz.com/python-programming"},
            {"name": "GREEKS FOR GEEKS", "link": "https://www.geeksforgeeks.org/python-basics/"},
            {"name": "JAVATPOINT", "link": "https://www.javatpoint.com/python-tutorial"},
            {"name": "LEARNPYTHON", "link": "https://www.learnpython.org/"},
            {"name": "W3SCHOOL", "link": "https://www.w3schools.com/python/"},
            {"name": "UDEMY", "link": "https://www.udemy.com/topic/python/"},
            {"name": "DATACAMP", "link": "https://www.datacamp.com/learn/python"},
            {"name": "TUTORIALSPOINT", "link": "https://www.tutorialspoint.com/python/index.htm"},
            {"name": "GOOGLE DEVELOPERS", "link": "https://developers.google.com/edu/python"},
            {"name": "REAL PYTHON", "link": "https://realpython.com/products/"},
            {"name": "PYTHON TUTORIAL", "link": "https://www.pythontutorial.net/"}
        ]

        # Calculate the number of columns for the grid layout
        num_cols = 4

        # Create buttons for each resource
        for i, resource in enumerate(resources):
            button = ctk.CTkButton(buttons_frame, text=resource["name"], cursor="hand2", font=("Helvetica", 14),
                                   command=lambda link=resource["link"]: self.open_link(link))
            button.grid(row=i // num_cols, column=i % num_cols, padx=15, pady=15)

        # Create the back arrow button
        back_button = ctk.CTkButton(resources_frame, text="⬅", font=("Helvetica", 16, "bold"), command=self.go_to_main)
        back_button.place(x=10, y=self.winfo_height() - 100, anchor="sw")

    def open_link(self, link):
        webbrowser.open(link)

    def go_to_main(self):
        # Code to navigate to main.py
        self.destroy()
        os.system("python main.py")


if __name__ == "__main__":
    app = StudyPlannerApp()
    app.mainloop()
