# This program is a number guessing game.
# A random number between 0 and 99 is generated.
# The player has 8 chances to guess the correct number.
# After each guess, the program provides feedback:
# whether the guess is too high, too low, or correct.
# If the player guesses correctly within the chances, they win.
# Otherwise, the correct number is revealed at the end.


import random

print("Hi, welcome to the game! This is a number guessing game.")
print("You have 8 chances to guess the number. Let's start the game!")

number_to_guess = random.randrange(100)
chances = 8
guess_counter = 0

while guess_counter < chances:
    guess_counter += 1
    try:
        my_guess = int(input(f'Attempt {guess_counter} - Enter your guess (0 to 99): '))
        
        if my_guess == number_to_guess:
            print(f' Correct! The number was {number_to_guess}. You found it in {guess_counter} attempts.')
            break

        elif my_guess > number_to_guess:
            print('Your guess is too high.')

        elif my_guess < number_to_guess:
            print('Your guess is too low.')

        if guess_counter == chances:
            print(f' Out of attempts! The number was {number_to_guess}. Better luck next time.')
    except ValueError:
        print(" Please enter a valid integer.")
