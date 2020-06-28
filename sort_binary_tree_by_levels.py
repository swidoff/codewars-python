class Node:
    def __init__(self, L, R, n):
        self.left = L
        self.right = R
        self.value = n


from collections import deque


def tree_by_levels(node):
    q = deque()

    if node:
        q.append(node)

    res = []
    while q:
        n = q.popleft()
        res.append(n.value)

        if n.left:
            q.append(n.left)

        if n.right:
            q.append(n.right)

    return res


if __name__ == '__main__':
    assert tree_by_levels(None) == []
    assert tree_by_levels(
        Node(Node(None, Node(None, None, 4), 2), Node(Node(None, None, 5), Node(None, None, 6), 3), 1)), [1, 2, 3, 4, 5,
                                                                                                          6]
