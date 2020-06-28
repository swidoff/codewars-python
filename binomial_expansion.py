import re

import math


def expand(expr):
    m = re.match(r'\((-?\d*)(\w)([-+]\d+)\)\^(\d+)', expr)
    a = int(m.group(1) if m.group(1)[-1:].isdigit() else m.group(1) + '1')
    x = m.group(2)
    b = int(m.group(3))
    n = int(m.group(4))

    if n == 0:
        return "1"

    terms = []
    for i in range(n, -1, -1):
        binomial = math.factorial(n) // (math.factorial(i) * math.factorial(n - i))
        coefficient = binomial * a ** i * b ** (n - i)
        if coefficient != 0:
            sign = '-' if coefficient < 0 else ('+' if terms else '')
            c_str = str(abs(coefficient)) if abs(coefficient) != 1 or i == 0 else ''
            exp_str = '' if i == 0 else x + (f"^{str(i)}" if i > 1 else "")
            terms.append(sign + c_str + exp_str)

    return ''.join(terms)


if __name__ == '__main__':
    from test import Test

    Test.assert_equals(expand("(x+1)^0"), "1")
    Test.assert_equals(expand("(x+1)^1"), "x+1")
    Test.assert_equals(expand("(x+1)^2"), "x^2+2x+1")

    Test.assert_equals(expand("(x-1)^0"), "1")
    Test.assert_equals(expand("(x-1)^1"), "x-1")
    Test.assert_equals(expand("(x-1)^2"), "x^2-2x+1")

    Test.assert_equals(expand("(5m+3)^4"), "625m^4+1500m^3+1350m^2+540m+81")
    Test.assert_equals(expand("(2x-3)^3"), "8x^3-36x^2+54x-27")
    Test.assert_equals(expand("(7x-7)^0"), "1")

    Test.assert_equals(expand("(-5m+3)^4"), "625m^4-1500m^3+1350m^2-540m+81")
    Test.assert_equals(expand("(-2k-3)^3"), "-8k^3-36k^2-54k-27")
    Test.assert_equals(expand("(-7x-7)^0"), "1")
