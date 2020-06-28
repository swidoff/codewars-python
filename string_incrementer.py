import re


def increment_string(strng):
    match = re.search(r"(\d*)$", strng)
    digits = match.group(1)
    num_digits = len(digits)
    if num_digits == 0:
        return strng + "1"
    else:
        return f"{strng[:-num_digits]}{int(digits) + 1 :0{num_digits}d}"


if __name__ == '__main__':
    from test import Test

    Test.assert_equals(increment_string("foo"), "foo1")
    Test.assert_equals(increment_string("foobar001"), "foobar002")
    Test.assert_equals(increment_string("foobar1"), "foobar2")
    Test.assert_equals(increment_string("foobar00"), "foobar01")
    Test.assert_equals(increment_string("foobar99"), "foobar100")
    Test.assert_equals(increment_string("foobar099"), "foobar100")
    Test.assert_equals(increment_string(""), "1")
