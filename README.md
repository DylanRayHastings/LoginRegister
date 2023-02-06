This is a GUI based application that provides functionality for user authentication. It is built using the tkinter module for creating the graphical user interface and the sqlite3 module for database connectivity. The application has two main frames: the LoginScreen and the RegisterScreen.

The MainApplication class acts as a container for these two frames and manages their lifecycle. It uses a dictionary to map the frame classes to their instances and has a method show_frame to raise the specified frame to the top of the window stack and make it visible to the user.

The LoginScreen class provides functionality for user login. It has entry widgets for the username and password and a login button to check if the provided credentials match any existing user in the database. If the username and password match, it outputs a successful login message. The password entry widget uses the bcrypt library to hash the password before storing in the database for security purposes.

The RegisterScreen class provides functionality for user registration. It has entry widgets for the username, email, and password and a register button to add the new user information to the database. The password entry widget also uses the bcrypt library to hash the password before storing in the database.
