class add(int):
    def __call__(self, *args, **kwargs):
        return add(self + args[0])


if __name__ == '__main__':
    assert (add(1) == 1)
    assert (add(1)(2) == 3)
    assert (add(1)(2)(3) == 6)
