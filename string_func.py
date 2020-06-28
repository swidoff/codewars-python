def string_func(s, x):
    if x == 0:
        return s

    n = len(s)
    index_to_cycle_index = {}
    remaining = set(range(n))
    median = n // 2
    while remaining:
        cycle = []
        i = remaining.pop()
        j = 0
        while i not in index_to_cycle_index:
            cycle.append(i)
            index_to_cycle_index[i] = (cycle, j)
            remaining.discard(i)

            if i < median:
                i = i * 2 + 1
            else:
                i = (n - i - 1) * 2
            j += 1

    res = []
    for i in range(n):
        cycle, start_idx = index_to_cycle_index[i]
        end_idx = cycle[start_idx - x % len(cycle)]
        res.append(s[end_idx])

    return ''.join(res)


if __name__ == '__main__':
    from test import Test

    Test.assert_equals(string_func("This is a string exemplification!", 0), "This is a string exemplification!")
    Test.assert_equals(string_func("String", 3), "nrtgSi")
    Test.assert_equals(string_func("abcde", 1), "eadbc")
    Test.assert_equals(string_func("String for test: incommensurability", 1), "ySttirliinbga rfuosrn etmemsotc:n i")
    Test.assert_equals(string_func("Ohh Man God Damn", 7), " nGOnmohaadhMD  ")
    Test.assert_equals(string_func("Ohh Man God Damnn", 19), "haG mnad MhO noDn")
