import mock

from .test_client import ClientTestBase


class TestDockerflowEndpoints(ClientTestBase):
    def testVersion(self):
        ret = self.client.get("/__version__")
        self.assertEqual(
            ret.get_data(as_text=True),
            """
{
  "source":"https://github.com/mozilla/balrog",
  "version":"1.0",
  "commit":"abcdef123456"
}
""",
        )

    def testHeartbeat(self):
        with mock.patch("auslib.global_state.dbo.rules.count") as cr:
            ret = self.client.get("/__heartbeat__")
            self.assertEqual(ret.status_code, 200)
            self.assertEqual(cr.call_count, 1)
            self.assertEqual(ret.headers["Cache-Control"], "public, max-age=60")

    def testHeartbeatWithException(self):
        with mock.patch("auslib.global_state.dbo.rules.count") as cr:
            cr.side_effect = Exception("kabom!")
            # Because there's no web server between us and the endpoint, we receive
            # the Exception directly instead of a 500 error
            ret = self.client.get("/__heartbeat__")
            self.assertEqual(ret.status_code, 502)
            self.assertEqual(ret.get_data(as_text=True), "Can't connect to the database.")
            self.assertEqual(ret.headers["Cache-Control"], "public, max-age=60")
            self.assertEqual(cr.call_count, 1)

    def testLbHeartbeat(self):
        ret = self.client.get("/__lbheartbeat__")
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.headers["Cache-Control"], "no-cache")
