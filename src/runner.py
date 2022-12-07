#!usr/bin/env python3
"""SpartanChess: a Python GUI to play the Spartan chess variant against a friend."""

__author__ = "Chris Bao"
__version__ = "0.9"

# EXTERNAL IMPORTS
import sys
import pygame
from pygame.locals import *

# INTERNAL IMPORTS
from board import Board
from piece import Piece

#############
# CONSTANTS #
#############
FPS: int = 60
WIDTH: int = 1600
HEIGHT: int = 900
DARK_BG_COLOR: tuple[int, int, int] = (28, 28, 28)

#########
# SETUP #
#########
pygame.init()
pygame.display.set_caption("SpartanChess")

displaySurface = pygame.display.set_mode((WIDTH, HEIGHT))
displayClock = pygame.time.Clock()
displayClock.tick(FPS)

board = Board()
Piece.loadIcons()

pygame.display.set_icon(Piece.icons[Piece.KNIGHT])

############
# MAINLOOP #
############
while True:
    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            board.mousePressed()
        if event.type == MOUSEBUTTONUP and event.button == 1:
            board.mouseReleased()

    # draw screen
    displaySurface.fill(DARK_BG_COLOR)
    board.draw(displaySurface)

    pygame.display.update()
