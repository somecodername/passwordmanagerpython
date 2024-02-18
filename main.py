import sqlcipher3
import getpass

# Provide the encryption key (replace 'your_key_here' with your actual key)
key = 'your_key_here'

def create_table(conn):
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS passwords
                     (website TEXT PRIMARY KEY, password TEXT)''')
        conn.commit()
    except sqlcipher3.Error as e:
        print("An error occurred while creating the table:", e)

def add_password(conn):
    website = input("Enter website or service name: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Confirm password: ")
    
    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return
    
    try:
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO passwords VALUES (?, ?)", (website, password))
        conn.commit()
        print("Password added successfully.")
    except sqlcipher3.Error as e:
        print("An error occurred while adding the password:", e)

def retrieve_password(conn):
    website = input("Enter website or service name: ")
    
    try:
        c = conn.cursor()
        c.execute("SELECT password FROM passwords WHERE website=?", (website,))
        result = c.fetchone()
    
        if result:
            print("Password:", result[0])
        else:
            print("Password not found.")
    except sqlcipher3.Error as e:
        print("An error occurred while retrieving the password:", e)

def main():
    conn = sqlcipher3.connect('passwords.db')
    conn.execute('PRAGMA key="{}"'.format(key))
    
    create_table(conn)
    
    while True:
        print("\nPassword Manager Menu:")
        print("1. Add Password")
        print("2. Retrieve Password")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice not in ["1", "2", "3"]:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue

        if choice == "1":
            add_password(conn)
        elif choice == "2":
            retrieve_password(conn)
        elif choice == "3":
            print("Exiting...")
            break
    
    conn.close()

if __name__ == "__main__":
    main()
