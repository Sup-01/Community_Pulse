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

def create_event():
    print("\n--- Create Event ---")
    title = input("Title: ")
    category = input("Category (Garage Sale, Sports Match, etc.): ")
    description = input("Description: ")
    date = input("Date (YYYY-MM-DD): ")
    location = input("Location: ")

    cursor.execute('''
        INSERT INTO events (title, category, description, date, location, created_by)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, category, description, date, location, current_user[0]))
    conn.commit()
    print("✅ Event created! Waiting for admin approval.")

def view_events():
    print("\n--- Approved Events ---")
    cursor.execute("SELECT * FROM events WHERE approved = 1")
    events = cursor.fetchall()
    if not events:
        print("No approved events yet.")
        return

    for event in events:
        print(f"#{event[0]}: {event[1]} ({event[2]}) on {event[4]} at {event[5]}")
        print(f"  {event[3]}\n")

def view_my_events():
    print("\n--- My Events ---")
    cursor.execute("SELECT * FROM events WHERE created_by = ?", (current_user[0],))
    events = cursor.fetchall()
    if not events:
        print("You haven't posted any events.")
        return

    for event in events:
        status = "✅ Approved" if event[7] else "⌛ Pending"
        print(f"#{event[0]}: {event[1]} - {status}")

def user_menu():
    while True:
        print("\n=== User Menu ===")
        print("1. Create Event")
        print("2. View Approved Events")
        print("3. View My Events")
        print("4. Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            create_event()
        elif choice == '2':
            view_events()
        elif choice == '3':
            view_my_events()
        elif choice == '4':
            print("🔒 Logged out.")
            break
        else:
            print("❌ Invalid choice.")
