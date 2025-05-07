
# Program 3: Build a contact book using a dictionary and save/load from a file

import json
import os

class ContactBook:
    def __init__(self, file_path):
        self.file_path = file_path
        self.contacts = {}
        self.load_contacts()
    
    def load_contacts(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    self.contacts = json.load(file)
                print("Contacts loaded successfully!")
            else:
                print("No existing contacts file found. Starting with empty contact book.")
        except json.JSONDecodeError:
            print("Error reading contacts file. Starting with empty contact book.")
        except Exception as e:
            print(f"Error loading contacts: {e}")
    
    def save_contacts(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(self.contacts, file, indent=4)
            print("Contacts saved successfully!")
            return True
        except Exception as e:
            print(f"Error saving contacts: {e}")
            return False
    
    def add_contact(self, name, phone, email=""):
        self.contacts[name] = {
            "phone": phone,
            "email": email,
            "address": ""
        }
        self.save_contacts()
        print(f"Contact '{name}' added successfully!")
    
    def view_contact(self, name):
        if name in self.contacts:
            contact = self.contacts[name]
            print(f"\nContact: {name}")
            print(f"Phone: {contact['phone']}")
            print(f"Email: {contact['email']}")
            print(f"Address: {contact['address']}")
        else:
            print(f"Contact '{name}' not found!")
    
    def list_contacts(self):
        if not self.contacts:
            print("Contact book is empty!")
            return
        
        print("\nAll Contacts:")
        for name in self.contacts:
            print(f"- {name}: {self.contacts[name]['phone']}")
    
    def delete_contact(self, name):
        if name in self.contacts:
            del self.contacts[name]
            self.save_contacts()
            print(f"Contact '{name}' deleted successfully!")
        else:
            print(f"Contact '{name}' not found!")

def main():
    print("===== Contact Book Application =====")
    contacts_file = input("Enter contacts file path (default: contacts.json): ") or "contacts.json"
    contact_book = ContactBook(contacts_file)
    
    while True:
        print("\n----- Contact Book Menu -----")
        print("1. Add Contact")
        print("2. View Contact")
        print("3. List All Contacts")
        print("4. Delete Contact")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            name = input("Enter name: ")
            phone = input("Enter phone number: ")
            email = input("Enter email (optional): ")
            contact_book.add_contact(name, phone, email)
        
        elif choice == '2':
            name = input("Enter name to view: ")
            contact_book.view_contact(name)
        
        elif choice == '3':
            contact_book.list_contacts()
        
        elif choice == '4':
            name = input("Enter name to delete: ")
            contact_book.delete_contact(name)
        
        elif choice == '5':
            print("Exiting Contact Book. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
