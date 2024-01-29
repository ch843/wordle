# File: Wordle.py

"""
This application is called Wordle. It takes user input of a word, checks it against the correct word and sees if they are correct.
"""

import random

from WordleDictionary import EN_WORDS, ES_WORDS
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS

def wordle():
    def enter_action(s):
        # s is the variable passed in that the user typed in
        if s.lower() in FIVE_LETTER_WORDS:
            # here is where the color logic will go
            row = gw.get_current_row()
            matched_indices = set()
            correct_indices = set()

            for i in range(len(s)):
                if s[i] == random_word[i] and i not in correct_indices:
                    gw.set_square_color(row, i, CORRECT_COLOR)
                    correct_indices.add(i)
                elif s[i] in random_word and i not in matched_indices:
                    gw.set_square_color(row, i, PRESENT_COLOR)
                    matched_indices.add(i)
                elif i not in correct_indices and i not in matched_indices:
                    gw.set_square_color(row, i, MISSING_COLOR)
        else:
            gw.show_message("Not the right guess")
    
    gw = WordleGWindow()
    language = gw.get_language()
    random_word = ''
     #choose random word
    if language == "English":
        random_word = random.choice(EN_WORDS).upper()
    elif language == "Espanol":
        random_word = random.choice(EN_WORDS).upper()

    gw.add_enter_listener(enter_action)

    gw.show_message("Enter a word")
    gw.set_current_row(0)

if __name__ == "__main__":
    wordle()
