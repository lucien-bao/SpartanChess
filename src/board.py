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
    X_OFFSET: int = 440
    """displacement between board and left side of window"""
    Y_OFFSET: int = 90
    """displacement between board and top of window"""
    LIGHT_SQUARE_COLOR: tuple[int, int, int] = (255, 187, 255)
    DARK_SQUARE_COLOR: tuple[int, int, int] = (183, 95, 191)

    ######################
    # INSTANCE VARIABLES #
    ######################
    grid: list[list[Piece]]
    draggedR: int
    draggedF: int

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
        # note that this is in the opposite order of how it's
        # displayed on the screen
        self.grid.append([Piece(Piece.ROOK, 0, 0),
                          Piece(Piece.KNIGHT, 0, 1),
                          Piece(Piece.BISHOP, 0, 2),
                          Piece(Piece.QUEEN, 0, 3),
                          Piece(Piece.PKING, 0, 4),
                          Piece(Piece.BISHOP, 0, 5),
                          Piece(Piece.KNIGHT, 0, 6),
                          Piece(Piece.ROOK, 0, 7)])
        self.grid.append([Piece(Piece.PAWN, 1, i) for i in range(8)])
        for i in range(4):
            self.grid.append([Piece(Piece.EMPTY, i, j) for j in range(8)])
        self.grid.append([Piece(Piece.HOPLITE, 6, i) for i in range(8)])
        self.grid.append([Piece(Piece.LIEUTENANT, 7, 0),
                          Piece(Piece.GENERAL, 7, 1),
                          Piece(Piece.SKING, 7, 2),
                          Piece(Piece.CAPTAIN, 7, 3),
                          Piece(Piece.CAPTAIN, 7, 4),
                          Piece(Piece.SKING, 7, 5),
                          Piece(Piece.WARLORD, 7, 6),
                          Piece(Piece.LIEUTENANT, 7, 7)])

        self.draggedF = self.draggedR = -1

        Board.moveSound = pygame.mixer.Sound("../sound/move.wav")
        Board.captureSound = pygame.mixer.Sound("../sound/capture.wav")
        Board.lowTimeSound = pygame.mixer.Sound("../sound/lowTime.wav")
        Board.gameEndSound = pygame.mixer.Sound("../sound/gameEnd.wav")

    ###########
    # METHODS #
    ###########
    def draw(self, surface: pygame.Surface) -> None:
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
                rect = pygame.Rect(Board.X_OFFSET + file * Piece.SIZE,
                                   Board.Y_OFFSET + (7-rank) * Piece.SIZE,
                                   Piece.SIZE,
                                   Piece.SIZE)
                pygame.draw.rect(surface,
                                 color,
                                 rect)

                # draw piece (if not being dragged)
                if rank != self.draggedR or file != self.draggedF:
                    self.grid[rank][file].draw(surface)

        if self.draggedR != -1 and self.draggedF != -1:
            mouseX, mouseY = pygame.mouse.get_pos()
            self.grid[self.draggedR][self.draggedF].draw(surface,
                                                         mouseX, mouseY)

    def mousePressed(self) -> None:
        """
        Handle mouse-press events. Manages movement of pieces.

        Parameters
        ---
        (no parameters)

        Returns
        ---
        None
        """
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseX -= Board.X_OFFSET
        mouseY -= Board.Y_OFFSET
        self.draggedR = 7 - int(mouseY / Piece.SIZE)
        self.draggedF = int(mouseX / Piece.SIZE)

    def mouseReleased(self) -> None:
        """
        Handle mouse-release events. Manages movement of pieces.

        Parameters
        ---
        (no parameters)

        Returns
        ---
        None
        """
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseX -= Board.X_OFFSET
        mouseY -= Board.Y_OFFSET
        targetR = 7 - int(mouseY / Piece.SIZE)
        targetF = int(mouseX / Piece.SIZE)

        # no piece selected
        if self.draggedR == -1 or self.draggedF == -1:
            return
        if self.grid[self.draggedR][self.draggedF].pieceId == Piece.EMPTY:
            self.draggedR = self.draggedF = -1
            return

        # selected and target square are the same
        if self.draggedR == targetR and self.draggedF == targetF:
            self.draggedR = self.draggedF = -1
            return

        self.attemptMove(self.draggedR, self.draggedF, targetR, targetF)
        self.draggedR = self.draggedF = -1

    def attemptMove(self, startR: int, startF: int,
                    destR: int, destF: int) -> None:
        """
        Attempts to move the selected piece to the target square.

        Parameters
        ---
        startR: int rank of piece to move
        startF: int file of piece to move
        destR: int rank of square to move to
        destF: int file of square to move to

        Returns
        ---
        None
        """
        # TODO: check for valid moves
        if self.grid[destR][destF].pieceId == Piece.EMPTY:
            print("play move")
            Board.moveSound.play()
        else:
            Board.captureSound.play()
        self.grid[destR][destF] = self.grid[startR][startF]
        self.grid[destR][destF].pieceRank = destR
        self.grid[destR][destF].pieceFile = destF
        self.grid[startR][startF] = Piece(Piece.EMPTY,
                                          startR,
                                          startF)