from collections import Counter


def scramble(s1, s2):
    counter1 = Counter(s1)
    counter2 = Counter(s2)
    return len(counter2 - counter1) == 0


if __name__ == '__main__':
    assert scramble('rkqodlw', 'world')
    assert scramble('cedewaraaossoqqyt', 'codewars')
    assert not scramble('katas', 'steak')
    assert scramble('scriptjava', 'javascript')
    assert scramble('scriptingjava', 'javascript')
