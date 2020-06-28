from collections import deque
from typing import Tuple

Pos = Tuple[Tuple[int, int], ...]


def move_pos(pos: Pos, move: str) -> Pos:
    if len(pos) == 1:  # Upright
        r, c = pos[0]
        if move == "U":
            new_pos = tuple((r - i, c) for i in range(2, 0, -1))
        elif move == "D":
            new_pos = tuple((r + i, c) for i in range(1, 3))
        elif move == "L":
            new_pos = tuple((r, c - i) for i in range(2, 0, -1))
        else:
            new_pos = tuple((r, c + i) for i in range(1, 3))
    elif pos[0][0] == pos[1][0]:  # Horizontal
        if move == "U":
            new_pos = tuple((r - 1, c) for r, c in pos)
        elif move == "D":
            new_pos = tuple((r + 1, c) for r, c in pos)
        elif move == "L":
            new_pos = ((pos[0][0], pos[0][1] - 1),)
        else:
            new_pos = ((pos[0][0], pos[1][1] + 1),)
    else:  # Vertical
        assert pos[0][1] == pos[1][1]
        if move == "U":
            new_pos = ((pos[0][0] - 1, pos[0][1]),)
        elif move == "D":
            new_pos = ((pos[1][0] + 1, pos[0][1]),)
        elif move == "L":
            new_pos = tuple((r, c - 1) for r, c in pos)
        else:
            new_pos = tuple((r, c + 1) for r, c in pos)

    return new_pos


def blox_solver(ar):
    floor = set()
    start = None
    goal = None

    for r in range(len(ar)):
        for c in range(len(ar[r])):
            char = ar[r][c]
            if char != '0':
                floor.add((r, c))
            if char == 'B':
                start = ((r, c),)
            elif char == 'X':
                goal = ((r, c),)

    res = None
    seen = set()
    q = deque([(start, "")])
    while q:
        pos, moves = q.popleft()
        if pos == goal:
            res = moves
            break
        else:
            seen.add(pos)
            if all(p in floor for p in pos):
                for move in "RDLU":
                    new_pos = move_pos(pos, move)
                    if new_pos not in seen:
                        q.append((new_pos, moves + move))

    return res


if __name__ == '__main__':
    from test import Test as test

    test.describe('Example Tests')
    example_tests = [
        ['1110000000',
         '1B11110000',
         '1111111110',
         '0111111111',
         '0000011X11',
         '0000001110'],
        ['000000111111100',
         '111100111001100',
         '111111111001111',
         '1B11000000011X1',
         '111100000001111',
         '000000000000111'],
        ['00011111110000',
         '00011111110000',
         '11110000011100',
         '11100000001100',
         '11100000001100',
         '1B100111111111',
         '11100111111111',
         '000001X1001111',
         '00000111001111'],
        ['11111100000',
         '1B111100000',
         '11110111100',
         '11100111110',
         '10000001111',
         '11110000111',
         '11110000111',
         '00110111111',
         '01111111111',
         '0110011X100',
         '01100011100'],
        ['000001111110000',
         '000001001110000',
         '000001001111100',
         'B11111000001111',
         '0000111000011X1',
         '000011100000111',
         '000000100110000',
         '000000111110000',
         '000000111110000',
         '000000011100000']
    ]
    example_sols = [['RRDRRRD', 'RDDRRDR', 'RDRRDDR'], ['ULDRURRRRUURRRDDDRU', 'RURRRULDRUURRRDDDRU'],
                    ['ULURRURRRRRRDRDDDDDRULLLLLLD'], ['DRURURDDRRDDDLD'],
                    ['RRRDRDDRDDRULLLUULUUURRRDDLURRDRDDR', 'RRRDDRDDRDRULLLUULUUURRDRRULDDRRDDR',
                     'RRRDRDDRDDRULLLUULUUURRDRRULDDRRDDR', 'RRRDDRDDRDRULLLUULUUURRRDDLURRDRDDR']]
    for i, x in enumerate(example_tests):
        actual = blox_solver(x)
        test.expect(actual in example_sols[i])

    # pos = ((0, 0),)
    # for move in "DRULDRULDRRDDRR":
    #     new_pos = move_pos(pos, move)
    #     print(f"{move}: {pos} -> {new_pos}")
    #     pos = new_pos
