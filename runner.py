#!usr/bin/env python3
"""SpartanChess: a Python GUI to play the Spartan chess variant against a friend."""

__author__ = "Chris Bao"
__version__ = "0.9"
__date__ = "19 Nov 2022"

# external imports
from tkinter import Tk, Event

# internal imports
from board import Board

# constants and pseudo-constants
SCREEN_WIDTH: int
SCREEN_HEIGHT: int

DARK_BG_COLOR: str = "#1c1c1c"

# global variables
window: Tk
board: Board


def resize_update(_: Event) -> None:
    """
    Updates contents to match new size. Called when window is resized.

    Parameters
    ---
    _: Event given by tkinter event handler on resize. Ignored.

    Returns
    ---
    None
    """
    # get tkinter to update window dimensions correctly
    window.update_idletasks()
    board.place_forget()
    board.resize()
    lbound = (window.winfo_width() - board.size) / 2
    ubound = (window.winfo_height() - board.size) / 2
    board.place(x=lbound, y=ubound)


def main() -> None:
    """
    Entry point. Runs the app.

    Parameters
    ---
    (no parameters)

    Returns
    ---
    None
    """
    global window, board
    window = Tk()
    SCREEN_WIDTH = window.winfo_screenwidth()
    SCREEN_HEIGHT = window.winfo_screenheight()
    window.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    window.minsize(600, 500)
    window.title("SpartanChess")
    window.config(bg=DARK_BG_COLOR)

    # make sure tkinter knows the window dimensions before adding stuff to it
    window.update_idletasks()
    board = Board(window)
    lbound = (window.winfo_width() - board.size) / 2
    ubound = (window.winfo_height() - board.size) / 2
    board.place(x=lbound, y=ubound)

    window.bind("<Configure>", resize_update)
    window.mainloop()


if __name__ == "__main__":
    main()
