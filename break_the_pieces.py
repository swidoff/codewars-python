import operator
from collections import deque
from typing import Tuple, Dict


def break_pieces(shape):
    mat = [list(line) for line in shape.splitlines()]
    perimeters = [locate_perimeter(mat, r, c) for r in range(len(mat)) for c in range(len(mat[r])) if mat[r][c] == ' ']
    return sorted([draw_piece(p) for p in perimeters if p])


def locate_perimeter(mat, r_start, c_start) -> Dict[Tuple[int, int], str]:
    rows, cols = len(mat), len(mat[0])
    q = deque([(r_start, c_start)])
    seen = {(r_start, c_start)}
    perimeter = {}
    failed = False
    while q:
        r, c = q.popleft()
        char = mat[r][c]
        if char == ' ':
            mat[r][c] = '#'
            for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                new_r, new_c = r + dr, c + dc
                if 0 <= new_r < rows and 0 <= new_c < cols:
                    if (new_r, new_c) not in seen:
                        seen.add((new_r, new_c))
                        q.append((new_r, new_c))
                else:
                    failed = True
        elif char != '#':
            perimeter[(r, c)] = char

    return perimeter if not failed else {}


def draw_piece(perimeter: Dict[Tuple[int, int], str]) -> str:
    min_r, max_r = min(map(operator.itemgetter(0), perimeter)), max(map(operator.itemgetter(0), perimeter))
    min_c, max_c = min(map(operator.itemgetter(1), perimeter)), max(map(operator.itemgetter(1), perimeter))
    rows, cols = max_r - min_r + 1, max_c - min_c + 1
    mat = [[' '] * cols for _ in range(rows)]

    for (r, c), char in perimeter.items():
        t_r, t_c = r - min_r, c - min_c

        # Replace unnecessary joints.
        if char == '+':
            if perimeter.get((r, c - 1), ' ') == '-' and perimeter.get((r, c + 1), ' ') == '-':
                char = '-'
            elif perimeter.get((r - 1, c), ' ') == '|' and perimeter.get((r + 1, c), ' ') == '|':
                char = '|'

        mat[t_r][t_c] = char

    return "\n".join(''.join(row).rstrip() for row in mat)


if __name__ == '__main__':
    from test import Test

    shape = '\n'.join(["+------------+",
                       "|            |",
                       "|            |",
                       "|            |",
                       "+------+-----+",
                       "|      |     |",
                       "|      |     |",
                       "+------+-----+"])

    solution = ['\n'.join(["+------------+",
                           "|            |",
                           "|            |",
                           "|            |",
                           "+------------+"]),
                '\n'.join(["+------+",
                           "|      |",
                           "|      |",
                           "+------+"]),
                '\n'.join(["+-----+",
                           "|     |",
                           "|     |",
                           "+-----+"])]

    # Test.assert_equals(sorted(break_pieces(shape)), sorted(solution))

    shape = """
+-------------------+--+
|                   |  |
|                   |  |
|  +----------------+  |
|  |                   |
|  |                   |
+--+-------------------+
"""
    # for piece in break_pieces(shape.strip()):
    #     print(piece)

    shape = """
           +-+             
           | |             
         +-+-+-+           
         |     |           
      +--+-----+--+        
      |           |        
   +--+-----------+--+     
   |                 |     
   +-----------------+     
"""

    for piece in break_pieces(shape[1:-1]):
        print(piece)
