import string
from typing import List

def knight_moves(square: str) -> List[str]:
    """
    Given a square in algebraic notation (e.g. 'e4'), return all valid knight moves
    from that square on an empty 8×8 board.
    """
    files = {f: i for i, f in enumerate(string.ascii_lowercase[:8], start=1)}
    ranks = {str(i): i for i in range(1, 9)}
    file, rank = square[0], square[1]
    if file not in files or rank not in ranks:
        raise ValueError(f"Invalid square: {square}")

    x, y = files[file], ranks[rank]
    deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    moves = []

    for dx, dy in deltas:
        nx, ny = x + dx, y + dy
        if 1 <= nx <= 8 and 1 <= ny <= 8:
            # convert back to algebraic
            file_char = list(files.keys())[list(files.values()).index(nx)]
            rank_char = str(ny)
            moves.append(f"{file_char}{rank_char}")

    return sorted(moves)
