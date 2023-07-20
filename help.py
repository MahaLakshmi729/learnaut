import tkinter as tk
import tkinter.messagebox as messagebox
import customtkinter
import os


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light")
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("HELP")
        self.geometry(f"{1100}x{580}")

        # Create a sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create a back arrow button
        self.back_button = customtkinter.CTkButton(self.sidebar_frame, text="⬅", command=self.go_to_main)
        self.back_button.place(x=10, rely=1.0, anchor=tk.SW)

        # Create task list
        self.tasks = []

        # Create a frame to hold the label and scrollbar
        frame = tk.Frame(self)
        frame.pack()

        # Create a scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a text widget to display the long text
        text_widget = tk.Text(frame, font=("Arial", 18), padx=10, pady=10, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH)

        # Configure the scrollbar
        scrollbar.config(command=text_widget.yview)

        long_text = "- Dashboard: Include a button/tab to navigate to the dashboard, which provides an overview of the user's study schedule, progress, and upcoming tasks.\n" \
                    "\n" \
                    "- Calendar: Provided a button/tab to access the calendar view, where users can add an event on their respective day.Stay on top of your workload by receiving notifications of upcoming classes, assignments or exams, as well as incomplete tasks, on all your devices.\n" \
                    "\n" \
                    "- Tasks/Goal: Provided a button/tab to manage tasks or assignments. Users can add, edit, or delete specific tasks related to their subjects and provided with goal button by that graph will be generate accordingly.\n" \
                    "\n" \
                    "- Study Timetable: Shows the user's daily or weekly study schedule, showing the subjects or courses, time slots, and allocated study hours. Allow users to click on a study session to view or edit their subjects.\n" \
                    "\n" \
                    "- Study Resources: Provide quick access to study materials, resources, or links that users frequently refer to during their study sessions.\n" \
                    "\n" \
                    "- TIC-TAC-TOE: You can now play against the computer in the Tic Tac Toe game. Have fun!.\n" \
                    "\n" \
                    "- Settings: Include a button/link to access Dark Mode/Light Mode, where users can personalize their preferences, UI - Scaling to Zoom in/Zoom out according to their preferences.\n" \
                    "\n" \
                    "- Help/Support: Provide a button/link to access help or support documentation.\n" \
                    "\n" \
                    "Credits:\n" \
                    "The Study Planner Application is developed by Python Team (2023) from Cybernaut.\n" \
                    "\n" \
                    "Team members:\n" \
                    "Melvin Joseph\n" \
                    "Kevin Joseph\n" \
                    "Mahalakshmi G\n" \
                    "Samiya Banu\n" \
                    "Sharvesh R\n" \
                    "\n" \
                    "Thank You for using the app.\n" \
                    "\n" \
                    "Made with❤️by python team"

        # Insert the long text into the text widget
        text_widget.insert(tk.END, long_text)

        # Disable editing in the text widget
        text_widget.configure(state=tk.DISABLED)

    def go_to_main(self):
        # Code to navigate to main.py
        self.destroy()
        os.system("python main.py")

if __name__ == "__main__":
    app = App()
    app.mainloop()
