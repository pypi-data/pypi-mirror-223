"""
Integration tests against Trial's "dist reporter".
"""

from io import BytesIO, TextIOWrapper
from typing import TextIO

from subunit.v2 import ByteStreamToStreamResult
from testtools import StreamToDict, TestCase
from testtools.matchers import Always, HasLength
from testtools.twistedsupport import succeeded
from twisted.test.iosim import FakeTransport, connect
from twisted.trial._dist.worker import LocalWorkerAMP, WorkerProtocol

from .. import _SubunitReporter


class DistReporterTests(TestCase):
    """
    Tests for interactions between ``subunitreporter`` and trial's
    "distributed" reporter.
    """

    def test_addError(self):
        """
        If a test fails with an error then that error makes it into the subunit
        output stream.
        """
        # Set up a disttrial worker and coordinator communicating over the
        # disttrial AMP protocol.
        ampClient = WorkerProtocol()
        clientTransport = FakeTransport(ampClient, isServer=False)

        ampServer = LocalWorkerAMP()
        serverTransport = FakeTransport(ampServer, isServer=False)

        # Connect them to each other (in memory).
        pump = connect(ampServer, serverTransport, ampClient, clientTransport)

        # Get a test case to run.  The import is hidden here because we don't
        # want SomeTest discovered and run by the top-level runner.
        from .cases import SomeTest

        # Make a test case and run it.
        case = SomeTest("test_error")
        output = TextIOWrapper(BytesIO())
        subunitreporter = _SubunitReporter(output)
        d = ampServer.run(case, subunitreporter)

        # Let the coordinator and worker talk to each other.  The loop runs
        # until they run out of things to say.
        while pump.pump():
            pass

        self.assertThat(d, succeeded(Always()))

        # Inspect the subunit output our reporter produced to make sure it is
        # as we expect.
        output.seek(0)
        tests = parse_subunit(output)
        self.assertThat(tests, HasLength(1))
        self.assertThat(
            [test for test in tests if test['status'] == 'fail'],
            HasLength(1),
        )
        print(tests)


def parse_subunit(stream: TextIO) -> list[dict]:
    """
    Parse a subunit stream into a list of test results.
    """
    tests = []
    result = StreamToDict(tests.append)
    result.startTestRun()
    ByteStreamToStreamResult(stream).run(result)
    result.stopTestRun()
    return tests
