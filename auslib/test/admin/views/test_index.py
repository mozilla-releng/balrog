from auslib.test.admin.views.base import ViewTest


class TestIndexPage(ViewTest):

    def testLandingPage(self):
        ret = self.client.get('/')
        self.assertStatusCode(ret, 200)
        # know thy fixtures
        self.assertTrue('5 rules' in ret.data)
        self.assertTrue('5 releases' in ret.data)
        self.assertTrue('2 users' in ret.data)
