# File: WordleGraphics.py

"""
This file implements the WordleGWindow class, which manages the
graphical display for the Wordle project.
"""

import atexit
import time
import tkinter as tk
from WordleDictionary import FIVE_LETTER_WORDS

# Constants

N_ROWS = 6			# Number of rows
N_COLS = 5			# Number of columns

MISSING_COLOR = "#999999"       # Gray for letters that don't appear
UNKNOWN_COLOR = "#FFFFFF"       # Undetermined letters are white
KEY_COLOR = "#DDDDDD"           # Keys are colored light gray

CANVAS_WIDTH = 500		# Width of the tkinter canvas (pixels)
CANVAS_HEIGHT = 700		# Height of the tkinter canvas (pixels)

SQUARE_SIZE = 60		# Size of each square (pixels)
SQUARE_SEP = 5                  # Separation between squares (pixels)
TOP_MARGIN = 30    		# Top margin (pixels)
BOTTOM_MARGIN = 30    		# Bottom margin (pixels)
MESSAGE_SEP = 20                # Space between board and message center

SQUARE_FONT = ("Helvetica Neue", -44, "bold")
MESSAGE_FONT = ("Helvetica Neue", -20, "bold")
KEY_FONT = ("Helvetica Neue", -18)
ENTER_FONT = ("Helvetica Neue", -14)

KEY_WIDTH = 40
KEY_HEIGHT = 60
KEY_CORNER = 9
KEY_XSEP = 5
KEY_YSEP = 7

KEY_LABELS = [
    [ "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P" ],
    [ "A", "S", "D", "F", "G", "H", "J", "K", "L" ],
    [ "ENTER", "Z", "X", "C", "V", "B", "N", "M", "DELETE" ]
]

CLICK_MAX_DISTANCE = 2
CLICK_MAX_DELAY = 0.5

# Derived constants

SQUARE_DELTA = SQUARE_SIZE + SQUARE_SEP
BOARD_WIDTH = N_COLS * SQUARE_SIZE + (N_COLS - 1) * SQUARE_SEP
BOARD_HEIGHT = N_ROWS * SQUARE_SIZE + (N_ROWS - 1) * SQUARE_SEP
MESSAGE_X = CANVAS_WIDTH / 2
MESSAGE_Y = TOP_MARGIN + BOARD_HEIGHT + MESSAGE_SEP

class WordleGWindow:
    """This class creates the Wordle window."""

    def __init__(self):
        """Creates the Wordle window."""

        def create_grid():
            return [
                [
                    WordleSquare(canvas, i, j) for j in range(N_COLS)
                ] for i in range(N_ROWS)
            ]

        def create_keyboard():
            keys = { }
            nk = len(KEY_LABELS[0])
            h = KEY_HEIGHT
            y0 = CANVAS_HEIGHT - BOTTOM_MARGIN - 3 * KEY_HEIGHT - 2 * KEY_YSEP
            for row in range(len(KEY_LABELS)):
                y = y0 + row * (KEY_HEIGHT + KEY_YSEP)
                x = (CANVAS_WIDTH - nk * KEY_WIDTH - (nk - 1) * KEY_XSEP) / 2
                if row == 1:
                    x += (KEY_WIDTH + KEY_XSEP) / 2
                for col in range(len(KEY_LABELS[row])):
                    label = KEY_LABELS[row][col]
                    w = KEY_WIDTH
                    if len(label) > 1:
                        w += (KEY_WIDTH + KEY_XSEP) / 2
                    keys[label] = WordleKey(self._canvas, x, y, w, h, label)
                    x += w + KEY_XSEP
            return keys

        def create_message():
            return WordleMessage(self._canvas,
                                CANVAS_WIDTH / 2,
                                MESSAGE_Y)

        def key_action(tke):
            if isinstance(tke, str):
                ch = tke.upper()
            else:
                ch = tke.char.upper()
            
            #if the user presses the DELETE button on the screen or keyboard
            if ch in ["\007", "\177", "\x08", "\x7F", "DELETE"]:
                self.show_message("")
                if self._row < N_ROWS and self._col > 0:
                    self._col -= 1
                    sq = self._grid[self._row][self._col]
                    sq.set_letter(" ")
            # if user presses ENTER or TAB keys
            elif ch in ["\r", "\n", "\t", "ENTER"]:
                self.show_message("")
                s = ""
                for col in range(N_COLS):
                    s += self._grid[self._row][col].get_letter()
                
                for fn in self._enter_listeners:
                    fn(s)

                # move to next row if not at last row and word exists in dictionary
                if (self._row < (N_ROWS - 1)) and (s.lower() in FIVE_LETTER_WORDS):
                    current_row = self._row
                    self.set_current_row(current_row + 1)
                # show  that the user didn't guess it right
                elif (self._row == (N_ROWS - 1)):
                    self.show_stats()
                
            elif ch.isalpha():
                self.show_message("")
                if self._row < N_ROWS and self._col < N_COLS:
                    sq = self._grid[self._row][self._col]
                    sq.set_letter(ch)
                    self._col += 1

        def press_action(tke):
            self._down_x = tke.x
            self._down_y = tke.y
            self._down_time = time.time()

        def release_action(tke):
            if abs(self._down_x - tke.x) <= CLICK_MAX_DISTANCE:
                if abs(self._down_y - tke.y) <= CLICK_MAX_DISTANCE:
                    t = time.time()
                    if t - self._down_time < CLICK_MAX_DELAY:
                        key = find_key(tke.x, tke.y)
                        if key:
                            key_action(key._label)

        def find_key(x, y):
            for key in self._keys.values():
                kx, ky, kw, kh = key._bounds
                if x >= kx and x <= kx + kw and y >= ky and y <= ky + kh:
                    return key
            return None

        def delete_window():
            """Closes the window and exits from the event loop."""
            root.destroy()

        def start_event_loop():
            """Starts the tkinter event loop when the program exits."""
            root.mainloop()

        root = tk.Tk()
        root.title("Wordle")
        root.protocol("WM_DELETE_WINDOW", delete_window)
        self._root = root
        canvas = tk.Canvas(root,
                                bg="White",
                                width=CANVAS_WIDTH,
                                height=CANVAS_HEIGHT,
                                highlightthickness=0)
        canvas.pack()
        self._canvas = canvas
        self._grid = create_grid()
        self._message = create_message()
        self._keys = create_keyboard()
        self._enter_listeners = []
        root.bind("<Key>", key_action)
        root.bind("<ButtonPress-1>", press_action)
        root.bind("<ButtonRelease-1>", release_action)
        self._row = 0
        self._col = 0
        atexit.register(start_event_loop)

        # Create a dropdown menu
        self.dropdown_var = tk.StringVar()
        self.dropdown_var.set("Normal Mode")
        self.dropdown = tk.OptionMenu(root, self.dropdown_var, "Normal Mode", "Colorblind Mode")
        self.dropdown.pack(pady=10)

        # Button to apply selected mode
        self.apply_button = tk.Button(root, text="Apply", command=self.apply_mode)
        self.apply_button.pack(pady=5)
        
    def get_square_letter(self, row, col):
        return self._grid[row][col].get_letter()

    def set_square_letter(self, row, col, ch):
        self._grid[row][col].set_letter(ch)

    def get_square_color(self, row, col):
        return self._grid[row][col].get_color()

    def set_square_color(self, row, col, color):
        self._grid[row][col].set_color(color)

    def get_key_color(self, ch):
        return self._keys[ch].get_color()

    def set_key_color(self, ch, color):
        self._keys[ch].set_color(color)

    def get_current_row(self):
        return self._row

    def set_current_row(self, row):
        self._row = row
        self._col = 0
        for col in range(N_COLS):
            self.set_square_letter(row, col, " ")
            self.set_square_color(row, col, UNKNOWN_COLOR)

    def add_enter_listener(self, fn):
        self._enter_listeners.append(fn)

    def show_message(self, msg, color="Black"):
        self._message.set_text(msg, color)

    def show_stats(self):
        stats = {
            1: "You are among the elite!\n0.02% of Wordle users get it on their first try." ,
            2: "You are AWESOME!\n5.67% of Wordle users get it on their second guess.",
            3: "You are really good!\n22.66% of Wordle users get it on their third guess.",
            4: "You are good!\n33.10% of Wordle users get it on their fourth guess.",
            5: "You are pretty average!\n23.91% of Wordle users get it on their fifth guess.",
            6: "You barely squeaked by!\n11.72% of Wordle users get it on their sixth guess.",
            "No": "Good try!\n2.92% of Wordle users guess don't guess it right."
        }
        num_guesses = self._row + 1
        if num_guesses > 6:
            title = "You didn't guess it"
            message = stats['No']
            CustomPopup(self._root, title, message)
        else:
            title = f"You guessed it in {num_guesses} tries."
            message = stats[num_guesses]
            CustomPopup(self._root, title, message)

    # applies 
    def apply_mode(self):
        selected_mode = self.dropdown_var.get()
        if selected_mode == "Colorblind Mode":
            CORRECT_COLOR = "#4f82f0"
            PRESENT_COLOR = "#fcbd5d" 
            return CORRECT_COLOR, PRESENT_COLOR
        elif selected_mode == "Normal Mode":
            CORRECT_COLOR = "#66BB66"
            PRESENT_COLOR = "#CCBB66"
            return CORRECT_COLOR, PRESENT_COLOR

class CustomPopup(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.parent = parent
        self.title(title)
        label = tk.Label(self, text=message)
        label.pack(padx=20, pady=10)
        share_button = tk.Button(self, text="Share", command=self.on_share_clicked)
        share_button.pack(pady=5)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_share_clicked(self):
        # The action when the "Share" button is clicked
        # Right now, it just closes the window when share is clicked
        # This would be built out more in teh future
        self.parent.destroy()
    
    def on_close(self):
        # Close the entire application when the dialog is closed, so they can't go back to the game
        self.parent.destroy()

class WordleSquare:

    def __init__(self, canvas, row, col):
        x0 = (CANVAS_WIDTH - BOARD_WIDTH) / 2 + col * SQUARE_DELTA
        y0 = TOP_MARGIN + row * SQUARE_DELTA
        x1 = x0 + SQUARE_SIZE
        y1 = y0 + SQUARE_SIZE
        self._canvas = canvas
        self._ch = " "
        self._color = UNKNOWN_COLOR
        self._frame = canvas.create_rectangle(x0, y0, x1, y1)
        self._text = canvas.create_text(x0 + SQUARE_SIZE / 2,
                                        y0 + SQUARE_SIZE / 2,
                                        text=self._ch,
                                        font=SQUARE_FONT)

    def get_letter(self):
        return self._ch

    def set_letter(self, ch):
        self._ch = ch
        self._canvas.itemconfigure(self._text, text=ch)

    def get_color(self):
        return self._color

    def set_color(self, color):
        color = color.upper()
        self._color = color
        fg = "White"
        if color == UNKNOWN_COLOR:
            fg = "Black"
        self._canvas.itemconfig(self._frame, fill=color)
        self._canvas.itemconfig(self._text, fill=fg)


class WordleKey:

    def __init__(self, canvas, x, y, width, height, label):
        self._canvas = canvas
        self._label = label
        self._bounds = [ x, y, width, height ]
        self._color = UNKNOWN_COLOR
        font = KEY_FONT
        if label == "ENTER":
            font = ENTER_FONT
        if label == "DELETE":
            label = "\u232B"
        points = [ x + KEY_CORNER, y,
                   x + KEY_CORNER, y,
                   x + width - KEY_CORNER, y,
                   x + width - KEY_CORNER, y,
                   x + width, y,
                   x + width, y + KEY_CORNER,
                   x + width, y + KEY_CORNER,
                   x + width, y + height - KEY_CORNER,
                   x + width, y + height - KEY_CORNER,
                   x + width, y + height,
                   x + width - KEY_CORNER, y + height,
                   x + width - KEY_CORNER, y + height,
                   x + KEY_CORNER, y + height,
                   x + KEY_CORNER, y + height,
                   x, y + height,
                   x, y + height - KEY_CORNER,
                   x, y + height - KEY_CORNER,
                   x, y + KEY_CORNER,
                   x, y + KEY_CORNER,
                   x, y]
        self._frame = canvas.create_polygon(points,
                                            fill=KEY_COLOR,
                                            outline=KEY_COLOR,
                                            smooth=True)
        self._text = canvas.create_text(x + width / 2,
                                        y + height / 2,
                                        text=label,
                                        font=font)

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color
        fg = "White"
        if color == UNKNOWN_COLOR:
            fg = "Black"
        self._canvas.itemconfig(self._frame, fill=color)
        self._canvas.itemconfig(self._text, fill=fg)


class WordleMessage:

    def __init__(self, canvas, x, y):
        self._canvas = canvas
        self._text = ""
        self._msg = canvas.create_text(x, y,
                                       text="",
                                       font=MESSAGE_FONT,
                                       anchor=tk.CENTER)

    def get_text(self):
        return self._text

    def set_text(self, text, color="Black"):
        self._text = text
        self._canvas.itemconfigure(self._msg, text=text, fill=color)
