def rot13(message):
    def shift(c: str):
        if c.isalpha():
            base = ord('a' if c.islower() else 'A')
            return chr((ord(c) - base + 13) % 26 + base)
        else:
            return c

    return ''.join(shift(c) for c in message)


if __name__ == '__main__':
    assert rot13("test") == "grfg"
    assert rot13("Test") == "Grfg"
