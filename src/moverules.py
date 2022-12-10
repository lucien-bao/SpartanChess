#!usr/bin/env python3
"""Functions encoding move rules for SpartanChess."""

__author__ = "Chris Bao"
__version__ = "0.9"

# IMPORTS
from piece import Piece


def findPawnMoves(grid: list[list[Piece]],
                  rank: int, file: int) -> list[list[bool]]:
    """
    Find all legal moves for a pawn at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    list[list[bool]]: matrix of possible moves
    """
    validMatrix = [[False]*8 for _ in range(8)]
    # normal single-step move
    if grid[rank+1][file].pieceId == Piece.EMPTY:
        validMatrix[rank+1][file] = True
        # starting double-step move
        if rank == 1 and grid[rank+2][file].pieceId == Piece.EMPTY:
            validMatrix[rank+2][file] = True
    # diagonal capture northwest
    if file != 0 and grid[rank+1][file-1].pieceColor == Piece.BLACK:
        validMatrix[rank+1][file-1] = True
    # diagonal capture northeast
    if file != 7 and grid[rank+1][file+1].pieceColor == Piece.BLACK:
        validMatrix[rank+1][file+1] = True
    return validMatrix


KNIGHT_R_OFFSETS: tuple[int] = (-2, -2, -1, -1, +1, +1, +2, +2)
KNIGHT_F_OFFSETS: tuple[int] = (-1, +1, -2, +2, -2, +2, -1, +1)


def findKnightMoves(grid: list[list[Piece]],
                    rank: int, file: int) -> list[list[bool]]:
    """
    Find all legal moves for a knight at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    list[list[bool]]: matrix of possible moves
    """
    validMatrix = [[False]*8 for _ in range(8)]
    for i in range(8):
        destRank = rank + KNIGHT_R_OFFSETS[i]
        destFile = file + KNIGHT_F_OFFSETS[i]
        if destRank < 0 or destRank > 7\
                or destFile < 0 or destFile > 7:
            continue
        if grid[destRank][destFile].pieceId == Piece.EMPTY\
                or grid[destRank][destFile].pieceColor == Piece.BLACK:
            validMatrix[destRank][destFile] = True

    return validMatrix


BISHOP_R_OFFSETS: tuple[int] = (-1, -1, +1, +1)
BISHOP_F_OFFSETS: tuple[int] = (-1, +1, -1, +1)


def findBishopMoves(grid: list[list[Piece]],
                    rank: int, file: int) -> list[list[bool]]:
    """
    Find all legal moves for a bishop at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    list[list[bool]]: matrix of possible moves
    """
    validMatrix = [[False]*8 for _ in range(8)]
    for direction in range(4):
        for step in range(1, 8):
            destRank = rank + step * BISHOP_R_OFFSETS[direction]
            destFile = file + step * BISHOP_F_OFFSETS[direction]
            # out of bounds, stop
            if destRank < 0 or destRank > 7\
                    or destFile < 0 or destFile > 7:
                break
            # piece of same color, stop
            if grid[destRank][destFile].pieceColor == Piece.WHITE:
                break
            validMatrix[destRank][destFile] = True
            # piece of opposing color, stop (but mark valid)
            if grid[destRank][destFile].pieceColor == Piece.BLACK:
                break

    return validMatrix


ROOK_R_OFFSETS: tuple[int] = (0, 0, +1, -1)
ROOK_F_OFFSETS: tuple[int] = (+1, -1, 0, 0)


def findRookMoves(grid: list[list[Piece]],
                  rank: int, file: int) -> list[list[bool]]:
    """
    Find all legal moves for a rook at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    list[list[bool]]: matrix of possible moves
    """
    validMatrix = [[False]*8 for _ in range(8)]
    for direction in range(4):
        for step in range(1, 8):
            destRank = rank + step * ROOK_R_OFFSETS[direction]
            destFile = file + step * ROOK_F_OFFSETS[direction]
            # out of bounds, stop
            if destRank < 0 or destRank > 7\
                    or destFile < 0 or destFile > 7:
                break
            # piece of same color, stop
            if grid[destRank][destFile].pieceColor == Piece.WHITE:
                break
            validMatrix[destRank][destFile] = True
            # piece of opposing color, stop (but mark valid)
            if grid[destRank][destFile].pieceColor == Piece.BLACK:
                break

    return validMatrix


# note that these are just the union of rook and bishop offset lists
QUEEN_R_OFFSETS: tuple[int] = (0, 0, +1, -1, -1, -1, +1, +1)
QUEEN_F_OFFSETS: tuple[int] = (+1, -1, 0, 0, -1, +1, -1, +1)


def findQueenMoves(grid: list[list[Piece]],
                   rank: int, file: int) -> list[list[bool]]:
    """
    Find all legal moves for a queen at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    list[list[bool]]: matrix of possible moves
    """
    validMatrix = [[False]*8 for _ in range(8)]
    for direction in range(8):
        for step in range(1, 8):
            destRank = rank + step * QUEEN_R_OFFSETS[direction]
            destFile = file + step * QUEEN_F_OFFSETS[direction]
            # out of bounds, stop
            if destRank < 0 or destRank > 7\
                    or destFile < 0 or destFile > 7:
                break
            # piece of same color, stop
            if grid[destRank][destFile].pieceColor == Piece.WHITE:
                break
            validMatrix[destRank][destFile] = True
            # piece of opposing color, stop (but mark valid)
            if grid[destRank][destFile].pieceColor == Piece.BLACK:
                break

    return validMatrix


# these are the same as the queen offsets
KING_R_OFFSETS: tuple[int] = (0, 0, +1, -1, -1, -1, +1, +1)
KING_F_OFFSETS: tuple[int] = (+1, -1, 0, 0, -1, +1, -1, +1)


def findKingMoves(grid: list[list[Piece]], rank: int, file: int,
                  castleShort: bool, castleLong: bool) -> list[list[bool]]:
    """
    Find all legal moves for a king at the given board, rank, and file.

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
    validMatrix = [[False]*8 for _ in range(8)]
    # normal directional moves
    for direction in range(8):
        destRank = rank + KING_R_OFFSETS[direction]
        destFile = file + KING_F_OFFSETS[direction]
        # out of bounds
        if destRank < 0 or destRank > 7\
                or destFile < 0 or destFile > 7:
            continue
        # piece of same color, invalid
        if grid[destRank][destFile].pieceColor == Piece.WHITE:
            continue
        validMatrix[destRank][destFile] = True

    # TODO: castling
    if castleShort:
        validMatrix[0][6] = validMatrix[0][7] = True
    if castleLong:
        validMatrix[0][2] = validMatrix[0][0] = True

    return validMatrix
