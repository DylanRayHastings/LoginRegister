# BUG : CANNOT CLICK OFF OF APP

import tkinter as tk  #  MODULES FOR GUI
import tkinter.ttk as ttk
from tkinter import * 
from tkinter import messagebox
import sqlite3  # DATABASE CONNECTIVITY
import webbrowser  # WEB CONNECTIVITY
import subprocess  # SUBPROCESS
import time  # TIME
import bcrypt # ENCRYPTION
import logging # LOGGING USER 

logging.basicConfig(
    filename='app.log', level=logging.DEBUG, format='%(asctime)s %(message)s'
)

class TopBar(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.left_frame = tk.Frame(self, background='#212121')
        self.left_frame.pack(side='left')

        self.right_frame = tk.Frame(self, background='#212121')
        self.right_frame.pack(side='right')

        exit_icon = PhotoImage(file='X.png', width=30, height=30)
        self.exit_button = tk.Button(self.right_frame, image=exit_icon, command=self.master)
        self.exit_button.grid(row=1, column=2)
        self.exit_icon = exit_icon

    def pack(self, *args, **kwargs):
        tk.Frame.pack(self, *args, **kwargs)

class MainApplication(tk.Tk):
    '''
    The MainApplication class is a Tkinter GUI based application that acts as a container for the login and register screens.

    Attributes:
    container: A frame widget that acts as the parent container for other frames in the application.
    frames: A dictionary that maps the frame classes to their instances.

    Methods:
    __init__: Initializes the Tkinter window and creates the container frame widget. It also creates instances of the LoginScreen and RegisterScreen frames and adds them to the frames dictionary.
    show_frame: Raises the specified frame to the top of the window stack and makes it visible to the user.
    '''

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self, background='#212121')
        container.pack(fill='both', expand=True)
        self.top_bar = TopBar(self, background='#212121')
        self.top_bar.pack(side='top')

        width = 350
        height = 150
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coord = (screen_width/2) - (width/2)
        y_coord = (screen_height/2) - (height/2)
        self.geometry('{}x{}+{}+{}'.format(width, height, int(x_coord), int(y_coord)))
        self.resizable(width=False, height=False)
        self.frames = {}

        for F in (LoginScreen, RegisterScreen):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(LoginScreen)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class LoginScreen(tk.Frame):
    '''
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
    '''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#212121')
        self.controller = controller
        self.font = ('Courier', 20)

        self.username_entry = ttk.Entry(self, font=self.font, background='#20C20E')
        self.username_entry.insert(0, 'Username')
        self.username_entry.bind('<FocusIn>', self.clear_username)
        self.username_entry.grid(row=0, column=0, padx=10, pady=10)

        self.password_entry = ttk.Entry(self, font=self.font, show='*', background='#20C20E')
        self.password_entry.insert(0, 'Password')
        self.password_entry.bind('<FocusIn>', self.clear_password)
        self.password_entry.grid(row=1, column=0, padx=10, pady=10)

        login_button = ttk.Button(self, text='Login', command=self.login)
        login_button.grid(row=2, column=0, padx=5, pady=10, sticky='w')
        register_button = ttk.Button(
            self,
            text='Register',
            command=lambda: self.controller.show_frame(RegisterScreen),
        )
        register_button.grid(row=2, column=0, padx=5, pady=10, sticky='e')

    def login(self):
        logging.debug('Starting the login process')
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        

        try:
            logging.debug('Connected to the database')
            with sqlite3.connect('user_information.db') as conn:
                cursor = conn.cursor()
                query = 'SELECT password FROM users WHERE username = ?'
                cursor.execute(query, (self.username,))
                row = cursor.fetchone()

            if row:
                stored_hash = row[0]
            else: 
                messagebox.showerror('Error', 'Username not found')
                return

            if stored_hash and bcrypt.checkpw(self.password.encode(), stored_hash):
                logging.debug(f'Provided password matches stored password: {bcrypt.checkpw(self.password.encode(), stored_hash)}')
                logging.debug(f'Login successful for {self.username}')
                messagebox.showinfo('Login', 'Login Successful')
                subprocess.call(['python', '3D.py'])
                
            else:
                messagebox.showerror('Login', 'Incorrect username or password')
                logging.debug(f'Login failed for {self.username}')
                
        except Exception as e:
            logging.exception(e)
            messagebox.showerror('Login', 'Login failed')
        finally:
            conn.close()
            logging.debug('Connection to the database closed')
    
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
            self.password_entry.insert(0, 'Password')
        self.password_entry.unbind('<FocusOut>')

    def on_raise(self):
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, 'Username')
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, 'Password')


class RegisterScreen(tk.Frame):
    '''
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
    '''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.font = ('Courier', 20)

        self.username_entry = ttk.Entry(self, font=self.font, background='#212121')
        self.username_entry.insert(0, 'Username')
        self.username_entry.bind('<FocusIn>', self.clear_username)
        self.username_entry.grid(row=0, column=0, padx=10, pady=10)

        self.password_entry = ttk.Entry(self, font=self.font, show='*', background='#212121')
        self.password_entry.insert(0, 'Password')
        self.password_entry.bind('<FocusIn>', self.clear_password)
        self.password_entry.grid(row=1, column=0, padx=10, pady=10)

        register_button = ttk.Button(self, text='Register', command=self.register)
        register_button.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        back_button = ttk.Button(
            self, text='Back', command=lambda: self.controller.show_frame(LoginScreen)
        )
        back_button.grid(row=2, column=0, padx=10, pady=10, sticky='e')

        self.winfo_toplevel().title('Login | Register')
        

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
            self.password_entry.insert(0, 'Password')
        self.password_entry.unbind('<FocusOut>')

    def register(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()

        # Use bcrypt to hash the password before storing in the database
        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect('user_information.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=?', (self.username,))
        result = c.fetchone()
        if result is not None:
            messagebox.showerror('Error', 'Username already exists.')
            logging.debug('Register Failed: Username already exists.')
        else:
            c.execute('INSERT INTO users VALUES (?,?)', (self.username, hashed_password))
            conn.commit()
            messagebox.showinfo('Success', 'User registered successfully.')
            logging.debug('Register Success: User registered successfully.')
        conn.close()

    def on_raise(self):
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, 'Username')
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, 'Password')

app = MainApplication()
app.configure(background='#212121')
#app.overrideredirect(True)
app.show_frame(LoginScreen)
top_bar = TopBar(app, '')
app.mainloop()

