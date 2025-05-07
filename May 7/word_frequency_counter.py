
# Program 1: Read a text file and count word frequency

from collections import Counter

def count_word_frequency(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read().lower()
            # Remove punctuation and split into words
            words = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in text).split()
            # Count frequency
            word_counts = Counter(words)
            return word_counts
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def main():
    print("===== Word Frequency Counter =====")
    file_path = input("Enter the path to a text file: ")
    word_counts = count_word_frequency(file_path)
    
    if word_counts:
        print("\nWord Frequency :")
        for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
            print(f"{word}: {count}")

if __name__ == "__main__":
    main()
