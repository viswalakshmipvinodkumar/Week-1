# Constants for the login system
# USERNAME: Predefined correct username
# PASSWORD: Predefined correct password
# MAX_ATTEMPTS: Maximum number of login attempts allowed

# Function to check if the provided username and password are correct
# Arguments:
# - username (str): The entered username
# - password (str): The entered password
# Returns:
# - True if both username and password match the predefined ones, False otherwise
# Logic:
# - Compares the entered username and password with predefined ones

# Main function to handle the login process
# Includes:
# - Input validation for username and password
# - Case-sensitive login check
# - Retry mechanism with a set number of attempts (MAX_ATTEMPTS)
# - Error handling for empty username/password input

# Loop to allow the user to attempt logging in up to MAX_ATTEMPTS
# Prompts the user to input username and password
# Checks if either username or password is empty and raises an error
# Attempts the login check using the provided credentials
# If login is successful, print success and break the loop
# If login is unsuccessful, increment the attempt counter and inform the user of remaining attempts
# If maximum attempts are reached, print a failure message

# Call the main function to start the login process


import getpass

USERNAME = "Viswalakshmi"
PASSWORD = "Lakshmi123"
MAX_ATTEMPTS = 3

def login(username, password):
    # Check username and password validity (case-sensitive for both)
    if username == USERNAME and password == PASSWORD:
        return True
    return False

def main():
    print("=== Login System ===")
    attempts = 0
    
    while attempts < MAX_ATTEMPTS:
        try:
            username = input("Enter username: ").strip()
            password = getpass.getpass("Enter password: ").strip()  # Mask the password input

            # Check for empty input
            if not username or not password:
                raise ValueError("Username and password cannot be empty.")
            
            # Attempt login
            if login(username, password):
                print("Login successful!")
                break  # Exit after successful login
            else:
                attempts += 1
                print(f"Incorrect username or password. You have {MAX_ATTEMPTS - attempts} attempts left.")
        
        except ValueError as e:
            print("Error:", e)

        if attempts == MAX_ATTEMPTS:
            print("Too many failed login attempts. Please try again later.")

main()
