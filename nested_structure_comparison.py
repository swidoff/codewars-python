def same_structure_as(original, other):
    orig_arr = type(original) is list
    other_arr = type(other) is list
    if orig_arr and other_arr:
        return len(original) == len(other) and all(same_structure_as(x, y) for x, y in zip(original, other))
    elif orig_arr or other_arr:
        return False
    else:
        return True


if __name__ == '__main__':
    assert same_structure_as([1, [1, 1]], [2, [2, 2]])
    assert not same_structure_as([1, [1, 1]], [[2, 2], 2])
    assert same_structure_as([1, '[', ']'], ['[', ']', 1])
