from testtools import TestCase


class SomeTest(TestCase):
    def test_error(self):
        raise Exception("some error")

