import mock

from .base import ViewTest


class TestDockerflowEndpoints(ViewTest):
    @mock.patch("auslib.web.admin.base.statsd.timer")
    def testVersion(self, mocked_timer):
        ret = self.client.get("/__version__")
        self.assertEqual(
            ret.text,
            """
{
  "source":"https://github.com/mozilla-releng/balrog",
  "version":"1.0",
  "commit":"abcdef123456"
}
""",
        )
        assert mocked_timer.call_count == 0

    @mock.patch("auslib.web.admin.base.statsd.timer")
    def testHeartbeat(self, mocked_timer):
        with mock.patch("auslib.global_state.dbo.dockerflow.incrementWatchdogValue") as cr:
            cr.side_effect = (1, 2, 3)
            for i in range(1, 3):
                ret = self.client.get("/__heartbeat__")
                self.assertEqual(ret.status_code, 200)
                self.assertEqual(cr.call_count, i)
                self.assertEqual(ret.headers["Cache-Control"], "public, max-age=60")
                returned_digit = int(ret.text)
                self.assertEqual(returned_digit, i)
        assert mocked_timer.call_count == 0

    @mock.patch("auslib.web.admin.base.statsd.timer")
    def testHeartbeatWithException(self, mocked_timer):
        with mock.patch("auslib.global_state.dbo.dockerflow.incrementWatchdogValue") as cr:
            cr.side_effect = Exception("kabom!")
            # Because there's no web server between us and the endpoint, we receive
            # the Exception directly instead of a 500 error
            ret = self.client.get("/__heartbeat__")
            self.assertEqual(ret.status_code, 502)
            self.assertEqual(ret.text, "Can't connect to the database.")
            self.assertEqual(ret.headers["Cache-Control"], "public, max-age=60")
            self.assertEqual(cr.call_count, 1)
        assert mocked_timer.call_count == 0

    @mock.patch("auslib.web.admin.base.statsd.timer")
    def testLbHeartbeat(self, mocked_timer):
        ret = self.client.get("/__lbheartbeat__")
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.headers["Cache-Control"], "no-cache")
        assert mocked_timer.call_count == 0
