import tkinter as tk
import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import sqlite3
import webbrowser
import bcrypt
import logging
import sys
import traceback
import math
from PIL import Image, ImageTk

# TODO: Allow for connection to a live server. 
# TODO: Make the 

# /$$$$$$$            /$$                           /$$   /$$                       /$$     /$$                              
#| $$__  $$          | $$                          | $$  | $$                      | $$    |__/                              
#| $$  \ $$ /$$   /$$| $$  /$$$$$$  /$$$$$$$       | $$  | $$  /$$$$$$   /$$$$$$$ /$$$$$$   /$$ /$$$$$$$   /$$$$$$   /$$$$$$$
#| $$  | $$| $$  | $$| $$ |____  $$| $$__  $$      | $$$$$$$$ |____  $$ /$$_____/|_  $$_/  | $$| $$__  $$ /$$__  $$ /$$_____/
#| $$  | $$| $$  | $$| $$  /$$$$$$$| $$  \ $$      | $$__  $$  /$$$$$$$|  $$$$$$   | $$    | $$| $$  \ $$| $$  \ $$|  $$$$$$ 
#| $$  | $$| $$  | $$| $$ /$$__  $$| $$  | $$      | $$  | $$ /$$__  $$ \____  $$  | $$ /$$| $$| $$  | $$| $$  | $$ \____  $$
#| $$$$$$$/|  $$$$$$$| $$|  $$$$$$$| $$  | $$      | $$  | $$|  $$$$$$$ /$$$$$$$/  |  $$$$/| $$| $$  | $$|  $$$$$$$ /$$$$$$$/
#|_______/  \____  $$|__/ \_______/|__/  |__/      |__/  |__/ \_______/|_______/    \___/  |__/|__/  |__/ \____  $$|_______/ 
#           /$$  | $$                                                                                     /$$  \ $$          
#          |  $$$$$$/                                                                                    |  $$$$$$/          
#           \______/                                                                                      \______/           

 #client = None  # Create a new client object that will be used to connect to the server.
#HOST_ADDR = 'localhost'  # Set the host address to localhost.
#HOST_PORT = 8000  # Set the host port to 8000.

try:  # Try to import the socket module.
    ctk.set_appearance_mode('Dark')  # Set the appearance mode to dark.
    logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(message)s',) # Set the logging level to debug.
    
    class RotatingSphere(tk.Canvas):
        '''
        MainApplication class is the main tkinter GUI based application that holds all the different screens.

        Methods:
        __init__: initializes the application and creates the different screens'''
        def __init__(self, master): # Create a new instance of the RotatingSphere class.
            super().__init__(master) # Call the parent class constructor.
            # Set the radius and number of points to use for the sphere
            self.r = 125 # Radius of the sphere
            self.num_points = 10 # Number of points to use for the sphere

            self.angle = 0 # Initial angle of rotation

            self.angle_x = 0.5 # Initial angle of rotation in the x direction
            self.angle_y = 0.5 # Initial angle of rotation in the y direction
            self.angle_z = 0.5 # Initial angle of rotation in the z direction

            self.canvas = tk.Canvas(self, background='#212121', borderwidth=0, highlightthickness=0) # Create a new canvas object.
            self.canvas.pack(fill=tk.BOTH, expand=True) # Pack the canvas object into the window.

            self.update_sphere() # Update the sphere

        # Define a function to update the position of the points on the sphere
        def update_sphere(self):
            self.angle += 0.05 # Increment the angle by 0.05 degrees each time the function is called.
            self.angle_x += 0.03 # Increment the angle_x by 0.03 degrees each time the function is called.  
            self.angle_y += 0.01 # Increment the angle_y by 0.01 degrees each time the function is called.
            self.angle_z += 0.02 # Increment the angle_z by 0.02 degrees each time the function is called.

            self.canvas.delete('all') # Delete all the points from the canvas.

            # Loop over the angles u and v to create the points on the sphere
            for u in range(0, self.num_points): # Loop over the number of points to create the points on the sphere
                for v in range(0, self.num_points): # Loop over the number of points to create the points on the sphere
                    x = self.r * math.sin(u * math.pi / self.num_points) * math.cos(2 * v * math.pi / self.num_points) # Calculate the x position of the point
                    y = self.r * math.sin(u * math.pi / self.num_points) * math.sin(2 * v * math.pi / self.num_points) # Calculate the y position of the point
                    z = self.r * math.cos(u * math.pi / self.num_points) # Calculate the z position of the point

                    # Rotate the points around the x-axis
                    x_rot1 = x # Rotate the point around the x-axis
                    y_rot1 = y * math.cos(self.angle_x) - z * math.sin(self.angle_x) # Rotate the point around the y-axis
                    z_rot1 = y * math.sin(self.angle_x) + z * math.cos(self.angle_x) # Rotate the point around the z-axis

                    # Rotate the points around the y-axis
                    x_rot2 = x_rot1 * math.cos(self.angle_y) + z_rot1 * math.sin(self.angle_y) # Rotate the point around the x-axis
                    y_rot2 = y_rot1 # Rotate the point around the y-axis
                    z_rot2 = -x_rot1 * math.sin(self.angle_y) + z_rot1 * math.cos(self.angle_y) # Rotate the point around the z-axis

                    # Rotate the points around the z-axis
                    x_rot3 = x_rot2 * math.cos(self.angle_z) - y_rot2 * math.sin(self.angle_z) # Rotate the point around the x-axis
                    y_rot3 = x_rot2 * math.sin(self.angle_z) + y_rot2 * math.cos(self.angle_z) # Rotate the point around the y-axis
                    z_rot3 = z_rot2 # Rotate the point around the z-axis

                    # Map the 3D points to 2D points on the canvas
                    canvas_x = x_rot3 + 250 # Add 250 to the x position of the point on the canvas
                    canvas_y = 250 - y_rot3 # Add 250 to the y position of the point on the canvas

                    if ((u + v) // 5) % 2 == 0: # Determine the color of the point based on the value of u and v
                        point_color = 'white' # Set the color of the point to white
                    else: 
                        point_color = '#404040' # Set the color of the point to black

                    self.canvas.create_rectangle(canvas_x, canvas_y, canvas_x+1, canvas_y+1, fill=point_color, outline='') # Create a rectangle around the point on the canvas

            self.canvas.after(30, self.update_sphere) # Call the update_sphere function every 30 milliseconds.

    class MainApplication(tk.Tk):
        '''
        RotatingSphere is a tkinter canvas that displays a rotating sphere composed of points.

        Attributes:
        r (int): the radius of the sphere
        num_points (int): the number of points to use for the sphere
        angle (float): the angle of rotation
        angle_x (float): the rotation angle around the x-axis
        angle_y (float): the rotation angle around the y-axis
        angle_z (float): the rotation angle around the z-axis
        canvas (tk.Canvas): the tkinter canvas where the sphere is drawn

        Methods:
        __init__(self, master): Initializes the canvas and sets the attributes of the sphere.
        update_sphere(self): Updates the position of the points on the sphere and rotates the sphere around x-, y-, and z-axes.
        '''

        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)
            self.title('Login | Register') # Set the Title of the application.
            self.geometry('350x390') # Set the size of the application.
            self.resizable(width=False, height=False) # Make the application non-resizable.

            container = tk.Frame(self) # Create a frame to hold all the widgets.
            container.grid(row=0, column=0) # Place the frame in the center of the screen.

            signature_image = Image.open('signature.jpg') # Load the signature image.
            signature_image = signature_image.resize((300, 100), Image.ANTIALIAS) # Resize the signature image.
            signature_photo = ImageTk.PhotoImage(signature_image) # Convert the image to a photo image.

            # Create the label for the signature and add it to the container.
            label = tk.Label(self, image=signature_photo, borderwidth=0, highlightthickness=0)
            label.image = signature_photo  # Keep a reference to prevent garbage collection
            label.grid(row=0, column=0, pady=(0,300))

            self.frames = {}
            for F in (LoginScreen, RegisterScreen):
                frame = F(container)  # Pass the reference of the container to each screen
                self.frames[F] = frame # Store the reference of each screen in a dictionary
                frame.grid(row=0, column=0) # Place the frame in the grid

            self.show_frame(LoginScreen) # Show the Login screen

        def show_frame(self, cont): # Show the requested frame
            frame = self.frames[cont] # Get the reference of the frame
            frame.tkraise() # Raise the frame

            for other_frame in self.frames.values(): # For each other frame
                if other_frame is not frame:  # If the other frame is not the current frame
                    other_frame.grid_remove() # Remove the other frame from the grid

            # Handle navigation between frames
            if cont == LoginScreen:
                # If the LoginScreen is being shown, show the Register button and hide the Back button
                self.frames[LoginScreen].grid(row=2, column=0)
                self.frames[RegisterScreen].grid_forget() # Hide the Register button
            elif cont == RegisterScreen:
                # If the RegisterScreen is being shown, hide the Register button and show the Back button
                self.frames[LoginScreen].grid_forget() # Hide the Login button
                self.frames[RegisterScreen].grid(row=2, column=0) # Show the Register button and hide the Back button

            # update the window title
            self.title(f'Login | Register - {cont.__name__}') # Set the Title of the application.

        def go_to_login_screen(self):
            self.show_frame(LoginScreen) # Show the Login Screen

        def go_to_register_screen(self):
            self.show_frame(RegisterScreen) # Show the Register Screen

    class LoginScreen(tk.Frame):
        '''
        LoginScreen class is a tkinter GUI based frame that provides functionality for user login.

        Attributes:
        parent: parent widget for the frame

        Methods:
        __init__: initializes the frame and creates the necessary widgets for the login screen
        login: connects to the database, checks if the provided username and password match any existing user, and outputs the result
        clear_username: clears the username entry widget if it contains the placeholder text
        set_username: sets the placeholder text in the username entry widget if it's empty
        clear_password: clears the password entry widget if it contains the placeholder text
        set_password: sets the placeholder text in the password entry widget if it's empty
        '''

        def __init__(self, parent):  # Define the __init__ method that initializes the LoginScreen object.
            tk.Frame.__init__(self, parent, background='#212121', pady=100, padx=100)  # Call the __init__ method of the tkinter.Frame class.
            self.grid(row=0, column=0, sticky='w')
            self.sphere = RotatingSphere(self)
            self.sphere.place(relx=0.5, rely=0.5, anchor=tk.CENTER, height=450, width=500)
            logging.debug('Initializing LoginScreen.')
            self.font = ('Courier', 20)  # Set the font for the widgets.
            self.username_entry = ctk.CTkEntry(
                self, 
                font=self.font, # Set the font for the username entry widget.
                justify="center", # Set the text justification to center.
                bg_color='#212121', # Set the background color of the username entry widget.
                fg_color='transparent',
                border_width=0,
                corner_radius=0
            )  # Create a new entry widget for the username.
            self.username_entry.insert(0, 'Username')  # Set the placeholder text for the username entry widget.
            self.username_entry.bind('<FocusIn>', self.clear_username)  # Bind the clear_username method to the <FocusIn> event.
            self.username_entry.grid(row=0, column=0, padx=0, pady=5)  # Pack the username entry widget onto the LoginScreen object.
            self.password_entry = ctk.CTkEntry(
                self, 
                font=self.font, 
                show='*', 
                justify="center", # Set the text justification to center.
                bg_color='#212121',  # Create a new entry widget for the password.
                fg_color='transparent',
                border_width=0,
                corner_radius=0
            )  
            self.password_entry.insert(0,'Password')  # Set the placeholder text for the password entry widget.
            self.password_entry.bind('<FocusIn>',self.clear_password)  # Bind the clear_password method to the <FocusIn> event.
            self.password_entry.grid(row=1, column=0, padx=0, pady=10)  # Pack the password entry widget onto the LoginScreen object.
            login_button = ctk.CTkButton(
                self, 
                text='Login', # Set the text for the login button.
                command=self.login, # Set the command for the login button.
                fg_color='#171717', # Set the foreground color of the login button.
                hover_color='#404040',
                corner_radius=0,
            )  # Create a new button widget for the login button.
            login_button.grid(row=2, column=0, padx=0, pady=5)  # Pack the login button widget onto the LoginScreen object.
            register_button = (
                ctk.CTkButton(  # Create a new button widget for the register button.
                    self,
                    text='Register', # Set the text for the register button.
                    command=lambda: app.show_frame(RegisterScreen), # Set the command for the register button.
                    fg_color='#171717', # Set the foreground color of the register button.
                    hover_color='#404040',
                    corner_radius=0,
                )
            )
            register_button.grid(row=3, column=0, padx=0, pady=5)  # Pack the register button widget onto the LoginScreen object.

        def login(self):
            username = self.username_entry.get() # Get the username from the username entry widget.
            password = self.password_entry.get() # Get the password from the password entry widget.

            with sqlite3.connect('user_information.db') as conn: # Connect to the database.
                cursor = conn.cursor() # Create a new cursor for the database.

                cursor.execute("PRAGMA table_info(users)") # Check if the users table exists.
                columns = [column[1] for column in cursor.fetchall()] # Get the column names from the users table.
                if 'salt' not in columns: # Check if the salt column exists.
                    conn.execute("ALTER TABLE users ADD COLUMN salt TEXT;") # Add the salt column.
                    conn.commit() # Commit the changes to the database.

                query = 'SELECT password, salt FROM users WHERE username = ?' # Create the query for the database.
                cursor.execute(query, (username,)) # Execute the query.
                row = cursor.fetchone() # Get the row from the database.

            # Check if the user exists
            if row:
                stored_password = row[0] # Get the stored password from the database.
                salt = row[1] # Get the salt from the database.
                
                hashed_password = bcrypt.hashpw(password.encode(), salt) # Hash the provided password without salt

                if hashed_password == stored_password: # Check if the hashed password matches the stored password
                    messagebox.showinfo('Login', 'Login Successful') # Show successful login message.
                    webbrowser.open('https://www.youtube.com/watch?v=xvFZjo5PgG0&ab_channel=Duran')
                else:
                    messagebox.showerror('Login', 'Incorrect username or password') # Show unsuccessful login message (INCORRECT USERNAME / PASSWORD).
            else:
                messagebox.showerror('Login', 'Username not found') # Show unsuccessful login message (USERNAME NOT FOUND).

            conn.close() # Close the database connection.
 
        def clear_username(self, event): # Define the clear_username method that clears the username entry widget if it contains the placeholder text.
            if (self.username_entry.get() == 'Username'): # If the username entry widget contains the placeholder text, clear it.
                self.username_entry.delete(0, tk.END) # Clear the username entry widget. 
            self.username_entry.unbind('<FocusOut>') # Unbind the set_username method from the <FocusOut> event.
            self.username_entry.bind('<FocusOut>', self.set_username ) 

        def set_username(
            self, event
        ):  # Define the set_username method that sets the username entry widget to the placeholder text if it is empty.
            if (self.username_entry.get() == ''): # If the username entry widget is empty, set it to the placeholder text. 
                self.username_entry.insert(0,'Username') # Set the username entry widget to the placeholder text. 
            self.username_entry.unbind('<FocusOut>') # Unbind the set_username method from the <FocusOut> event) 

        def clear_password(self, event):  # Define the clear_password method that clears the password entry widget if it contains the placeholder text.
            if (self.password_entry.get() == 'Password'): # If the password entry widget contains the placeholder text, clear it.
                self.password_entry.delete(0,tk.END) # Clear the password entry widget.
            self.password_entry.unbind('<FocusOut>') # Unbind the set_password method from the <FocusOut> event. 
            self.password_entry.bind('<FocusOut>', self.set_password) # Bind the set_password method to the <FocusOut> event.

        def set_password(self, event):  # Define the set_password method that sets the password entry widget to the placeholder text if it is empty.
            if (self.password_entry.get() == ''):  # If the password entry widget is empty, set it to the placeholder text.
                self.password_entry.insert(0,'Password') # Set the password entry widget to the placeholder text.
            self.password_entry.unbind('<FocusOut>') # Unbind the set_password method from the <FocusOut> event.

        def on_raise(self,):  # Define the on_raise method that runs when the LoginScreen object is raised.
            self.username_entry.delete(0, tk.END)  # Clear the username entry widget.
            self.username_entry.insert(0, 'Username')  # Set the username entry widget to the placeholder text.
            self.password_entry.delete(0, tk.END)  # Clear the password entry widget.
            self.password_entry.insert(0, 'Password')  # Set the password entry widget to the placeholder text.

    class RegisterScreen(tk.Frame):
        '''
        RegisterScreen class is a tkinter GUI based frame that provides functionality for user registration.

        Attributes:
        parent: parent widget for the frame

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

        def __init__(self, parent):
            tk.Frame.__init__(self, parent, background='#212121', pady=100, padx=100) # Initialize the frame.
            self.grid(row=0, column=0, sticky='w') # Create the grid for the frame.

            self.font = ('Courier', 20) # Define the font for the labels.

            self.username_entry = ctk.CTkEntry( # Create the username entry widget.
                self, 
                font=self.font, # Define the font for the username entry widget.
                justify="center", # Set the text alignment for the username entry widget.
                bg_color='#212121', # Set the background color for the username entry widget.
                fg_color='transparent', # Set the foreground color for the username entry widget.
                border_width=0, # Set the border width for the username entry widget.
                corner_radius=0 # Set the corner radius for the username entry widget.
            )
            self.username_entry.insert(0, 'Username') # Set the username entry widget to the placeholder text.
            self.username_entry.bind('<FocusIn>', self.clear_username) # Bind the clear_username method to the <FocusIn> event.
            self.username_entry.grid(row=0, column=0, padx=0, pady=5) # Create the grid for the username entry widget.

            self.password_entry = ctk.CTkEntry( # Create the password entry widget.
                self,
                font=self.font, # Define the font for the password entry widget.
                show='*', # Set the password entry widget to show asterisks.
                justify="center", # Set the text alignment for the password entry widget.
                bg_color='#212121', # Set the background color for the password entry widget.
                fg_color='transparent', # Set the foreground color for the password entry widget.
                border_width=0, # Set the border width for the password entry widget.
                corner_radius=0 # Set the corner radius for the password entry widget.
            )
            self.password_entry.insert(0, 'Password') # Set the password entry widget to the placeholder text.
            self.password_entry.bind('<FocusIn>', self.clear_password) # Bind the clear_password method to the <FocusIn> event.
            self.password_entry.grid(row=1, column=0, padx=0, pady=10) # Create the grid for the password entry widget.

            register_button = ctk.CTkButton( # Create the register button widget.
                self,
                text='Register', # Define the text for the register button widget.
                command=self.register, # Define the command for the register button widget.
                fg_color='#171717', # Set the foreground color for the register button widget.
                hover_color='#404040', # Set the hover color for the register button widget.
                corner_radius=0, # Set the corner radius for the register button widget.
            )
            register_button.grid(row=2, column=0, padx=0, pady=5) # Create the grid for the register button widget.

            back_button = ctk.CTkButton( # Create the back button widget.
                self, # Define the back button widget.
                text='Back', # Define the text for the back button widget.
                command=lambda: app.show_frame(LoginScreen), # Define the command for the back button widget.
                fg_color='#171717', # Set the foreground color for the back button widget.
                hover_color='#404040', # Set the hover color for the back button widget.
                corner_radius=0, # Set the corner radius for the back button widget.
            )
            back_button.grid(row=3, column=0, padx=0, pady=5) # Create the grid for the back button widget.

     
        def clear_username(self, event): # Define the clear_username method.
            if (self.username_entry.get() == 'Username'): # If the username entry widget contains the placeholder text.
                self.username_entry.delete(0, tk.END) # Clear the username entry widget.
            self.username_entry.unbind('<FocusOut>') # Unbind the clear_username method from the <FocusOut> event.
            self.username_entry.bind('<FocusOut>', self.set_username) # Bind the set_username method to the <FocusOut> event.

        def set_username(self, event): # Define the set_username method.
            if (self.username_entry.get() == ''): # If the username entry widget is empty.
                self.username_entry.insert(0, 'Username') # Set the username entry widget to the placeholder text.
            self.username_entry.unbind('<FocusOut>') # Unbind the set_username method from the <FocusOut> event.

        def clear_password(self, event):  # Define the clear_password method that clears the password entry widget if it contains the placeholder text.
            if (self.password_entry.get() == 'Password'):  # If the password entry widget contains the placeholder text, clear it.
                self.password_entry.delete(0, tk.END)  # Clear the password entry widget.
            self.password_entry.unbind('<FocusOut>')  # Unbind the set_password method from the <FocusOut> event.
            self.password_entry.bind('<FocusOut>', self.set_password)  # Bind the set_password method to the <FocusOut> event.

        def set_password(self, event):  # Define the set_password method that sets the password entry widget to the placeholder text if it is empty.
            if (self.password_entry.get() == ''):  # If the password entry widget is empty, set it to the placeholder text.
                self.password_entry.insert(0, 'Password')  # Set the password entry widget to the placeholder text.
            self.password_entry.unbind('<FocusOut>')  # Unbind the set_password method from the <FocusOut> event.

        def register(self,):  # Define the register method that connects to the database, inserts the new user's information into the database, and outputs the result.
            self.username = (self.username_entry.get())  # Get the username from the username entry widget.
            self.password = (self.password_entry.get())  # Get the password from the password entry widget.
            self.salt = bcrypt.gensalt(rounds=12)
            hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), self.salt)  # Hash the password.
            conn = sqlite3.connect('user_information.db')  # Connect to the database.
            c = conn.cursor()  # Create a cursor object.
            c.execute('SELECT * FROM users WHERE username=?', (self.username,))  # Execute a query to check if the username already exists.
            result = c.fetchone()  # Fetch the result of the query.
            if (result is not None):  # If the username already exists, output an error message.
                messagebox.showerror('Error', 'Username already exists.')  # Output an error message.
                logging.debug('Register Failed: Username already exists.')  # Log the error.
            else:  # If the username does not already exist, insert the new user's information into the database.
                c.execute('INSERT INTO users VALUES (?,?,?)', (self.username, hashed_password, self.salt))
                conn.commit()  # Commit the changes to the database.
                messagebox.showinfo('Success', 'User registered successfully.')  # Output a success message.
                logging.debug('Register Success: User registered successfully.')  # Log the success.
            conn.close()  # Close the connection to the database.

        def on_raise(self,):  # Define the on_raise method that is called when the frame is raised.
            self.username_entry.delete(0, tk.END)  # Clear the username entry widget.
            self.username_entry.insert(0, 'Username')  # Set the username entry widget to the placeholder text.
            self.password_entry.delete(0, tk.END)  # Clear the password entry widget.
            self.password_entry.insert(0, 'Password')  # Set the password entry widget to the placeholder text.

    app = MainApplication()  # Create the main application object.
    app.configure(background='#212121')
    # app.overrideredirect(True) # Remove the window decorations.
    app.show_frame(LoginScreen)  # Show the login screen frame.
    app.mainloop()  # Start the main loop.
    
except Exception as e:  # If an error occurs, output the error message and log the error.
    exc_info = sys.exc_info()  # Get the exception information.
    traceback.print_exception(*exc_info)  # Print the exception information.
    logging.error(f'An error occurred: {e}')  # Log the error.
