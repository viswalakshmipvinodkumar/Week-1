
# Program 2: Save user input to a file and read it back

def save_and_read_user_input(file_path):
    # Save user input to file
    try:
        user_input = input("Enter some text to save to file: ")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(user_input)
        print(f"Text saved to {file_path}")
        
        # Read back from file
        print("\nReading back from file:")
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("===== User Input File Saver =====")
    file_path = input("Enter file path to save text: ")
    save_and_read_user_input(file_path)

if __name__ == "__main__":
    main()
