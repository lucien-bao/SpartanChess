#!usr/bin/env python3
"""The pieces for SpartanChess."""

__author__ = "Chris Bao"
__version__ = "1.0"

# IMPORTS
import pygame


class Piece:
    #############
    # CONSTANTS #
    #############
    EMPTY: int = -1
    WHITE: int = -2
    BLACK: int = -3

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

    X_OFFSET: int = 440
    """displacement between board and left side of window"""
    Y_OFFSET: int = 90
    """displacement between board and top of window"""

    SIZE: int = 90
    """size of piece icons and board squares"""

    ICON_FILE_MAP: dict[int, str] = {
        PAWN: "../img/pawn.png",
        KNIGHT: "../img/knight.png",
        BISHOP: "../img/bishop.png",
        ROOK: "../img/rook.png",
        QUEEN: "../img/queen.png",
        PKING: "../img/pking.png",

        HOPLITE: "../img/hoplite.png",
        LIEUTENANT: "../img/lieutenant.png",
        CAPTAIN: "../img/captain.png",
        GENERAL: "../img/general.png",
        WARLORD: "../img/warlord.png",
        SKING: "../img/sking.png",
    }

    SMALL_ICON_FILE_MAP: dict[int, str] = {
        PAWN: "../icon/pawn.png",
        KNIGHT: "../icon/knight.png",
        BISHOP: "../icon/bishop.png",
        ROOK: "../icon/rook.png",
        QUEEN: "../icon/queen.png",
        PKING: "../icon/pking.png",

        HOPLITE: "../icon/hoplite.png",
        LIEUTENANT: "../icon/lieutenant.png",
        CAPTAIN: "../icon/captain.png",
        GENERAL: "../icon/general.png",
        WARLORD: "../icon/warlord.png",
        SKING: "../icon/sking.png",
    }

    ######################
    # STATIC VARIABLES #
    ######################
    icons: dict[int, pygame.Surface] = {}
    smallIcons: dict[int, pygame.Surface] = {}

    ######################
    # INSTANCE VARIABLES #
    ######################
    pieceId: int
    pieceColor: bool
    pieceRank: int
    pieceFile: int
    smallIcon: bool

    ###############
    # CONSTRUCTOR #
    ###############
    def __init__(self, id: int, rank: int = 0, file: int = 0, smallIcon: bool = False) -> None:
        """
        Constructor.

        Parameters
        ---
        id: int piece type id number
        rank: int
        file: int
        """
        self.pieceId = id
        if id == Piece.EMPTY:
            self.pieceColor = Piece.EMPTY
        elif id < 10:
            self.pieceColor = Piece.WHITE
        else:
            self.pieceColor = Piece.BLACK
        self.pieceRank = rank
        self.pieceFile = file
        self.smallIcon = smallIcon

    ###########
    # METHODS #
    ###########
    def loadIcons() -> None:
        """
        Loads the images for the pieces into memory.

        Parameters
        ---
        (no parameters)

        Returns
        ---
        None
        """
        # Persian (white) pieces
        for i in range(0, 6):
            Piece.icons[i] = pygame.image.load(
                Piece.ICON_FILE_MAP[i]).convert_alpha()

        # Spartan (black) pieces
        for i in range(10, 16):
            Piece.icons[i] = pygame.image.load(
                Piece.ICON_FILE_MAP[i]).convert_alpha()

        # Small icons
        for i in range(0, 6):
            Piece.smallIcons[i] = pygame.image.load(
                Piece.SMALL_ICON_FILE_MAP[i]).convert_alpha()
        for i in range(10, 16):
            Piece.smallIcons[i] = pygame.image.load(
                Piece.SMALL_ICON_FILE_MAP[i]).convert_alpha()

    def draw(self, surface: pygame.Surface,
             forceX: int = None, forceY: int = None) -> None:
        """
        Draw self to given surface.

        Parameters
        ---
        surface: pygame.Surface to draw on
        forceX: int = None force x-position (center of icon)
        forceY: int = None force y-position (center of icon)

        Returns
        ---
        None
        """
        if self.pieceId == Piece.EMPTY:
            return

        if forceX is None or forceY is None:
            surface.blit(Piece.smallIcons[self.pieceId] if self.smallIcon else Piece.icons[self.pieceId],
                         (Piece.X_OFFSET + Piece.SIZE * self.pieceFile,
                         Piece.Y_OFFSET + Piece.SIZE * (7-self.pieceRank)))
        else:
            surface.blit(Piece.smallIcons[self.pieceId] if self.smallIcon else Piece.icons[self.pieceId],
                         (forceX - Piece.SIZE/(4 if self.smallIcon else 2),
                          forceY - Piece.SIZE/(4 if self.smallIcon else 2)))
