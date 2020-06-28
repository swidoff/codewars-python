from test import Test
from typing import Iterator


def rail_fence_cipher_indexes(msg_len: int, num_rails: int) -> Iterator[int]:
    """
    Returns a generator that produces the series of source message indexes in the order they appear in the encoded
    message.

    :param msg_len: the len of the message to be encoded/decoded
    :param num_rails: the number of rails
    :return: a generator of (source_msg_index, target_msg_index)
    """
    max_inc = num_rails * 2 - 2
    for rail in range(num_rails):
        src_index = rail
        inc = max_inc - 2 * rail if rail < num_rails - 1 else max_inc
        while src_index < msg_len:
            yield src_index
            src_index += inc
            inc = max_inc - inc if inc < max_inc else max_inc


def encode_rail_fence_cipher(string, n):
    res = [''] * len(string)
    for target_index, src_index in enumerate(rail_fence_cipher_indexes(len(string), n)):
        res[target_index] = string[src_index]

    return ''.join(res)


def decode_rail_fence_cipher(string, n):
    res = [''] * len(string)
    for target_index, src_index in enumerate(rail_fence_cipher_indexes(len(string), n)):
        res[src_index] = string[target_index]

    return ''.join(res)


if __name__ == '__main__':
    Test.assert_equals(encode_rail_fence_cipher("WEAREDISCOVEREDFLEEATONCE", 3), "WECRLTEERDSOEEFEAOCAIVDEN")
    Test.assert_equals(encode_rail_fence_cipher("Hello, World!", 3), "Hoo!el,Wrdl l")
    Test.assert_equals(encode_rail_fence_cipher("Hello, World!", 4), "H !e,Wdloollr")
    Test.assert_equals(encode_rail_fence_cipher("", 3), "")

    Test.assert_equals(decode_rail_fence_cipher("H !e,Wdloollr", 4), "Hello, World!")
    Test.assert_equals(decode_rail_fence_cipher("WECRLTEERDSOEEFEAOCAIVDEN", 3), "WEAREDISCOVEREDFLEEATONCE")
    Test.assert_equals(decode_rail_fence_cipher("", 3), "")
