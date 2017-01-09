import simplejson as json

from auslib.global_state import dbo
from auslib.test.admin.views.base import ViewTest


class TestUsersAPI_JSON(ViewTest):

    def testUsers(self):
        ret = self._get('/users')
        self.assertEqual(ret.status_code, 200)
        data = json.loads(ret.data)
        data['users'] = set(data['users'])
        self.assertEqual(data, dict(users=set(['bill', 'billy', 'bob', 'ashanti', 'mary'])))


class TestPermissionsAPI_JSON(ViewTest):

    def testPermissionsCollection(self):
        ret = self._get('/users/bill/permissions')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(json.loads(ret.data), dict(admin=dict(options=None, data_version=1)))

    def testPermissionGet(self):
        ret = self._get('/users/bill/permissions/admin')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(json.loads(ret.data), dict(options=None, data_version=1))

    def testPermissionGetMissing(self):
        ret = self.client.get("/users/bill/permissions/rule")
        self.assertEqual(ret.status_code, 404)

    def testPermissionPut(self):
        ret = self._put('/users/bob/permissions/admin', data=dict(options=json.dumps(dict(products=["a"]))))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=1)), "Data: %s" % ret.data)
        query = dbo.permissions.t.select()
        query = query.where(dbo.permissions.username == 'bob')
        query = query.where(dbo.permissions.permission == 'admin')
        self.assertEqual(query.execute().fetchone(), ('admin', 'bob', {"products": ["a"]}, 1))

    def testPermissionPutWithEmail(self):
        ret = self._put('/users/bob@bobsworld.com/permissions/admin', data=dict(options=json.dumps(dict(products=["a"]))))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=1)), "Data: %s" % ret.data)
        query = dbo.permissions.t.select()
        query = query.where(dbo.permissions.username == 'bob@bobsworld.com')
        query = query.where(dbo.permissions.permission == 'admin')
        self.assertEqual(query.execute().fetchone(), ('admin', 'bob@bobsworld.com', {"products": ["a"]}, 1))

    # This test is meant to verify that the app properly unquotes URL parts
    # as part of routing, because it is required when running under uwsgi.
    # Unfortunately, Werkzeug's test Client will unquote URL parts before
    # the app sees them, so this test doesn't actually verify that case...
    def testPermissionPutWithQuotedEmail(self):
        ret = self._put('/users/bob%40bobsworld.com/permissions/admin', data=dict(options=json.dumps(dict(products=["a"]))))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=1)), "Data: %s" % ret.data)
        query = dbo.permissions.t.select()
        query = query.where(dbo.permissions.username == 'bob@bobsworld.com')
        query = query.where(dbo.permissions.permission == 'admin')
        self.assertEqual(query.execute().fetchone(), ('admin', 'bob@bobsworld.com', {"products": ["a"]}, 1))

    def testPermissionsPostWithHttpRemoteUser(self):
        ret = self._httpRemoteUserPost('/users/bob/permissions/release_read_only', username="bob", data=dict(options=json.dumps(dict(products=["a", "b"])),
                                       data_version=1))
        self.assertEqual(ret.status_code, 200, ret.data)
        self.assertEqual(json.loads(ret.data), dict(new_data_version=2))
        r = dbo.permissions.t.select().where(dbo.permissions.username == 'bob').where(dbo.permissions.permission == "release_read_only").execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], ('release_read_only', 'bob', {"products": ["a", "b"]}, 2))

    def testPermissionsPost(self):
        ret = self._post('/users/bob/permissions/release_read_only', data=dict(options=json.dumps(dict(products=["a", "b"])), data_version=1))
        self.assertEqual(ret.status_code, 200, ret.data)
        self.assertEqual(json.loads(ret.data), dict(new_data_version=2))
        r = dbo.permissions.t.select().where(dbo.permissions.username == 'bob').where(dbo.permissions.permission == "release_read_only").execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], ('release_read_only', 'bob', {"products": ["a", "b"]}, 2))

    def testPermissionsPostMissing(self):
        ret = self._post("/users/bill/permissions/rule", data=dict(options="", data_version=1))
        self.assertStatusCode(ret, 404)

    def testPermissionsPostBadInput(self):
        ret = self._post("/users/bill/permissions/admin")
        self.assertStatusCode(ret, 400)

    def testPermissionsPostWithoutPermission(self):
        ret = self._post("/users/bob/permissions/rule", username="shane", data=dict(data_version=1, options=json.dumps(dict(actions=["create"]))))
        self.assertStatusCode(ret, 403)

    def testPermissionPutWithOption(self):
        ret = self._put('/users/bob/permissions/release_locale', data=dict(options=json.dumps(dict(products=['a']))))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=1)), "Data: %s" % ret.data)
        query = dbo.permissions.t.select()
        query = query.where(dbo.permissions.username == 'bob')
        query = query.where(dbo.permissions.permission == 'release_locale')
        self.assertEqual(query.execute().fetchone(), ('release_locale', 'bob', dict(products=['a']), 1))

    def testPermissionModify(self):
        ret = self._put('/users/bob/permissions/rule',
                        data=dict(options=json.dumps(dict(products=['a', 'b'])), data_version=1))
        self.assertStatusCode(ret, 200)
        self.assertEqual(json.loads(ret.data), dict(new_data_version=2))
        query = dbo.permissions.t.select()
        query = query.where(dbo.permissions.username == 'bob')
        query = query.where(dbo.permissions.permission == 'rule')
        self.assertEqual(query.execute().fetchone(), ('rule', 'bob', dict(products=['a', 'b']), 2))

    def testPermissionModifyWithoutDataVersion(self):
        ret = self._put("/users/bob/permissions/release",
                        data=dict(options=json.dumps(dict(products=["different"]))))
        self.assertStatusCode(ret, 400)

    def testPermissionPutBadPermission(self):
        ret = self._put('/users/bob/permissions/fake')
        self.assertStatusCode(ret, 400)

    def testPermissionPutBadOption(self):
        ret = self._put('/users/bob/permissions/admin', data=dict(options=json.dumps(dict(foo=2))))
        self.assertStatusCode(ret, 400)

    # Discovered in https://bugzilla.mozilla.org/show_bug.cgi?id=1237264
    def testPermissionPutBadJSON(self):
        ret = self._put("/users/ashanti/permissions/rule", data=dict(options='{"products":'))
        self.assertStatusCode(ret, 400)

    def testPermissionPutWithoutPermission(self):
        ret = self._put('/users/bob/permissions/admin', username="joseph")
        self.assertStatusCode(ret, 403)

    def testPermissionDelete(self):
        ret = self._delete('/users/bob/permissions/release_read_only', qs=dict(data_version=1))
        self.assertStatusCode(ret, 200)
        query = dbo.permissions.t.select()
        query = query.where(dbo.permissions.username == 'bob')
        query = query.where(dbo.permissions.permission == 'release_read_only')
        self.assertEqual(query.execute().fetchone(), None)

    def testPermissionDeleteMissing(self):
        ret = self._delete("/users/bill/permissions/release")
        self.assertStatusCode(ret, 404)

    def testPermissionDeleteBadInput(self):
        ret = self._delete("/users/bill/permissions/admin")
        self.assertStatusCode(ret, 400)

    def testPermissionDeleteWithoutPermission(self):
        ret = self._delete("/users/bob/permissions/permission", qs=dict(data_version=1), username="anna")
        self.assertStatusCode(ret, 403)


class TestUserRolesAPI_JSON(ViewTest):

    def testGetRoles(self):
        ret = self._get("/users/bill/roles")
        self.assertStatusCode(ret, 200)
        got = set(json.loads(ret.data)["roles"])
        self.assertEquals(got, set(["releng", "qa"]))

    def testGetRolesMissingUserReturnsEmptyList(self):
        ret = self.client.get("/users/dean/roles")
        self.assertStatusCode(ret, 200)

    def testGrantRole(self):
        ret = self._put("/users/ashanti/roles/dev")
        self.assertStatusCode(ret, 201)
        self.assertEquals(ret.data, json.dumps(dict(new_data_version=1)), ret.data)
        got = dbo.permissions.user_roles.t.select().where(dbo.permissions.user_roles.username == "ashanti").execute().fetchall()
        self.assertEquals(got, [("ashanti", "dev", 1)])

    def testGrantExistingRole(self):
        ret = self._put("/users/bill/roles/releng")
        self.assertStatusCode(ret, 200)
        self.assertEquals(ret.data, json.dumps(dict(new_data_version=1)), ret.data)
        got = dbo.permissions.user_roles.t.select().where(dbo.permissions.user_roles.username == "bill").execute().fetchall()
        self.assertEquals(got, [("bill", "qa", 1), ("bill", "releng", 1)])

    def testGrantRoleWithoutPermission(self):
        ret = self._put("/users/emily/roles/relman", username="rory", data=dict(data_version=1))
        self.assertStatusCode(ret, 403)

    def testRevokeRole(self):
        ret = self._delete("/users/bob/roles/relman", qs=dict(data_version=1))
        self.assertStatusCode(ret, 200)
        got = dbo.permissions.user_roles.t.select().where(dbo.permissions.user_roles.username == "bob").execute().fetchall()
        self.assertEquals(got, [])

    def testRevokeRoleWithoutPermission(self):
        ret = self._delete("/users/bob/roles/relman", username="lane", qs=dict(data_version=1))
        self.assertStatusCode(ret, 403)

    def testRevokeRoleBadDataVersion(self):
        ret = self._delete("/users/bob/roles/relman", qs=dict(data_version=3))
        self.assertStatusCode(ret, 400)
