import os
import json
import secrets
import string
from cryptography.fernet import Fernet

#Path to the file where passwords will be stored
pass_file = "assists.json"

#Function to generate the password
def gen_pass(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(length))
    return password

#Function to load or create encryption key
def load_key():
    key_file = "secret.key"
    if os.path.exists(key_file):
        with open(key_file, "rb") as file:
            key = file.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, "wb") as file:
            file.write(key)
    return key

#Function to encrypt data
def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

#Function to decrypt data
def decrypt_data(data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(data).decode()
    return decrypted_data

#Function to store passwords securely
def store_pass(site, password, key):
    if os.path.exists(pass_file):
        with open(pass_file, "r") as file:
            passwords = json.load(file)
    else:
        passwords = {}

    passwords[site] = encrypt_data(password, key).decode()

    with open(pass_file, "w") as file:
        json.dump(passwords,file )


#Function to retrieve passwords
def get_pass(site, key):
    if os.path.exists(pass_file):
        with open(pass_file, "r") as file:
            passwords = json.load(file)

        if site in passwords:
            return decrypt_data(passwords[site].encode(), key)
        else:
            return "No password was found for this website."
    else:
        return "The password file does not exist."
    
#Main function
def main():
    key = load_key()

    while True:
        print("\nDime Man Assists")
        print("1. Make and save a new pass.")
        print("2. Grab a pass.")
        print("3. Exit")
        choice = input("Select what you would like to do: ")

        if choice == "1":
            site = input("Enter the site name: ")
            password = gen_pass()
            store_pass(site, password, key)
            print(f"Generated and stored password for {site}: {password}")

        elif choice == "2":
            site = input("Enter the website name: ")
            password = get_pass(site, key)
            print(f"Password for {site}: {password}")

        elif choice == "3":
            break
        else:
            print("That's not an option bucko. :( ")

if __name__ == "__main__":
    main()