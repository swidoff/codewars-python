class Test(object):

    @staticmethod
    def assert_equals(actual, expected, msg=""):
        try:
            assert expected == actual, msg
        except AssertionError as e:
            raise AssertionError(f"Expected was {str(expected)} actual was {str(actual)}")

    @staticmethod
    def assert_not_equals(actual, expected, msg=""):
        try:
            assert expected != actual, msg
        except AssertionError as e:
            raise AssertionError(f"Expected was {str(expected)} actual was {str(actual)}")


    @staticmethod
    def expect(actual, msg=""):
        Test.assert_equals(actual, True, msg)

    @staticmethod
    def it(msg: str):
        print(msg)

    describe = it