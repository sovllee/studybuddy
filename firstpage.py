import tkinter as tk
from tkinter import messagebox
import mysql.connector
from second_page import SecondPage  # Import the SecondPage class from second_page.py

class StudyBuddyApp:
    def __init__(self, master):
        self.master = master
        master.title("STUDY BUDDY")
        master.geometry('340x440')
        master.state('zoomed')

        self.label = tk.Label(master, text="Welcome to Study Buddy!", font=("Helvetica", 24))
        self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(side=tk.TOP, padx=20, pady=10)

        self.button_sign_in = tk.Button(self.button_frame, text="Sign In", command=self.open_login_window)
        self.button_sign_in.pack(side=tk.RIGHT, padx=10, pady=10)

        self.button_sign_up = tk.Button(self.button_frame, text="Sign Up", command=self.open_signup_window)
        self.button_sign_up.pack(side=tk.RIGHT, padx=10, pady=10)

    def open_signup_window(self):
        self.signup_window = tk.Toplevel(self.master)
        self.signup_window.title("Sign Up")
        self.signup_window.geometry('340x440')
        self.signup_window.state('zoomed')

        self.signup_label = tk.Label(self.signup_window, text="Sign Up", font=("Helvetica", 24))
        self.signup_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.username_label = tk.Label(self.signup_window, text='Username')
        self.username_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.username_entry = tk.Entry(self.signup_window)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self.signup_window, text='Password')
        self.password_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.password_entry = tk.Entry(self.signup_window, show='*')
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        self.confirm_password_label = tk.Label(self.signup_window, text='Confirm Password')
        self.confirm_password_label.grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.confirm_password_entry = tk.Entry(self.signup_window, show='*')
        self.confirm_password_entry.grid(row=3, column=1, padx=10, pady=5)

        self.signup_button = tk.Button(self.signup_window, text="Sign Up", command=self.signup)
        self.signup_button.grid(row=4, column=0, columnspan=2, pady=10)

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if password == confirm_password:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                existing_user = cursor.fetchone()

                if existing_user:
                    messagebox.showerror("Error", "Username already exists. Please choose a different username.")
                else:
                    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                    conn.commit()
                    messagebox.showinfo("Success", "Signup successful! You can now login.")
                    self.username_entry.delete(0, 'end')
                    self.password_entry.delete(0, 'end')
                    self.confirm_password_entry.delete(0, 'end')
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Database error: {err}")
            finally:
                cursor.close()
        else:
            messagebox.showerror("Error", "Passwords do not match. Please try again.")

    def open_login_window(self):
        self.login_window = tk.Toplevel(self.master)
        self.login_window.title("Login")
        self.login_window.geometry('340x440')
        self.login_window.state('zoomed')

        self.login_label = tk.Label(self.login_window, text="Login")
        self.username_label = tk.Label(self.login_window, text="Username")
        self.username_entry = tk.Entry(self.login_window)
        self.password_entry = tk.Entry(self.login_window, show='*')
        self.password_label = tk.Label(self.login_window, text='Password')
        self.login_button = tk.Button(self.login_window, text="Login", command=self.login)

        self.login_label.grid(row=0, column=0, columnspan=2)
        self.username_label.grid(row=1, column=0)
        self.username_entry.grid(row=1, column=1)
        self.password_label.grid(row=2, column=0)
        self.password_entry.grid(row=2, column=1)
        self.login_button.grid(row=3, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo("Success", "Login successful!")
                # Open the second page upon successful login
                self.open_second_page()
            else:
                messagebox.showerror("Error", "Invalid username or password. Please try again.")
        except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Database error: {err}")
        finally:
            cursor.close()
            self.login_window.destroy()  # Close the login window after login attempt

    def open_second_page(self):
        # Open the SecondPage upon successful login
        self.master.withdraw()
        second_page = SecondPage(self.master)
        second_page.mainloop()


# MySQL database configuration
db_configuration = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Qwerty123!',
    'database': 'studybuddy'
}

# Connect to the MySQL database
conn = mysql.connector.connect(**db_configuration)

# Create the Tkinter application
root = tk.Tk()
app = StudyBuddyApp(root)
root.mainloop()
