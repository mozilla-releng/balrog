from auslib.test.admin.views.base import ViewTest


class TestDockerflowEndpoints(ViewTest):

    def testVersion(self):
        ret = self.client.get("/__version__").json()
        print ret
        self.fail()
