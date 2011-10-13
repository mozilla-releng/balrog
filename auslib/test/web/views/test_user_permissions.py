import simplejson as json

from auslib.web.base import db
from auslib.test.web.views.base import ViewTest, HTMLTestMixin

class TestUserPermissionsPage(ViewTest, HTMLTestMixin):
    def testGet(self):
        self.assertIn('admin', self._get('/user_permissions.html', query_string=dict(username='bill')).data)

    def testPost(self):
        ret = self._post('/users/bill/permissions/admin', data=dict(options="", data_version=1))
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        r = db.permissions.t.select().where(db.permissions.username=='bill').execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0], ('admin', 'bill', None, 2))
