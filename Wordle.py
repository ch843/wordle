# File: Wordle.py

"""
This application is called Wordle. It takes user input of a word, checks it against the correct word and sees if they are correct.
"""

import random

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS, CORRECT_COLOR, MISSING_COLOR, PRESENT_COLOR, UNKNOWN_COLOR

def wordle():

    def enter_action(s):
        # s is the variable passed in that the user typed in

        if s.lower() in FIVE_LETTER_WORDS:
            # here is where the color logic will go
            gw.show_message("Great job picking a valid word!")
            row = gw.get_current_row()
            i = 0
            for i in range(len(s)):
                if (s[i] == random_word[i]):
                  gw.set_square_color(row, i, CORRECT_COLOR)
                elif (s[i] in random_word):
                  gw.set_square_color(row, i, PRESENT_COLOR)
                else:
                  gw.set_square_color(row, i, MISSING_COLOR)  

        else:
            gw.show_message("Not in word list")

    #choose random word
    random_word = random.choice(FIVE_LETTER_WORDS).upper()
    
    gw = WordleGWindow()

    gw.add_enter_listener(enter_action)

    gw.show_message("Enter a word")
    gw.set_current_row(0)

if __name__ == "__main__":
    wordle()