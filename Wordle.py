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

        if s == random_word:
            gw.show_message("You guessed correct, great job!")
        elif s.lower() in EN_WORDS or s.lower() in ES_WORDS:
            # here is where the color logic will go
            gw.show_message("Valid word")
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
