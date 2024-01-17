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
        # gets current row user is on
        current_row = gw.get_current_row()

        userWord = ''
        # uses list comprehension to take each letter in the row and add it to a list
        letterList = [gw.get_square_letter(int(current_row), int(col)) for col in range(N_COLS)]

        # takes list and joins all letters together into a string
        userWord = userWord.join(letterList)

        if userWord.lower() in FIVE_LETTER_WORDS:
            gw.show_message("Great job picking a valid word!")
        else:
            gw.show_message("Not in word list")

    gw = WordleGWindow()
    gw.add_enter_listener(enter_action)

    #choose random word
    random_word = random.choice(FIVE_LETTER_WORDS).upper()
    # print(f"Random Word: {random_word}")

    # Display the random word in the first row
    for col, letter in enumerate(random_word):
        if col < N_COLS:
            gw.set_square_letter(0, col, letter)

# Startup code

if __name__ == "__main__":
    wordle()
