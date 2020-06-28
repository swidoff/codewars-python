from collections import namedtuple
from itertools import permutations, accumulate
from typing import Optional, Tuple, Set, List, Dict

State = namedtuple("State", ["board", "clues", "remaining"])
Pos = Tuple[int, int]
Change = Dict[Pos, int]
Key = Tuple[str, int]

clue_idx = {
    ('c', 0): (0, 17), ('c', 1): (1, 16), ('c', 2): (2, 15), ('c', 3): (3, 14), ('c', 4): (4, 13), ('c', 5): (5, 12),
    ('r', 0): (23, 6), ('r', 1): (22, 7), ('r', 2): (21, 8), ('r', 3): (20, 9), ('r', 4): (19, 10), ('r', 5): (18, 11)
}
keys = [(pos, i) for pos in ('c', 'r') for i in range(6)]
perms = list(permutations(list(range(7))))


def solve_puzzle(in_clues):
    board = [[0] * 6 for _ in range(6)]
    clues = {k: (in_clues[clue_idx[k][0]], in_clues[clue_idx[k][1]]) for k in keys}
    remaining = {k: set(range(1, 7)) for k in keys}
    initial_state = State(board, clues, remaining)

    final_state = search(initial_state)
    res = final_state.board
    return tuple(tuple(c for c in row) for row in res)


def search(state: State, changes: Dict[Key, List[Change]] = None) -> Optional[State]:
    choices = [k for k, v in state.remaining.items() if len(v) > 0]
    if not choices:
        return state

    new_changes = {
        key: legal_changes(state, key, changes[key] if changes else None)
        for key in choices
    }

    sorted_choices = sorted(choices, key=lambda k: len(new_changes[k]))
    key = sorted_choices[0]

    for change in new_changes[key]:
        update_state(state, change)
        res = search(state, new_changes)
        if res:
            return res
        revert_state(state, change)


def legal_changes(state: State, key: Key, prev_changes: Optional[List[Change]]) -> List[Change]:
    if prev_changes is None:
        pos, i = key
        indexes = [(i, c) for c in range(6)] if pos == 'r' else [(r, i) for r in range(6)]
        changes = [dict(zip(indexes, move)) for move in perms]
    else:
        changes = [
            {pos: val for pos, val in change.items() if state.board[pos[0]][pos[1]] == 0}
            for change in prev_changes
        ]

    return [change for change in changes if is_legal_change(state, change) and obeys_clues(state, change)]


def is_legal_change(state: State, change: Change) -> bool:
    return all(val in state.remaining[('c', c)] and val in state.remaining[('r', r)] for (r, c), val in change.items())


def obeys_clues(state: State, change: Change) -> bool:
    def is_valid_for(k):
        pos, i = k
        clue1, clue2 = state.clues[k]
        if pos == 'r':
            vals = [change.get((i, c), state.board[i][c]) for c in range(6)]
        else:
            vals = [change.get((r, i), state.board[r][i]) for r in range(6)]
        return any(v == 0 for v in vals) or values_obeys_clues(vals, clue1, clue2)

    return all(is_valid_for(k) for k in keys)


def values_obeys_clues(vals: List[int], clue1: int, clue2: int) -> bool:
    visible1 = len(set(accumulate(vals, max)))
    visible2 = len(set(accumulate(reversed(vals), max)))
    return (clue1 == 0 or clue1 == visible1) and (clue2 == 0 or clue2 == visible2)


def update_state(state: State, change: Change):
    for (r, c), val in change.items():
        if state.board[r][c] == 0:
            state.board[r][c] = val
            state.remaining[('r', r)].remove(val)
            state.remaining[('c', c)].remove(val)


def revert_state(state, change: Change):
    for (r, c), val in change.items():
        state.board[r][c] = 0
        state.remaining[('r', r)].add(val)
        state.remaining[('c', c)].add(val)


if __name__ == '__main__':
    from test import Test
    import time

    Test.describe("Skyscrapers")
    Test.it("can solve 6x6 puzzle 1")
    clues = (3, 2, 2, 3, 2, 1,
             1, 2, 3, 3, 2, 2,
             5, 1, 2, 2, 4, 3,
             3, 2, 1, 2, 2, 4)

    expected = ((2, 1, 4, 3, 5, 6),
                (1, 6, 3, 2, 4, 5),
                (4, 3, 6, 5, 1, 2),
                (6, 5, 2, 1, 3, 4),
                (5, 4, 1, 6, 2, 3),
                (3, 2, 5, 4, 6, 1))

    start = time.time()
    actual = solve_puzzle(clues)
    duration = time.time() - start
    print(duration)
    Test.assert_equals(actual, expected)

    Test.it("can solve 6x6 puzzle 2")
    clues = (0, 0, 0, 2, 2, 0,
             0, 0, 0, 6, 3, 0,
             0, 4, 0, 0, 0, 0,
             4, 4, 0, 3, 0, 0)

    expected = ((5, 6, 1, 4, 3, 2),
                (4, 1, 3, 2, 6, 5),
                (2, 3, 6, 1, 5, 4),
                (6, 5, 4, 3, 2, 1),
                (1, 2, 5, 6, 4, 3),
                (3, 4, 2, 5, 1, 6))

    start = time.time()
    actual = solve_puzzle(clues)
    duration = time.time() - start
    print(duration)
    Test.assert_equals(actual, expected)

    Test.it("can solve 6x6 puzzle 3")
    clues = (0, 3, 0, 5, 3, 4,
             0, 0, 0, 0, 0, 1,
             0, 3, 0, 3, 2, 3,
             3, 2, 0, 3, 1, 0)

    expected = ((5, 2, 6, 1, 4, 3),
                (6, 4, 3, 2, 5, 1),
                (3, 1, 5, 4, 6, 2),
                (2, 6, 1, 5, 3, 4),
                (4, 3, 2, 6, 1, 5),
                (1, 5, 4, 3, 2, 6))

    start = time.time()
    actual = solve_puzzle(clues)
    duration = time.time() - start
    print(duration)
    Test.assert_equals(actual, expected)
