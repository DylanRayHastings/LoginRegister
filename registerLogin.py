# There is no check to prevent a user from logging in with an empty username or password field.
# The password hash is stored in plain text in the database. This is a security issue as the passwords can be easily retrieved in case of a data breach.
# There is no password confirmation field during registration, so there's no way to confirm that the user has entered the correct password.
# The query to retrieve the password from the database is vulnerable to SQL injection attacks.
# There is no error handling for the database connection, so the code may crash if there is a problem connecting to the database.

import tkinter as tk  #  MODULES FOR GUI
import tkinter.ttk as ttk
from tkinter import messagebox  # MESSAGE BOXES
from tkinter import PhotoImage  # IMAGES
import sqlite3  # DATABASE CONNECTIVITY
import webbrowser  # WEB CONNECTIVITY
import subprocess  # SUBPROCESS
from PIL import Image  # IMAGE PROCESSING
import time  # TIME
import bcrypt
import logging

logging.basicConfig(
    filename="app.log", level=logging.DEBUG, format="%(asctime)s %(message)s"
)


class MainApplication(tk.Tk):
    """
    The MainApplication class is a Tkinter GUI based application that acts as a container for the login and register screens.

    Attributes:
    container: A frame widget that acts as the parent container for other frames in the application.
    frames: A dictionary that maps the frame classes to their instances.

    Methods:
    __init__: Initializes the Tkinter window and creates the container frame widget. It also creates instances of the LoginScreen and RegisterScreen frames and adds them to the frames dictionary.
    show_frame: Raises the specified frame to the top of the window stack and makes it visible to the user.
    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (LoginScreen, RegisterScreen):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginScreen)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class LoginScreen(tk.Frame):
    """
    LoginScreen class is a tkinter GUI based frame that provides functionality for user login.

    Attributes:
    parent: parent widget for the frame
    controller: object of MainApplication class

    Methods:
    __init__: initializes the frame and creates the necessary widgets for the login screen
    login: connects to the database, checks if the provided username and password match any existing user, and outputs the result
    clear_username: clears the username entry widget if it contains the placeholder text
    set_username: sets the placeholder text in the username entry widget if it's empty
    clear_password: clears the password entry widget if it contains the placeholder text
    set_password: sets the placeholder text in the password entry widget if it's empty
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.font = ("Courier", 20)

        self.username_entry = ttk.Entry(self, font=self.font)
        self.username_entry.insert(0, "Username")
        self.username_entry.bind("<FocusIn>", self.clear_username)
        self.username_entry.grid(row=0, column=0, padx=10, pady=10)

        self.password_entry = ttk.Entry(self, font=self.font, show="*")
        self.password_entry.insert(0, "Password")
        self.password_entry.bind("<FocusIn>", self.clear_password)
        self.password_entry.grid(row=1, column=0, padx=10, pady=10)

        login_button = ttk.Button(self, text="Login", command=self.login)
        login_button.grid(row=2, column=0, padx=5, pady=10, sticky="w")
        register_button = ttk.Button(
            self,
            text="Register",
            command=lambda: self.controller.show_frame(RegisterScreen),
        )
        register_button.grid(row=2, column=0, padx=5, pady=10, sticky="e")

    def login(self):
        logging.debug("Starting the login process")
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        

        try:
            logging.debug("Connected to the database")
            with sqlite3.connect("user_information.db") as conn:
                cursor = conn.cursor()
                query = "SELECT password FROM users WHERE username = ?"
                cursor.execute(query, (self.username,))
                row = cursor.fetchone()

            if row:
                stored_hash = row[0]
            else: 
                messagebox.showerror("Error", "Username not found")
                return

            if stored_hash and bcrypt.checkpw(self.password.encode(), stored_hash):
                logging.debug(f"Provided password matches stored password: {bcrypt.checkpw(self.password.encode(), stored_hash)}")
                logging.debug(f"Login successful for {self.username}")
                messagebox.showinfo("Login", "Login Successful")
                subprocess.call(["python", "3D.py"])
                
            else:
                messagebox.showerror("Login", "Incorrect username or password")
                logging.debug(f"Login failed for {self.username}")
                
        except Exception as e:
            logging.exception(e)
            messagebox.showerror("Login", "Login failed")
        finally:
            conn.close()
            logging.debug("Connection to the database closed")
    
    def clear_username(self, event):
        if self.username_entry.get() == "Username":
            self.username_entry.delete(0, tk.END)
        self.username_entry.unbind("<FocusOut>")
        self.username_entry.bind("<FocusOut>", self.set_username)

    def set_username(self, event):
        if self.username_entry.get() == "":
            self.username_entry.insert(0, "Username")
        self.username_entry.unbind("<FocusOut>")

    def clear_password(self, event):
        if self.password_entry.get() == "Password":
            self.password_entry.delete(0, tk.END)
        self.password_entry.unbind("<FocusOut>")
        self.password_entry.bind("<FocusOut>", self.set_password)

    def set_password(self, event):
        if self.password_entry.get() == "":
            self.password_entry.insert(0, "Password")
        self.password_entry.unbind("<FocusOut>")

    def on_raise(self):
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, "Username")
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, "Password")


class RegisterScreen(tk.Frame):
    """
    RegisterScreen class is a tkinter GUI based frame that provides functionality for user registration.

    Attributes:
    parent: parent widget for the frame
    controller: object of MainApplication class

    Methods:
    __init__: initializes the frame and creates the necessary widgets for the register screen
    register: connects to the database, inserts the new user's information into the database, and outputs the result
    clear_username: clears the username entry widget if it contains the placeholder text
    set_username: sets the placeholder text in the username entry widget if it's empty
    clear_password: clears the password entry widget if it contains the placeholder text
    set_password: sets the placeholder text in the password entry widget if it's empty
    clear_confirm_password: clears the confirm password entry widget if it contains the placeholder text
    set_confirm_password: sets the placeholder text in the confirm password entry widget if it's empty
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.font = ("Courier", 20)

        self.username_entry = ttk.Entry(self, font=self.font)
        self.username_entry.insert(0, "Username")
        self.username_entry.bind("<FocusIn>", self.clear_username)
        self.username_entry.grid(row=0, column=0, padx=10, pady=10)

        self.password_entry = ttk.Entry(self, font=self.font, show="*")
        self.password_entry.insert(0, "Password")
        self.password_entry.bind("<FocusIn>", self.clear_password)
        self.password_entry.grid(row=1, column=0, padx=10, pady=10)

        register_button = ttk.Button(self, text="Register", command=self.register)
        register_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        back_button = ttk.Button(
            self, text="Back", command=lambda: self.controller.show_frame(LoginScreen)
        )
        back_button.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.winfo_toplevel().title("Register")
        

    def clear_username(self, event):
        if self.username_entry.get() == "Username":
            self.username_entry.delete(0, tk.END)
        self.username_entry.unbind("<FocusOut>")
        self.username_entry.bind("<FocusOut>", self.set_username)

    def set_username(self, event):
        if self.username_entry.get() == "":
            self.username_entry.insert(0, "Username")
        self.username_entry.unbind("<FocusOut>")

    def clear_password(self, event):
        if self.password_entry.get() == "Password":
            self.password_entry.delete(0, tk.END)
        self.password_entry.unbind("<FocusOut>")
        self.password_entry.bind("<FocusOut>", self.set_password)

    def set_password(self, event):
        if self.password_entry.get() == "":
            self.password_entry.insert(0, "Password")
        self.password_entry.unbind("<FocusOut>")

    def register(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()

        # Use bcrypt to hash the password before storing in the database
        hashed_password = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt())

        conn = sqlite3.connect("user_information.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (self.username,))
        result = c.fetchone()
        if result is not None:
            messagebox.showerror("Error", "Username already exists.")
            logging.debug("Register Failed: Username already exists.")
        else:
            c.execute("INSERT INTO users VALUES (?,?)", (self.username, hashed_password))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully.")
            logging.debug("Register Success: User registered successfully.")
        conn.close()

    def on_raise(self):
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, "Username")
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, "Password")


class CloseButton(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.config(text="Close", command=self.quit)


class HomeScreen(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        CloseButton(self).pack(side="right", padx=10)
        self.label = tk.Label(self, text="Welcome to the home screen")
        self.label.pack(pady=10)

app = MainApplication()
# app.overrideredirect(True)
app.show_frame(LoginScreen)
app.title("Login | 3D Game")
app.mainloop()
