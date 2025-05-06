def is_palindrome(s):
    s = s.lower().replace(" ", "")  # Normalize input
    return s == s[::-1]

def validate_input(user_input):
    if not ((user_input.startswith('"') and user_input.endswith('"')) or 
            (user_input.startswith("'") and user_input.endswith("'"))):
        raise ValueError("Input must be a string enclosed in quotes.")
    return user_input[1:-1]  # Strip quotes

def main():
    try:
        user_input = input('Enter a string in quotes (e.g., "madam"): ')
        cleaned = validate_input(user_input)
        if is_palindrome(cleaned):
            print("It is a palindrome.")
        else:
            print("It is not a palindrome.")
    except ValueError as e:
        print("Error:", e)

main()
