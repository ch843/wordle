# File: Wordle.py

"""
This module is the starter file for the Wordle assignment.
BE SURE TO UPDATE THIS COMMENT WHEN YOU WRITE THE CODE.
"""

import random

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS

def wordle():

    def enter_action(s):
        gw.show_message("You have to implement this method.")

    gw = WordleGWindow()
    gw.add_enter_listener(enter_action)

    #choose random word
    random_word = random.choice(FIVE_LETTER_WORDS).upper()
    print(f"Random Word: {random_word}")

    # Display the random word in the first row
    for col, letter in enumerate(random_word):
        if col < N_COLS:
            gw.set_square_letter(0, col, letter)


# Startup code

if __name__ == "__main__":
    wordle()
