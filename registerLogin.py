# TODO : Make the complete application look modern and clean.
# TODO : Add proper error handling and validation to ensure that the input entered by the user is valid.
# TODO : Use Python's logging module to log messages and events that occur during the runtime of the application.
# TODO : Refactor the code to make it more readable and understandable by adding comments and meaningful variable names.
# TODO : Use Python's built-in libraries like subprocess and webbrowser sparingly and only when necessary.
# TODO : Use Python's with statement when working with databases to ensure that the database connection is properly closed after use.
# TODO : Make the button in RegisterScreen() class the same in LoginScreen() class.
# TODO : Test the code thoroughly to ensure that all functionalities work as intended.
# TODO : Pressing Enter in the Register Screen will register the user.

# BUG : Title of the application should change from Login | Pong on the Login Screen and change to Register on the Register Screen.
# BUG : Buttons from Login Screen and Register Screen are slightly off-positioned.
# BUG : Get the Registration to work
# BUG : Refactor the code to make it more readable and understandable by adding comments and meaningful variable names. START WITH MainApplication() 
import tkinter as tk # GUI module
import tkinter.ttk as ttk
import sqlite3 # Database connectivity
import bcrypt # Hashing password
import logging

# Configure logging for the app
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        # Initialize the Tk class
        tk.Tk.__init__(self, *args, **kwargs)

        # Container frame to hold all other frames
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        # Dictionary to store all the frames
        self.frames = {}
        for F in (LoginScreen, RegisterScreen):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        # Show the login screen first
        self.show_frame(LoginScreen)

    # Raise the specified frame to the front
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.font = ('Courier', 20)

        self.username_entry = ttk.Entry(self, font=self.font)
        self.username_entry.insert(0, 'Username')
        self.username_entry.bind('<FocusIn>', self.clear_username)
        self.username_entry.grid(row=0, column=0, padx=10, pady=10)

        self.password_entry = ttk.Entry(self, font=self.font, show='*')
        self.password_entry.insert(0, 'Password')
        self.password_entry.bind('<FocusIn>', self.clear_password)
        self.password_entry.grid(row=1, column=0, padx=10, pady=10)

        ttk.Button(self, text='Login', command=self.login).grid(row=2, column=0, padx=5, pady=10, sticky='w')
        ttk.Button(self, text='Register', command=lambda: controller.show_frame(RegisterScreen)).grid(row=2, column=0, padx=5, pady=10, sticky='e')

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect('user_information.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, hashed_password))
        user = c.fetchone()
        conn.close()

        if user:
            print('Successful login')
        else:
            print('Incorrect username or password')

    def clear_username(self, event):
        if self.username_entry.get() == 'Username':
            self.username_entry.delete(0, tk.END)
        self.username_entry.unbind('<FocusOut>')
        self.username_entry.bind('<FocusOut>', self.set_username)

    def set_username(self, event):
        if self.username_entry.get() == '':
            self.username_entry.insert(0, 'Username')
        self.username_entry.unbind('<FocusOut>')

    def clear_password(self, event):
        if self.password_entry.get() == 'Password':
            self.password_entry.delete(0, tk.END)
        self.password_entry.unbind('<FocusOut>')
        self.password_entry.bind('<FocusOut>', self.set_password)

    def set_password(self, event):
        if self.password_entry.get() == '':
            self.password_entry


