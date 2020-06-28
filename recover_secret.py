from collections import defaultdict, deque


def recoverSecret(triplets):
    letters = set()
    comes_after = defaultdict(set)
    for t in triplets:
        letters.update(t)
        comes_after[t[1]].add(t[0])
        comes_after[t[2]].add(t[1])

    q = deque()
    for l in letters:
        if not comes_after[l]:
            q.append(l)

    res = []
    while q:
        l = q.pop()
        res.append(l)

        for o, after in comes_after.items():
            if l in after:
                after.remove(l)
                if not after:
                    q.append(o)

    return ''.join(res)


if __name__ == '__main__':
    secret = "whatisup"
    triplets = [
        ['t', 'u', 'p'],
        ['w', 'h', 'i'],
        ['t', 's', 'u'],
        ['a', 't', 's'],
        ['h', 'a', 'p'],
        ['t', 'i', 's'],
        ['w', 'h', 's']
    ]

    assert recoverSecret(triplets) == secret
