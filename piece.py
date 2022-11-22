#!usr/bin/env python3
"""The pieces for SpartanChess."""

__author__ = "Chris Bao"
__version__ = "0.9"
__date__ = "19 Nov 2022"

from tkinter import Canvas
from PIL import Image, ImageTk


class Piece:
    # constants
    EMPTY: int = -1

    # Persian (White) piece ids
    PAWN: int = 0
    KNIGHT: int = 1
    BISHOP: int = 2
    ROOK: int = 3
    QUEEN: int = 4
    PKING: int = 5

    # Spartan (Black) piece ids
    HOPLITE: int = 10
    LIEUTENANT: int = 11
    CAPTAIN: int = 12
    GENERAL: int = 13
    WARLORD: int = 14
    SKING: int = 15

    icon_map: dict = {
        PAWN: Image.open("img/pawn.png"),
        KNIGHT: Image.open("img/knight.png"),
        BISHOP: Image.open("img/bishop.png"),
        ROOK: Image.open("img/rook.png"),
        QUEEN: Image.open("img/queen.png"),
        PKING: Image.open("img/pking.png"),

        HOPLITE: Image.open("img/hoplite.png"),
        LIEUTENANT: Image.open("img/lieutenant.png"),
        CAPTAIN: Image.open("img/captain.png"),
        GENERAL: Image.open("img/general.png"),
        WARLORD: Image.open("img/warlord.png"),
        SKING: Image.open("img/sking.png"),
    }

    # instance varaibles
    id: int
    # rank and file
    r: int
    f: int

    def __init__(self, id: int, r: int, f: int) -> None:
        """
        Constructor.

        Parameters
        ---
        id: int piece type id
        r: int rank
        f: int file
        """
        self.id = id
        self.r = r
        self.f = f

    def draw(self, canvas: Canvas) -> None:
        """
        Draw self to given canvas.

        Parameters
        ---
        canvas: tk.Canvas to draw on

        Returns
        ---
        None
        """
        if self.id == self.EMPTY:
            return
        resized = self.icon_map[self.id].resize((int(canvas.size / 8),)*2)
        icon = ImageTk.PhotoImage(resized)
        # subtract rank from 7 bc ranks go from high to low
        canvas.create_image(canvas.size * self.f // 8,
                            canvas.size * (7-self.r) // 8,
                            anchor="nw", image=icon)
        canvas.imageList.append(icon)

    def inCheckAfterMove(start: tuple[int, int], end: tuple[int, int],
                         whiteToMove: bool) -> bool:
        return False

    def findLegalMoves(r: int, f: int, board: list[list], whiteToMove: bool,
                       whiteShort: bool, whiteLong: bool, blackShort: bool, blackLong: bool) -> set[tuple[int, int]]:
        """
        Finds the legal moves for a given piece, board, and turn.

        Parameters
        ---
        r: int piece rank
        f: int piece file
        board: list[list[Piece]]
        whiteToMove: bool
        whiteShort: bool White short castle privilege
        whiteLong: bool White long castle privilege
        blackShort: bool White short castle privilege
        blackLong: bool White long castle privilege

        Returns
        ---
        set[tuple[int, int]]: set of valid (rank, file) tuples
        """
        print(board[r][f].id)
        if board[r][f].id == Piece.PAWN:
            valid = set()
            # normal move
            if board[r+1][f].id == Piece.EMPTY:
                if not Piece.inCheckAfterMove((r, f), (r+1, f), whiteToMove):
                    valid.add((r+1, f))
            # double-step move
            if r == 1 and board[r+1][f].id == Piece.EMPTY\
                    and board[r+1][f].id == Piece.EMPTY\
                    and not Piece.inCheckAfterMove((r, f), (r+2, f),
                                                   whiteToMove):
                valid.add((r+2, f))
            # captures
            if board[r+1][f+1].id >= Piece.HOPLITE\
                    and not Piece.inCheckAfterMove((r, f), (r+1, f+1),
                                                   whiteToMove):
                valid.add((r+1, f+1))
            if board[r+1][f-1].id >= Piece.HOPLITE\
                    and not Piece.inCheckAfterMove((r, f), (r+1, f-1),
                                                   whiteToMove):
                valid.add((r+1, f-1))
            return valid
