#!usr/bin/env python3
"""SpartanChess: a Python GUI to play the Spartan chess variant against a friend."""

import time
__author__ = "Chris Bao"
__version__ = "1.0"

# EXTERNAL IMPORTS
import sys
import pygame
from pygame.locals import *

# INTERNAL IMPORTS
from board import Board
from piece import Piece
from ui import UI

#############
# CONSTANTS #
#############
FPS: int = 60
WIDTH: int = 1600
HEIGHT: int = 900
DARK_BG_COLOR: tuple[int, int, int] = (28, 28, 28)

TICK_EVENT: int = USEREVENT + 1
WHITE_TIME_OUT_EVENT: int = pygame.USEREVENT + 2
BLACK_TIME_OUT_EVENT: int = pygame.USEREVENT + 3

#########
# SETUP #
#########
pygame.init()
pygame.display.set_caption("SpartanChess")

displaySurface = pygame.display.set_mode((WIDTH, HEIGHT))
displayClock = pygame.time.Clock()
displayClock.tick(FPS)

ui = UI()
board = Board()
Piece.loadIcons()

pygame.display.set_icon(Piece.icons[Piece.KNIGHT])

############
# MAINLOOP #
############
# number of moves by white or black
numPlies = 0
gameOngoing = True

while True:
    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if gameOngoing and event.type == MOUSEBUTTONDOWN and event.button == 1:
            board.mousePressed()
        if gameOngoing and event.type == MOUSEBUTTONUP and event.button == 1:
            board.mouseReleased()
        if gameOngoing and event.type == Board.MOVED_EVENT:
            numPlies += 1
            ui.whiteTimeGoing = not ui.whiteTimeGoing
            if numPlies == 2:
                # delay of 10 = 1000 ms/sec / 100 ticks per second
                pygame.time.set_timer(TICK_EVENT, 10)
        if gameOngoing and event.type == TICK_EVENT:
            if ui.whiteTimeGoing:
                ui.whiteTicksLeft -= 1
                # 30 seconds left
                if ui.whiteTicksLeft == 100 * 30:
                    board.lowTimeSound.play()
                if ui.whiteTicksLeft == 0:
                    pygame.event.post(pygame.event.Event(WHITE_TIME_OUT_EVENT))
            else:
                ui.blackTicksLeft -= 1
                # 30 seconds left
                if ui.blackTicksLeft == 100 * 30:
                    board.lowTimeSound.play()
                if ui.blackTicksLeft == 0:
                    pygame.event.pos(pygame.event.Event(BLACK_TIME_OUT_EVENT))
        if event.type == Board.CAPTURE_EVENT:
            # captured piece is white
            if event.pieceType < 10:
                ui.whiteCapturedPieces.append(event.pieceType)
                ui.whiteCapturedPieces = sorted(
                    ui.whiteCapturedPieces, reverse=True)
            # captured piece is black
            else:
                ui.blackCapturedPieces.append(event.pieceType)
                ui.blackCapturedPieces = sorted(
                    ui.blackCapturedPieces, reverse=True)
        if event.type == WHITE_TIME_OUT_EVENT:
            gameOngoing = False
            ui.gameOverMessage = "0–1 • Black wins on time"
        if event.type == BLACK_TIME_OUT_EVENT:
            gameOngoing = False
            ui.gameOverMessage = "1–0 • White wins on time"
        if event.type == Board.WHITE_CHECKMATE_EVENT:
            gameOngoing = False
            ui.gameOverMessage = "0–1 • Black wins by checkmate"
        if event.type == Board.BLACK_CHECKMATE_EVENT:
            gameOngoing = False
            ui.gameOverMessage = "1–0 • White wins by checkmate"
        if event.type == Board.STALEMATE_EVENT:
            gameOngoing = False
            ui.gameOverMessage = "½–½ • Draw by stalemate"

    # draw screen
    displaySurface.fill(DARK_BG_COLOR)
    board.draw(displaySurface)
    ui.draw(displaySurface)

    pygame.display.update()
