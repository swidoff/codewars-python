from collections import deque
from itertools import product
from typing import Tuple, Set, Dict

Coord = Tuple[int, int]  # row, column coordinate in the battle field.
PieceCount = Tuple[int, ...]  # Count of pieces of len i + 1 for each index i from 0 to 3


def validate_battlefield(battle_field):
    valid_counts = (4, 3, 2, 1)
    num_pieces = sum(valid_counts)
    num_squares = sum(count * length for count, length in zip(valid_counts, range(1, 5)))
    ones_sets = [extract_ones(battle_field, i, j) for i in range(10) for j in range(10) if battle_field[i][j] == 1]

    if len(ones_sets) > num_pieces:
        return False

    if any(len(ones) > num_squares for ones in ones_sets):
        return False

    combos = [
        list(piece_combinations(piece))
        for piece in ones_sets
    ]
    return any(
        tuple(sum(c) for c in zip(*counts)) == valid_counts
        for counts in product(*combos)
    )


def extract_ones(battle_field, start_row: int, start_column: int) -> Set[Coord]:
    """Returns the coordinates of contiguous regions of 1s from the battle_field matrix."""
    res = set()
    q = deque([(start_row, start_column)])
    while q:
        r, c = q.popleft()
        res.add((r, c))
        battle_field[r][c] = 2
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 10 and 0 <= nc < 10 and battle_field[nr][nc] == 1:
                q.append((nr, nc))
    return res


def piece_combinations(coords: Set[Coord], seen: Dict[Tuple[Coord, ...], Set[PieceCount]] = None) -> Set[PieceCount]:
    """Returns the piece size counts that can be made from the set of coordinates."""
    if not coords:
        return {(0, 0, 0, 0)}

    sorted_coords = tuple(sorted(coords))
    if seen is None:
        seen = {}
    elif sorted_coords in seen:
        return seen[sorted_coords]

    res = set()
    r, c = sorted_coords[0]

    pieces = [{(r, c)}]
    for height in range(2, 5):
        pieces.append({(r + dr, c) for dr in range(0, height)})
    for width in range(2, 5):
        pieces.append({(r, c + dc) for dc in range(0, width)})
    pieces = list(filter(lambda p: all(coord in coords for coord in p), pieces))

    for piece in pieces:
        new_coords = coords - piece
        combos = piece_combinations(new_coords, seen)
        for count in combos:
            new_combo = list(count)
            new_combo[len(piece) - 1] += 1
            res.add(tuple(new_combo))

    seen[sorted_coords] = res
    return res


if __name__ == '__main__':
    from test import Test as test

    test.expect(validate_battlefield(
        [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
         [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
         [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "Must return true for valid field")

    # concat test case
    test.expect(validate_battlefield(
        [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
         [1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
         [1, 1, 0, 0, 1, 1, 1, 0, 1, 0],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "Must return true if ships are in contact")

    test.expect(validate_battlefield(
        [[1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
         [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
         [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
         [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
         [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "Must return true if ships are in contact")
