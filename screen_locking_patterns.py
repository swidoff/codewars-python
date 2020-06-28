from collections import deque

graph = {
    'A': {'C': 'B', 'G': 'D', 'I': 'E'},
    'B': {'H': 'E'},
    'C': {'I': 'F', 'A': 'B', 'G': 'E'},
    'D': {'F': 'E'},
    'E': {},
    'F': {'D': 'E'},
    'G': {'I': 'H', 'A': 'D', 'C': 'E'},
    'H': {'B': 'E'},
    'I': {'G': 'H', 'C': 'F', 'A': 'E'},
}


def count_patterns_from(firstPoint, length):
    if length > 9 or length <= 0:
        return 0
    elif length == 1:
        return 1

    count = 0
    q = deque([(firstPoint, {firstPoint})])
    while q:
        point, visited = q.popleft()
        if len(visited) == length:
            count += 1
        else:
            blocked = graph[point]
            for node in graph:
                if node not in visited and (node not in blocked or blocked[node] in visited):
                    q.append((node, visited | {node}))
    return count


if __name__ == '__main__':
    from test import Test

    Test.assert_equals(count_patterns_from('A', 10), 0)
    Test.assert_equals(count_patterns_from('A', 0), 0)
    Test.assert_equals(count_patterns_from('E', 14), 0)
    Test.assert_equals(count_patterns_from('B', 1), 1)
    Test.assert_equals(count_patterns_from('C', 2), 5)
    Test.assert_equals(count_patterns_from('E', 2), 8)
    Test.assert_equals(count_patterns_from('E', 4), 256)
