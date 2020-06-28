def solve(s, ops):
    return do_solve(s, ops, seen={})[0]


def update_counts(c1, c2, op):
    t1, f1 = c1
    t2, f2 = c2
    if op == '|':
        res = t1 * (t2 + f2) + f1 * t2, f1 * f2
    elif op == '&':
        res = t1 * t2, t1 * f2 + f1 * (t2 + f2)
    else:
        res = t1 * f2 + f1 * t2, f1 * f2 + t1 * t2
    return res


def do_solve(s, ops, seen):
    if (s, ops) not in seen:
        if len(s) == 1:
            counts = (1, 0) if s == 't' else (0, 1)
        else:
            res = []
            for i in range(1, len(s)):
                left_count = do_solve(s[:i], ops[:i-1], seen)
                right_count = do_solve(s[i:], ops[i:], seen)
                res.append(update_counts(left_count, right_count, ops[i-1]))

            counts = tuple(sum(c) for c in zip(*res))

        seen[(s, ops)] = counts

    return seen[(s, ops)]


if __name__ == '__main__':
    from test import Test

    Test.it("Basic tests")
    Test.assert_equals(solve("tft", "^&"), 2)
    Test.assert_equals(solve("ttf", "|&"), 1)
    Test.assert_equals(solve("tff", "&&"), 0)
    Test.assert_equals(solve("tft", "&^"), 2)
    Test.assert_equals(solve("ftff", "^&&"), 0)
    Test.assert_equals(solve("ttft", "|&^"), 4)
    Test.assert_equals(solve("tftff", "&^&&"), 0)
    Test.assert_equals(solve("ttftff", "|&^&&"), 16)
    Test.assert_equals(solve("ttftfftf", "|&^&&||"), 339)
    Test.assert_equals(solve("ttftfftft", "|&^&&||^"), 851)
    Test.assert_equals(solve("ttftfftftf", "|&^&&||^&"), 2434)
