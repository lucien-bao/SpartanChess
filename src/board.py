#!usr/bin/env python3
"""The chess board for SpartanChess. Note that board indices follow
ranks 1 to 8 and files a to h."""

__author__ = "Chris Bao"
__version__ = "0.9"

# EXTERNAL IMPORTS
from math import floor
import pygame
from pygame import gfxdraw

# INTERNAL IMPORTS
from piece import Piece
import moverules as mr


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
    HIGHLIGHT_COLOR: tuple[int, int, int] = (115, 14, 125)

    ######################
    # INSTANCE VARIABLES #
    ######################
    grid: list[list[Piece]]
    draggedR: int
    draggedF: int
    whiteToMove: bool
    castleShortRight: bool
    castleLongRight: bool

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

        self.whiteToMove = True
        self.castleShortRight = self.castleLongRight = True
        self.draggedF = self.draggedR = -1

        Board.moveSound = pygame.mixer.Sound("../sound/move.wav")
        Board.captureSound = pygame.mixer.Sound("../sound/capture.wav")
        Board.errorSound = pygame.mixer.Sound("../sound/error.wav")
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

        # piece is selected
        if self.draggedR != -1 and self.draggedF != -1:
            # draw valid move indicators
            valid = Board.findValidMoves(self.grid, self.draggedR, self.draggedF,
                                         self.castleShortRight, self.castleLongRight)
            for rank in range(8):
                for file in range(8):
                    if valid is not None and valid[rank][file] == mr.CAPTURE:
                        rect = pygame.Rect(Board.X_OFFSET + file * Piece.SIZE,
                                           Board.Y_OFFSET +
                                           (7-rank) * Piece.SIZE,
                                           Piece.SIZE,
                                           Piece.SIZE)
                        pygame.draw.rect(surface, Board.HIGHLIGHT_COLOR,
                                         rect, width=Piece.SIZE // 12)
                    elif valid is not None and valid[rank][file] != mr.ILLEGAL:
                        squareCenter = (int(Board.X_OFFSET + (file + 0.5) * Piece.SIZE),
                                        int(Board.Y_OFFSET + (7 - rank + 0.5) * Piece.SIZE))

                        # smooth the edge
                        for i in range(3):
                            gfxdraw.aacircle(surface, squareCenter[0], squareCenter[1],
                                             int(Piece.SIZE / 6.5) - i, Board.HIGHLIGHT_COLOR)
                        pygame.draw.circle(surface, Board.HIGHLIGHT_COLOR,
                                           squareCenter, Piece.SIZE / 6.5)

            # draw dragged piece
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

        self.draggedR = 7 - floor(mouseY / Piece.SIZE)
        self.draggedF = floor(mouseX / Piece.SIZE)

        # if piece is wrong color, don't allow move
        if (self.grid[self.draggedR][self.draggedF].pieceColor == Piece.WHITE)\
                != self.whiteToMove:
            self.draggedR = self.draggedF = -1

        # out of bounds
        if self.draggedR < 0 or self.draggedR > 7\
                or self.draggedF < 0 or self.draggedF > 7:
            self.draggedR = self.draggedF = -1

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
        targetR = 7 - floor(mouseY / Piece.SIZE)
        targetF = floor(mouseX / Piece.SIZE)

        # no piece selected
        if self.draggedR == -1 or self.draggedF == -1:
            return
        # out of bounds
        if self.draggedR < 0 or self.draggedR > 7\
                or self.draggedF < 0 or self.draggedF > 7\
                or targetR < 0 or targetR > 7\
                or targetF < 0 or targetF > 7:
            self.draggedR = self.draggedF = -1
            return
        # empty square selected
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
        # TODO: handle promotion
        # check if valid move
        if not Board.isValidMove(self.grid, startR, startF, destR, destF,
                                 self.whiteToMove, self.castleShortRight,
                                 self.castleLongRight):
            Board.errorSound.play()
            return

        # update castling rights
        if (startR, startF) == (0, 4):
            self.castleLongRight = self.castleShortRight = False
        if (startR, startF) == (0, 0) or (destR, destF) == (0, 0):
            self.castleLongRight = False
        if (startR, startF) == (0, 7) or (destR, destF) == (0, 7):
            self.castleShortRight = False

        # play sound effect
        if self.grid[destR][destF].pieceId == Piece.EMPTY:
            Board.moveSound.play()
        else:
            Board.captureSound.play()

        # update board
        self.grid[destR][destF] = self.grid[startR][startF]
        self.grid[destR][destF].pieceRank = destR
        self.grid[destR][destF].pieceFile = destF
        self.grid[startR][startF] = Piece(Piece.EMPTY,
                                          startR,
                                          startF)
        self.whiteToMove = not self.whiteToMove

    def isValidMove(grid: list[list[Piece]], startR: int, startF: int,
                    destR: int, destF: int, whiteToMove: bool,
                    castleShort: bool, castleLong: bool) -> bool:
        """
        Checks if a given move is legal.

        Parameters
        ---
        grid: list[list[Piece]] matrix representing the board state
        startR: int starting rank of piece
        startF: int starting file of piece
        destR: int destination rank of piece
        destF: int destination file of piece
        whiteToMove: bool
        castleShort: bool whether White retains short castling rights
        castleLong: bool whether White retains long castling rights

        Returns
        ---
        bool
        """
        # TODO: take into account moving into check

        # check if destination square is in the matrix of possible moves
        return Board.findValidMoves(grid, startR, startF,
                                    castleShort, castleLong)[destR][destF]

    def findValidMoves(grid: list[list[Piece]], rank: int, file: int,
                       castleShort: bool, castleLong: bool) -> list[list[bool]]:
        """
        Find all legal moves for the given board and piece to move.

        Parameters
        ---
        grid: list[list[Piece]] board state
        rank: int
        file: int
        castleShort: bool whether White retains short castle rights
        castleLong: bool whether White retains long castle rights

        Returns
        ---
        list[list[bool]]: matrix of possible moves
        """
        match grid[rank][file].pieceId:
            case Piece.PAWN:
                return mr.findPawnMoves(grid, rank, file)
            case Piece.KNIGHT:
                return mr.findKnightMoves(grid, rank, file)
            case Piece.BISHOP:
                return mr.findBishopMoves(grid, rank, file)
            case Piece.ROOK:
                return mr.findRookMoves(grid, rank, file)
            case Piece.QUEEN:
                return mr.findQueenMoves(grid, rank, file)
            case Piece.PKING:
                return mr.findPersianKingMoves(grid, rank, file, castleShort, castleLong)

            case Piece.HOPLITE:
                return mr.findHopliteMoves(grid, rank, file)
            case Piece.LIEUTENANT:
                return mr.findLieutenantMoves(grid, rank, file)
            case Piece.CAPTAIN:
                return mr.findCaptainMoves(grid, rank, file)
            case Piece.GENERAL:
                return mr.findGeneralMoves(grid, rank, file)
            case Piece.WARLORD:
                return mr.findWarlordMoves(grid, rank, file)
            case Piece.SKING:
                return mr.findSpartanKingMoves(grid, rank, file)
