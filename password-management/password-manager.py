import sqlite3
import getpass
import secrets
import string
from cryptography.fernet import Fernet

# encryption_key = Fernet.generate_key()
encryption_key = b'Ke3NG7IWYBOdv42RPxPRhdQcK0WRVY-cGnGvpHyTVvM='
cipher_suite = Fernet(encryption_key)

conn = sqlite3.connect('passwd_manager.db')
cursor = conn.cursor()
cursor.execute('''
	CREATE TABLE IF NOT EXISTS passwords(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	website TEXT NOT NULL,
	username TEXT NOT NULL,
	password TEXT NOT NULL
	)
''')

conn.commit()

cursor.execute('''
	CREATE TABLE IF NOT EXISTS users(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	password TEXT NOT NULL
	)
''')

conn.commit()

def register_user():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                   (username, encrypted_password))
    conn.commit()
    print("User registration successful!")

def login():
    global username
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user:
        stored_password = user[2]
        decrypted_password = cipher_suite.decrypt(stored_password.encode()).decode()
        if password == decrypted_password:
            print("Login successful!")
            return True
    print("Login failed. Please try again.")
    return False

def generate_strong_password(length = 12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+<>?"
    strong_password = ''.join(secrets.choice(characters) for _ in range(length))
    return strong_password


def change_password():
    if not login():
        return
    new_password = getpass.getpass("Enter your password (or leave blank to generate strong password): ")
    if not new_password:
        new_password = generate_strong_password()
        print(f"Your new password is {new_password}")
    encrypted_password = cipher_suite.encrypt(new_password.encode()).decode()
    cursor.execute("UPDATE users SET password=? WHERE username=?",(encrypted_password, username))
    conn.commit()
    print("Your new password changed successfully!")


def add_password():
    if not login():
        return
    website = input("Website or Service: ")
    username = input("Username: ")
    print("Do you want to generate a strong password for this service?(y/n): ")
    generate_option = input()
    if generate_option.lower() == "y":
        password = generate_strong_password()
        print(f"Your password is {password}")
    else:
        password = getpass.getpass("Password: ")
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()
    cursor.execute("INSERT INTO passwords (website ,username, password) VALUES (?, ?, ?)",
                   (website, username, encrypted_password))
    conn.commit()
    print("Password added successfully!")


def view_passwords():
    if not login():
        return
    cursor.execute("SELECT * FROM passwords")
    passwords = cursor.fetchall()
    for password in passwords:
        website = password[1]
        username = password[2]
        encrypted_password = password[3]
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
        print(f"ID: {password[0]}, Website: {password[1]}, Username: {username}, Password: {decrypted_password}")

def delete_password():
    if not login():
        return
    password_id = input("Enter the password ID to delete: ")
    cursor.execute("DELETE FROM passwords WHERE id=?", (password_id, ))
    conn.commit()
    print("Password deleted!")


while True:
    print("\nPassword Manager:")
    print("\t1. Register")
    print("\t2. Change password")
    print("\t3. Add password")
    print("\t4. View passwords")
    print("\t5. Delete password")
    print("\t6. Exit")

    choice = input("Select an option: ")
    if choice == '1':
        register_user()
    elif choice == '2':
        change_password()
    elif choice == '3':
        add_password()
    elif choice == '4':
        view_passwords()
    elif choice == '5':
        delete_password()
    elif choice == '6':
        break
    else:
        print("Invalid choice! Please select again.")

conn.close()