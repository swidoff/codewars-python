import re
from itertools import groupby


class Term(object):
    def __init__(self, coef, vars):
        self.coef = coef
        self.vars = vars

    def to_term_str(self, pos: int) -> str:
        sign = '-' if self.coef < 0 else '+' if pos > 0 else ''
        coef = str(abs(self.coef) if abs(self.coef) != 1 else '')
        return f"{sign}{coef}{self.vars}"


term_pattern = r"([+-]?)(\d*)(\w+)"


def simplify(poly):
    # Parse into term objects with sorted variable lists
    terms = [
        Term(int(f"{sign}{coef if coef else '1'}"), ''.join(sorted(vars)))
        for sign, coef, vars in re.findall(term_pattern, poly)
    ]

    # Order by number of variables
    terms = sorted(terms, key=lambda t: (len(t.vars), t.vars))

    # Reduce terms of like variables
    terms = [
        Term(sum([t.coef for t in like_terms]), vars)
        for vars, like_terms in groupby(terms, key=lambda t: t.vars)
    ]

    # Join terms into a string
    return ''.join(term.to_term_str(i) for i, term in enumerate(terms) if term.coef != 0)


if __name__ == '__main__':
    assert simplify("dc+dcba") == "cd+abcd"
    assert simplify("2xy-yx") == "xy"
    assert simplify("-a+5ab+3a-c-2a") == "-c+5ab"
    assert simplify("-abc+3a+2ac") == "3a+2ac-abc"
    assert simplify("xyz-xz") == "-xz+xyz"
    assert simplify("a+ca-ab") == "a-ab+ac"
    assert simplify("xzy+zby") == "byz+xyz"
    assert simplify("-y+x") == "x-y"
    assert simplify("y-x") == "-x+y"
