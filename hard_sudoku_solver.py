from collections import namedtuple
from typing import Set
from copy import deepcopy

State = namedtuple("State", ["puzzle", "unknown", "row_remains", "col_remains", "box_remains"])


def sudoku_solver(puzzle):
    if len(puzzle) != 9:
        raise ValueError("Not a 9x9 puzzle")
    if any(len(puzzle[i]) != 9 for i in range(9)):
        raise ValueError("Not a 9x9 puzzle")
    if not all(0 <= puzzle[r][c] <= 9 for r in range(9) for c in range(9)):
        raise ValueError("Invalid values in the puzzle")

    row_remains = [set(range(1, 10)) for _ in range(9)]
    col_remains = [set(range(1, 10)) for _ in range(9)]
    box_remains = [set(range(1, 10)) for _ in range(9)]
    unknown = set()

    for r in range(9):
        for c in range(9):
            num = puzzle[r][c]
            if num:
                row_remains[r].remove(num)
                col_remains[c].remove(num)
                box_remains[3 * (r // 3) + c // 3].remove(num)
            else:
                unknown.add((r, c))

    res = solve(State(puzzle, unknown, row_remains, col_remains, box_remains))
    if not res:
        raise ValueError("No solution.")
    return res


def solve(state: State):
    if len(state.unknown) == 0:
        return state.puzzle
    else:
        moves = [(r, c, possible_values(r, c, state)) for r, c in state.unknown]
        r, c, values = min(moves, key=lambda t: len(t[2]))

        if len(values) == 0:
            return None

        res = None
        for v in values:
            make_move(r, c, v, state)
            new_res = solve(state)
            if new_res:
                if res:
                    raise ValueError("Multiple solutions!")
                else:
                    res = deepcopy(new_res)
            undo_move(r, c, v, state)

        return res


def possible_values(r: int, c: int, s: State) -> Set[int]:
    return set(range(1, 10)) & s.row_remains[r] & s.col_remains[c] & s.box_remains[3 * (r // 3) + c // 3]


def make_move(r: int, c: int, v: int, s: State) -> State:
    s.puzzle[r][c] = v
    s.unknown.remove((r, c))
    s.row_remains[r].remove(v)
    s.col_remains[c].remove(v)
    s.box_remains[3 * (r // 3) + c // 3].remove(v)
    return s


def undo_move(r: int, c: int, v: int, s: State) -> State:
    s.puzzle[r][c] = 0
    s.unknown.add((r, c))
    s.row_remains[r].add(v)
    s.col_remains[c].add(v)
    s.box_remains[3 * (r // 3) + c // 3].add(v)
    return s


if __name__ == '__main__':
    from test import Test

    puzzle = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
              [6, 0, 0, 1, 9, 5, 0, 0, 0],
              [0, 9, 8, 0, 0, 0, 0, 6, 0],
              [8, 0, 0, 0, 6, 0, 0, 0, 3],
              [4, 0, 0, 8, 0, 3, 0, 0, 1],
              [7, 0, 0, 0, 2, 0, 0, 0, 6],
              [0, 6, 0, 0, 0, 0, 2, 8, 0],
              [0, 0, 0, 4, 1, 9, 0, 0, 5],
              [0, 0, 0, 0, 8, 0, 0, 7, 9]]

    solution = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
                [6, 7, 2, 1, 9, 5, 3, 4, 8],
                [1, 9, 8, 3, 4, 2, 5, 6, 7],
                [8, 5, 9, 7, 6, 1, 4, 2, 3],
                [4, 2, 6, 8, 5, 3, 7, 9, 1],
                [7, 1, 3, 9, 2, 4, 8, 5, 6],
                [9, 6, 1, 5, 3, 7, 2, 8, 4],
                [2, 8, 7, 4, 1, 9, 6, 3, 5],
                [3, 4, 5, 2, 8, 6, 1, 7, 9]]

    # Test.it('Puzzle 1')
    # Test.assert_equals(sudoku_solver(puzzle), solution, "Incorrect solution for the following puzzle: " + str(puzzle))

    puzzle = [[0, 0, 6, 1, 0, 0, 0, 0, 8],
              [0, 8, 0, 0, 9, 0, 0, 3, 0],
              [2, 0, 0, 0, 0, 5, 4, 0, 0],
              [4, 0, 0, 0, 0, 1, 8, 0, 0],
              [0, 3, 0, 0, 7, 0, 0, 4, 0],
              [0, 0, 7, 9, 0, 0, 0, 0, 3],
              [0, 0, 8, 4, 0, 0, 0, 0, 6],
              [0, 2, 0, 0, 5, 0, 0, 8, 0],
              [1, 0, 0, 0, 0, 2, 5, 0, 0]]

    solution = [[3, 4, 6, 1, 2, 7, 9, 5, 8],
                [7, 8, 5, 6, 9, 4, 1, 3, 2],
                [2, 1, 9, 3, 8, 5, 4, 6, 7],
                [4, 6, 2, 5, 3, 1, 8, 7, 9],
                [9, 3, 1, 2, 7, 8, 6, 4, 5],
                [8, 5, 7, 9, 4, 6, 2, 1, 3],
                [5, 9, 8, 4, 1, 3, 7, 2, 6],
                [6, 2, 4, 7, 5, 9, 3, 8, 1],
                [1, 7, 3, 8, 6, 2, 5, 9, 4]]

    Test.it('Puzzle 2')
    Test.assert_equals(sudoku_solver(puzzle), solution)
