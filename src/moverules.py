#!usr/bin/env python3
"""Functions encoding move rules for SpartanChess."""

__author__ = "Chris Bao"
__version__ = "0.9"

# IMPORTS
from piece import Piece

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
    if file != 0 and grid[rank+1][file-1].pieceColor == Piece.BLACK:
        if rank+1 == 7:
            validMatrix[rank+1][file-1] = PROMOTE_CAPTURE
        else:
            validMatrix[rank+1][file-1] = CAPTURE
    # diagonal capture northeast
    if file != 7 and grid[rank+1][file+1].pieceColor == Piece.BLACK:
        if rank+1 == 7:
            validMatrix[rank+1][file+1] = PROMOTE_CAPTURE
        validMatrix[rank+1][file+1] = CAPTURE
    return validMatrix


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
        if grid[destRank][destFile].pieceColor == Piece.EMPTY:
            validMatrix[destRank][destFile] = MOVE
        else:
            validMatrix[destRank][destFile] = CAPTURE

    # TODO: castling (requires attack logic)
    if castleShort:
        validMatrix[0][6] = validMatrix[0][7] = CASTLE
    if castleLong:
        validMatrix[0][2] = validMatrix[0][0] = CASTLE

    return validMatrix


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
            validMatrix[rank-1][file-1] = PROMOTE
        else:
            validMatrix[rank-1][file+1] = MOVE
    # starting double-step move southwest
    if file >= 2 and grid[rank-2][file-2].pieceId == Piece.EMPTY:
        validMatrix[rank-2][file-2] = MOVE
    # starting double-step move southeast
    if file <= 5 and grid[rank-2][file+2].pieceId == Piece.EMPTY:
        validMatrix[rank-2][file+2] = MOVE
    # capture forward
    if grid[rank-1][file].pieceColor == Piece.WHITE:
        validMatrix[rank-1][file] = CAPTURE
    return validMatrix


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


def findSpartanKingMoves(grid: list[list[Piece]],
                         rank: int, file: int) -> list[list[int]]:
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
    # normal directional moves
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
