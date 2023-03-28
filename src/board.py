#!usr/bin/env python3
"""The chess board for SpartanChess. Note that board indices follow
ranks 1 to 8 and files a to h."""

__author__ = "Chris Bao"
__version__ = "1.0"

# EXTERNAL IMPORTS
from math import floor
import pygame
from pygame import gfxdraw

# INTERNAL IMPORTS
from piece import Piece
from ui import UI
import moverules as mr

# DEBUG SWITCH
_ATTACK_DEBUG: bool = False


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
    LAST_MOVE_COLOR: tuple[int, int, int] = (128, 40, 136)
    HIGHLIGHT_COLOR: tuple[int, int, int] = (95, 7, 95)
    DEBUG_COLOR: tuple[int, int, int] = (255, 255, 0)

    ONGOING: int = 0
    CHECKMATE: int = 1
    STALEMATE: int = 2

    MOVED_EVENT: int = pygame.USEREVENT + 10
    CAPTURE_EVENT: int = pygame.USEREVENT + 11
    WHITE_CHECKMATE_EVENT: int = pygame.USEREVENT + 12
    BLACK_CHECKMATE_EVENT: int = pygame.USEREVENT + 13
    STALEMATE_EVENT: int = pygame.USEREVENT + 14

    ######################
    # INSTANCE VARIABLES #
    ######################
    grid: list[list[Piece]]
    draggedR: int
    draggedF: int
    whiteToMove: bool
    castleShortRight: bool
    castleLongRight: bool

    promoting: int  # either Piece.WHITE, Piece.BLACK, or Piece.EMPTY
    promotionFile: int
    promotionOriginalPosition: tuple[int, int]
    blackKingCount: int

    lastStartR: int
    lastStartF: int
    lastDestR: int
    lastDestF: int

    moveSound: pygame.mixer.Sound
    captureSound: pygame.mixer.Sound
    lowTimeSound: pygame.mixer.Sound
    errorSound: pygame.mixer.Sound
    gameEndSound: pygame.mixer.Sound

    ###############
    # CONSTRUCTOR #
    ###############
    def __init__(self) -> None:
        """
        Constructor.
        Parameters
        ---
        ui: UI the external UI that should be updated by this board.

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
        self.promoting = Piece.EMPTY
        self.promotionFile = -1
        self.promotionOriginalPosition = (-1, -1)
        self.blackKingCount = 2
        self.lastStartR = None
        self.lastStartF = None
        self.lastDestR = None
        self.lastDestF = None

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
        self.drawStatic(surface)

        if self.draggedR != -1 and self.draggedF != -1:
            self.drawMoving(surface)

        # draw promotion menu
        if self.promoting == Piece.WHITE:
            # draw menu column
            rect = pygame.Rect(Board.X_OFFSET + self.promotionFile * Piece.SIZE,
                               Board.Y_OFFSET,
                               Piece.SIZE,
                               Piece.SIZE * 4.5)
            pygame.draw.rect(surface,
                             Board.HIGHLIGHT_COLOR,
                             rect)
            # create piece icons
            icons = [Piece(Piece.QUEEN, 7, self.promotionFile),
                     Piece(Piece.KNIGHT, 6, self.promotionFile),
                     Piece(Piece.ROOK, 5, self.promotionFile),
                     Piece(Piece.BISHOP, 4, self.promotionFile)]
            for icon in icons:
                icon.draw(surface)
            # draw cancel 'x' button
            top_left = (Board.X_OFFSET + (self.promotionFile + 0.4) * Piece.SIZE,
                        Board.Y_OFFSET + 4.15 * Piece.SIZE)
            bottom_right = (Board.X_OFFSET + (self.promotionFile + 0.6) * Piece.SIZE,
                            Board.Y_OFFSET + 4.35 * Piece.SIZE)
            top_right = (Board.X_OFFSET + (self.promotionFile + 0.6) * Piece.SIZE,
                         Board.Y_OFFSET + 4.15 * Piece.SIZE)
            bottom_left = (Board.X_OFFSET + (self.promotionFile + 0.4) * Piece.SIZE,
                           Board.Y_OFFSET + 4.35 * Piece.SIZE)
            pygame.draw.line(surface, Board.LIGHT_SQUARE_COLOR,
                             top_left, bottom_right, width=3)
            pygame.draw.line(surface, Board.LIGHT_SQUARE_COLOR,
                             top_right, bottom_left, width=3)
        elif self.promoting == Piece.BLACK:
            # draw menu column
            # note that Black can promote to king if has only one
            rect = pygame.Rect(Board.X_OFFSET + self.promotionFile * Piece.SIZE,
                               Board.Y_OFFSET + Piece.SIZE *
                               (3.5 if self.blackKingCount == 2 else 2.5),
                               Piece.SIZE,
                               Piece.SIZE * (4.5 if self.blackKingCount == 2 else 5.5))
            pygame.draw.rect(surface,
                             Board.HIGHLIGHT_COLOR,
                             rect)
            # create piece icons
            icons = [Piece(Piece.LIEUTENANT, 3, self.promotionFile),
                     Piece(Piece.CAPTAIN, 2, self.promotionFile),
                     Piece(Piece.WARLORD, 1, self.promotionFile),
                     Piece(Piece.GENERAL, 0, self.promotionFile)]
            if self.blackKingCount < 2:
                icons.append(Piece(Piece.SKING, 4, self.promotionFile))
            for icon in icons:
                icon.draw(surface)
            # draw cancel 'x' button
            top_left = (Board.X_OFFSET + (self.promotionFile + 0.4) * Piece.SIZE,
                        Board.Y_OFFSET + Piece.SIZE * (3.65 if self.blackKingCount == 2 else 2.65))
            bottom_right = (Board.X_OFFSET + (self.promotionFile + 0.6) * Piece.SIZE,
                            Board.Y_OFFSET + Piece.SIZE * (3.85 if self.blackKingCount == 2 else 2.85))
            top_right = (Board.X_OFFSET + (self.promotionFile + 0.6) * Piece.SIZE,
                         Board.Y_OFFSET + Piece.SIZE * (3.65 if self.blackKingCount == 2 else 2.65))
            bottom_left = (Board.X_OFFSET + (self.promotionFile + 0.4) * Piece.SIZE,
                           Board.Y_OFFSET + Piece.SIZE * (3.85 if self.blackKingCount == 2 else 2.85))
            pygame.draw.line(surface, Board.LIGHT_SQUARE_COLOR,
                             top_left, bottom_right, width=3)
            pygame.draw.line(surface, Board.LIGHT_SQUARE_COLOR,
                             top_right, bottom_left, width=3)

        # show squares attacked by opponent; for debug purposes
        if _ATTACK_DEBUG:
            attacked = mr.findAttackedSquares(self.grid, not self.whiteToMove)
            for rank in range(8):
                for file in range(8):
                    if attacked[rank, file]:
                        squareCenter = (int(Board.X_OFFSET + (file + 0.5) * Piece.SIZE),
                                        int(Board.Y_OFFSET + (7 - rank + 0.5) * Piece.SIZE))
                        pygame.draw.circle(surface, Board.DEBUG_COLOR,
                                           squareCenter, Piece.SIZE / 6.5)

    def drawStatic(self, surface: pygame.Surface) -> None:
        """
        Draw the board and static pieces (those not being moved) to the
        given surface. Also draws the highlight on the target square (if valid)
        when dragging.

        Parameters
        ---
        surface: pygame.Surface to draw on

        Returns
        ---
        None
        """
        for rank in range(8):
            for file in range(8):
                # light vs. dark square colors
                color = Board.LIGHT_SQUARE_COLOR if (rank+file) % 2 == 1\
                    else Board.DARK_SQUARE_COLOR

                if self.lastStartR is not None:
                    if rank == self.lastStartR and file == self.lastStartF or\
                            rank == self.lastDestR and file == self.lastDestF:
                        color = Board.LAST_MOVE_COLOR

                # change color to highlight if targeted square
                # and is a valid move
                if self.draggedR != -1 and self.draggedF != -1:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    mouseX -= Board.X_OFFSET
                    mouseY -= Board.Y_OFFSET
                    targetR = 7 - floor(mouseY / Piece.SIZE)
                    targetF = floor(mouseX / Piece.SIZE)
                    valid = Board.findValidMoves(self.grid, self.draggedR, self.draggedF,
                                                 self.castleShortRight, self.castleLongRight,
                                                 self.blackKingCount)
                    if rank == targetR and file == targetF and valid[rank][file]:
                        color = Board.HIGHLIGHT_COLOR

                # draw square
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

    def drawMoving(self, surface: pygame.Surface) -> None:
        """
        Draw moving piece and highlights/indicators to the given surface.

        Parameters
        ---
        surface: pygame.Surface

        Returns
        ---
        None
        """
        # draw valid move indicators
        valid = Board.findValidMoves(self.grid, self.draggedR, self.draggedF,
                                     self.castleShortRight, self.castleLongRight,
                                     self.blackKingCount)
        for rank in range(8):
            for file in range(8):
                # valid capture -> square outline
                if valid is not None and (valid[rank][file] == mr.CAPTURE
                                          or valid[rank][file] == mr.PROMOTE_CAPTURE):
                    rect = pygame.Rect(Board.X_OFFSET + file * Piece.SIZE,
                                       Board.Y_OFFSET +
                                       (7-rank) * Piece.SIZE,
                                       Piece.SIZE,
                                       Piece.SIZE)
                    pygame.draw.rect(surface, Board.HIGHLIGHT_COLOR,
                                     rect, width=Piece.SIZE // 12)
                # valid move -> dot
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
        Handle mouse-press events. Manages movement of pieces and promotion.

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

        # out of bounds
        if self.draggedR < 0 or self.draggedR > 7\
                or self.draggedF < 0 or self.draggedF > 7:
            self.draggedR = self.draggedF = -1
            return

        # if piece is wrong color, don't allow move
        if self.promoting == Piece.WHITE:
            # check for piece selection
            if self.draggedF == self.promotionFile and\
                    5 <= self.draggedR < 8:
                # add piece at promotion square depending on menu choice
                match(self.draggedR):
                    case 7:
                        self.grid[7][self.promotionFile] = Piece(
                            Piece.QUEEN, 7, self.promotionFile)
                    case 6:
                        self.grid[7][self.promotionFile] = Piece(
                            Piece.KNIGHT, 7, self.promotionFile)
                    case 5:
                        self.grid[7][self.promotionFile] = Piece(
                            Piece.ROOK, 7, self.promotionFile)
                    case 4:
                        self.grid[7][self.promotionFile] = Piece(
                            Piece.BISHOP, 7, self.promotionFile)
                self.promoting = Piece.EMPTY
                self.promotionFile = -1
                self.promotionOriginalPosition = (-1, -1)
                # stop dragging; prevents minor highlight
                # glitch when promoting to queen
                self.draggedF = self.draggedR = -1
                return
            # if click on board otherwise, cancel promotion
            elif 0 <= self.draggedF < 8 and\
                    0 <= self.draggedR < 8:
                # add back pawn
                r, f = self.promotionOriginalPosition
                self.grid[r][f] = Piece(Piece.PAWN, r, f)
                self.promoting = Piece.EMPTY
                self.promotionFile = -1
                self.promotionOriginalPosition = (-1, -1)
                # stop dragging; allows for normal new piece selection
                self.draggedF = self.draggedR = -1
        elif self.promoting == Piece.BLACK:
            # check for piece selection
            if self.draggedF == self.promotionFile and\
                    0 <= self.draggedR < (4 if self.blackKingCount == 2 else 5):
                # add piece at promotion square depending on menu choice
                match(self.draggedR):
                    case 0:
                        self.grid[0][self.promotionFile] = Piece(
                            Piece.GENERAL, 0, self.promotionFile)
                    case 1:
                        self.grid[0][self.promotionFile] = Piece(
                            Piece.WARLORD, 0, self.promotionFile)
                    case 2:
                        self.grid[0][self.promotionFile] = Piece(
                            Piece.CAPTAIN, 0, self.promotionFile)
                    case 3:
                        self.grid[0][self.promotionFile] = Piece(
                            Piece.LIEUTENANT, 0, self.promotionFile)
                    case 4:
                        self.grid[0][self.promotionFile] = Piece(
                            Piece.SKING, 0, self.promotionFile)
                self.promoting = Piece.EMPTY
                self.promotionFile = -1
                self.promotionOriginalPosition = (-1, -1)
                # stop dragging; prevents minor highlight
                # glitch when promoting to queen
                self.draggedF = self.draggedR = -1
                return
            # if click on board otherwise, cancel promotion
            elif 0 <= self.draggedF < 8 and\
                    0 <= self.draggedR < 8:
                # add back pawn
                r, f = self.promotionOriginalPosition
                self.grid[r][f] = Piece(Piece.PAWN, r, f)
                self.promoting = Piece.EMPTY
                self.promotionFile = -1
                self.promotionOriginalPosition = (-1, -1)
                # stop dragging; allows for normal new piece selection
                self.draggedF = self.draggedR = -1

        else:  # self.promoting == Piece.EMPTY (normal moves)
            if (self.grid[self.draggedR][self.draggedF].pieceColor == Piece.WHITE)\
                    != self.whiteToMove:
                self.draggedR = self.draggedF = -1

    def mouseReleased(self) -> None:
        """
        Handle mouse-release events. Manages movement of pieces and promotion.

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
        moveCode = Board.checkValidMove(self.grid, startR, startF, destR, destF,
                                        self.whiteToMove, self.castleShortRight,
                                        self.castleLongRight, self.blackKingCount)
        match moveCode:
            case mr.ILLEGAL:
                Board.errorSound.play()
                return
            case mr.MOVE:
                # update castling rights
                if (startR, startF) == (0, 4):
                    # king has moved
                    self.castleLongRight = self.castleShortRight = False
                if (startR, startF) == (0, 0) or (destR, destF) == (0, 0):
                    # rook has moved or has been captured
                    self.castleLongRight = False
                if (startR, startF) == (0, 7) or (destR, destF) == (0, 7):
                    # rook has moved or has been captured
                    self.castleShortRight = False

                # play sound effect
                Board.moveSound.play()

                # update board
                self.grid[destR][destF] = self.grid[startR][startF]
                self.grid[destR][destF].pieceRank = destR
                self.grid[destR][destF].pieceFile = destF
                self.grid[startR][startF] = Piece(Piece.EMPTY,
                                                  startR,
                                                  startF)
            case mr.CAPTURE:
                # communicate the captured piece so that the UI can update
                pygame.event.post(pygame.event.Event(
                    Board.CAPTURE_EVENT, pieceType=self.grid[destR][destF].pieceId))

                # update castling rights
                if (startR, startF) == (0, 4):
                    # king has moved
                    self.castleLongRight = self.castleShortRight = False
                if (startR, startF) == (0, 0) or (destR, destF) == (0, 0):
                    # rook has moved or has been captured
                    self.castleLongRight = False
                if (startR, startF) == (0, 7) or (destR, destF) == (0, 7):
                    # rook has moved or has been captured
                    self.castleShortRight = False

                # update Spartan king count if one is captured
                if self.grid[destR][destF].pieceId == Piece.SKING:
                    self.blackKingCount -= 1

                # play sound effect
                Board.captureSound.play()

                # update board
                self.grid[destR][destF] = self.grid[startR][startF]
                self.grid[destR][destF].pieceRank = destR
                self.grid[destR][destF].pieceFile = destF
                self.grid[startR][startF] = Piece(Piece.EMPTY,
                                                  startR,
                                                  startF)
            case mr.CASTLE:
                # play sound effect
                Board.moveSound.play()

                # castle short
                if destF in (6, 7):
                    # move king
                    self.grid[0][6] = self.grid[0][4]
                    self.grid[0][6].pieceFile = 6
                    # clear old king
                    self.grid[0][4] = Piece(Piece.EMPTY, 0, 4)
                    # move rook
                    self.grid[0][5] = self.grid[0][7]
                    self.grid[0][5].pieceFile = 5
                    # clear old rook
                    self.grid[0][7] = Piece(Piece.EMPTY, 0, 7)
                # castle long
                else:
                    # move king
                    self.grid[0][2] = self.grid[0][4]
                    self.grid[0][2].pieceFile = 2
                    # clear old king
                    self.grid[0][4] = Piece(Piece.EMPTY, 0, 4)
                    # move rook
                    self.grid[0][3] = self.grid[0][0]
                    self.grid[0][3].pieceFile = 3
                    # clear old rook
                    self.grid[0][0] = Piece(Piece.EMPTY, 0, 0)
                pass
            case mr.PROMOTE:
                # delete pawn
                self.grid[startR][startF] = Piece(Piece.EMPTY, startR, startF)
                # promote pawn
                if destR == 7:
                    self.promoting = Piece.WHITE
                # promote hoplite
                else:
                    self.promoting = Piece.BLACK
                self.promotionFile = destF
                self.promotionOriginalPosition = (startR, startF)

                # play sound effect
                Board.moveSound.play()
            case mr.PROMOTE_CAPTURE:
                # delete pawn
                self.grid[startR][startF] = Piece(Piece.EMPTY, startR, startF)
                # promote pawn
                if destR == 7:
                    self.promoting = Piece.WHITE
                # promote hoplite
                else:
                    self.promoting = Piece.BLACK
                self.promotionFile = destF
                self.promotionOriginalPosition = (startR, startF)

                # play sound effect
                Board.captureSound.play()

        self.lastStartR = startR
        self.lastStartF = startF
        self.lastDestR = destR
        self.lastDestF = destF

        # switch who is to move
        self.whiteToMove = not self.whiteToMove
        pygame.event.post(pygame.event.Event(Board.MOVED_EVENT))

        # check for game end condition
        gameOverState = self.checkGameOver()
        match gameOverState:
            case Board.ONGOING:
                return
            case Board.CHECKMATE:
                if self.whiteToMove:
                    pygame.event.post(pygame.event.Event(
                        Board.WHITE_CHECKMATE_EVENT))
                else:
                    pygame.event.post(pygame.event.Event(
                        Board.BLACK_CHECKMATE_EVENT))
            case Board.STALEMATE:
                pygame.event.post(pygame.event.Event(Board.STALEMATE_EVENT))
        self.gameEndSound.play()

    def checkGameOver(self) -> int:
        """
        Checks for game-ending conditions.

        Parameters
        ---
        (no parameters)

        Returns
        ---
        int: 0 if game not over, 1 if checkmate, 2 if stalemate
        """
        # check all possible moves
        for rank0 in range(8):
            for file0 in range(8):
                if self.grid[rank0][file0].pieceColor == Piece.WHITE and not self.whiteToMove\
                        or self.grid[rank0][file0].pieceColor == Piece.BLACK and self.whiteToMove:
                    continue
                for rank1 in range(8):
                    for file1 in range(8):
                        if Board.checkValidMove(self.grid, rank0, file0, rank1, file1,
                                                self.whiteToMove, self.castleShortRight,
                                                self.castleLongRight, self.blackKingCount):
                            return 0
        # no valid moves, see if checkmate or stalemate
        if self.whiteToMove:
            attackedMatrix = mr.findAttackedSquares(self.grid, False)
            for rank in range(8):
                for file in range(8):
                    if self.grid[rank][file].pieceId == Piece.PKING and\
                            attackedMatrix[rank, file]:
                        return 1
        else:
            attackedMatrix = mr.findAttackedSquares(self.grid, True)
            numInCheck = 0
            for rank in range(8):
                for file in range(8):
                    if self.grid[rank][file].pieceId == Piece.SKING and\
                            attackedMatrix[rank, file]:
                        numInCheck += 1
            if numInCheck == self.blackKingCount:
                return 1

        # not in check and no valid moves, stalemate
        return 2

    def checkValidMove(grid: list[list[Piece]], startR: int, startF: int,
                       destR: int, destF: int, whiteToMove: bool,
                       castleShort: bool, castleLong: bool, blackKingCount: int) -> int:
        """
        Checks if a given move is legal and returns a code specifying move type.

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
        blackKingCount: int number of Spartan kings left

        Returns
        ---
        int: the corresponding move code inside the module moverules. 0: illegal,
        1: move, 2: capture, 3: castle, 4: promotion, 5: promotion capture
        """
        # Make sure piece is correct color
        if grid[startR][startF].pieceColor == Piece.WHITE and not whiteToMove or\
                grid[startR][startF].pieceColor == Piece.BLACK and whiteToMove:
            return mr.ILLEGAL
        # Make sure we aren't moving into check
        gridCopy = Board.copyGrid(grid)
        gridCopy[destR][destF] = gridCopy[startR][startF]
        gridCopy[destR][destF].pieceRank = destR
        gridCopy[destR][destF].pieceFile = destF
        gridCopy[startR][startF] = Piece(Piece.EMPTY,
                                         startR,
                                         startF)
        attackedMatrix = mr.findAttackedSquares(gridCopy, not whiteToMove)
        if whiteToMove:
            for rank in range(8):
                for file in range(8):
                    if gridCopy[rank][file].pieceId == Piece.PKING and\
                            attackedMatrix[rank, file]:
                        return mr.ILLEGAL
        else:
            numInCheck = 0
            for rank in range(8):
                for file in range(8):
                    if gridCopy[rank][file].pieceId == Piece.SKING and\
                            attackedMatrix[rank, file]:
                        numInCheck += 1
            if numInCheck == blackKingCount:
                return mr.ILLEGAL

        # check if destination square is in the matrix of possible moves
        return Board.findValidMoves(grid, startR, startF,
                                    castleShort, castleLong,
                                    blackKingCount)[destR][destF]

    def copyGrid(grid: list[list[Piece]]) -> list[list[Piece]]:
        """
        Returns a copy of the given board state.

        Parameters
        ---
        grid: list[list[Piece]]

        Returns
        ---
        list[list[Piece]]
        """
        return [[Piece(grid[rank][file].pieceId, rank, file)
                 for file in range(8)] for rank in range(8)]

    def findValidMoves(grid: list[list[Piece]], rank: int, file: int,
                       castleShort: bool, castleLong: bool,
                       numSpartanKings: int) -> list[list[int]]:
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
        list[list[int]]: matrix of possible moves
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
                return mr.findSpartanKingMoves(grid, rank, file, numSpartanKings)

        # empty square, obviously no legal ways to move
        return [[mr.ILLEGAL]*8 for _ in range(8)]
