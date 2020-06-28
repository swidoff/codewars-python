def spiralize(size):
    mat = [[0] * size for _ in range(size)]
    do_spiralize(size, mat, offset=0)
    return mat


def do_spiralize(size, mat, offset):
    if size <= 0:
        return
    else:
        for c in range(offset, size + offset):
            mat[offset][c] = 1
        for r in range(offset + 1, size + offset):
            mat[r][offset + size - 1] = 1
        if size > 2:
            for c in range(offset, size + offset - 1):
                mat[offset + size - 1][c] = 1
            for r in range(offset + 2, size + offset - 1):
                mat[r][offset] = 1

        new_size = size - 4
        if new_size > 0:
            mat[offset + 2][offset + 1] = 1

        do_spiralize(new_size, mat, offset + 2)


if __name__ == '__main__':
    from test import Test

    Test.assert_equals(spiralize(5), [[1, 1, 1, 1, 1],
                                      [0, 0, 0, 0, 1],
                                      [1, 1, 1, 0, 1],
                                      [1, 0, 0, 0, 1],
                                      [1, 1, 1, 1, 1]])
    Test.assert_equals(spiralize(6), [[1, 1, 1, 1, 1, 1],
                                      [0, 0, 0, 0, 0, 1],
                                      [1, 1, 1, 1, 0, 1],
                                      [1, 0, 0, 1, 0, 1],
                                      [1, 0, 0, 0, 0, 1],
                                      [1, 1, 1, 1, 1, 1]])

    Test.assert_equals(spiralize(8), [[1, 1, 1, 1, 1, 1, 1, 1],
                                      [0, 0, 0, 0, 0, 0, 0, 1],
                                      [1, 1, 1, 1, 1, 1, 0, 1],
                                      [1, 0, 0, 0, 0, 1, 0, 1],
                                      [1, 0, 1, 0, 0, 1, 0, 1],
                                      [1, 0, 1, 1, 1, 1, 0, 1],
                                      [1, 0, 0, 0, 0, 0, 0, 1],
                                      [1, 1, 1, 1, 1, 1, 1, 1]])
