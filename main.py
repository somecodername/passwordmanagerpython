import sqlcipher3
import getpass
import re
import random
import string

key = 'your_key_here'

password_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')

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
    strength = input("Enter password strength (easy, normal, hard,): ").lower()
    
    if strength == 'one-time':
        length = int(input("Enter password length (max 16): "))
        if length > 16:
            print("Password length cannot exceed 16 characters.")
            return
        password = generate_one_time_password(length)
        print("Generated one-time password:", password)
        return
    elif strength not in ['easy', 'normal', 'hard']:
        print("Invalid password strength. Please choose 'easy', 'normal', 'hard'.")
        return
    
    password = generate_password(strength)
    
    if not password:
        print("Invalid password strength. Please choose 'easy', 'normal', or 'hard'.")
        return
    
    print("Generated password:", password)
    
    #confirm_password = getpass.getpass("Confirm password: ")
    
    #if password != confirm_password:
        #print("Passwords do not match. Please try again.")
        #return
    
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

def generate_password(strength):
    if strength == 'easy':
        length = 10
    elif strength == 'normal':
        length = 30
    elif strength == 'hard':
        length = 50
    else:
        return None
    
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def generate_one_time_password(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def main():
    conn = sqlcipher3.connect('passwords.db')
    conn.execute('PRAGMA key="{}"'.format(key))
    
    create_table(conn)
    
    while True:
        print("\nPassword Manager Menu:")
        print("1. Add Password")
        print("2. Retrieve Password")
        print("3. Generate One-Time Password")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice not in ["1", "2", "3", "4"]:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
            continue

        if choice == "1":
            add_password(conn)
        elif choice == "2":
            retrieve_password(conn)
        elif choice == "3":
            length = int(input("Enter password length (max 16): "))
            if length > 16:
                print("Password length cannot exceed 16 characters.")
                continue
            password = generate_one_time_password(length)
            print("Generated one-time password:", password)
        elif choice == "4":
            print("Exiting...")
            break
    
    conn.close()

if __name__ == "__main__":
    main()

