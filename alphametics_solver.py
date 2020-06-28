import re
from collections import namedtuple, Counter
from itertools import permutations

State = namedtuple('State', ['equation', 'place', 'carry', 'counter', 'remaining', 'mapping'])

def alphametics(puzzle):
    equation = tuple(re.split(r'\W+', puzzle))
    letters = {c for c in puzzle if c.isalpha()}
    initial_state = State(equation, -1, 0, Counter(letters), letters, {})
    final_state = search(initial_state)
    return ''.join(str(final_state.mapping.get(c, '?')) if c.isalpha() else c for c in puzzle)


def search(state: State):
    if len(state.remaining) == 0:
        return state if is_valid(state) else None

    place_letters = [term[state.place] for term in state.equation if len(term) >= abs(state.place)]
    unassigned_numbers = sorted(set(range(10)) - set(state.mapping.values()), key=lambda l: state.counter[l])
    unassigned_letters = sorted(set(l for l in place_letters if l not in state.mapping))

    for assigned_numbers in permutations(unassigned_numbers, len(unassigned_letters)):
        new_mapping = dict(state.mapping)
        new_mapping.update(zip(unassigned_letters, assigned_numbers))
        lhs = sum(new_mapping[l] for l in place_letters[:-1]) + state.carry
        rhs = new_mapping[place_letters[-1]]
        lhs_digit = lhs % 10

        if lhs_digit == rhs:
            new_state = state._replace(
                place=state.place - 1,
                carry=lhs // 10,
                remaining=state.remaining - set(unassigned_letters),
                mapping=new_mapping)
            res = search(new_state)
            if res:
                return res

    return None


def is_valid(state):
    if any(state.mapping[eq[0]] == 0 for eq in state.equation):
        return False
    else:
        terms = [int(''.join(str(state.mapping[c]) for c in eq)) for eq in state.equation]
        return sum(terms[:-1]) == terms[-1]


if __name__ == '__main__':
    from test import Test as test

    test.describe('Example Tests')
    example_tests = (
        ('SEND + MORE = MONEY', '9567 + 1085 = 10652'),
        ('ZEROES + ONES = BINARY', '698392 + 3192 = 701584'),
        ('COUPLE + COUPLE = QUARTET', '653924 + 653924 = 1307848'),
        ('DO + YOU + FEEL = LUCKY', '57 + 870 + 9441 = 10368'),
        ('ELEVEN + NINE + FIVE + FIVE = THIRTY', '797275 + 5057 + 4027 + 4027 = 810386')
    )

    for inp, out in example_tests:
        test.assert_equals(alphametics(inp), out)

    print('<COMPLETEDIN::>')
