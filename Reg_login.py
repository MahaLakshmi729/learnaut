import subprocess
import customtkinter as ctk
import sqlite3
import os
import tkinter
from tkinter import messagebox
import tkinter as tk
from PIL import ImageTk,Image
import hashlib

class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("STUDY_PLANNER")
        self.geometry("1100x580")
        
        img1=ImageTk.PhotoImage(Image.open("pattern.png"))
        l1=ctk.CTkLabel(master=self,image=img1)
        l1.pack()

        # Create a frame for the login form
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame = frame=ctk.CTkFrame(master=l1, width=380, height=340, corner_radius=15)
        self.login_frame.grid(row=0, column=0, padx=(50,50), pady=50)
        #self.login_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)



        # Create a label and entry for the username
        self.username_label = ctk.CTkLabel(self.login_frame, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = ctk.CTkEntry(self.login_frame)
        self.username_entry.pack()

        # Create a label and entry for the password
        self.password_label = ctk.CTkLabel(self.login_frame, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.login_frame, show="*")
        self.password_entry.pack()

        # Create a login button
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        # Create a register label
        self.register_label = ctk.CTkLabel(self.login_frame, text="Don't have an account?")
        self.register_label.pack()

        # Create a register link
        self.register_link = ctk.CTkLabel(self.login_frame, text="Register", cursor="hand2")
        self.register_link.pack()
        self.register_link.bind("<Button-1>", lambda event: self.open_registration_page())

    def login(self):
        # Get the entered username and password
        global username
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(password)

        # Validate the username and password
        if username and password:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            print(hashed_password)
            # if user:
            #     stored_password = user[1]
            #     hashed_password = hashlib.sha256(password.encode()).hexdigest()
            #     if hashed_password == stored_password:
            #         # Passwords match, login successful
            #         subprocess.Popen(["python", "main.py"])
            #         self.destroy()
            #     else:
            #         messagebox.showerror("Error", "Invalid username or password.")
            # else:
            #     messagebox.showerror("Error", "Invalid username or password.")
            # Create a connection to the database
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()

            # Retrieve the user from the database
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
            user = cursor.fetchone()
            if user:
                
                
                    
                subprocess.Popen(["python", "main.py"])
                self.destroy()
                cursor.execute(f"UPDATE status SET state=True WHERE username='{username}' ")
                conn.commit()
                
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        

            # Close the database connection
            conn.close()
        else:
            messagebox.showerror("Error", "Please enter a username and password.")

    def open_registration_page(self):
        # Close the login page
        self.destroy()

        # Open the registration page
        registration_page = RegistrationPage()
        registration_page.mainloop()

class RegistrationPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Registration Page")
        self.geometry("1100x580")

        img1=ImageTk.PhotoImage(Image.open("pattern.png"))
        l1=ctk.CTkLabel(master=self,image=img1)
        l1.pack()
        
        
        self.registration_frame = ctk.CTkFrame(self)
        self.registration_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create a label and entry for the username
        self.username_label = ctk.CTkLabel(self.registration_frame, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = ctk.CTkEntry(self.registration_frame)
        self.username_entry.pack()

        # Create a label and entry for the password
        self.password_label = ctk.CTkLabel(self.registration_frame, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.registration_frame, show="*")
        self.password_entry.pack()

        # Create a label and entry for confirming the password
        self.confirm_password_label = ctk.CTkLabel(self.registration_frame, text="Confirm Password:")
        self.confirm_password_label.pack(pady=5)
        self.confirm_password_entry = ctk.CTkEntry(self.registration_frame, show="*")
        self.confirm_password_entry.pack()

        # Create a register button
        self.register_button = ctk.CTkButton(self.registration_frame, text="Register", command=self.register)
        self.register_button.pack(pady=10)

        # Create a login label
        self.login_label = ctk.CTkLabel(self.registration_frame, text="Already have an account?")
        self.login_label.pack()

        # Create a login link
        self.login_link = ctk.CTkLabel(self.registration_frame, text="Login", cursor="hand2")
        self.login_link.pack()
        self.login_link.bind("<Button-1>", lambda event: self.open_login_page())

    def register(self):
        # Get the entered username and password
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Validate the username and password
        if username and password and confirm_password:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()

                # Create the users table if it doesn't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS users
                                  (username TEXT, password TEXT)''')

                # Check if the username already exists
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                messagebox.showerror("Error", "Username already exists!")
                self.destory()
                subprocess.Popen(["python", "Reg_login.py"])
                
            try:
                if password == confirm_password:
        #if user:
                    #stored_password = [1]
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                    #if hashed_password == stored_password:
                        # Passwords match, login successful
                    conn=sqlite3.connect('user_data.db')
                    cursor=conn.cursor()
                    # cursor.execute("SELECT username FROM users")
                    # username_data=cursor.fetchall()
                    # usernames = [user_tuple[0] for user_tuple in username_data]
                    # for u in usernames:
                    #     if u==username:
                    #         messagebox.showerror("Error")
                    cursor.execute("INSERT INTO users VALUES (?, ?)", (username, hashed_password))
                    conn.commit()
                    messagebox.showinfo("Success", "Registration successful!")
                    conn = sqlite3.connect('user_data.db')
                    cursor = conn.cursor()
                    cursor.execute('''CREATE TABLE IF NOT EXISTS status
                    (username TEXT, state BINARY)''')
                    cursor.execute("INSERT INTO status VALUES (?, ?)", (username, False))
                    conn.commit()
                    #subprocess.Popen(["python", "main.py"])
                    #self.destroy()
                else:
                    messagebox.showerror("Error", "Password doesn't match!!")
                    # Create a connection to the database
            except:
                pass
            
                
        else:
            messagebox.showerror("Error", "Please enter a username, password, and confirm password.")
        

    def open_login_page(self):
        # Close the registration page
        self.destroy()
        

        # Open the login page
        login_page = LoginPage()
        login_page.mainloop()
        #subprocess.Popen(["python", "main.py"])
        
if __name__ == "__main__":
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT username from status WHERE state=True")
        active_user=cursor.fetchone()[0]
        if active_user:
            subprocess.Popen(["python", "main.py"])
    except:
        app = LoginPage()
        app.mainloop()

