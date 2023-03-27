#!usr/bin/env python3
"""Functions encoding move rules for SpartanChess."""

__author__ = "Chris Bao"
__version__ = "1.0"

# IMPORTS
import numpy as np
from piece import Piece

# CONSTANTS
ILLEGAL: int = 0
MOVE: int = 1
CAPTURE: int = 2
CASTLE: int = 3
PROMOTE: int = 4
PROMOTE_CAPTURE: int = 5


def findPawnMoves(grid: list[list[Piece]],
                  rank: int, file: int) -> list[list[int]]:
    """
    Find all legal moves for a pawn at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    list[list[int]]: matrix of possible moves
    """
    validMatrix = [[ILLEGAL]*8 for _ in range(8)]
    # normal single-step move
    if grid[rank+1][file].pieceId == Piece.EMPTY:
        if rank+1 == 7:
            validMatrix[rank+1][file] = PROMOTE
        else:
            validMatrix[rank+1][file] = MOVE
        # starting double-step move
        if rank == 1 and grid[rank+2][file].pieceId == Piece.EMPTY:
            validMatrix[rank+2][file] = MOVE
    # diagonal capture northwest
    if file != 0 and rank != 7 and grid[rank+1][file-1].pieceColor == Piece.BLACK:
        if rank+1 == 7:
            validMatrix[rank+1][file-1] = PROMOTE_CAPTURE
        else:
            validMatrix[rank+1][file-1] = CAPTURE
    # diagonal capture northeast
    if file != 7 and rank != 7 and grid[rank+1][file+1].pieceColor == Piece.BLACK:
        if rank+1 == 7:
            validMatrix[rank+1][file+1] = PROMOTE_CAPTURE
        else:
            validMatrix[rank+1][file+1] = CAPTURE
    return validMatrix


def findPawnAttacks(grid: list[list[Piece]],
                    rank: int, file: int) -> np.ndarray:
    """
    Find all attacked squares for a pawn at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    np.ndarray: matrix of attacked squares
    """
    attackedMatrix = np.zeros((8, 8), dtype=int)
    # diagonal capture northwest
    if file != 0 and rank != 7:
        attackedMatrix[rank+1, file-1] = 1
    # diagonal capture northeast
    if file != 7 and rank != 7:
        attackedMatrix[rank+1][file+1] = 1
    return attackedMatrix


KNIGHT_R_OFFSETS: tuple[int] = (-2, -2, -1, -1, +1, +1, +2, +2)
KNIGHT_F_OFFSETS: tuple[int] = (-1, +1, -2, +2, -2, +2, -1, +1)


def findKnightMoves(grid: list[list[Piece]],
                    rank: int, file: int) -> list[list[int]]:
    """
    Find all legal moves for a knight at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    list[list[int]]: matrix of possible moves
    """
    validMatrix = [[ILLEGAL]*8 for _ in range(8)]
    for i in range(8):
        destRank = rank + KNIGHT_R_OFFSETS[i]
        destFile = file + KNIGHT_F_OFFSETS[i]
        if destRank < 0 or destRank > 7\
                or destFile < 0 or destFile > 7:
            continue
        if grid[destRank][destFile].pieceId == Piece.EMPTY:
            validMatrix[destRank][destFile] = MOVE
        elif grid[destRank][destFile].pieceColor == Piece.BLACK:
            validMatrix[destRank][destFile] = CAPTURE
    return validMatrix


def findKnightAttacks(grid: list[list[Piece]],
                      rank: int, file: int) -> np.ndarray:
    """
    Find all attacked squares for a knight at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    np.ndarray: matrix of attacked squares
    """
    attackedMatrix = np.zeros((8, 8), dtype=int)
    for i in range(8):
        destRank = rank + KNIGHT_R_OFFSETS[i]
        destFile = file + KNIGHT_F_OFFSETS[i]
        if destRank < 0 or destRank > 7\
                or destFile < 0 or destFile > 7:
            continue
        attackedMatrix[destRank, destFile] = 1
    return attackedMatrix


BISHOP_R_OFFSETS: tuple[int] = (-1, -1, +1, +1)
BISHOP_F_OFFSETS: tuple[int] = (-1, +1, -1, +1)


def findBishopMoves(grid: list[list[Piece]],
                    rank: int, file: int) -> list[list[int]]:
    """
    Find all legal moves for a bishop at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    list[list[int]]: matrix of possible moves
    """
    validMatrix = [[ILLEGAL]*8 for _ in range(8)]
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
            validMatrix[destRank][destFile] = MOVE
            # piece of opposing color, stop (but mark valid)
            if grid[destRank][destFile].pieceColor == Piece.BLACK:
                validMatrix[destRank][destFile] = CAPTURE
                break
    return validMatrix


def findBishopAttacks(grid: list[list[Piece]],
                      rank: int, file: int) -> np.ndarray:
    """
    Find all attacked squares for a bishop at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    np.ndarray: matrix of attacked squares
    """
    attackedMatrix = np.zeros((8, 8), dtype=int)
    for direction in range(4):
        for step in range(1, 8):
            destRank = rank + step * BISHOP_R_OFFSETS[direction]
            destFile = file + step * BISHOP_F_OFFSETS[direction]
            # out of bounds, stop
            if destRank < 0 or destRank > 7\
                    or destFile < 0 or destFile > 7:
                break
            # mark this square
            attackedMatrix[destRank, destFile] = 1
            # piece blocking sight, stop
            if grid[destRank][destFile].pieceId != Piece.EMPTY:
                break
    return attackedMatrix


ROOK_R_OFFSETS: tuple[int] = (0, 0, +1, -1)
ROOK_F_OFFSETS: tuple[int] = (+1, -1, 0, 0)


def findRookMoves(grid: list[list[Piece]],
                  rank: int, file: int) -> list[list[int]]:
    """
    Find all legal moves for a rook at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    list[list[int]]: matrix of possible moves
    """
    validMatrix = [[ILLEGAL]*8 for _ in range(8)]
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
            validMatrix[destRank][destFile] = MOVE
            # piece of opposing color, stop (but mark valid)
            if grid[destRank][destFile].pieceColor == Piece.BLACK:
                validMatrix[destRank][destFile] = CAPTURE
                break

    return validMatrix


def findRookAttacks(grid: list[list[Piece]],
                    rank: int, file: int) -> np.ndarray:
    """
    Find all attacked squares for a rook at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    np.ndarray: matrix of attacked squares
    """
    attackedMatrix = np.zeros((8, 8), dtype=int)
    for direction in range(4):
        for step in range(1, 8):
            destRank = rank + step * ROOK_R_OFFSETS[direction]
            destFile = file + step * ROOK_F_OFFSETS[direction]
            # out of bounds, stop
            if destRank < 0 or destRank > 7\
                    or destFile < 0 or destFile > 7:
                break
            # mark this square
            attackedMatrix[destRank, destFile] = 1
            # piece blocking sight, stop
            if grid[destRank][destFile].pieceId != Piece.EMPTY:
                break
    return attackedMatrix


# note that these are just the union of rook and bishop offset lists
QUEEN_R_OFFSETS: tuple[int] = (0, 0, +1, -1, -1, -1, +1, +1)
QUEEN_F_OFFSETS: tuple[int] = (+1, -1, 0, 0, -1, +1, -1, +1)


def findQueenMoves(grid: list[list[Piece]],
                   rank: int, file: int) -> list[list[int]]:
    """
    Find all legal moves for a queen at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    list[list[int]]: matrix of possible moves
    """
    validMatrix = [[ILLEGAL]*8 for _ in range(8)]
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
            validMatrix[destRank][destFile] = MOVE
            # piece of opposing color, stop (but mark valid)
            if grid[destRank][destFile].pieceColor == Piece.BLACK:
                validMatrix[destRank][destFile] = CAPTURE
                break

    return validMatrix


def findQueenAttacks(grid: list[list[Piece]],
                     rank: int, file: int) -> np.ndarray:
    """
    Find all attacked squares for a queen at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    np.ndarray: matrix of attacked squares
    """
    attackedMatrix = np.zeros((8, 8), dtype=int)
    for direction in range(8):
        for step in range(1, 8):
            destRank = rank + step * QUEEN_R_OFFSETS[direction]
            destFile = file + step * QUEEN_F_OFFSETS[direction]
            # out of bounds, stop
            if destRank < 0 or destRank > 7\
                    or destFile < 0 or destFile > 7:
                break
            # mark this square
            attackedMatrix[destRank, destFile] = 1
            # piece blocking sight, stop
            if grid[destRank][destFile].pieceId != Piece.EMPTY:
                break
    return attackedMatrix


# these are the same as the queen offsets
KING_R_OFFSETS: tuple[int] = (0, 0, +1, -1, -1, -1, +1, +1)
KING_F_OFFSETS: tuple[int] = (+1, -1, 0, 0, -1, +1, -1, +1)


def findPersianKingMoves(grid: list[list[Piece]], rank: int, file: int,
                         castleShort: bool, castleLong: bool) -> list[list[int]]:
    """
    Find all legal moves for a persian king at the given board, rank, and file.

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
    validMatrix = [[ILLEGAL]*8 for _ in range(8)]
    attackedMatrix = findAttackedSquares(grid, False)
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
        # would be check, invalid
        if attackedMatrix[destRank, destFile]:
            continue
        if grid[destRank][destFile].pieceColor == Piece.EMPTY:
            validMatrix[destRank][destFile] = MOVE
        else:
            validMatrix[destRank][destFile] = CAPTURE

    if castleShort and checkCastle(grid, True):
        validMatrix[0][6] = validMatrix[0][7] = CASTLE
    if castleLong and checkCastle(grid, False):
        validMatrix[0][2] = validMatrix[0][0] = CASTLE

    return validMatrix


def checkCastle(grid: list[list[Piece]], castleShort: bool):
    """
    Check whether it is a legal move to castle in the specified direction.
    Does not check if the king or rook have moved; this method only
    checks for intervening pieces and castling out of, into, or through check.

    Parameters
    ---
    grid: list[list[Piece]] current board state
    castleShort: bool True if castling short, False if castling long

    Returns
    ---
    bool: whether castling is legal.
    """
    attacked = findAttackedSquares(grid, False)
    if castleShort:
        return grid[0][5].pieceId == Piece.EMPTY and\
            grid[0][6].pieceId == Piece.EMPTY and\
            np.sum(attacked[0, 4:7]) == 0
    else:  # castle long
        return grid[0][1].pieceId == Piece.EMPTY and\
            grid[0][2].pieceId == Piece.EMPTY and\
            grid[0][3].pieceId == Piece.EMPTY and\
            np.sum(attacked[0, 2:5]) == 0


def findPersianKingAttacks(grid: list[list[Piece]],
                           rank: int, file: int) -> np.ndarray:
    """
    Find all attacked squares for a persian king at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    np.ndarray: matrix of attacked squares
    """
    attackedMatrix = np.zeros((8, 8), dtype=int)
    for direction in range(8):
        destRank = rank + KING_R_OFFSETS[direction]
        destFile = file + KING_F_OFFSETS[direction]
        # out of bounds, stop
        if destRank < 0 or destRank > 7\
                or destFile < 0 or destFile > 7:
            continue
        # mark this square
        attackedMatrix[destRank, destFile] = 1
    return attackedMatrix


def findHopliteMoves(grid: list[list[Piece]],
                     rank: int, file: int) -> list[list[int]]:
    """
    Find all legal moves for a hoplite at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    list[list[int]]: matrix of possible moves
    """
    validMatrix = [[ILLEGAL]*8 for _ in range(8)]
    # normal diagonal move southwest
    if file != 0 and grid[rank-1][file-1].pieceId == Piece.EMPTY:
        if rank-1 == 0:
            validMatrix[rank-1][file-1] = PROMOTE
        else:
            validMatrix[rank-1][file-1] = MOVE
    # normal diagonal move northeast
    if file != 7 and grid[rank-1][file+1].pieceId == Piece.EMPTY:
        if rank-1 == 0:
            validMatrix[rank-1][file+1] = PROMOTE
        else:
            validMatrix[rank-1][file+1] = MOVE
    # starting double-step move southwest
    if rank == 6 and file >= 2 and grid[rank-2][file-2].pieceId == Piece.EMPTY:
        validMatrix[rank-2][file-2] = MOVE
    # starting double-step move southeast
    if rank == 6 and file <= 5 and grid[rank-2][file+2].pieceId == Piece.EMPTY:
        validMatrix[rank-2][file+2] = MOVE
    # capture forward
    if grid[rank-1][file].pieceColor == Piece.WHITE:
        if rank == 1:
            validMatrix[rank-1][file] = PROMOTE_CAPTURE
        else:
            validMatrix[rank-1][file] = CAPTURE
    return validMatrix


def findHopliteAttacks(grid: list[list[Piece]],
                       rank: int, file: int) -> np.ndarray:
    """
    Find all attacked squares for a hoplite at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    np.ndarray: matrix of attacked squares
    """
    attackedMatrix = np.zeros((8, 8), dtype=int)
    attackedMatrix[rank-1, file] = 1
    return attackedMatrix


LIEUTENANT_R_OFFSETS: tuple[int] = (-2, -2, -1, -1, +1, +1, +2, +2)
LIEUTENANT_F_OFFSETS: tuple[int] = (-2, +2, -1, +1, -1, +1, -2, +2)


def findLieutenantMoves(grid: list[list[Piece]],
                        rank: int, file: int) -> list[list[int]]:
    """
    Find all legal moves for a lieutenant at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    list[list[int]]: matrix of possible moves
    """
    validMatrix = [[ILLEGAL]*8 for _ in range(8)]
    # jumping diagonal move
    for i in range(8):
        destRank = rank + LIEUTENANT_R_OFFSETS[i]
        destFile = file + LIEUTENANT_F_OFFSETS[i]
        if destRank < 0 or destRank > 7\
                or destFile < 0 or destFile > 7:
            continue
        if grid[destRank][destFile].pieceId == Piece.EMPTY:
            validMatrix[destRank][destFile] = MOVE
        elif grid[destRank][destFile].pieceColor == Piece.WHITE:
            validMatrix[destRank][destFile] = CAPTURE
    # horizontal moves
    if file > 0 and grid[rank][file-1].pieceId == Piece.EMPTY:
        validMatrix[rank][file-1] = MOVE
    if file < 7 and grid[rank][file+1].pieceId == Piece.EMPTY:
        validMatrix[rank][file+1] = MOVE
    return validMatrix


def findLieutenantAttacks(grid: list[list[Piece]],
                          rank: int, file: int) -> np.ndarray:
    """
    Find all attacked squares for a lieutenant at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    np.ndarray: matrix of attacked squares
    """
    attackedMatrix = np.zeros((8, 8), dtype=int)
    # jumping diagonal move
    for i in range(8):
        destRank = rank + LIEUTENANT_R_OFFSETS[i]
        destFile = file + LIEUTENANT_F_OFFSETS[i]
        if destRank < 0 or destRank > 7\
                or destFile < 0 or destFile > 7:
            continue
        attackedMatrix[destRank, destFile] = 1
    return attackedMatrix


CAPTAIN_R_OFFSETS: tuple[int] = (-2, -1, 0, 0, +1, +2, 0, 0)
CAPTAIN_F_OFFSETS: tuple[int] = (0, 0, -2, -1, 0, 0, +1, +2)


def findCaptainMoves(grid: list[list[Piece]],
                     rank: int, file: int) -> list[list[int]]:
    """
    Find all legal moves for a captain at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    list[list[int]]: matrix of possible moves
    """
    validMatrix = [[ILLEGAL]*8 for _ in range(8)]
    # jumping cardinal move
    for i in range(8):
        destRank = rank + CAPTAIN_R_OFFSETS[i]
        destFile = file + CAPTAIN_F_OFFSETS[i]
        if destRank < 0 or destRank > 7\
                or destFile < 0 or destFile > 7:
            continue
        if grid[destRank][destFile].pieceId == Piece.EMPTY:
            validMatrix[destRank][destFile] = MOVE
        elif grid[destRank][destFile].pieceColor == Piece.WHITE:
            validMatrix[destRank][destFile] = CAPTURE
    return validMatrix


def findCaptainAttacks(grid: list[list[Piece]],
                       rank: int, file: int) -> np.ndarray:
    """
    Find all attacked squares for a captain at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    np.ndarray: matrix of attacked squares
    """
    attackedMatrix = np.zeros((8, 8), dtype=int)
    # jumping cardinal move
    for i in range(8):
        destRank = rank + CAPTAIN_R_OFFSETS[i]
        destFile = file + CAPTAIN_F_OFFSETS[i]
        if destRank < 0 or destRank > 7\
                or destFile < 0 or destFile > 7:
            continue
        attackedMatrix[destRank, destFile] = 1
    return attackedMatrix


def findGeneralMoves(grid: list[list[Piece]],
                     rank: int, file: int) -> list[list[int]]:
    """
    Find all legal moves for a general at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    list[list[int]]: matrix of possible moves
    """
    validMatrix = [[ILLEGAL]*8 for _ in range(8)]
    # move like a rook
    for direction in range(4):
        for step in range(1, 8):
            destRank = rank + step * ROOK_R_OFFSETS[direction]
            destFile = file + step * ROOK_F_OFFSETS[direction]
            # out of bounds, stop
            if destRank < 0 or destRank > 7\
                    or destFile < 0 or destFile > 7:
                break
            # piece of same color, stop
            if grid[destRank][destFile].pieceColor == Piece.BLACK:
                break
            validMatrix[destRank][destFile] = MOVE
            # piece of opposing color, stop (but mark valid)
            if grid[destRank][destFile].pieceColor == Piece.WHITE:
                validMatrix[destRank][destFile] = CAPTURE
                break
    # move like a king
    for direction in range(8):
        destRank = rank + KING_R_OFFSETS[direction]
        destFile = file + KING_F_OFFSETS[direction]
        # out of bounds
        if destRank < 0 or destRank > 7\
                or destFile < 0 or destFile > 7:
            continue
        # piece of same color, invalid
        if grid[destRank][destFile].pieceColor == Piece.BLACK:
            continue
        if grid[destRank][destFile].pieceColor == Piece.EMPTY:
            validMatrix[destRank][destFile] = MOVE
        else:
            validMatrix[destRank][destFile] = CAPTURE
    return validMatrix


def findGeneralAttacks(grid: list[list[Piece]],
                       rank: int, file: int) -> np.ndarray:
    """
    Find all attacked squares for a general at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    np.ndarray: matrix of attacked squares
    """
    attackedMatrix = np.zeros((8, 8), dtype=int)
    # move like a rook
    for direction in range(4):
        for step in range(1, 8):
            destRank = rank + step * ROOK_R_OFFSETS[direction]
            destFile = file + step * ROOK_F_OFFSETS[direction]
            # out of bounds, stop
            if destRank < 0 or destRank > 7\
                    or destFile < 0 or destFile > 7:
                break
            attackedMatrix[destRank, destFile] = 1
            # piece blocking sight, stop
            if grid[destRank][destFile].pieceId != Piece.EMPTY:
                break
    # move like a king
    for direction in range(8):
        destRank = rank + KING_R_OFFSETS[direction]
        destFile = file + KING_F_OFFSETS[direction]
        # out of bounds
        if destRank < 0 or destRank > 7\
                or destFile < 0 or destFile > 7:
            continue
        attackedMatrix[destRank][destFile] = 1
    return attackedMatrix


def findWarlordMoves(grid: list[list[Piece]],
                     rank: int, file: int) -> list[list[int]]:
    """
    Find all legal moves for a warlord at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    list[list[int]]: matrix of possible moves
    """
    validMatrix = [[ILLEGAL]*8 for _ in range(8)]
    # move like a bishop
    for direction in range(4):
        for step in range(1, 8):
            destRank = rank + step * BISHOP_R_OFFSETS[direction]
            destFile = file + step * BISHOP_F_OFFSETS[direction]
            # out of bounds, stop
            if destRank < 0 or destRank > 7\
                    or destFile < 0 or destFile > 7:
                break
            # piece of same color, stop
            if grid[destRank][destFile].pieceColor == Piece.BLACK:
                break
            validMatrix[destRank][destFile] = MOVE
            # piece of opposing color, stop (but mark valid)
            if grid[destRank][destFile].pieceColor == Piece.WHITE:
                validMatrix[destRank][destFile] = CAPTURE
                break
    # move like a knight
    for i in range(8):
        destRank = rank + KNIGHT_R_OFFSETS[i]
        destFile = file + KNIGHT_F_OFFSETS[i]
        if destRank < 0 or destRank > 7\
                or destFile < 0 or destFile > 7:
            continue
        if grid[destRank][destFile].pieceId == Piece.EMPTY:
            validMatrix[destRank][destFile] = MOVE
        elif grid[destRank][destFile].pieceColor == Piece.WHITE:
            validMatrix[destRank][destFile] = CAPTURE
    return validMatrix


def findWarlordAttacks(grid: list[list[Piece]],
                       rank: int, file: int) -> np.ndarray:
    """
    Find all attacked squares for a warlord at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    np.ndarray: matrix of attacked squares
    """
    attackedMatrix = np.zeros((8, 8), dtype=int)
    # move like a bishop
    for direction in range(4):
        for step in range(1, 8):
            destRank = rank + step * BISHOP_R_OFFSETS[direction]
            destFile = file + step * BISHOP_F_OFFSETS[direction]
            # out of bounds, stop
            if destRank < 0 or destRank > 7\
                    or destFile < 0 or destFile > 7:
                break
            attackedMatrix[destRank, destFile] = 1
            # piece blocking sight, stop
            if grid[destRank][destFile].pieceId != Piece.EMPTY:
                break
    # move like a knight
    for i in range(8):
        destRank = rank + KNIGHT_R_OFFSETS[i]
        destFile = file + KNIGHT_F_OFFSETS[i]
        if destRank < 0 or destRank > 7\
                or destFile < 0 or destFile > 7:
            continue
        attackedMatrix[destRank, destFile] = 1
    return attackedMatrix


def findSpartanKingMoves(grid: list[list[Piece]],
                         rank: int, file: int,
                         numSpartanKings: int) -> list[list[int]]:
    """
    Find all legal moves for a spartan king at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    list[list[int]]: matrix of possible moves
    """
    validMatrix = [[ILLEGAL]*8 for _ in range(8)]
    # if we have 2 kings, we don't care about check
    attackedMatrix = np.zeros((8, 8), dtype=int) if numSpartanKings == 2\
        else findAttackedSquares(grid, True)
    # normal directional moves
    for direction in range(8):
        destRank = rank + KING_R_OFFSETS[direction]
        destFile = file + KING_F_OFFSETS[direction]
        # out of bounds
        if destRank < 0 or destRank > 7\
                or destFile < 0 or destFile > 7:
            continue
        # would be check, invalid
        if attackedMatrix[destRank, destFile]:
            continue
        # piece of same color, invalid
        if grid[destRank][destFile].pieceColor == Piece.BLACK:
            continue
        if grid[destRank][destFile].pieceColor == Piece.EMPTY:
            validMatrix[destRank][destFile] = MOVE
        else:
            validMatrix[destRank][destFile] = CAPTURE

    return validMatrix


def findSpartanKingAttacks(grid: list[list[Piece]],
                           rank: int, file: int) -> np.ndarray:
    """
    Find all attacked squares for a spartan king at the given board, rank, and file.

    Parameters
    ---
    grid: list[list[Piece]] board state
    rank: int
    file: int

    Returns
    ---
    np.ndarray: matrix of attacked squares
    """
    # Thie is the exact same code as for a persian king
    attackedMatrix = np.zeros((8, 8), dtype=int)
    for direction in range(8):
        destRank = rank + KING_R_OFFSETS[direction]
        destFile = file + KING_F_OFFSETS[direction]
        # out of bounds, stop
        if destRank < 0 or destRank > 7\
                or destFile < 0 or destFile > 7:
            continue
        # mark this square
        attackedMatrix[destRank, destFile] = 1
    return attackedMatrix


def findAttackedSquares(grid: list[list[Piece]], whiteToMove: bool) -> np.ndarray:
    """
    Finds all squares attacked by the selected player on a given board.

    grid: list[list[Piece]] board state
    whiteToMove: bool True if White, False if Black

    Returns
    ---
    np.ndarray: matrix of attacked squares
    """
    attacked = np.zeros((8, 8), dtype=int)
    # Find squares that White (Persian pieces) are attacking
    if whiteToMove:
        for rank in range(8):
            for file in range(8):
                match grid[rank][file].pieceId:
                    case Piece.PAWN:
                        attacked += findPawnAttacks(grid, rank, file)
                    case Piece.KNIGHT:
                        attacked += findKnightAttacks(grid, rank, file)
                    case Piece.BISHOP:
                        attacked += findBishopAttacks(grid, rank, file)
                    case Piece.ROOK:
                        attacked += findRookAttacks(grid, rank, file)
                    case Piece.QUEEN:
                        attacked += findQueenAttacks(grid, rank, file)
                    case Piece.PKING:
                        attacked += findSpartanKingAttacks(grid, rank, file)
    # Find squares that Black (Spartan pieces) are attacking
    else:
        for rank in range(8):
            for file in range(8):
                match grid[rank][file].pieceId:
                    case Piece.HOPLITE:
                        attacked += findHopliteAttacks(grid, rank, file)
                    case Piece.LIEUTENANT:
                        attacked += findLieutenantAttacks(grid, rank, file)
                    case Piece.CAPTAIN:
                        attacked += findCaptainAttacks(grid, rank, file)
                    case Piece.GENERAL:
                        attacked += findGeneralAttacks(grid, rank, file)
                    case Piece.WARLORD:
                        attacked += findWarlordAttacks(grid, rank, file)
                    case Piece.SKING:
                        attacked += findSpartanKingAttacks(grid, rank, file)
    return attacked
