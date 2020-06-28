import operator
from collections import namedtuple, deque
from itertools import groupby
from typing import List, Any, Iterator, Dict
from functools import reduce

Term = namedtuple("Term", ["coef", "var"])


def simplify(examples, formula):
    rules = {}
    for ex in examples:
        lhs, rhs = ex.split('=')
        rules[rhs.strip()] = merge(list(parse(lhs)))

    terms = merge(list(parse(formula)))
    while len(terms) > 1 or terms[0].var in rules:
        terms = merge([
            new_term
            for term in terms
            for new_term in substitute(term, rules)
        ])

    return f"{terms[0].coef}{terms[0].var}"


def substitute(term: Term, rules: Dict[str, List[Term]]) -> List[Term]:
    if term.var in rules:
        return [Term(term.coef * s.coef, s.var) for s in rules[term.var]]
    else:
        return [term]


def merge(terms: List[Term]) -> List[Term]:
    key = operator.attrgetter('var')
    return [
        Term(sum(t.coef for t in terms), var)
        for var, terms in groupby(sorted(terms, key=key), key=key)
    ]


def parse(equation: str) -> Iterator[Term]:
    stack = deque()
    for tok in tokenize(equation):
        if type(tok) is int:
            stack.append(tok)
        elif tok == ')':
            stack.pop()
        elif tok.isalpha():
            coef = reduce(operator.mul, stack, 1)
            stack.pop()
            yield Term(coef, tok)


def tokenize(equation) -> Iterator[Any]:
    q = []
    for c in equation:
        if c.isnumeric() or c == '-' or c == '+':
            q.append(c)
        elif not c.isspace():  # Paren or letter
            if not q and c != ')':
                q.append('1')

            if q:
                if not q[-1].isnumeric():
                    q.append('1')
                yield int(''.join(q))
                q.clear()

            yield c


if __name__ == '__main__':
    from test import Test

    examples = [["a + a = b", "b - d = c", "a + b = d"],
                ["a + 3g = k", "-70a = g"],
                ["-j -j -j + j = b"]
                ]
    formula = ["c + a + b",
               "-k + a",
               "-j - b"
               ]
    answer = ["2a",
              "210a",
              "1j"
              ]

    for i in range(len(answer)):
        print('examples:' + str(examples[i]))
        print('formula:' + str(formula[i]))
        print('expected answer:' + str(answer[i]))
        Test.assert_equals(simplify(examples[i], formula[i]), answer[i])

    Test.assert_equals(simplify(['(-3f + q) + r = l', '4f + q = r', '-10f = q'], '20l + 20(q - 200f)'), '-4580f')
