from auslib.test.web.views.base import ViewTest

class TestRequirepermission(ViewTest):
    def testAdmin(self):
        ret = self._put('/users/foo/permissions/admin')
        self.assertStatusCode(ret, 201)

    def testGranular(self):
        ret = self._put('/users/foo/permissions/admin', username='bob')
        self.assertStatusCode(ret, 201)
