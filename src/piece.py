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

    # TODO: icon stuff

    ###########
    # METHODS #
    ###########
    def draw(self, surface: pygame.Surface):
        """
        Draw self to given surface.

        Parameters
        ---
        surface: pygame.Surface to draw on

        Returns
        ---
        None
        """
        # TODO: actually draw image
        # surface.blit(self.image, self.rect)
        # test: draw a circle
        # pygame.draw.circle(surface,
        #                    (127, 127, 127),
        #                    (self.pieceRank * 100, self.pieceFile * 100),
        #                    50)
        # self.pieceRank += 0.001
