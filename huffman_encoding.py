import math
import operator
from collections import Counter, deque
from functools import reduce
from itertools import product, chain
from typing import Tuple, List
import heapq


def frequencies(s):
    return list(Counter(s).items())


def freqs_to_code(freqs: List[Tuple[str, int]]) -> List[Tuple[str, str]]:
    q = [(count, i, {letter: ""}) for i, (letter, count) in enumerate(freqs)]
    heapq.heapify(q)

    while len(q) > 1:
        left_count, i, left_codes = heapq.heappop(q)
        right_count, _, right_codes = heapq.heappop(q)
        heapq.heappush(q, (left_count + right_count, i, {
            letter: code
            for letter, code in zip(
                chain(left_codes.keys(), right_codes.keys()),
                chain(("0" + v for v in left_codes.values()), ("1" + v for v in right_codes.values()))
            )
        }))

    return list(q[0][2].items())


# takes: [ (str, int) ], str; returns: String (with "0" and "1")
def encode(freqs, s):
    if len(freqs) <= 1:
        return None
    if not s:
        return ''

    code = dict(freqs_to_code(freqs))
    return ''.join(code[l] for l in s)


# takes [ [str, int] ], str (with "0" and "1"); returns: str
def decode(freqs, bits):
    if len(freqs) <= 1:
        return None
    if not bits:
        return ''

    reverse_code = {code: letter for letter, code in freqs_to_code(freqs)}
    res = []
    i = 0
    for j in range(1, len(bits) + 1):
        if bits[i:j] in reverse_code:
            res.append(reverse_code[bits[i:j]])
            i = j
    return ''.join(res)


if __name__ == '__main__':
    from test import Test as test

    test.describe("basic tests")
    fs = frequencies("aaaabcc")
    test.it("aaaabcc encoded should have length 10")


    def test_len(res):
        test.assert_not_equals(res, None)
        test.assert_equals(len(res), 10)


    test_len(encode(fs, "aaaabcc"))

    test.it("empty list encode")
    test.assert_equals(encode(fs, []), '')

    test.it("empty list decode")
    test.assert_equals(decode(fs, []), '')


    def test_enc_len(fs, strs, lens):
        def enc_len(s):
            return len(encode(fs, s))

        test.assert_equals(list(map(enc_len, strs)), lens)


    test.describe("length")
    test.it("equal lengths with same frequencies if alphabet size is a power of two")
    test_enc_len([('a', 1), ('b', 1)], ["a", "b"], [1, 1])

    test.it("smaller length for higher frequency, if size of alphabet is not power of two")
    test_enc_len([('a', 1), ('b', 1), ('c', 2)], ["a", "b", "c"], [2, 2, 1])

    test.describe("error handling")
    s = "aaaabcc"
    fs = frequencies(s)
    test.assert_equals(sorted(fs), [("a", 4), ("b", 1), ("c", 2)])
    test_enc_len(fs, [s], [10])
    test.assert_equals(encode(fs, ""), "")
    test.assert_equals(decode(fs, ""), "")

    test.assert_equals(encode([], ""), None)
    test.assert_equals(decode([], ""), None)
    test.assert_equals(encode([('a', 1)], ""), None)
    test.assert_equals(decode([('a', 1)], ""), None)

    fs = frequencies("abcdefgh")
    print(encode(fs, "abcdefgh"))
