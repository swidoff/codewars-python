def sudoku(puzzle):
    """return the solved puzzle as a 2d array of 9 x 9"""
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

    while unknown:
        found = False
        for r, c in list(unknown):
            sol = set(range(1, 10))
            sol &= row_remains[r]
            sol &= col_remains[c]
            sol &= box_remains[3 * (r // 3) + c // 3]
            assert len(sol), "Set management failed"
            if len(sol) == 1:
                val = sol.pop()
                puzzle[r][c] = val
                row_remains[r].remove(val)
                col_remains[c].remove(val)
                box_remains[3 * (r // 3) + c // 3].remove(val)
                unknown.remove((r, c))
                found = True
        assert found, "Deduction failed"

    return puzzle


if __name__ == '__main__':
    from test import Test

    Test.describe('Sudoku')

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

    Test.it('Puzzle 1')
    Test.assert_equals(sudoku(puzzle), solution, "Incorrect solution for the following puzzle: " + str(puzzle));
