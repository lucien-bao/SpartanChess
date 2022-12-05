#!usr/bin/env python3
"""The pieces for SpartanChess."""

__author__ = "Chris Bao"
__version__ = "0.9"
__date__ = "19 Nov 2022"

from tkinter import Canvas
from PIL import ImageTk


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

    ICON_FILE_MAP: dict[int, str] = {
        PAWN: "pawn.png",
        KNIGHT: "knight.png",
        BISHOP: "bishop.png",
        ROOK: "rook.png",
        QUEEN: "queen.png",
        PKING: "pking.png",

        HOPLITE: "hoplite.png",
        LIEUTENANT: "lieutenant.png",
        CAPTAIN: "captain.png",
        GENERAL: "general.png",
        WARLORD: "warlord.png",
        SKING: "sking.png",
    }

    # icon (piece) sizes, px
    ICON_SIZES: tuple[int] = (40, 55, 70, 85, 100)
    TINY = 0
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    HUGE = 4

    # static variables
    icons: list[dict[int, ImageTk.PhotoImage]] = []

    # instance variables
    id: int
    # rank and file
    rPos: int
    fPos: int

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
        self.rPos = r
        self.fPos = f

    def loadIcons():
        """
        Loads the images for the pieces into memory.

        Parameters
        ---
        (no parameters)

        Returns
        ---
        None
        """
        # TODO: load icons of different sizes
        for i in range(len(Piece.ICON_SIZES)):
            iconDict = {}
            # Persian (white) pieces
            for j in range(0, 6):
                filePath = "img/" + str(i) + "/" + Piece.ICON_FILE_MAP[j]
                iconDict[j] = ImageTk.PhotoImage(file=filePath)
            # Spartan (black) pieces
            for j in range(10, 16):
                filePath = "img/" + str(i) + "/" + Piece.ICON_FILE_MAP[j]
                iconDict[j] = ImageTk.PhotoImage(file=filePath)
            Piece.icons.append(iconDict)

    def draw(self, canvas: Canvas, iconSize: int,
             forceX: int = None, forceY: int = None) -> None:
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

        icon = Piece.icons[iconSize][self.id]
        if forceX is None:
            canvas.create_image(canvas.size * self.fPos // 8,
                                canvas.size * (7-self.rPos) // 8,
                                anchor="nw", image=icon)
        else:
            canvas.create_image(forceX, forceY, anchor="center", image=icon)
        canvas.imageList.append(icon)

    def inCheckAfterMove(start: tuple[int, int], end: tuple[int, int],
                         whiteToMove: bool) -> int:
        """
        Finds the number of kings exposed to check after the proposed move.
        Parameters
        ---
        start: tuple[int, int] starting rank and file
        end: tuple[int, int] ending rank and file
        whiteToMove: bool

        Returns
        ---
        int: number of kings in check after the move
        """
        # TODO: implement check detection
        return 1

    def findLegalMoves(r: int, f: int, board: list[list], whiteToMove: bool,
                       whiteShort: bool, whiteLong: bool, blackShort: bool,
                       blackLong: bool) -> set[tuple[int, int]]:
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
        blackShort: bool Black short castle privilege
        blackLong: bool Black long castle privilege

        Returns
        ---
        set[tuple[int, int]]: set of valid (rank, file) tuples
        """
        return True
        # TODO: implement finding legal moves for all pieces
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
