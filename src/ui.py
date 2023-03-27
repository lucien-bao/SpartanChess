#!usr/bin/env python3
"""The UI outside of the board for SpartanChess."""

__author__ = "Chris Bao"
__version__ = "1.0"

# EXTERNAL IMPORTS
import pygame
import pygame.freetype

# INTERNAL IMPORTS
from piece import Piece


class UI:
    #############
    # CONSTANTS #
    #############
    # 10 mins * 60 secs/min * 100 ticks/sec
    STARTING_TICKS: int = 10 * 60 * 100

    CLOCK_XPOS: int = 1230
    UPPER_CLOCK_YPOS: int = 270
    LOWER_CLOCK_YPOS: int = 540
    CLOCK_WIDTH: int = 300
    CLOCK_HEIGHT: int = 90

    UPPER_CLOCK_COLOR: tuple[int, int, int] = (115, 14, 125)  # (60, 60, 60)
    LOWER_CLOCK_COLOR: tuple[int, int, int] = (183, 95, 191)  # (100, 100, 100)

    CLOCK_TEXT_XPOS_MINUTES: int = 1240
    CLOCK_TEXT_XPOS_COLON: int = 1325
    CLOCK_TEXT_XPOS_SECONDS: int = 1340
    CLOCK_TEXT_XPOS_DOT: int = 1425
    CLOCK_TEXT_XPOS_TICKS: int = 1440
    UPPER_CLOCK_TEXT_YPOS: int = 290
    LOWER_CLOCK_TEXT_YPOS: int = 560

    MESSAGE_TEXT_XPOS: int = 920
    MESSAGE_TEXT_YPOS: int = 300

    CAPTURED_XPOS: int = 80
    WHITE_CAPTURED_YPOS: int = UPPER_CLOCK_YPOS + CLOCK_HEIGHT/2
    BLACK_CAPTURED_YPOS: int = LOWER_CLOCK_YPOS + CLOCK_HEIGHT/2

    TEXT_COLOR: tuple[int, int, int] = (255, 255, 255)

    ######################
    # INSTANCE VARIABLES #
    ######################
    # this chess clock is accurate to 10 ms (1/100 s)
    whiteTimeGoing: bool
    whiteTicksLeft: int
    blackTicksLeft: int

    clockFont: pygame.freetype.Font
    gameOverMessage: str

    # white and black denote piece color, not player
    whiteCapturedPieces: list[int]
    blackCapturedPieces: list[int]

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
        self.whiteTimeGoing = True
        self.whiteTicksLeft = UI.STARTING_TICKS
        self.blackTicksLeft = UI.STARTING_TICKS

        self.clockFont = pygame.freetype.Font("../font/robotoRegular.ttf", 72)
        self.messageFont = pygame.freetype.Font(
            "../font/robotoRegular.ttf", 20)
        self.gameOverMessage = None

        self.whiteCapturedPieces = []
        self.blackCapturedPieces = []

    ###########
    # METHODS #
    ###########
    def draw(self, surface: pygame.Surface):
        """
        Draw self to the given surface.

        Parameters
        ---
        surface: pygame.Surface

        Returns
        ---
        None
        """
        self.drawClocks(surface)

        self.drawCapturedPieces(surface)

        if self.gameOverMessage is not None:
            textRect = self.messageFont.get_rect(self.gameOverMessage, size=20)
            textRect.center = pygame.Rect(UI.MESSAGE_TEXT_XPOS, UI.MESSAGE_TEXT_YPOS,
                                          UI.MESSAGE_TEXT_XPOS, UI.MESSAGE_TEXT_YPOS).center
            self.clockFont.render_to(surface, textRect, self.gameOverMessage,
                                     UI.TEXT_COLOR, size=20)

    def drawCapturedPieces(self, surface: pygame.Surface):
        """
        Draw captured pieces.

        Parameters
        ---
        surface: pygame.Surface

        Returns
        ---
        None
        """
        # draw white captured pieces (pieces Black captured)
        xpos = UI.CAPTURED_XPOS
        for (i, id) in enumerate(self.whiteCapturedPieces):
            Piece(id, smallIcon=True).draw(
                surface, forceX=xpos, forceY=UI.WHITE_CAPTURED_YPOS)
            # if next piece is same, group them together
            if i < len(self.whiteCapturedPieces) - 1 and self.whiteCapturedPieces[i+1] == id:
                xpos += 15
            else:
                xpos += 40

        # draw black captured pieces (pieces White captured)
        xpos = UI.CAPTURED_XPOS
        for (i, id) in enumerate(self.blackCapturedPieces):
            Piece(id, smallIcon=True).draw(
                surface, forceX=xpos, forceY=UI.BLACK_CAPTURED_YPOS)
            # if next piece is same, group them together
            if i < len(self.blackCapturedPieces) - 1 and self.blackCapturedPieces[i+1] == id:
                xpos += 15
            else:
                xpos += 40

    def drawClocks(self, surface: pygame.Surface):
        """
        Draw the chess clocks to the given surface.

        Parameters
        ---
        surface: pygame.Surface

        Returns
        ---
        None
        """
        # draw upper clock (Black)
        upperClock = pygame.Rect(UI.CLOCK_XPOS,
                                 UI.UPPER_CLOCK_YPOS,
                                 UI.CLOCK_WIDTH,
                                 UI.CLOCK_HEIGHT)
        pygame.draw.rect(surface,
                         UI.UPPER_CLOCK_COLOR,
                         upperClock)
        # 100 ticks per second, 60 seconds per min
        minutes = str(int(self.blackTicksLeft / 100 / 60))
        seconds = str(int(self.blackTicksLeft / 100 % 60))
        ticks = str(int(self.blackTicksLeft % 100))
        self.clockFont.render_to(surface,
                                 (UI.CLOCK_TEXT_XPOS_MINUTES,
                                  UI.UPPER_CLOCK_TEXT_YPOS),
                                 minutes if len(minutes) == 2 else (
                                     "0" + minutes),
                                 UI.TEXT_COLOR)
        self.clockFont.render_to(surface,
                                 (UI.CLOCK_TEXT_XPOS_COLON,
                                  UI.UPPER_CLOCK_TEXT_YPOS + 10),
                                 ":",
                                 UI.TEXT_COLOR)
        self.clockFont.render_to(surface,
                                 (UI.CLOCK_TEXT_XPOS_SECONDS,
                                  UI.UPPER_CLOCK_TEXT_YPOS),
                                 seconds if len(seconds) == 2 else (
                                     "0" + seconds),
                                 UI.TEXT_COLOR)
        self.clockFont.render_to(surface,
                                 (UI.CLOCK_TEXT_XPOS_DOT,
                                  UI.UPPER_CLOCK_TEXT_YPOS + 42),
                                 ".",
                                 UI.TEXT_COLOR)
        self.clockFont.render_to(surface,
                                 (UI.CLOCK_TEXT_XPOS_TICKS,
                                  UI.UPPER_CLOCK_TEXT_YPOS),
                                 ticks if len(ticks) == 2 else ("0" + ticks),
                                 UI.TEXT_COLOR)

        # draw lower clock (White)
        lowerClock = pygame.Rect(UI.CLOCK_XPOS,
                                 UI.LOWER_CLOCK_YPOS,
                                 UI.CLOCK_WIDTH,
                                 UI.CLOCK_HEIGHT)
        pygame.draw.rect(surface,
                         UI.LOWER_CLOCK_COLOR,
                         lowerClock)
        # 100 ticks per second, 60 seconds per min
        minutes = str(int(self.whiteTicksLeft / 100 / 60))
        seconds = str(int(self.whiteTicksLeft / 100 % 60))
        ticks = str(int(self.whiteTicksLeft % 100))
        self.clockFont.render_to(surface,
                                 (UI.CLOCK_TEXT_XPOS_MINUTES,
                                  UI.LOWER_CLOCK_TEXT_YPOS),
                                 minutes if len(minutes) == 2 else (
                                     "0" + minutes),
                                 UI.TEXT_COLOR)
        self.clockFont.render_to(surface,
                                 (UI.CLOCK_TEXT_XPOS_COLON,
                                  UI.LOWER_CLOCK_TEXT_YPOS + 10),
                                 ":",
                                 UI.TEXT_COLOR)
        self.clockFont.render_to(surface,
                                 (UI.CLOCK_TEXT_XPOS_SECONDS,
                                  UI.LOWER_CLOCK_TEXT_YPOS),
                                 seconds if len(seconds) == 2 else (
                                     "0" + seconds),
                                 UI.TEXT_COLOR)
        self.clockFont.render_to(surface,
                                 (UI.CLOCK_TEXT_XPOS_DOT,
                                  UI.LOWER_CLOCK_TEXT_YPOS + 42),
                                 ".",
                                 UI.TEXT_COLOR)
        self.clockFont.render_to(surface,
                                 (UI.CLOCK_TEXT_XPOS_TICKS,
                                  UI.LOWER_CLOCK_TEXT_YPOS),
                                 ticks if len(ticks) == 2 else ("0" + ticks),
                                 UI.TEXT_COLOR)
