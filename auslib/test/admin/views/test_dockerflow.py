import mock

from auslib.test.admin.views.base import ViewTest


class TestDockerflowEndpoints(ViewTest):

    def testVersion(self):
        ret = self.client.get("/__version__")
        self.assertEquals(ret.data, """
{
  "source":"https://github.com/mozilla/balrog",
  "version":"1.0",
  "commit":"abcdef123456"
}
""")

    def testHeartbeat(self):
        with mock.patch("auslib.global_state.dbo.dockerflow.incrementWatchdogValue") as cr:
            ret = self.client.get("/__heartbeat__")
            self.assertEqual(ret.status_code, 200)
            self.assertEqual(cr.call_count, 1)
            self.assertEqual(ret.headers["Cache-Control"], "no-cache")

    def testHeartbeatWithException(self):
        with mock.patch("auslib.global_state.dbo.dockerflow.incrementWatchdogValue") as cr:
            cr.side_effect = Exception("kabom!")
            # Because there's no web server between us and the endpoint, we receive
            # the Exception directly instead of a 500 error
            self.assertRaises(Exception, self.client.get, "/__heartbeat__")
            self.assertEqual(cr.call_count, 1)

    def testLbHeartbeat(self):
        ret = self.client.get("/__lbheartbeat__")
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.headers["Cache-Control"], "no-cache")
