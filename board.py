#!usr/bin/env python3
"""The chess board for SpartanChess. Note that board indices follow
ranks 1 to 8 and files a to h."""

__author__ = "Chris Bao"
__version__ = "0.9"
__date__ = "19 Nov 2022"

# external imports
from tkinter import Tk, Canvas, Event
from PIL.ImageTk import PhotoImage

# internal imports
from piece import Piece


class Board(Canvas):
    # constants
    LIGHT_SQUARE_COLOR: str = "#ffbbff"
    DARK_SQUARE_COLOR: str = "#b75fbf"

    SCALE_RATIO: float = 4/5  # max proportion of width or height this takes up

    # instance variables
    size: int
    state: list[list[Piece]]
    selectedR: int
    selectedF: int
    # to keep images from being garbage collected. this is a known bug.
    imageList: list[PhotoImage] = []

    def __init__(self, window: Tk) -> None:
        """
        Constructor.

        Parameters
        ---
        window: root tkinter window

        Returns
        ---
        None
        """
        self.size = min(window.winfo_width() * self.SCALE_RATIO,
                        window.winfo_height() * self.SCALE_RATIO)
        super().__init__(
            master=window,
            borderwidth=0,
            highlightthickness=0,
            width=self.size,
            height=self.size
        )
        self.initBoard()
        self.draw()

        self.bind("<Button-1>", self.mousePressed)
        self.bind("<ButtonRelease-1>", self.mouseReleased)

    def mousePressed(self, event: Event) -> None:
        """
        Handle mouse-press events. Manages movement of pieces.

        Parameters
        ---
        event: Event given by tkinter event handler on mouse press.

        Returns
        ---
        None
        """
        self.selectedR = 7 - int(event.y / self.size * 7)
        self.selectedF = int(event.x / self.size * 8)

    def mouseReleased(self, event: Event) -> None:
        """
        Handle mouse-release events. Manages movement of pieces.

        Parameters
        ---
        event: Event given by tkinter event handler on mouse release.

        Returns
        ---
        None
        """
        # TODO: NOT WORKING!!!
        targetR = 7 - int(event.y / self.size * 7)
        targetF = int(event.x / self.size * 8)
        if self.selectedR == targetR and self.selectedF == targetF:
            return
        self.state[targetR][targetF] = self.state[self.selectedR][self.selectedF]
        self.state[self.selectedR][self.selectedF] = Piece(Piece.EMPTY,
                                                           self.selectedR,
                                                           self.selectedF)
        self.draw()

    def initBoard(self) -> None:
        """
        Put the pieces in their starting positions.

        Parameters
        ---
        (no parameters)

        Returns
        ---
        None
        """
        self.state = []
        # note that this is in the opposite order of how it's
        # displayed on the screen
        self.state.append([Piece(Piece.ROOK, 0, 0),
                           Piece(Piece.KNIGHT, 0, 1),
                           Piece(Piece.BISHOP, 0, 2),
                           Piece(Piece.QUEEN, 0, 3),
                           Piece(Piece.PKING, 0, 4),
                           Piece(Piece.BISHOP, 0, 5),
                           Piece(Piece.KNIGHT, 0, 6),
                           Piece(Piece.ROOK, 0, 7)])
        self.state.append([Piece(Piece.PAWN, 1, i) for i in range(8)])
        for i in range(4):
            self.state.append([Piece(Piece.EMPTY, i, j) for j in range(8)])
        self.state.append([Piece(Piece.HOPLITE, 6, i) for i in range(8)])
        self.state.append([Piece(Piece.LIEUTENANT, 7, 0),
                           Piece(Piece.GENERAL, 7, 1),
                           Piece(Piece.SKING, 7, 2),
                           Piece(Piece.CAPTAIN, 7, 3),
                           Piece(Piece.CAPTAIN, 7, 4),
                           Piece(Piece.SKING, 7, 5),
                           Piece(Piece.WARLORD, 7, 6),
                           Piece(Piece.LIEUTENANT, 7, 7)])

    def resize(self) -> None:
        """
        Resize the canvas according to the windows' new size.

        Parameters
        ---
        (no parameters)

        Returns
        ---
        None
        """
        newSize = min(self.master.winfo_width() * self.SCALE_RATIO,
                      self.master.winfo_height() * self.SCALE_RATIO)
        if newSize != self.size:
            self.size = newSize
            self.configure(width=self.size,
                           height=self.size)
            Piece.icons_cached = False
            self.draw()

    def draw(self) -> None:
        """
        Draw everything to the board. Note: this will clear all previously
        drawn graphics!

        Parameters
        ---
        (no parameters)

        Returns
        ---
        None
        """
        self.delete(all)
        self.imageList.clear()
        for r in range(0, 8):  # rank
            for f in range(0, 8):  # file
                # draw square
                # note ranks are subtracted from 7 bc ranks go from
                # bigger to smaller when going down
                self.create_rectangle(
                    self.size * f / 8,
                    self.size * (7-r) / 8,
                    self.size * (f+1) / 8,
                    self.size * (7-r+1) / 8,
                    fill=self.LIGHT_SQUARE_COLOR if (r + f) % 2 == 0
                    else self.DARK_SQUARE_COLOR,
                    width=0
                )

                # draw piece (on top)
                self.state[r][f].draw(self)

        Piece.icons_cached = True
