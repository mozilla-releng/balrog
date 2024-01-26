import json

import mock

from auslib.global_state import dbo

from .base import ViewTest


class TestUsersAPI_JSON(ViewTest):
    def testUsers(self):
        ret = self._get("/users")
        self.assertEqual(ret.status_code, 200)
        data = ret.get_json()
        self.assertEqual(
            data,
            (
                {
                    "ashanti": {"roles": []},
                    "bill": {"roles": [{"role": "qa", "data_version": 1}, {"role": "releng", "data_version": 1}]},
                    "billy": {"roles": []},
                    "bob": {"roles": [{"role": "relman", "data_version": 1}]},
                    "julie": {"roles": [{"role": "releng", "data_version": 1}]},
                    "mary": {"roles": [{"role": "relman", "data_version": 1}]},
                    "zawadi": {"roles": []},
                }
            ),
        )


class TestNamedUserAPI_JSON(ViewTest):
    def testGetSelfPermissionWithoutRolesAndWithoutPermission(self):
        ret = self._get("/users/vikas", username="vikas")
        self.assertEqual(ret.status_code, 404)

    def testGetNamedUser(self):
        ret = self._get("/users/mary", username="bill")
        self.assertEqual(ret.status_code, 200)
        data = ret.get_json()
        expected = {
            "username": "mary",
            "permissions": {"scheduled_change": {"options": {"actions": ["enact"]}, "data_version": 1}},
            "roles": {"relman": {"data_version": 1}},
        }
        self.assertEqual(data, expected)

    def testGetNamedUserWithSpecificPermission(self):
        ret = self._get("/users/mary", username="bob")
        self.assertEqual(ret.status_code, 200)
        data = ret.get_json()
        expected = {
            "username": "mary",
            "permissions": {"scheduled_change": {"options": {"actions": ["enact"]}, "data_version": 1}},
            "roles": {"relman": {"data_version": 1}},
        }
        self.assertEqual(data, expected)

    def testGetNamedUserWithoutPermission(self):
        ret = self._get("/users/bill", username="mary")
        self.assertEqual(ret.status_code, 403)

    def testGetNonExistentUser(self):
        ret = self._get("/users/huetonhu", username="bill")
        self.assertEqual(ret.status_code, 404)


class TestPermissionsAPI_JSON(ViewTest):
    def testPermissionsCollection(self):
        ret = self._get("/users/bill/permissions", username="bill")
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.get_json(), dict(admin=dict(options=None, data_version=1)))

    def testPermissionsCollectionWithoutPermission(self):
        ret = self._get("/users/bill/permissions", username="mary")
        self.assertEqual(ret.status_code, 403)

    def testPermissionGet(self):
        ret = self._get("/users/bill/permissions/admin", username="bill")
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.get_json(), dict(options=None, data_version=1))

    def testPermissionGetWithoutPermission(self):
        ret = self._get("/users/bill/permissions/admin", username="mary")
        self.assertEqual(ret.status_code, 403)

    def testPermissionGetMissing(self):
        ret = self._get("/users/bill/permissions/rule", username="bill")
        self.assertEqual(ret.status_code, 404)

    def testPermissionPut(self):
        ret = self._put("/users/bob/permissions/admin", data=dict(options=json.dumps(dict(products=["a"]))))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.get_data(as_text=True), json.dumps(dict(new_data_version=1)), "Data: %s" % ret.get_data())
        query = dbo.permissions.t.select()
        query = query.where(dbo.permissions.username == "bob")
        query = query.where(dbo.permissions.permission == "admin")
        self.assertEqual(query.execute().fetchone(), ("admin", "bob", {"products": ["a"]}, 1))

    # TODO: find something that doesn't require signoff. and fix the damn ui
    def testPermissionPutEmptyDictOptions(self):
        # The default fixtures prevent us from creating permissions like this
        # due to signoff requirements
        dbo.permissionsRequiredSignoffs.t.delete().execute()
        ret = self._put("/users/bob/permissions/admin", data=dict(options="{}"))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.get_data(as_text=True), json.dumps(dict(new_data_version=1)), "Data: %s" % ret.get_data())
        query = dbo.permissions.t.select()
        query = query.where(dbo.permissions.username == "bob")
        query = query.where(dbo.permissions.permission == "admin")
        self.assertEqual(query.execute().fetchone(), ("admin", "bob", None, 1))

    def testPermissionPutWithEmail(self):
        ret = self._put("/users/bob@bobsworld.com/permissions/admin", data=dict(options=json.dumps(dict(products=["a"]))))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.get_data(as_text=True), json.dumps(dict(new_data_version=1)), "Data: %s" % ret.get_data())
        query = dbo.permissions.t.select()
        query = query.where(dbo.permissions.username == "bob@bobsworld.com")
        query = query.where(dbo.permissions.permission == "admin")
        self.assertEqual(query.execute().fetchone(), ("admin", "bob@bobsworld.com", {"products": ["a"]}, 1))

    # This test is meant to verify that the app properly unquotes URL parts
    # as part of routing, because it is required when running under uwsgi.
    # Unfortunately, Werkzeug's test Client will unquote URL parts before
    # the app sees them, so this test doesn't actually verify that case...
    def testPermissionPutWithQuotedEmail(self):
        ret = self._put("/users/bob%40bobsworld.com/permissions/admin", data=dict(options=json.dumps(dict(products=["a"]))))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.get_data(as_text=True), json.dumps(dict(new_data_version=1)), "Data: %s" % ret.get_data())
        query = dbo.permissions.t.select()
        query = query.where(dbo.permissions.username == "bob@bobsworld.com")
        query = query.where(dbo.permissions.permission == "admin")
        self.assertEqual(query.execute().fetchone(), ("admin", "bob@bobsworld.com", {"products": ["a"]}, 1))

    def testPermissionsPost(self):
        ret = self._post("/users/bob/permissions/release_read_only", data=dict(options=json.dumps(dict(products=["a", "b"])), data_version=1))
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), dict(new_data_version=2))
        r = dbo.permissions.t.select().where(dbo.permissions.username == "bob").where(dbo.permissions.permission == "release_read_only").execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0], ("release_read_only", "bob", {"products": ["a", "b"]}, 2))

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
        ret = self._put("/users/bob/permissions/release_locale", data=dict(options=json.dumps(dict(products=["a"]))))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.get_data(as_text=True), json.dumps(dict(new_data_version=1)), "Data: %s" % ret.get_data())
        query = dbo.permissions.t.select()
        query = query.where(dbo.permissions.username == "bob")
        query = query.where(dbo.permissions.permission == "release_locale")
        self.assertEqual(query.execute().fetchone(), ("release_locale", "bob", dict(products=["a"]), 1))

    def testPermissionPutThatRequiresSignoff(self):
        ret = self._put("/users/nancy/permissions/admin")
        self.assertStatusCode(ret, 400)
        self.assertIn("No Signoffs given", ret.get_data(as_text=True))

    def testPermissionModify(self):
        ret = self._put("/users/bob/permissions/rule", data=dict(options=json.dumps(dict(products=["a", "b"])), data_version=1))
        self.assertStatusCode(ret, 200)
        self.assertEqual(ret.get_json(), dict(new_data_version=2))
        query = dbo.permissions.t.select()
        query = query.where(dbo.permissions.username == "bob")
        query = query.where(dbo.permissions.permission == "rule")
        self.assertEqual(query.execute().fetchone(), ("rule", "bob", dict(products=["a", "b"]), 2))

    def testPermissionModifyWithoutDataVersion(self):
        ret = self._put("/users/bob/permissions/release", data=dict(options=json.dumps(dict(products=["different"]))))
        self.assertStatusCode(ret, 400)

    def testPermissionPutBadPermission(self):
        ret = self._put("/users/bob/permissions/fake")
        self.assertStatusCode(ret, 400)

    def testPermissionPutBadOption(self):
        ret = self._put("/users/bob/permissions/admin", data=dict(options=json.dumps(dict(foo=2))))
        self.assertStatusCode(ret, 400)

    # Discovered in https://bugzilla.mozilla.org/show_bug.cgi?id=1237264
    def testPermissionPutBadJSON(self):
        ret = self._put("/users/ashanti/permissions/rule", data=dict(options='{"products":'))
        self.assertStatusCode(ret, 400)

    def testPermissionPutWithoutPermission(self):
        ret = self._put("/users/bob/permissions/admin", username="julie")
        self.assertStatusCode(ret, 403)

    def testPermissionDelete(self):
        ret = self._delete("/users/bob/permissions/release_read_only", qs=dict(data_version=1))
        self.assertStatusCode(ret, 200)
        query = dbo.permissions.t.select()
        query = query.where(dbo.permissions.username == "bob")
        query = query.where(dbo.permissions.permission == "release_read_only")
        self.assertEqual(query.execute().fetchone(), None)

    def testPermissionDeleteMissing(self):
        ret = self._delete("/users/bill/permissions/release", qs={"data_version": 1})
        self.assertStatusCode(ret, 404)

    def testPermissionDeleteBadInput(self):
        ret = self._delete("/users/bill/permissions/admin")
        self.assertStatusCode(ret, 400)

    def testPermissionDeleteWithoutPermission(self):
        ret = self._delete("/users/bob/permissions/permission", qs=dict(data_version=1), username="ashanti")
        self.assertStatusCode(ret, 403)

    def testPermissionDeleteRequiresSignoff(self):
        ret = self._delete("/users/bob/permissions/release", qs=dict(data_version=1))
        self.assertStatusCode(ret, 400)
        self.assertIn("No Signoffs given", ret.get_data(as_text=True))


class TestPermissionsScheduledChanges(ViewTest):
    maxDiff = 10000

    def setUp(self):
        super(TestPermissionsScheduledChanges, self).setUp()
        dbo.permissions.scheduled_changes.t.insert().execute(
            sc_id=1,
            scheduled_by="bill",
            change_type="insert",
            data_version=1,
            base_permission="rule",
            base_username="janet",
            base_options={"products": ["foo"]},
        )
        dbo.permissions.scheduled_changes.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=20, sc_id=1)
        dbo.permissions.scheduled_changes.history.t.insert().execute(
            change_id=2,
            changed_by="bill",
            timestamp=21,
            sc_id=1,
            scheduled_by="bill",
            change_type="insert",
            data_version=1,
            base_permission="rule",
            base_username="janet",
            base_options={"products": ["foo"]},
        )
        dbo.permissions.scheduled_changes.signoffs.t.insert().execute(sc_id=1, username="bill", role="admin")

        dbo.permissions.scheduled_changes.signoffs.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=30, sc_id=1, username="bill")
        dbo.permissions.scheduled_changes.signoffs.history.t.insert().execute(
            change_id=2, changed_by="bill", timestamp=31, sc_id=1, username="bill", role="admin"
        )
        dbo.permissions.scheduled_changes.conditions.t.insert().execute(sc_id=1, when=10000000, data_version=1)
        dbo.permissions.scheduled_changes.conditions.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=20, sc_id=1)
        dbo.permissions.scheduled_changes.conditions.history.t.insert().execute(
            change_id=2, changed_by="bill", timestamp=21, sc_id=1, when=10000000, data_version=1
        )
        dbo.permissions.scheduled_changes.signoffs.t.insert().execute(sc_id=1, username="zawadi", role="admin")

        dbo.permissions.scheduled_changes.t.insert().execute(
            sc_id=2,
            scheduled_by="bill",
            change_type="update",
            data_version=1,
            base_permission="release_locale",
            base_username="ashanti",
            base_options=None,
            base_data_version=1,
        )
        dbo.permissions.scheduled_changes.history.t.insert().execute(change_id=3, changed_by="bill", timestamp=40, sc_id=2)
        dbo.permissions.scheduled_changes.history.t.insert().execute(
            change_id=4,
            changed_by="bill",
            timestamp=41,
            sc_id=2,
            scheduled_by="bill",
            change_type="update",
            data_version=1,
            base_permission="release_locale",
            base_username="ashanti",
            base_options=None,
            base_data_version=1,
        )
        dbo.permissions.scheduled_changes.conditions.t.insert().execute(sc_id=2, when=20000000, data_version=1)
        dbo.permissions.scheduled_changes.conditions.history.t.insert().execute(change_id=3, changed_by="bill", timestamp=40, sc_id=2)
        dbo.permissions.scheduled_changes.conditions.history.t.insert().execute(
            change_id=4, changed_by="bill", timestamp=41, sc_id=2, when=20000000, data_version=1
        )
        dbo.permissions.scheduled_changes.signoffs.t.insert().execute(sc_id=2, username="bill", role="admin")
        dbo.permissions.scheduled_changes.signoffs.t.insert().execute(sc_id=2, username="zawadi", role="admin")

        dbo.permissions.scheduled_changes.t.insert().execute(
            sc_id=3, scheduled_by="bill", change_type="insert", data_version=2, base_permission="permission", base_username="bob", complete=True
        )
        dbo.permissions.scheduled_changes.history.t.insert().execute(change_id=5, changed_by="bill", timestamp=60, sc_id=3)
        dbo.permissions.scheduled_changes.history.t.insert().execute(
            change_id=6,
            changed_by="bill",
            timestamp=61,
            sc_id=3,
            scheduled_by="bill",
            change_type="insert",
            data_version=1,
            base_permission="permission",
            base_username="bob",
            complete=False,
        )
        dbo.permissions.scheduled_changes.history.t.insert().execute(
            change_id=7,
            changed_by="bill",
            timestamp=100,
            sc_id=3,
            scheduled_by="bill",
            change_type="insert",
            data_version=2,
            base_permission="permission",
            base_username="bob",
            complete=True,
        )
        dbo.permissions.scheduled_changes.conditions.t.insert().execute(sc_id=3, when=30000000, data_version=2)
        dbo.permissions.scheduled_changes.conditions.history.t.insert().execute(change_id=5, changed_by="bill", timestamp=60, sc_id=3)
        dbo.permissions.scheduled_changes.conditions.history.t.insert().execute(
            change_id=6, changed_by="bill", timestamp=61, sc_id=3, when=30000000, data_version=1
        )
        dbo.permissions.scheduled_changes.conditions.history.t.insert().execute(
            change_id=7, changed_by="bill", timestamp=100, sc_id=3, when=30000000, data_version=2
        )
        dbo.permissions.scheduled_changes.t.insert().execute(
            sc_id=4,
            scheduled_by="bill",
            change_type="delete",
            data_version=1,
            base_permission="scheduled_change",
            base_username="mary",
            complete=False,
            base_data_version=1,
        )
        dbo.permissions.scheduled_changes.history.t.insert().execute(change_id=8, changed_by="bill", timestamp=200, sc_id=4)
        dbo.permissions.scheduled_changes.history.t.insert().execute(
            change_id=9,
            changed_by="bill",
            timestamp=201,
            sc_id=4,
            scheduled_by="bill",
            change_type="delete",
            data_version=1,
            base_permission="scheduled_change",
            base_username="mary",
            complete=False,
        )
        dbo.permissions.scheduled_changes.conditions.t.insert().execute(sc_id=4, when=76000000, data_version=1)
        dbo.permissions.scheduled_changes.conditions.history.t.insert().execute(change_id=8, changed_by="bill", timestamp=200, sc_id=4)
        dbo.permissions.scheduled_changes.conditions.history.t.insert().execute(
            change_id=9, changed_by="bill", timestamp=201, sc_id=4, when=76000000, data_version=1
        )
        dbo.permissions.scheduled_changes.signoffs.t.insert().execute(sc_id=4, username="bill", role="admin")
        dbo.permissions.scheduled_changes.signoffs.t.insert().execute(sc_id=4, username="zawadi", role="admin")

        dbo.permissions.scheduled_changes.t.insert().execute(
            sc_id=5, scheduled_by="bill", change_type="insert", data_version=1, base_permission="rule", base_username="joe", base_options={"products": ["fake"]}
        )
        dbo.permissions.scheduled_changes.history.t.insert().execute(change_id=10, changed_by="bill", timestamp=204, sc_id=5)
        dbo.permissions.scheduled_changes.history.t.insert().execute(
            change_id=11,
            changed_by="bill",
            timestamp=205,
            sc_id=5,
            scheduled_by="bill",
            change_type="insert",
            data_version=1,
            base_permission="rule",
            base_username="joe",
            base_options={"products": ["fake"]},
        )
        dbo.permissions.scheduled_changes.conditions.t.insert().execute(sc_id=5, when=98000000, data_version=1)
        dbo.permissions.scheduled_changes.conditions.history.t.insert().execute(change_id=10, changed_by="bill", timestamp=204, sc_id=5)
        dbo.permissions.scheduled_changes.conditions.history.t.insert().execute(
            change_id=11, changed_by="bill", timestamp=205, sc_id=5, when=98000000, data_version=1
        )

        dbo.permissions.scheduled_changes.t.insert().execute(
            sc_id=6,
            scheduled_by="bill",
            change_type="update",
            data_version=1,
            base_permission="release",
            base_username="bob",
            base_options={"products": ["a", "b"]},
            base_data_version=1,
        )
        dbo.permissions.scheduled_changes.history.t.insert().execute(change_id=12, changed_by="bill", timestamp=404, sc_id=6)
        dbo.permissions.scheduled_changes.history.t.insert().execute(
            change_id=13,
            changed_by="bill",
            timestamp=405,
            sc_id=6,
            scheduled_by="bill",
            change_type="update",
            data_version=1,
            base_permission="release",
            base_username="bob",
            base_options={"products": ["a", "b"]},
            base_data_version=1,
        )
        dbo.permissions.scheduled_changes.conditions.t.insert().execute(sc_id=6, when=38000000, data_version=1)
        dbo.permissions.scheduled_changes.conditions.history.t.insert().execute(change_id=12, changed_by="bill", timestamp=404, sc_id=6)
        dbo.permissions.scheduled_changes.conditions.history.t.insert().execute(
            change_id=13, changed_by="bill", timestamp=405, sc_id=6, when=38000000, data_version=1
        )

    def testGetScheduledChanges(self):
        ret = self._get("/scheduled_changes/permissions")
        expected = {
            "count": 5,
            "scheduled_changes": [
                {
                    "sc_id": 1,
                    "when": 10000000,
                    "scheduled_by": "bill",
                    "change_type": "insert",
                    "complete": False,
                    "sc_data_version": 1,
                    "permission": "rule",
                    "username": "janet",
                    "options": {"products": ["foo"]},
                    "data_version": None,
                    "signoffs": {"bill": "admin", "zawadi": "admin"},
                    "required_signoffs": {"admin": 2},
                },
                {
                    "sc_id": 2,
                    "when": 20000000,
                    "scheduled_by": "bill",
                    "change_type": "update",
                    "complete": False,
                    "sc_data_version": 1,
                    "permission": "release_locale",
                    "username": "ashanti",
                    "options": None,
                    "data_version": 1,
                    "signoffs": {"bill": "admin", "zawadi": "admin"},
                    "required_signoffs": {"admin": 2},
                },
                {
                    "sc_id": 4,
                    "when": 76000000,
                    "scheduled_by": "bill",
                    "change_type": "delete",
                    "complete": False,
                    "sc_data_version": 1,
                    "permission": "scheduled_change",
                    "username": "mary",
                    "options": None,
                    "data_version": 1,
                    "signoffs": {"bill": "admin", "zawadi": "admin"},
                    "required_signoffs": {"admin": 2},
                },
                {
                    "sc_id": 5,
                    "when": 98000000,
                    "scheduled_by": "bill",
                    "change_type": "insert",
                    "complete": False,
                    "sc_data_version": 1,
                    "permission": "rule",
                    "username": "joe",
                    "options": {"products": ["fake"]},
                    "data_version": None,
                    "signoffs": {},
                    "required_signoffs": {"admin": 2},
                },
                {
                    "sc_id": 6,
                    "when": 38000000,
                    "scheduled_by": "bill",
                    "change_type": "update",
                    "complete": False,
                    "sc_data_version": 1,
                    "permission": "release",
                    "username": "bob",
                    "options": {"products": ["a", "b"]},
                    "data_version": 1,
                    "signoffs": {},
                    "required_signoffs": {"admin": 2},
                },
            ],
        }
        self.assertEqual(ret.get_json(), expected)

    def testGetScheduledChangesWithCompleted(self):
        ret = self._get("/scheduled_changes/permissions", qs={"all": 1})
        expected = {
            "count": 6,
            "scheduled_changes": [
                {
                    "sc_id": 1,
                    "when": 10000000,
                    "scheduled_by": "bill",
                    "change_type": "insert",
                    "complete": False,
                    "sc_data_version": 1,
                    "permission": "rule",
                    "username": "janet",
                    "options": {"products": ["foo"]},
                    "data_version": None,
                    "signoffs": {"bill": "admin", "zawadi": "admin"},
                    "required_signoffs": {"admin": 2},
                },
                {
                    "sc_id": 2,
                    "when": 20000000,
                    "scheduled_by": "bill",
                    "change_type": "update",
                    "complete": False,
                    "sc_data_version": 1,
                    "permission": "release_locale",
                    "username": "ashanti",
                    "options": None,
                    "data_version": 1,
                    "signoffs": {"bill": "admin", "zawadi": "admin"},
                    "required_signoffs": {"admin": 2},
                },
                {
                    "sc_id": 3,
                    "when": 30000000,
                    "scheduled_by": "bill",
                    "change_type": "insert",
                    "complete": True,
                    "sc_data_version": 2,
                    "permission": "permission",
                    "username": "bob",
                    "options": None,
                    "data_version": None,
                    "signoffs": {},
                    "required_signoffs": {"admin": 2},
                },
                {
                    "sc_id": 4,
                    "when": 76000000,
                    "scheduled_by": "bill",
                    "change_type": "delete",
                    "complete": False,
                    "sc_data_version": 1,
                    "permission": "scheduled_change",
                    "username": "mary",
                    "options": None,
                    "data_version": 1,
                    "signoffs": {"bill": "admin", "zawadi": "admin"},
                    "required_signoffs": {"admin": 2},
                },
                {
                    "sc_id": 5,
                    "when": 98000000,
                    "scheduled_by": "bill",
                    "change_type": "insert",
                    "complete": False,
                    "sc_data_version": 1,
                    "permission": "rule",
                    "username": "joe",
                    "options": {"products": ["fake"]},
                    "data_version": None,
                    "signoffs": {},
                    "required_signoffs": {"admin": 2},
                },
                {
                    "sc_id": 6,
                    "when": 38000000,
                    "scheduled_by": "bill",
                    "change_type": "update",
                    "complete": False,
                    "sc_data_version": 1,
                    "permission": "release",
                    "username": "bob",
                    "options": {"products": ["a", "b"]},
                    "data_version": 1,
                    "signoffs": {},
                    "required_signoffs": {"admin": 2},
                },
            ],
        }
        self.assertEqual(ret.get_json(), expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeExistingPermission(self):
        data = {"when": 400000000, "permission": "rule", "username": "bob", "options": None, "data_version": 1, "change_type": "update"}
        ret = self._post("/scheduled_changes/permissions", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"sc_id": 7, "signoffs": {"bill": "admin"}})
        r = dbo.permissions.scheduled_changes.t.select().where(dbo.permissions.scheduled_changes.sc_id == 7).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 7,
            "scheduled_by": "bill",
            "change_type": "update",
            "complete": False,
            "data_version": 1,
            "base_permission": "rule",
            "base_username": "bob",
            "base_options": None,
            "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)
        cond = dbo.permissions.scheduled_changes.conditions.t.select().where(dbo.permissions.scheduled_changes.conditions.sc_id == 7).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 7, "data_version": 1, "when": 400000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeNewPermission(self):
        data = {"when": 400000000, "permission": "release", "username": "jill", "options": '{"products": ["a"]}', "change_type": "insert"}
        ret = self._post("/scheduled_changes/permissions", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"sc_id": 7, "signoffs": {"bill": "admin"}})
        r = dbo.permissions.scheduled_changes.t.select().where(dbo.permissions.scheduled_changes.sc_id == 7).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 7,
            "scheduled_by": "bill",
            "change_type": "insert",
            "complete": False,
            "data_version": 1,
            "base_permission": "release",
            "base_username": "jill",
            "base_options": {"products": ["a"]},
            "base_data_version": None,
        }
        self.assertEqual(db_data, expected)
        cond = dbo.permissions.scheduled_changes.conditions.t.select().where(dbo.permissions.scheduled_changes.conditions.sc_id == 7).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 7, "data_version": 1, "when": 400000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeDeletePermission(self):
        data = {"when": 400000000, "permission": "release", "username": "ashanti", "change_type": "delete", "data_version": 1}
        ret = self._post("/scheduled_changes/permissions", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"sc_id": 7, "signoffs": {"bill": "admin"}})
        r = dbo.permissions.scheduled_changes.t.select().where(dbo.permissions.scheduled_changes.sc_id == 7).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 7,
            "scheduled_by": "bill",
            "change_type": "delete",
            "complete": False,
            "data_version": 1,
            "base_permission": "release",
            "base_username": "ashanti",
            "base_options": None,
            "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)
        cond = dbo.permissions.scheduled_changes.conditions.t.select().where(dbo.permissions.scheduled_changes.conditions.sc_id == 7).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 7, "data_version": 1, "when": 400000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeNewPermissionEmptyDictOptions(self):
        data = {"when": 400000000, "permission": "release", "username": "jill", "options": "{}", "change_type": "insert"}
        ret = self._post("/scheduled_changes/permissions", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"sc_id": 7, "signoffs": {"bill": "admin"}})
        r = dbo.permissions.scheduled_changes.t.select().where(dbo.permissions.scheduled_changes.sc_id == 7).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 7,
            "scheduled_by": "bill",
            "change_type": "insert",
            "complete": False,
            "data_version": 1,
            "base_permission": "release",
            "base_username": "jill",
            "base_options": None,
            "base_data_version": None,
        }
        self.assertEqual(db_data, expected)
        cond = dbo.permissions.scheduled_changes.conditions.t.select().where(dbo.permissions.scheduled_changes.conditions.sc_id == 7).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 7, "data_version": 1, "when": 400000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledUnknownScheduledChangeID(self):
        data = {"options": '{"products": ["Thunderbird"]}', "data_version": 1, "sc_data_version": 1, "when": 200000000}
        ret = self._post("/scheduled_changes/permissions/98765", data=data)
        self.assertEqual(ret.status_code, 404, ret.get_data())

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeExistingPermission(self):
        data = {"options": '{"products": ["Thunderbird"]}', "data_version": 1, "sc_data_version": 1, "when": 200000000}
        ret = self._post("/scheduled_changes/permissions/2", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"new_data_version": 2, "signoffs": {"bill": "releng"}})

        r = dbo.permissions.scheduled_changes.t.select().where(dbo.permissions.scheduled_changes.sc_id == 2).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 2,
            "complete": False,
            "data_version": 2,
            "scheduled_by": "bill",
            "change_type": "update",
            "base_permission": "release_locale",
            "base_username": "ashanti",
            "base_options": {"products": ["Thunderbird"]},
            "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)
        cond = dbo.permissions.scheduled_changes.conditions.t.select().where(dbo.permissions.scheduled_changes.conditions.sc_id == 2).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 2, "data_version": 2, "when": 200000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeExistingPermissionResetSignOffs(self):
        data = {"options": '{"products": ["Thunderbird"]}', "data_version": 1, "sc_data_version": 1, "when": 200000000}
        rows = dbo.permissions.scheduled_changes.signoffs.t.select().where(dbo.permissions.scheduled_changes.signoffs.sc_id == 2).execute().fetchall()
        self.assertEqual(len(rows), 2)
        ret = self._post("/scheduled_changes/permissions/2", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"new_data_version": 2, "signoffs": {"bill": "releng"}})

        r = dbo.permissions.scheduled_changes.t.select().where(dbo.permissions.scheduled_changes.sc_id == 2).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 2,
            "complete": False,
            "data_version": 2,
            "scheduled_by": "bill",
            "change_type": "update",
            "base_permission": "release_locale",
            "base_username": "ashanti",
            "base_options": {"products": ["Thunderbird"]},
            "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)
        rows = dbo.permissions.scheduled_changes.signoffs.t.select().where(dbo.releases.scheduled_changes.signoffs.sc_id == 2).execute().fetchall()
        self.assertEqual(len(rows), 0)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduleChangeExistingPermissionDiffUserResetSignOffs(self):
        data = {"options": '{"products": ["superfake"]}', "data_version": 1, "sc_data_version": 1, "when": 200000000}
        rows = dbo.permissions.scheduled_changes.signoffs.t.select().where(dbo.permissions.scheduled_changes.signoffs.sc_id == 2).execute().fetchall()
        self.assertEqual(len(rows), 2)
        ret = self._post("/scheduled_changes/permissions/2", data=data, username="bob")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"new_data_version": 2, "signoffs": {"bob": "relman"}})

        r = dbo.permissions.scheduled_changes.t.select().where(dbo.permissions.scheduled_changes.sc_id == 2).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 2,
            "complete": False,
            "data_version": 2,
            "scheduled_by": "bob",
            "change_type": "update",
            "base_permission": "release_locale",
            "base_username": "ashanti",
            "base_options": {"products": ["superfake"]},
            "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)
        rows = dbo.permissions.scheduled_changes.signoffs.t.select().where(dbo.releases.scheduled_changes.signoffs.sc_id == 2).execute().fetchall()
        self.assertEqual(len(rows), 0)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateCompletedScheduledChangeExistingPermission(self):
        data = {"options": '{"products": ["Thunderbird"]}', "data_version": 1, "sc_data_version": 1, "when": 200000000}
        ret = self._post("/scheduled_changes/permissions/3", data=data)
        self.assertEqual(ret.status_code, 400, ret.get_data())

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeNewPermission(self):
        data = {"options": '{"products": ["Firefox"]}', "sc_data_version": 1, "when": 450000000}
        ret = self._post("/scheduled_changes/permissions/1", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"new_data_version": 2, "signoffs": {"bill": "releng"}})

        r = dbo.permissions.scheduled_changes.t.select().where(dbo.permissions.scheduled_changes.sc_id == 1).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 1,
            "complete": False,
            "data_version": 2,
            "scheduled_by": "bill",
            "change_type": "insert",
            "base_permission": "rule",
            "base_username": "janet",
            "base_options": {"products": ["Firefox"]},
            "base_data_version": None,
        }
        self.assertEqual(db_data, expected)
        cond = dbo.permissions.scheduled_changes.conditions.t.select().where(dbo.permissions.scheduled_changes.conditions.sc_id == 1).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 1, "data_version": 2, "when": 450000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    def testDeleteScheduledChange(self):
        ret = self._delete("/scheduled_changes/permissions/1", qs={"data_version": 1})
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")
        got = dbo.permissions.scheduled_changes.t.select().where(dbo.permissions.scheduled_changes.sc_id == 1).execute().fetchall()
        self.assertEqual(got, [])
        cond_got = dbo.permissions.scheduled_changes.conditions.t.select().where(dbo.permissions.scheduled_changes.conditions.sc_id == 1).execute().fetchall()
        self.assertEqual(cond_got, [])

    def testDeleteCompletedScheduledChange(self):
        ret = self._delete("/scheduled_changes/permissions/3", qs={"data_version": 1})
        self.assertEqual(ret.status_code, 400, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")

    def testEnactScheduledChangeExistingPermission(self):
        ret = self._post("/scheduled_changes/permissions/2/enact")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")

        r = dbo.permissions.scheduled_changes.t.select().where(dbo.permissions.scheduled_changes.sc_id == 2).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 2,
            "complete": True,
            "data_version": 2,
            "scheduled_by": "bill",
            "change_type": "update",
            "base_permission": "release_locale",
            "base_username": "ashanti",
            "base_options": None,
            "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)

        base_row = (
            dbo.permissions.t.select()
            .where(dbo.permissions.username == "ashanti")
            .where(dbo.permissions.permission == "release_locale")
            .execute()
            .fetchall()[0]
        )
        base_expected = {"permission": "release_locale", "username": "ashanti", "options": None, "data_version": 2}
        self.assertEqual(dict(base_row), base_expected)

    def testEnactScheduledChangeNewPermission(self):
        ret = self._post("/scheduled_changes/permissions/1/enact")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")

        r = dbo.permissions.scheduled_changes.t.select().where(dbo.permissions.scheduled_changes.sc_id == 1).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 1,
            "complete": True,
            "data_version": 2,
            "scheduled_by": "bill",
            "change_type": "insert",
            "base_permission": "rule",
            "base_username": "janet",
            "base_options": {"products": ["foo"]},
            "base_data_version": None,
        }
        self.assertEqual(db_data, expected)

        base_row = dict(
            dbo.permissions.t.select().where(dbo.permissions.username == "janet").where(dbo.permissions.permission == "rule").execute().fetchall()[0]
        )
        base_expected = {"permission": "rule", "username": "janet", "options": {"products": ["foo"]}, "data_version": 1}
        self.assertEqual(dict(base_row), base_expected)

    def testEnactScheduledChangeDeletePermission(self):
        ret = self._post("/scheduled_changes/permissions/4/enact")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")

        r = dbo.permissions.scheduled_changes.t.select().where(dbo.permissions.scheduled_changes.sc_id == 4).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 4,
            "complete": True,
            "data_version": 2,
            "scheduled_by": "bill",
            "change_type": "delete",
            "base_permission": "scheduled_change",
            "base_username": "mary",
            "base_options": None,
            "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)

        base_row = (
            dbo.permissions.t.select().where(dbo.permissions.username == "mary").where(dbo.permissions.permission == "scheduled_change").execute().fetchall()
        )
        self.assertEqual(len(base_row), 0)

    def testGetScheduledChangeHistoryRevisions(self):
        ret = self._get("/scheduled_changes/permissions/3/revisions")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        expected = {
            "count": 2,
            "revisions": [
                {
                    "change_id": 7,
                    "changed_by": "bill",
                    "timestamp": 100,
                    "sc_id": 3,
                    "scheduled_by": "bill",
                    "change_type": "insert",
                    "data_version": None,
                    "permission": "permission",
                    "username": "bob",
                    "options": None,
                    "when": 30000000,
                    "complete": True,
                    "sc_data_version": 2,
                },
                {
                    "change_id": 6,
                    "changed_by": "bill",
                    "timestamp": 61,
                    "sc_id": 3,
                    "scheduled_by": "bill",
                    "change_type": "insert",
                    "data_version": None,
                    "permission": "permission",
                    "username": "bob",
                    "options": None,
                    "when": 30000000,
                    "complete": False,
                    "sc_data_version": 1,
                },
            ],
        }
        self.assertEqual(ret.get_json(), expected)

    def testGetPermissionsHistory(self):
        ret = self._get("/permissions/history")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        expected = {
            "Permissions": {"count": 0, "revisions": []},
            "Permissions Scheduled Change": {
                "count": 7,
                "revisions": [
                    {
                        "change_id": 13,
                        "change_type": "update",
                        "changed_by": "bill",
                        "complete": False,
                        "data_version": 1,
                        "options": {"products": ["a", "b"]},
                        "permission": "release",
                        "sc_data_version": 1,
                        "sc_id": 6,
                        "scheduled_by": "bill",
                        "timestamp": 405,
                        "username": "bob",
                        "when": 38000000,
                    },
                    {
                        "change_id": 11,
                        "change_type": "insert",
                        "changed_by": "bill",
                        "complete": False,
                        "data_version": None,
                        "options": {"products": ["fake"]},
                        "permission": "rule",
                        "sc_data_version": 1,
                        "sc_id": 5,
                        "scheduled_by": "bill",
                        "timestamp": 205,
                        "username": "joe",
                        "when": 98000000,
                    },
                    {
                        "change_id": 9,
                        "change_type": "delete",
                        "changed_by": "bill",
                        "complete": False,
                        "data_version": None,
                        "options": None,
                        "permission": "scheduled_change",
                        "sc_data_version": 1,
                        "sc_id": 4,
                        "scheduled_by": "bill",
                        "timestamp": 201,
                        "username": "mary",
                        "when": 76000000,
                    },
                    {
                        "change_id": 7,
                        "change_type": "insert",
                        "changed_by": "bill",
                        "complete": True,
                        "data_version": None,
                        "options": None,
                        "permission": "permission",
                        "sc_data_version": 2,
                        "sc_id": 3,
                        "scheduled_by": "bill",
                        "timestamp": 100,
                        "username": "bob",
                        "when": 30000000,
                    },
                    {
                        "change_id": 6,
                        "change_type": "insert",
                        "changed_by": "bill",
                        "complete": False,
                        "data_version": None,
                        "options": None,
                        "permission": "permission",
                        "sc_data_version": 1,
                        "sc_id": 3,
                        "scheduled_by": "bill",
                        "timestamp": 61,
                        "username": "bob",
                        "when": 30000000,
                    },
                    {
                        "change_id": 4,
                        "change_type": "update",
                        "changed_by": "bill",
                        "complete": False,
                        "data_version": 1,
                        "options": None,
                        "permission": "release_locale",
                        "sc_data_version": 1,
                        "sc_id": 2,
                        "scheduled_by": "bill",
                        "timestamp": 41,
                        "username": "ashanti",
                        "when": 20000000,
                    },
                    {
                        "change_id": 2,
                        "change_type": "insert",
                        "changed_by": "bill",
                        "complete": False,
                        "data_version": None,
                        "options": {"products": ["foo"]},
                        "permission": "rule",
                        "sc_data_version": 1,
                        "sc_id": 1,
                        "scheduled_by": "bill",
                        "timestamp": 21,
                        "username": "janet",
                        "when": 10000000,
                    },
                ],
            },
        }

        self.assertEqual(ret.get_json(), expected)

    def testGetPermissionsRequiredSignoffsHistory(self):
        ret = self._get("/required_signoffs/permissions/history")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        expected = {
            "count": 2,
            "required_signoffs": [
                {"data_version": 2, "changed_by": "bill", "product": "doop", "change_id": 3, "role": "releng", "signoffs_required": 1, "timestamp": 25},
                {"data_version": 1, "changed_by": "bill", "product": "doop", "change_id": 2, "role": "releng", "signoffs_required": 2, "timestamp": 11},
            ],
        }
        data = ret.get_json()
        revisions = data["Permissions Required Signoffs"]["required_signoffs"]
        expected_revisions = expected["required_signoffs"]
        for index in range(len(revisions)):
            self.assertEqual(revisions[index]["product"], expected_revisions[index]["product"])
            self.assertEqual(revisions[index]["timestamp"], expected_revisions[index]["timestamp"])
            self.assertEqual(revisions[index]["change_id"], expected_revisions[index]["change_id"])
            self.assertEqual(revisions[index]["data_version"], expected_revisions[index]["data_version"])
            self.assertEqual(revisions[index]["changed_by"], expected_revisions[index]["changed_by"])
        self.assertEqual(len(data["Permissions Required Signoffs"]["required_signoffs"]), 2)
        self.assertEqual(ret.get_json()["Permissions Required Signoffs"], expected)

    @mock.patch("time.time", mock.MagicMock(return_value=100))
    def testSignoffWithPermission(self):
        ret = self._post("/scheduled_changes/permissions/2/signoffs", data=dict(role="relman"), username="bob")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")
        r = dbo.permissions.scheduled_changes.signoffs.t.select().where(dbo.permissions.scheduled_changes.signoffs.sc_id == 2).execute().fetchall()
        r = [dict(rs) for rs in r]
        self.assertEqual(len(r), 3)
        self.assertIn({"sc_id": 2, "username": "bill", "role": "releng"}, r)
        self.assertIn({"sc_id": 2, "username": "mary", "role": "relman"}, r)
        self.assertIn({"sc_id": 2, "username": "bob", "role": "relman"}, r)
        r = (
            dbo.permissions.scheduled_changes.signoffs.history.t.select()
            .where(dbo.permissions.scheduled_changes.signoffs.history.sc_id == 2)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(r), 2)
        self.assertEqual(dict(r[0]), {"change_id": 3, "changed_by": "bob", "timestamp": 99999, "sc_id": 2, "username": "bob", "role": None})
        self.assertEqual(dict(r[1]), {"change_id": 4, "changed_by": "bob", "timestamp": 100000, "sc_id": 2, "username": "bob", "role": "relman"})

    def testSignoffWithoutPermission(self):
        ret = self._post("/scheduled_changes/permissions/2/signoffs", data=dict(role="relman"), username="bill")
        self.assertEqual(ret.status_code, 403, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")

    def testSignoffWithoutRole(self):
        ret = self._post("/scheduled_changes/permissions/2/signoffs", data=dict(lorem="random"), username="bill")
        self.assertEqual(ret.status_code, 400, ret.get_data())
        self.assertEqual(ret.mimetype, "application/problem+json")

    def testRevokeSignoff(self):
        ret = self._delete("/scheduled_changes/permissions/1/signoffs", username="bill")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")
        r = dbo.permissions.scheduled_changes.signoffs.t.select().where(dbo.permissions.scheduled_changes.signoffs.sc_id == 1).execute().fetchall()
        self.assertEqual(len(r), 0)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddNewFullAdminPermission(self):
        """Tests the entire process of adding a new full fledged admin, which requires
        creating a Scheduled Change, signoffs happening, and enacting the change."""
        # Scheduled Change creation
        data = {"when": 400000000, "permission": "admin", "username": "jill", "options": None, "change_type": "insert"}
        ret = self._post("/scheduled_changes/permissions", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"sc_id": 7, "signoffs": {"bill": "admin"}})
        r = dbo.permissions.scheduled_changes.t.select().where(dbo.permissions.scheduled_changes.sc_id == 7).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 7,
            "scheduled_by": "bill",
            "change_type": "insert",
            "complete": False,
            "data_version": 1,
            "base_permission": "admin",
            "base_username": "jill",
            "base_options": None,
            "base_data_version": None,
        }
        self.assertEqual(db_data, expected)
        cond = dbo.permissions.scheduled_changes.conditions.t.select().where(dbo.permissions.scheduled_changes.conditions.sc_id == 7).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 7, "data_version": 1, "when": 400000000}
        self.assertEqual(dict(cond[0]), cond_expected)

        # Signoffs, which require signoff from role in permissionsRequiredSignoffs
        # regardless of product (because a full fledged admin can mange all products).
        ret = self._post("/scheduled_changes/permissions/7/signoffs", data=dict(role="admin"), username="zawadi")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        ret = self._post("/scheduled_changes/permissions/7/signoffs", data=dict(role="admin"), username="bill")
        self.assertEqual(ret.status_code, 200, ret.get_data())

        # Enacting!
        ret = self._post("/scheduled_changes/permissions/7/enact")
        self.assertEqual(ret.status_code, 200, ret.get_data())

        r = dbo.permissions.scheduled_changes.t.select().where(dbo.permissions.scheduled_changes.sc_id == 7).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 7,
            "complete": True,
            "data_version": 2,
            "scheduled_by": "bill",
            "change_type": "insert",
            "base_permission": "admin",
            "base_username": "jill",
            "base_options": None,
            "base_data_version": None,
        }
        self.assertEqual(db_data, expected)

        base_row = dict(
            dbo.permissions.t.select().where(dbo.permissions.username == "jill").where(dbo.permissions.permission == "admin").execute().fetchall()[0]
        )
        base_expected = {"permission": "admin", "username": "jill", "options": None, "data_version": 1}
        self.assertEqual(dict(base_row), base_expected)


class TestUserRolesAPI_JSON(ViewTest):
    def testGrantRole(self):
        ret = self._put("/users/ashanti/roles/dev")
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.get_data(as_text=True), json.dumps(dict(new_data_version=1)), ret.get_data())
        got = dbo.permissions.user_roles.t.select().where(dbo.permissions.user_roles.username == "ashanti").execute().fetchall()
        self.assertEqual(got, [("ashanti", "dev", 1)])

    def testGrantExistingRole(self):
        ret = self._put("/users/bill/roles/releng")
        self.assertStatusCode(ret, 200)
        self.assertEqual(ret.get_data(as_text=True), json.dumps(dict(new_data_version=1)), ret.get_data())
        got = dbo.permissions.user_roles.t.select().where(dbo.permissions.user_roles.username == "bill").execute().fetchall()
        self.assertEqual(got, [("bill", "qa", 1), ("bill", "releng", 1)])

    def testGrantRoleWithoutPermission(self):
        ret = self._put("/users/emily/roles/relman", username="rory", data=dict(data_version=1))
        self.assertStatusCode(ret, 403)

    def testRevokeRole(self):
        ret = self._delete("/users/bob/roles/relman", qs=dict(data_version=1))
        self.assertStatusCode(ret, 200)
        got = dbo.permissions.user_roles.t.select().where(dbo.permissions.user_roles.username == "bob").execute().fetchall()
        self.assertEqual(got, [])

    def testRevokeRoleWithoutPermission(self):
        ret = self._delete("/users/bob/roles/relman", username="lane", qs=dict(data_version=1))
        self.assertStatusCode(ret, 403)

    def testRevokeRoleBadDataVersion(self):
        ret = self._delete("/users/bob/roles/relman", qs=dict(data_version=3))
        self.assertStatusCode(ret, 400)
