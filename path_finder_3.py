from test import Test

import heapq


def path_finder(area):
    mat = area.split('\n')
    N = len(mat)
    distances = {(0, 0): 0}
    q = [(0, 0, 0)]

    res = -1
    while q:
        dist, x, y = heapq.heappop(q)
        if x == y == N - 1:
            res = dist
            break

        for x_offset, y_offset in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x = x + x_offset
            new_y = y + y_offset
            if 0 <= new_x < N and 0 <= new_y < N:
                new_dist = dist + abs(int(mat[new_y][new_x]) - int(mat[y][x]))
                if new_dist < distances.get((new_x, new_y), 1e100):
                    distances[(new_x, new_y)] = new_dist
                    heapq.heappush(q, (new_dist, new_x, new_y))

    return res


if __name__ == '__main__':
    a = "\n".join([
        "000",
        "000",
        "000"
    ])

    b = "\n".join([
        "010",
        "010",
        "010"
    ])

    c = "\n".join([
        "010",
        "101",
        "010"
    ])

    d = "\n".join([
        "0707",
        "7070",
        "0707",
        "7070"
    ])

    e = "\n".join([
        "700000",
        "077770",
        "077770",
        "077770",
        "077770",
        "000007"
    ])

    f = "\n".join([
        "777000",
        "007000",
        "007000",
        "007000",
        "007000",
        "007777"
    ])

    g = "\n".join([
        "000000",
        "000000",
        "000000",
        "000010",
        "000109",
        "001010"
    ])

    Test.assert_equals(path_finder(a), 0)
    Test.assert_equals(path_finder(b), 2)
    Test.assert_equals(path_finder(c), 4)
    Test.assert_equals(path_finder(d), 42)
    Test.assert_equals(path_finder(e), 14)
    Test.assert_equals(path_finder(f), 0)
    Test.assert_equals(path_finder(g), 4)
