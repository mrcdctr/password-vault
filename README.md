# Password Manager

A secure and user-friendly password manager application built using Python and Tkinter. This application allows you to generate, store, retrieve, update, delete, and manage your passwords efficiently. It uses the `cryptography` library to encrypt and decrypt your saved passwords for enhanced security.

---

## Features

- **Password Generator**: Generate strong and random passwords with a mix of letters, numbers, and symbols.
- **Password Strength Indicator**: Visual feedback on the strength of your entered or generated password.
- **Save Passwords**: Store passwords securely in an encrypted format.
- **Search Functionality**: Retrieve saved credentials for a specific website.
- **Delete Functionality**: Remove an entry for a specific website.
- **Data Import/Export**: Import and export data in JSON format for backups.
- **Secure Encryption**: Passwords are encrypted using the `cryptography` library.

---

## Prerequisites

Make sure you have Python 3 installed. You’ll also need the following Python libraries:
- `tkinter` (usually included with Python installations)
- `pyperclip`
- `cryptography`

You can install the required libraries using pip:
```bash
pip install pyperclip cryptography
