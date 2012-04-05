import simplejson as json

from auslib.web.base import db
from auslib.test.web.views.base import ViewTest, JSONTestMixin, HTMLTestMixin

class TestPermissionsAPI_JSON(ViewTest, JSONTestMixin):
    def testUsers(self):
        ret = self._get('/users')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(json.loads(ret.data), dict(users=['bill', 'bob']))

    def testPermissionsCollection(self):
        ret = self._get('/users/bill/permissions')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(json.loads(ret.data), dict(admin=dict(options=None, data_version=1)))

    def testPermissionGet(self):
        ret = self._get('/users/bill/permissions/admin')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(json.loads(ret.data), dict(options=None, data_version=1))

    def testPermissionPut(self):
        ret = self._put('/users/bob/permissions/admin')
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=1)), "Data: %s" % ret.data)
        query = db.permissions.t.select()
        query = query.where(db.permissions.username=='bob')
        query = query.where(db.permissions.permission=='admin')
        self.assertEqual(query.execute().fetchone(), ('admin', 'bob', None, 1))

    def testPermissionsPost(self):
        ret = self._post('/users/bill/permissions/admin', data=dict(options="", data_version=1))
        self.assertEqual(ret.status_code, 200, "Status Code: %d" % ret.status_code)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        r = db.permissions.t.select().where(db.permissions.username=='bill').execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], ('admin', 'bill', None, 2))

    def testPermissionUrl(self):
        ret = self._put('/users/cathy/permissions/releases/:name')
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=1)), "Data: %s" % ret.data)
        query = db.permissions.t.select()
        query = query.where(db.permissions.username=='cathy')
        query = query.where(db.permissions.permission=='/releases/:name')
        self.assertEqual(query.execute().fetchone(), ('/releases/:name', 'cathy', None, 1))

    def testPermissionPutWithOption(self):
        ret = self._put('/users/bob/permissions/rules', data=dict(options=json.dumps(dict(product='fake'))))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=1)), "Data: %s" % ret.data)
        query = db.permissions.t.select()
        query = query.where(db.permissions.username=='bob')
        query = query.where(db.permissions.permission=='/rules')
        self.assertEqual(query.execute().fetchone(), ('/rules', 'bob', json.dumps(dict(product='fake')), 1))

    def testPermissionModify(self):
        ret = self._put('/users/bob/permissions/releases/:name',
            data=dict(options=json.dumps(dict(product='different')), data_version=1))
        self.assertStatusCode(ret, 200)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        query = db.permissions.t.select()
        query = query.where(db.permissions.username=='bob')
        query = query.where(db.permissions.permission=='/releases/:name')
        self.assertEqual(query.execute().fetchone(), ('/releases/:name', 'bob', json.dumps(dict(product='different')), 2))

    def testPermissionPutBadPermission(self):
        ret = self._put('/users/bob/permissions/fake')
        self.assertStatusCode(ret, 400)
        
    def testPermissionPutBadOption(self):
        ret = self._put('/users/bob/permissions/admin', data=dict(options=json.dumps(dict(foo=2))))
        self.assertStatusCode(ret, 400)

    def testPermissionDelete(self):
        ret = self._delete('/users/bob/permissions/users/:id/permissions/:permission', qs=dict(data_version=1))
        self.assertStatusCode(ret, 200)
        query = db.permissions.t.select()
        query = query.where(db.permissions.username=='bob')
        query = query.where(db.permissions.permission=='/users/:id/permissions/:permission')
        self.assertEqual(query.execute().fetchone(), None)


class TestPermissionsPage(ViewTest, HTMLTestMixin):
    def testGet(self):
        ret = self._get('/permissions.html')
        self.assertEqual(ret.status_code, 200)
        self.assertTrue('bill' in ret.data, msg=ret.data)
        self.assertTrue('bob' in ret.data, msg=ret.data)

class TestUserPermissionsPage(ViewTest, HTMLTestMixin):
    def testGet(self):
        ret = self._get('/user_permissions.html', query_string=dict(username='bill'))
        self.assertEqual(ret.status_code, 200)
        self.assertTrue('admin' in ret.data, msg=ret.data)
