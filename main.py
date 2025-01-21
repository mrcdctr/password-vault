from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
from random import choice, randint, shuffle
import pyperclip
import json
import os
from cryptography.fernet import Fernet

# ---------------------------- ENCRYPTION SETUP ------------------------------- #
# Replace this with a key loaded from a secure location or environment variable
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

FONT_NAME = "Courier"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- PASSWORD STRENGTH ------------------------------- #
def check_password_strength(password):
    length = len(password)
    strength = 0

    if any(char.islower() for char in password): strength += 1
    if any(char.isupper() for char in password): strength += 1
    if any(char.isdigit() for char in password): strength += 1
    if any(char in "!#$%&()*+" for char in password): strength += 1
    if length >= 8: strength += 1

    # Update the progress bar
    strength_bar["value"] = strength * 20
    strength_label.config(text=f"Strength: {strength * 20}%")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops!", message="Please make sure you haven't left any fields empty.")
        return

    # Encrypt the password
    encrypted_password = cipher.encrypt(password.encode()).decode()

    new_data = {
        website: {
            "email": email,
            "password": encrypted_password
        }
    }

    try:
        with open("data.json", "r") as data_file:
            # Load existing data
            data = json.load(data_file)
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty dictionary
        data = {}

    # Update or add new data
    data.update(new_data)

    # Save the updated data
    with open("data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)

    messagebox.showinfo(title="Success", message="Data saved successfully!")
    website_entry.delete(0, END)
    password_entry.delete(0, END)

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    website = website_entry.get()

    if len(website) == 0:
        messagebox.showinfo(title="Oops!", message="Please enter a website to search.")
        return

    try:
        with open("data.json", "r") as data_file:
            # Load data from the JSON file
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")
        return

    if website in data:
        email = data[website]["email"]
        encrypted_password = data[website]["password"]
        password = cipher.decrypt(encrypted_password.encode()).decode()
        messagebox.showinfo(
            title=website,
            message=f"Email: {email}\nPassword: {password}"
        )
        pyperclip.copy(password)
    else:
        messagebox.showinfo(title="Not Found", message="No details for the website exist.")

# ---------------------------- DELETE ENTRY ------------------------------- #
def delete_entry():
    website = website_entry.get()

    if len(website) == 0:
        messagebox.showinfo("Oops!", "Please enter a website to delete.")
        return

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo("Error", "No data file found.")
        return

    if website in data:
        data.pop(website)
        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
        messagebox.showinfo("Deleted", f"Details for {website} have been deleted.")
    else:
        messagebox.showinfo("Not Found", "No details for the website exist.")

# ---------------------------- EXPORT DATA ------------------------------- #
def export_data():
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
        with open("exported_data.json", "w") as export_file:
            json.dump(data, export_file, indent=4)
        messagebox.showinfo("Export Successful", "Data exported to 'exported_data.json'.")
    except FileNotFoundError:
        messagebox.showinfo("Error", "No data to export.")

# ---------------------------- IMPORT DATA ------------------------------- #
def import_data():
    try:
        with open("imported_data.json", "r") as import_file:
            imported_data = json.load(import_file)
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            data = {}

        data.update(imported_data)

        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)

        messagebox.showinfo("Import Successful", "Data imported successfully.")
    except FileNotFoundError:
        messagebox.showinfo("Error", "No imported_data.json file found.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Vault")
window.config(padx=50, pady=50,)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:", font=(FONT_NAME, 12, "bold"))
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:", font=(FONT_NAME, 12, "bold"))
email_label.grid(row=2, column=0)
password_label = Label(text="Password:", font=(FONT_NAME, 12, "bold"))
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=37)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=60)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "example@gmail.com")
password_entry = Entry(width=37)
password_entry.grid(row=3, column=1)
password_entry.bind("<KeyRelease>", lambda _: check_password_strength(password_entry.get()))

# Password Strength UI
strength_label = Label(text="Strength: 0%", font=(FONT_NAME, 10, "bold"))
strength_label.grid(row=5, column=1, sticky="w")
strength_bar = Progressbar(window, length=200, mode="determinate")
strength_bar.grid(row=5, column=2)

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password, font=(FONT_NAME, 8, "bold"))
generate_password_button.grid(row=3, column=2)
search_button = Button(text="Search", width=15, command=search_password, font=(FONT_NAME, 8, "bold"))
search_button.grid(row=1, column=2)
add_button = Button(text="Add", width=20, command=save, font=(FONT_NAME, 8, "bold"))
add_button.grid(row=4, column=1, columnspan=2)
export_button = Button(text="Export Data", command=export_data, font=(FONT_NAME, 8, "bold"))
export_button.grid(row=6, column=0)
import_button = Button(text="Import Data", command=import_data, font=(FONT_NAME, 8, "bold"))
import_button.grid(row=6, column=2)
delete_button = Button(text="Delete", width=15, command=delete_entry, font=(FONT_NAME, 8, "bold"))
delete_button.grid(row=7, column=1)

window.mainloop()
