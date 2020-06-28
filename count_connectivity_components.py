import operator
from collections import Counter, deque
from typing import List, Dict, Set


def components(grid):
    graph = make_graph(grid)
    return count_components(graph)


def count_components(graph: List[List[int]]):
    sizes = []
    remaining = set(range(len(graph)))
    while remaining:
        node = remaining.pop()
        reachable = reachable_from(node, graph)
        remaining -= reachable
        sizes.append(len(reachable))

    return sorted(Counter(sizes).items(), key=operator.itemgetter(0), reverse=True)


def reachable_from(node: int, graph: List[List[int]]) -> Set[int]:
    seen = set()
    q = deque([node])
    while q:
        n1 = q.pop()
        seen.add(n1)
        for n2 in graph[n1]:
            if n2 not in seen:
                q.append(n2)
    return seen


def make_graph(grid: str) -> List[List[int]]:
    mat = list(map(str.strip, grid.splitlines()))
    rows = (len(mat) - 1) // 2
    columns = mat[0].count('+') - 1

    def is_connected(r1: int, c1: int, r2: int, c2: int) -> bool:
        div_y = (2 * r1 + 2 * r2 + 2) // 2
        div_x = (3 * c1 + 3 * c2 + 3) // 2
        char = mat[div_y][div_x]
        return char != '|' and char != '-'

    res = []
    for r in range(rows):
        for c in range(columns):
            edges = []
            for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                new_r, new_c = r + dr, c + dc
                if 0 <= new_r < rows and 0 <= new_c < columns and is_connected(r, c, new_r, new_c):
                    edges.append(new_r * columns + new_c)
            res.append(edges)

    return res


if __name__ == '__main__':
    from test import Test as test

    test.describe('Example Test Cases')
    test.assert_equals(components('''\
    +--+--+--+
    |  |  |  |
    +--+--+--+
    |  |  |  |
    +--+--+--+'''), [(1, 6)])

    test.assert_equals(components('''\
    +--+--+--+
    |  |     |
    +  +  +--+
    |  |  |  |
    +--+--+--+'''), [(3, 1), (2, 1), (1, 1)])

    test.assert_equals(components('''\
    +--+--+--+
    |  |     |
    +  +  +--+
    |        |
    +--+--+--+'''), [(6, 1)])

    test.assert_equals(components('''\
    +--+--+--+
    |        |
    +  +  +  +
    |        |
    +--+--+--+'''), [(6, 1)])
