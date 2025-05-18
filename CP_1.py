import sqlite3

# Connect to DB (or create if doesn't exist)
conn = sqlite3.connect('community_pulse.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0,
    is_banned INTEGER DEFAULT 0,
    is_verified INTEGER DEFAULT 0
)
''')

# Create events table
cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    category TEXT,
    description TEXT,
    date TEXT,
    location TEXT,
    created_by INTEGER,
    approved INTEGER DEFAULT 0
)
''')

# Create interests table
cursor.execute('''
CREATE TABLE IF NOT EXISTS interests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    num_people INTEGER,
    event_id INTEGER
)
''')

conn.commit()
print("✅ Database and tables ready.")

import getpass

# Global variable for current user session
current_user = None

# Registration
def register():
    print("\n--- Register ---")
    username = input("Username: ")
    email = input("Email: ")
    password = getpass.getpass("Password (hidden): ")

    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, password))
        conn.commit()
        print("✅ Registration successful!")
    except sqlite3.IntegrityError:
        print("❌ Email already registered.")

# Login
def login():
    global current_user
    print("\n--- Login ---")
    email = input("Email: ")
    password = getpass.getpass("Password (hidden): ")

    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()

    if user:
        if user[5]:  # is_banned
            print("❌ This user is banned.")
            return
        current_user = user
        print(f"✅ Welcome, {user[1]}!")
    else:
        print("❌ Invalid credentials.")

def main_menu():
    while True:
        print("\n=== Community Pulse ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            register()
        elif choice == '2':
            login()
            if current_user:
                user_menu()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

# Start the program
main_menu()
