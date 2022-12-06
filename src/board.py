#!usr/bin/env python3
"""The chess board for SpartanChess. Note that board indices follow
ranks 1 to 8 and files a to h."""

__author__ = "Chris Bao"
__version__ = "0.9"

# EXTERNAL IMPORTS
import pygame

# INTERNAL IMPORTS
from piece import Piece


class Board:
    #############
    # CONSTANTS #
    #############
    SIZE: int = 720
    X_OFFSET: int = 440  # displacement between board and left side of window
    Y_OFFSET: int = 90  # same but for top of window
    LIGHT_SQUARE_COLOR: tuple[int, int, int] = (255, 187, 255)
    DARK_SQUARE_COLOR: tuple[int, int, int] = (183, 95, 191)

    ######################
    # INSTANCE VARIABLES #
    ######################
    grid: list[list[Piece]]

    ###############
    # CONSTRUCTOR #
    ###############
    def __init__(self) -> None:
        """
        Constructor.
        Parameters
        ---
        (no parameters)

        Returns
        ---
        None
        """
        self.grid = []
        for i in range(8):
            rank = []
            for j in range(8):
                rank.append(Piece(0, i, j))
            self.grid.append(rank)

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
        for rank in range(8):
            for file in range(8):
                # draw square
                color = Board.LIGHT_SQUARE_COLOR if (rank+file) % 2 == 1\
                    else Board.DARK_SQUARE_COLOR
                rect = pygame.Rect(Board.X_OFFSET + file * Board.SIZE / 8,
                                   Board.Y_OFFSET + (7-rank) * Board.SIZE / 8,
                                   Board.SIZE / 8,
                                   Board.SIZE / 8)
                pygame.draw.rect(surface,
                                 color,
                                 rect)

                # draw piece
                self.grid[rank][file].draw(surface)
