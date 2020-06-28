def solution(args):
    if not args:
        return ''

    def format_values(values):
        return [f'{str(values[0])}-{str(values[-1])}'] if len(values) > 2 else [str(v) for v in values]

    res = []
    ls = [args[0]]
    for num in args[1:]:
        if num - ls[-1] != 1:
            res.extend(format_values(ls))
            ls.clear()
        ls.append(num)

    if ls:
        res.extend(format_values(ls))

    return ','.join(res)


if __name__ == '__main__':
    assert solution([-6, -3, -2, -1, 0, 1, 3, 4, 5, 7, 8, 9, 10, 11, 14, 15, 17, 18, 19, 20]) == '-6,-3-1,3-5,7-11,14,15,17-20'
    assert solution([-3, -2, -1, 2, 10, 15, 16, 18, 19, 20]) == '-3--1,2,10,15,16,18-20'
