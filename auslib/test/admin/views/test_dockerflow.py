import mock

from auslib.test.admin.views.base import ViewTest


class TestDockerflowEndpoints(ViewTest):

    def testVersion(self):
        ret = self.client.get("/__version__").json()
        print ret
        self.fail()

    def testHeartbeat(self):
        with mock.patch("auslib.global_state.dbo.rules.countRules") as cr:
            ret = self.client.get("/__heartbeat__")
            self.assertEqual(ret.status_code, 200)
            self.assertEqual(cr.call_count, 1)

    def testLbHeartbeat(self):
        ret = self.client.get("/__lbheartbeat__")
        self.assertEqual(ret.status_code, 200)
