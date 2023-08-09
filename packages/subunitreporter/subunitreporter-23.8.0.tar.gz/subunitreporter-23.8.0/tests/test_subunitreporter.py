from unittest import TestCase, skip as skip_

class ATest(TestCase):
    def test_pass(self):
        pass

    def test_fail(self):
        self.fail("failure")

    def test_error(self):
        raise Exception("error")

    @skip_("skip")
    def test_skip(self):
        pass

    def test_expected_failure(self):
        self.fail("failure")
    test_expected_failure.todo = "expected failure"

    def test_unexpected_success(self):
        pass
    test_expected_failure.todo = "unexpected success"
    
