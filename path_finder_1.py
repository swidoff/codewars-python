from collections import deque


def path_finder(maze):
    grid = maze.split("\n")
    N = len(grid)
    q = deque([(0, 0)])
    seen = {(0, 0)}

    while q:
        x, y = q.popleft()
        if x == y == N - 1:
            return True

        for x_offset, y_offset in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x = x + x_offset
            new_y = y + y_offset
            if 0 <= new_x < N and 0 <= new_y < N and grid[new_y][new_x] != 'W' and not (new_x, new_y) in seen:
                seen.add((new_x, new_y))
                q.append((new_x, new_y))

    return False


if __name__ == '__main__':
    from test import Test
    a = "\n".join([
        ".W.",
        ".W.",
        "..."
    ])

    b = "\n".join([
        ".W.",
        ".W.",
        "W.."
    ])

    c = "\n".join([
        "......",
        "......",
        "......",
        "......",
        "......",
        "......"
    ])

    d = "\n".join([
        "......",
        "......",
        "......",
        "......",
        ".....W",
        "....W."
    ])

    Test.assert_equals(path_finder(a), True)
    Test.assert_equals(path_finder(b), False)
    Test.assert_equals(path_finder(c), True)
    Test.assert_equals(path_finder(d), False)