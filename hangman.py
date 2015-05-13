# Hangman, The Game!
# Created by Josien Braas to practice Python

import random
import string
import sys
import time

# If a dictionary file is specified, use it -
# otherwise, use a default dictionary
if len(sys.argv) > 1:
    dictionary_file = sys.argv[1]
else:
    dictionary_file = 'dictionary.txt'

game_state = [
    """






     _____________
""",
    """

    |
    |
    |
    |
    |
    |_____________
""",
    """
    _________
    |
    |
    |
    |
    |
    |_____________
""",
    """
    _________
    |         |
    |
    |
    |
    |
    |_____________
""",
    """
    _________
    |         |
    |         0
    |
    |
    |
    |_____________
""",
    """
    _________
    |         |
    |         0
    |         |
    |
    |
    |_____________
""",
    """
    _________
    |         |
    |         0
    |        /|\\
    |
    |
    |_____________
""",
    """
    _________
    |         |
    |         0
    |        /|\\
    |        /
    |
    |_____________
""",
    """
    _________
    |         |
    |         0
    |        /|\\
    |        / \\
    |
    |_____________
"""
]


def start_game(player_score, computer_score):
    """
    Initialize the game and execute the game turns. A
    new game starts with score 0 for both the player
    and the computer. Subsequent game rounds should be
    called with the updated scores.
    """

    # Initialize the game if this is the first round.
    if player_score == 0 and computer_score == 0:
        print("\nWelcome to Hangman, The Game!")
        print("\nWhat is your name?")
        player_name = input("> ")
        time.sleep(0.4)
        print("\nHi " + player_name + ", let's play!")
        time.sleep(0.4)

    word = pick_word()
    current_state = 0
    guess_list = []

    print("\n--------------------\nHangman Rules\n"
          + """
The rules are as follows. You have to guess the word
before the hanging is completed. For every letter you
guessed that is not part of the word, the hanging
advances one step... Have fun!""")

    # Execute game turns until end condition is reached.
    while current_state < 8:

        player_guess = input("\nGuess a letter: ")
        while len(check_guess(player_guess, guess_list)) > 0:
            print(check_guess(player_guess, guess_list))
            player_guess = input("\nGuess a letter: ")

        guess_list.append(player_guess.lower())

        if player_guess not in word:
            current_state = current_state + 1
            print("Uh oh! That letter is not in the word: "
                  + show_word(word, guess_list)
                  + "\n"
                  + game_state[current_state])
        else:
            print("Good guess! The word is now: "
                  + show_word(word, guess_list))

        # Win condition
        if check_win(word, guess_list) == 1:
            player_score += 1
            print("\n>> YOU WIN! <<\n")
            print("The score is now:")
            print("Player " + str(player_score) + " - Computer "
                  + str(computer_score) + "\n")
            break

        # Lose condition
        if current_state == 8:
            computer_score += 1
            print("\nThe word was: "
                  + show_word(word, list(string.ascii_lowercase)))
            print("\n>> YOU LOSE! <<\n")
            print("The score is now:")
            print("Player " + str(player_score) + " - Computer "
                  + str(computer_score) + "\n")

    print("Do you want to play another game?")
    choice = input("y/n: ")

    if choice == 'y':
        start_game(player_score, computer_score)


def pick_word(minimum_length=5):
    """() -> string

    Return a random word from the dictionary file. The minimum
    length of the word can optionally be provided as a parameter.
    """
    file_length = file_len(dictionary_file)

    while True:
        random_number = random.randint(0, file_length)
        random_line = get_line(random_number, dictionary_file)
        if len(random_line) >= minimum_length:
            word = random_line
            break

    return word


def file_len(file_name):
    """(string) -> int

    Source:
    http://stackoverflow.com/questions/845058/
    how-to-get-line-count-cheaply-in-python

    >>> file_len('dictionary_small.txt')
    10
    >>> file_len('dictionary.txt')
    45349
    """
    with open(file_name) as f:
        for i, element in enumerate(f):
            pass
    return i + 1


def get_line(line_number, dictionary_file):
    """(int, string) -> string

    Source:
    http://stackoverflow.com/questions/2081836/
    reading-specific-lines-only-python

    >>> get_line(5, 'dictionary_small.txt')
    'gruff'
    >>> get_line(20, 'dictionary.txt')
    'abasing'
    """
    fp = open(dictionary_file)
    for i, line in enumerate(fp):
        if i == line_number - 1:
            result = line
            break
    fp.close()
    return result.rstrip()


def check_guess(player_guess, guesses):
    """(string, [string]) -> string

    Check if the guess provided by the user is a correct guess -
    that is, one that is just 1 letter and not guessed before.

    >>> check_guess('', [])
    'Please enter at least one letter.'
    >>> check_guess('bacon', [])
    'Please enter only one character.'
    >>> check_guess('c', ['f', 'c', 'g', 'e'])
    'Please pick a letter you did not guess before.'
    >>> check_guess('bacon', ['c', 'a', 'b', 'o', 'n'])
    'Please enter only one character.'
    """
    message = ""
    if len(player_guess) == 1:
        if player_guess not in string.ascii_letters:
            message = "Please enter only letters."
        elif player_guess.lower() in guesses:
            message = "Please pick a letter you did not guess before."
    elif len(player_guess) == 0:
        message = "Please enter at least one letter."
    else:
        message = "Please enter only one character."
    return message


def show_word(word, guesses):
    """(string, [string]) -> string

    Return the word to guess with guessed letters filled in and
    underscores for un-guessed letters.

    >>> show_word("", [])
    ''
    >>> show_word("bacon", [])
    '_ _ _ _ _'
    >>> show_word("bacon", ['f', 'c', 'g', 'e'])
    '_ _ c _ _'
    >>> show_word("bacon", ['c', 'a', 'b', 'o', 'n'])
    'b a c o n'
    """
    word_list = list(word)
    for i, element in enumerate(word_list):
        if element not in guesses:
            word_list[i] = '_'
    return " ".join(word_list)


def check_win(word, guesses):
    """(string, [string]) -> int

    Return the guess status of a word based on the word to be guessed
    and the guesses a player has made.

    >>> check_win("", [])
    1
    >>> check_win("bacon", [])
    0
    >>> check_win("bacon", ['f', 'c', 'g', 'e'])
    0
    >>> check_win("bacon", ['c', 'a', 'b', 'o', 'n'])
    1
    """
    state = 1
    for letter in word:
        if letter not in guesses:
            state = 0
    return state


if __name__ == "__main__":
    start_game(0, 0)