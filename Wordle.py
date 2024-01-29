# File: Wordle.py

"""
This application is called Wordle. It takes user input of a word, checks it against the correct word and sees if they are correct.
"""

import random

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS, MISSING_COLOR, UNKNOWN_COLOR

def wordle():
    def enter_action(s):
        # s is the word that the user typed in
        if s.lower() in FIVE_LETTER_WORDS:
            row = gw.get_current_row()
            matched_indices = set()
            correct_indices = set()

            CORRECT_COLOR, PRESENT_COLOR = gw.apply_mode()

            for i in range(len(s)):
                if s[i] == random_word[i] and i not in correct_indices:
                    gw.set_square_color(row, i, CORRECT_COLOR)
                    correct_indices.add(i)
                elif s[i] in random_word and i not in matched_indices:
                    gw.set_square_color(row, i, PRESENT_COLOR)
                    matched_indices.add(i)
                elif i not in correct_indices and i not in matched_indices:
                    gw.set_square_color(row, i, MISSING_COLOR)

            if s == random_word:
                gw.show_stats()
        else:
            gw.show_message("Not a valid word. Try again!")

    #choose random word
    random_word = random.choice(FIVE_LETTER_WORDS).upper()
    print(random_word)
    
    gw = WordleGWindow()

    gw.add_enter_listener(enter_action)

    gw.show_message("Enter a word")
    gw.set_current_row(0)

if __name__ == "__main__":
    wordle()
