from collections import namedtuple
from itertools import permutations, accumulate
from typing import Optional, Tuple, List, Dict

State = namedtuple("State", ["board", "clues", "remaining"])
Pos = Tuple[int, int]
Change = Dict[Pos, int]
Key = Tuple[str, int]

n = 4

clue_idx = {
    ('c', 0): (0, 11), ('c', 1): (1, 10), ('c', 2): (2, 9), ('c', 3): (3, 8),
    ('r', 0): (15, 4), ('r', 1): (14, 5), ('r', 2): (13, 6), ('r', 3): (12, 7),
}
keys = [(pos, i) for pos in ('c', 'r') for i in range(n)]
perms = list(permutations(list(range(n + 1))))


def solve_puzzle(in_clues):
    board = [[0] * n for _ in range(n)]
    clues = {k: (in_clues[clue_idx[k][0]], in_clues[clue_idx[k][1]]) for k in keys}
    remaining = {k: set(range(1, n + 1)) for k in keys}
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
        indexes = [(i, c) for c in range(n)] if pos == 'r' else [(r, i) for r in range(n)]
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
            vals = [change.get((i, c), state.board[i][c]) for c in range(n)]
        else:
            vals = [change.get((r, i), state.board[r][i]) for r in range(n)]
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
    from test import Test as test

    clues = (
        (2, 2, 1, 3,
         2, 2, 3, 1,
         1, 2, 2, 3,
         3, 2, 1, 3),
        (0, 0, 1, 2,
         0, 2, 0, 0,
         0, 3, 0, 0,
         0, 1, 0, 0)
    )

    outcomes = (
        ((1, 3, 4, 2),
         (4, 2, 1, 3),
         (3, 4, 2, 1),
         (2, 1, 3, 4)),
        ((2, 1, 4, 3),
         (3, 4, 1, 2),
         (4, 2, 3, 1),
         (1, 3, 2, 4))
    )

    test.describe("4 by 4 skyscrapers")
    test.it("should pass all the tests provided")

    test.assert_equals(solve_puzzle(clues[0]), outcomes[0])
    test.assert_equals(solve_puzzle(clues[1]), outcomes[1])
