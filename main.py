import tkinter as tk
from tkinter import messagebox
import sqlite3
import bcrypt

# Create a SQLite database and establish a connection
conn = sqlite3.connect('banking_portal.db')
cursor = conn.cursor()

# Create a 'users' table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
   id INTEGER PRIMARY KEY,
   first_name TEXT NOT NULL,
   last_name TEXT NOT NULL,
   username TEXT NOT NULL,
   password TEXT NOT NULL,
   mobile_number TEXT NOT NULL,
   age INTEGER NOT NULL,
   balance REAL NOT NULL DEFAULT 0.0
)
''')
conn.commit()

# Initialize the Tkinter window
window = tk.Tk()
window.title("Banking Portal")

# Set the window size to 500x600
window.geometry("500x600")  # Adjust the height for additional input fields

# Declare global variables for entry fields
entry_first_name = None
entry_last_name = None
entry_username = None
entry_password = None
entry_mobile = None
entry_age = None


# Function to encrypt and verify passwords using bcrypt
def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(input_password, hashed_password):
    input_password = input_password.encode('utf-8') if isinstance(input_password, str) else input_password
    hashed_password = hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password
    return bcrypt.checkpw(input_password, hashed_password)


# Function for user registration
def open_registration():
    global entry_first_name, entry_last_name, entry_username, entry_password, entry_mobile, entry_age

    registration_window = tk.Toplevel(window)
    registration_window.title("Registration")
    registration_window.geometry("500x500")

    label_first_name = tk.Label(registration_window, text="First Name:")
    label_last_name = tk.Label(registration_window, text="Last Name:")
    label_username = tk.Label(registration_window, text="Username:")
    label_password = tk.Label(registration_window, text="Password:")
    label_mobile = tk.Label(registration_window, text="Mobile Number:")
    label_age = tk.Label(registration_window, text="Age")

    entry_first_name = tk.Entry(registration_window)
    entry_last_name = tk.Entry(registration_window)
    entry_username = tk.Entry(registration_window)
    entry_password = tk.Entry(registration_window, show="*")  # Hide the password
    entry_mobile = tk.Entry(registration_window)
    entry_age = tk.Entry(registration_window)

    button_register = tk.Button(registration_window, text="Register", command=register)

    label_first_name.grid(row=0, column=0, columnspan=2)
    entry_first_name.grid(row=1, column=0, columnspan=2)
    label_last_name.grid(row=2, column=0, columnspan=2)
    entry_last_name.grid(row=3, column=0, columnspan=2)
    label_username.grid(row=4, column=0, columnspan=2)
    entry_username.grid(row=5, column=0, columnspan=2)
    label_password.grid(row=6, column=0, columnspan=2)
    entry_password.grid(row=7, column=0, columnspan=2)
    label_mobile.grid(row=8, column=0, columnspan=2)
    entry_mobile.grid(row=9, column=0, columnspan=2)
    label_age.grid(row=10, column=0, columnspan=2)
    entry_age.grid(row=11, column=0, columnspan=2)
    button_register.grid(row=12, column=0, columnspan=2, pady=(50, 0))


# Function for user registration
def register():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    username = entry_username.get()
    password = entry_password.get()
    mobile_number = entry_mobile.get()
    age = entry_age.get()

    if not (first_name and last_name and username and password and mobile_number and age):
        messagebox.showerror("Error", "All fields are required.")
        return

    cursor.execute("SELECT username FROM users WHERE username=?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        messagebox.showerror("Error", "Username already exists. Please choose another.")
    else:
        # Encrypt the password
        hashed_password = encrypt_password(password)

        cursor.execute(
            "INSERT INTO users (first_name, last_name, username, password, mobile_number, age, balance) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (first_name, last_name, username, hashed_password, mobile_number, age, 0.0))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        # Clear the registration form
        entry_first_name.delete(0, tk.END)
        entry_last_name.delete(0, tk.END)
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        entry_mobile.delete(0, tk.END)
        entry_age.delete(0, tk.END)


# Function for user login
def login():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "Username and password are required.")
        return

    cursor.execute("SELECT id, password FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user and verify_password(password, user[1]):
        messagebox.showinfo("Success", "Login successful!")
        open_dashboard(username)  # Redirect to the dashboard
    else:
        messagebox.showerror("Error", "Login failed. Please check your credentials.")


# Function to open a dashboard window
def open_dashboard(username):
    dashboard_window = tk.Toplevel(window)
    dashboard_window.title(f"Welcome, {username}")
    dashboard_window.geometry("800x600")  # Adjust size for the dashboard window

    # Add widgets and functionality for the dashboard here
    label = tk.Label(dashboard_window, text=f"Welcome, {username}!")
    label.pack()


# Create and configure labels and entry fields for login
label_username = tk.Label(window, text="Username:")
label_password = tk.Label(window, text="Password:")
entry_username = tk.Entry(window)
entry_password = tk.Entry(window, show="*")  # Hide the password

# Create and configure buttons for login, registration, and open registration
button_login = tk.Button(window, text="Login", command=login)
button_register = tk.Button(window, text="Register", command=open_registration)

# Place widgets using the grid layout
label_username.grid(row=0, column=0, columnspan=2)
entry_username.grid(row=1, column=0, columnspan=2)
label_password.grid(row=2, column=0, columnspan=2)
entry_password.grid(row=3, column=0, columnspan=2)

# Center-align the buttons within the window
button_login.grid(row=4, column=0, columnspan=2, pady=(50, 0))
button_register.grid(row=5, column=0, columnspan=2, pady=10)

# Adjust grid row weights to center-align the buttons vertically
for _ in range(6):
    window.grid_rowconfigure(_, weight=1)

# Start the Tkinter main loop
window.mainloop()
