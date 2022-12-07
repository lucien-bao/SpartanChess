#!usr/bin/env python3
"""The pieces for SpartanChess."""

__author__ = "Chris Bao"
__version__ = "0.9"

# IMPORTS
import pygame


class Piece:
    #############
    # CONSTANTS #
    #############
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

    ######################
    # STATIC VARIABLES #
    ######################
    icons: dict[int, pygame.Surface] = {}

    ######################
    # INSTANCE VARIABLES #
    ######################
    pieceId: int
    pieceRank: int
    pieceFile: int

    ###############
    # CONSTRUCTOR #
    ###############
    def __init__(self, id: int, rank: int, file: int) -> None:
        """
        Constructor.

        Parameters
        ---
        id: int piece type id number
        rank: int
        file: int
        """
        self.pieceId = id
        self.pieceRank = rank
        self.pieceFile = file

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
            surface.blit(Piece.icons[self.pieceId],
                         (Piece.X_OFFSET + Piece.SIZE * self.pieceFile,
                         Piece.Y_OFFSET + Piece.SIZE * (7-self.pieceRank)))
        else:
            surface.blit(Piece.icons[self.pieceId],
                         (forceX - Piece.SIZE/2, forceY - Piece.SIZE/2))
