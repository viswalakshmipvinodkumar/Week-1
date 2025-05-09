"""
Simple Bank Account Implementation
- Demonstrates OOP concepts (classes, objects, methods, attributes)
- Focuses on core banking operations: deposit, withdraw, and balance checking
- Takes input from the user
"""

class BankAccount:
       
    def __init__(self, account_number, account_holder, initial_balance=0.0):
        """Initialize a new bank account with account details."""
        self.account_number = account_number
        self.account_holder = account_holder
        self.__balance = initial_balance  # Private attribute using name mangling
        
        # Print initial account information
        print(f"\nAccount created successfully!")
        print(f"Account Number: {self.account_number}")
        print(f"Account Holder: {self.account_holder}")
        print(f"Initial Balance: ${self.__balance:.2f}")
    
    def deposit(self, amount):
        """Deposit money into the account."""
        if amount <= 0:
            print("Error: Deposit amount must be positive.")
            return False
        
        self.__balance += amount
        print(f"${amount:.2f} deposited successfully.")
        print(f"New balance: ${self.__balance:.2f}")
        return True
    
    def withdraw(self, amount):
        """Withdraw money from the account."""
        if amount <= 0:
            print("Error: Withdrawal amount must be positive.")
            return False
        
        if amount > self.__balance:
            print(f"Error: Insufficient funds. Current balance: ${self.__balance:.2f}")
            return False
        
        self.__balance -= amount
        print(f"${amount:.2f} withdrawn successfully.")
        print(f"New balance: ${self.__balance:.2f}")
        return True
    
    def check_balance(self):
        """Display the current account balance."""
        print(f"Account Balance for {self.account_holder}: ${self.__balance:.2f}")


def display_menu():
    """Display the main menu options."""
    print("\n===== Bank Account Menu =====")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Check Balance")
    print("4. Exit")
    print("============================")


def get_valid_amount():
    """Get a valid amount input from the user."""
    while True:
        try:
            amount = float(input("Enter amount: $"))
            if amount <= 0:
                print("Amount must be positive. Please try again.")
                continue
            return amount
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# Main program
if __name__ == "__main__":
    print("Welcome to the Simple Banking System!")
    
    # Get account information from user
    account_number = input("Enter account number: ")
    account_holder = input("Enter account holder name: ")
    
    # Get initial balance
    try:
        initial_balance = float(input("Enter initial balance (0 for none): $"))
        if initial_balance < 0:
            print("Initial balance cannot be negative. Setting to 0.")
            initial_balance = 0
    except ValueError:
        print("Invalid input. Setting initial balance to 0.")
        initial_balance = 0
    
    # Create bank account
    account = BankAccount(account_number, account_holder, initial_balance)
    
    # Main menu loop
    while True:
        display_menu()
        
        try:
            choice = int(input("Enter your choice (1-4): "))
            
            if choice == 1:
                # Deposit
                amount = get_valid_amount()
                account.deposit(amount)
            
            elif choice == 2:
                # Withdraw
                amount = get_valid_amount()
                account.withdraw(amount)
            
            elif choice == 3:
                # Check balance
                account.check_balance()
            
            elif choice == 4:
                # Exit
                print("Thank you for using the Simple Banking System. Goodbye!")
                break
            
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
        
        except ValueError:
            print("Invalid input. Please enter a valid number.")
