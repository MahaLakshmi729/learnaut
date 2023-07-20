import subprocess
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

        # Configure the main window
        self.title("STUDY_PLANNER")
        self.geometry(f"{1100}x{580}")
        
        #self.attributes("-fullscreen", True)
        #self.bind("<Escape>", self.exit_fullscreen) 

        # Configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create the sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        # Create widgets in the sidebar frame
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Dashboard", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="TASK/GOAL", command=self.open_task_app)
        self.sidebar_button_2.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="CALENDAR",command=self.open_calender_app)
        self.sidebar_button_3.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="TIMETABLE",command=self.open_timetable_app)
        self.sidebar_button_4.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text="RESOURCES",command=self.open_resources_app)
        self.sidebar_button_5.grid(row=4, column=0, padx=20, pady=10)
        self.sidebar_button_6 = customtkinter.CTkButton(self.sidebar_frame, text="TIC_TAC_TOE",command=self.open_tic_app)
        self.sidebar_button_6.grid(row=5, column=0, padx=20, pady=10)
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="HELP", command=self.open_help_app)
        self.sidebar_button_1.grid(row=6, column=0, padx=20, pady=10)
        self.sidebar_button_7 = customtkinter.CTkButton(self.sidebar_frame, text="LOGOUT", command=self.logout)
        self.sidebar_button_7.grid(row=7, column=0, padx=20, pady=10)
        #self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        #self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))

        # Create the textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

               

        # Create the scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="COURSE TASK")
        self.scrollable_frame.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for i in range(1, 26, 1):
            switch = customtkinter.CTkCheckBox(master=self.scrollable_frame, text=f"DAY {i}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)

        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.textbox.insert("0.1", " " + " " )
        self.textbox = customtkinter.CTkLabel(self.textbox, text="NOTE", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.textbox.grid(row=0, column=0, padx=0, pady=(0), sticky="N")

        # Create the digital clock label
        self.clock_label = customtkinter.CTkLabel(self, font=customtkinter.CTkFont(size=50, weight="bold"))
        self.clock_label.grid(row=1, column=1, pady=(20, 0), sticky="nsew")

        # Create the date label
        self.date_label = customtkinter.CTkLabel(self, font=customtkinter.CTkFont(size=20))
        self.date_label.grid(row=2, column=1, padx=(0, 20), pady=(0, 20),sticky="nsew")

        # Update the clock and date every second
        self.update_clock()

    def update_clock(self):
        current_time = strftime("%H:%M:%S")
        current_date = date.today().strftime("%B %d, %Y")
        self.clock_label.configure(text=current_time)
        self.date_label.configure(text=current_date)
        self.after(1000, self.update_clock)


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def open_task_app(self):
        self.destroy()
        os.system("python task.py")

    def open_tic_app(self):
        self.destroy()
        os.system("python tic.py")

    def open_calender_app(self):
        self.destroy()
        os.system("python calender.py")

    def open_timetable_app(self):
        self.destroy()
        os.system("python timetable.py")

    def open_resources_app(self):
        self.destroy()
        os.system("python resources.py")

    def open_help_app(self):
        self.destroy()
        os.system("python help.py")
        
    def logout(self):
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT username from status WHERE state=True")
            active_user=cursor.fetchone()[0]
        except:
            pass
        if active_user:
            cursor.execute(f"UPDATE status set state=False WHERE username='{active_user}'")
            conn.commit()
            self.destroy()
            os.system("python reg_login.py")
            
            #subprocess.Popen(["python", "main.py"])
            
        #app.destroy()
        # self.destroy()
        # os.system("python reg_login.py")
        

if __name__ == "__main__":
    app = App()
    app.mainloop()

