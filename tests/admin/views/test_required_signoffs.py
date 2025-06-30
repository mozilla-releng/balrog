import mock

from auslib.global_state import dbo

from .base import ViewTest


class TestProductRequiredSignoffs(ViewTest):
    def testGetRequiredSignoffs(self):
        ret = self._get("/required_signoffs/product")
        got = ret.json()
        self.assertEqual(got["count"], 4)
        expected = [
            {"product": "fake", "channel": "a", "role": "releng", "signoffs_required": 1, "data_version": 1},
            {"product": "fake", "channel": "e", "role": "releng", "signoffs_required": 1, "data_version": 1},
            {"product": "fake", "channel": "j", "role": "releng", "signoffs_required": 1, "data_version": 1},
            {"product": "fake", "channel": "k", "role": "relman", "signoffs_required": 1, "data_version": 2},
        ]
        self.assertEqual(got["required_signoffs"], expected)

    def testGetRequiredSignoffsWithArgs(self):
        ret = self._get("/required_signoffs/product", qs={"product": "fake", "channel": "e"})
        got = ret.json()
        self.assertEqual(got["count"], 1)
        expected = [{"product": "fake", "channel": "e", "role": "releng", "signoffs_required": 1, "data_version": 1}]
        self.assertEqual(got["required_signoffs"], expected)

    def testAddRequiredSignoff(self):
        ret = self._post("/required_signoffs/product", data=dict(product="fake", channel="b", role="releng", signoffs_required=1))
        self.assertStatusCode(ret, 201)
        rs = (
            dbo.productRequiredSignoffs.t.select()
            .where(dbo.productRequiredSignoffs.product == "fake")
            .where(dbo.productRequiredSignoffs.channel == "b")
            .where(dbo.productRequiredSignoffs.role == "releng")
            .execute()
            .fetchall()
        )
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0]["signoffs_required"], 1)
        self.assertEqual(rs[0]["data_version"], 1)

    def testAddRequiredSignoffWithoutEnoughUsersInRole(self):
        ret = self._post("/required_signoffs/product", data=dict(product="fake", channel="b", role="releng", signoffs_required=3))
        self.assertStatusCode(ret, 400)
        self.assertIn("Cannot require 3 signoffs", ret.text)

    def testAddRequiredSignoffThatRequiresSignoff(self):
        ret = self._post("/required_signoffs/product", data=dict(product="fake", channel="a", role="relman", signoffs_required=1))
        self.assertStatusCode(ret, 400)
        self.assertIn("No Signoffs given", ret.text)

    def testAddRequiredSignoffWithoutPermission(self):
        ret = self._post("/required_signoffs/product", data=dict(product="fake", channel="b", role="releng", signoffs_required=1), username="janet")
        self.assertStatusCode(ret, 403)

    def testModifyRequiredSignoff(self):
        ret = self._post("/required_signoffs/product", data=dict(product="fake", channel="a", role="relman", signoffs_required=1, data_version=1))
        self.assertStatusCode(ret, 400)
        self.assertIn("No Signoffs given", ret.text)

    def testDeleteRequiredSignoff(self):
        ret = self._delete("/required_signoffs/product", qs=dict(product="fake", channel="a", role="relman", data_version=1))
        self.assertStatusCode(ret, 400)


class TestProductRequiredSignoffsHistoryView(ViewTest):
    maxDiff = 1000

    def testGetRevisions(self):
        ret = self._get("/required_signoffs/product/revisions", qs={"product": "fake", "channel": "k", "role": "relman"})
        self.assertStatusCode(ret, 200)

        got = ret.json()
        expected = [
            {
                "change_id": 3,
                "changed_by": "bill",
                "timestamp": 25,
                "product": "fake",
                "channel": "k",
                "role": "relman",
                "signoffs_required": 1,
                "data_version": 2,
            },
            {
                "change_id": 2,
                "changed_by": "bill",
                "timestamp": 11,
                "product": "fake",
                "channel": "k",
                "role": "relman",
                "signoffs_required": 2,
                "data_version": 1,
            },
        ]
        self.assertEqual(got["count"], 2)
        self.assertEqual(got["required_signoffs"], expected)

    def testGetProductRequiedSignoffsHistory(self):
        ret = self._get("/required_signoffs/product/history", qs={})
        self.assertStatusCode(ret, 200)

        got = ret.json()
        expected = [
            {
                "change_id": 3,
                "changed_by": "bill",
                "timestamp": 25,
                "product": "fake",
                "channel": "k",
                "role": "relman",
                "signoffs_required": 1,
                "data_version": 2,
            },
            {
                "change_id": 2,
                "changed_by": "bill",
                "timestamp": 11,
                "product": "fake",
                "channel": "k",
                "role": "relman",
                "signoffs_required": 2,
                "data_version": 1,
            },
        ]
        self.assertEqual(got["Product Required Signoffs"]["count"], 2)
        self.assertEqual(got["Product Required Signoffs"]["required_signoffs"], expected)

    def testGetProductRequiedSignoffsWithinTimeRange(self):
        ret = self._get("/required_signoffs/product/history", qs={"timestamp_from": 20, "timestamp_to": 30})
        self.assertStatusCode(ret, 200)

        got = ret.json()
        expected = [
            {
                "change_id": 3,
                "changed_by": "bill",
                "timestamp": 25,
                "product": "fake",
                "channel": "k",
                "role": "relman",
                "signoffs_required": 1,
                "data_version": 2,
            }
        ]
        self.assertEqual(got["Product Required Signoffs"]["count"], 1)
        self.assertEqual(got["Product Required Signoffs"]["required_signoffs"], expected)


class TestProductRequiredSignoffsScheduledChanges(ViewTest):
    maxDiff = 10000

    def setUp(self):
        super(TestProductRequiredSignoffsScheduledChanges, self).setUp()
        dbo.productRequiredSignoffs.scheduled_changes.t.insert().execute(
            sc_id=1,
            scheduled_by="bill",
            change_type="insert",
            data_version=1,
            base_product="fake",
            base_channel="a",
            base_role="relman",
            base_signoffs_required=1,
        )
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=20, sc_id=1)
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(
            change_id=2,
            changed_by="bill",
            timestamp=21,
            sc_id=1,
            scheduled_by="bill",
            change_type="insert",
            data_version=1,
            base_product="fake",
            base_channel="a",
            base_role="relman",
            base_signoffs_required=1,
        )
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.t.insert().execute(sc_id=1, username="bill", role="releng")
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(
            change_id=1, changed_by="bill", timestamp=30, sc_id=1, username="bill"
        )
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(
            change_id=2, changed_by="bill", timestamp=31, sc_id=1, username="bill", role="releng"
        )
        dbo.productRequiredSignoffs.scheduled_changes.conditions.t.insert().execute(sc_id=1, when=100000000, data_version=1)
        dbo.productRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=20, sc_id=1)
        dbo.productRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(
            change_id=2, changed_by="bill", timestamp=21, sc_id=1, when=100000000, data_version=1
        )

        dbo.productRequiredSignoffs.scheduled_changes.t.insert().execute(
            sc_id=2,
            scheduled_by="bill",
            change_type="update",
            data_version=1,
            base_product="fake",
            base_channel="a",
            base_role="releng",
            base_signoffs_required=2,
            base_data_version=1,
        )
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(change_id=3, changed_by="bill", timestamp=40, sc_id=2)
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(
            change_id=4,
            changed_by="bill",
            timestamp=41,
            sc_id=2,
            scheduled_by="bill",
            change_type="update",
            data_version=1,
            base_product="fake",
            base_channel="a",
            base_role="releng",
            base_signoffs_required=2,
            base_data_version=1,
        )
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.t.insert().execute(sc_id=2, username="bill", role="releng")
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(
            change_id=3, changed_by="bill", timestamp=60, sc_id=2, username="bill"
        )
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(
            change_id=4, changed_by="bill", timestamp=61, sc_id=2, username="bill", role="releng"
        )
        dbo.productRequiredSignoffs.scheduled_changes.conditions.t.insert().execute(sc_id=2, when=200000000, data_version=1)
        dbo.productRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(change_id=3, changed_by="bill", timestamp=40, sc_id=2)
        dbo.productRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(
            change_id=4, changed_by="bill", timestamp=41, sc_id=2, when=200000000, data_version=1
        )

        dbo.productRequiredSignoffs.scheduled_changes.t.insert().execute(
            sc_id=3,
            scheduled_by="bill",
            change_type="insert",
            data_version=2,
            base_product="fake",
            base_channel="e",
            base_role="releng",
            base_signoffs_required=1,
            complete=True,
        )
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(change_id=5, changed_by="bill", timestamp=80, sc_id=3)
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(
            change_id=6,
            changed_by="bill",
            timestamp=81,
            sc_id=3,
            scheduled_by="bill",
            change_type="insert",
            data_version=1,
            base_product="fake",
            base_channel="e",
            base_role="releng",
            base_signoffs_required=2,
            complete=False,
        )
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(
            change_id=7,
            changed_by="bill",
            timestamp=100,
            sc_id=3,
            scheduled_by="bill",
            change_type="insert",
            data_version=2,
            base_product="fake",
            base_channel="e",
            base_role="releng",
            base_signoffs_required=1,
            complete=True,
        )
        dbo.productRequiredSignoffs.scheduled_changes.conditions.t.insert().execute(sc_id=3, when=300000000, data_version=2)
        dbo.productRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(change_id=5, changed_by="bill", timestamp=80, sc_id=3)
        dbo.productRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(
            change_id=6, changed_by="bill", timestamp=81, sc_id=3, when=300000000, data_version=1
        )
        dbo.productRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(
            change_id=7, changed_by="bill", timestamp=100, sc_id=3, when=300000000, data_version=2
        )

        dbo.productRequiredSignoffs.scheduled_changes.t.insert().execute(
            sc_id=4, scheduled_by="bill", change_type="delete", data_version=1, base_product="fake", base_channel="j", base_role="releng", base_data_version=1
        )
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(change_id=8, changed_by="bill", timestamp=200, sc_id=4)
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(
            change_id=9,
            changed_by="bill",
            timestamp=201,
            sc_id=4,
            scheduled_by="bill",
            change_type="delete",
            data_version=1,
            base_product="fake",
            base_channel="j",
            base_role="releng",
            base_data_version=1,
        )
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.t.insert().execute(sc_id=4, username="bill", role="releng")
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(
            change_id=8, changed_by="bill", timestamp=300, sc_id=1, username="bill"
        )
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(
            change_id=9, changed_by="bill", timestamp=301, sc_id=1, username="bill", role="releng"
        )
        dbo.productRequiredSignoffs.scheduled_changes.conditions.t.insert().execute(sc_id=4, when=400000000, data_version=1)
        dbo.productRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(change_id=8, changed_by="bill", timestamp=200, sc_id=4)
        dbo.productRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(
            change_id=9, changed_by="bill", timestamp=201, sc_id=4, when=400000000, data_version=1
        )

    def testGetScheduledChanges(self):
        ret = self._get("/scheduled_changes/required_signoffs/product")
        expected = {
            "count": 3,
            "scheduled_changes": [
                {
                    "sc_id": 1,
                    "when": 100000000,
                    "scheduled_by": "bill",
                    "change_type": "insert",
                    "complete": False,
                    "sc_data_version": 1,
                    "product": "fake",
                    "channel": "a",
                    "role": "relman",
                    "signoffs_required": 1,
                    "data_version": None,
                    "signoffs": {"bill": "releng"},
                    "required_signoffs": {"releng": 1},
                },
                {
                    "sc_id": 2,
                    "when": 200000000,
                    "scheduled_by": "bill",
                    "change_type": "update",
                    "complete": False,
                    "sc_data_version": 1,
                    "product": "fake",
                    "channel": "a",
                    "role": "releng",
                    "signoffs_required": 2,
                    "data_version": 1,
                    "signoffs": {"bill": "releng"},
                    "required_signoffs": {"releng": 1},
                },
                {
                    "sc_id": 4,
                    "when": 400000000,
                    "scheduled_by": "bill",
                    "change_type": "delete",
                    "complete": False,
                    "sc_data_version": 1,
                    "product": "fake",
                    "channel": "j",
                    "role": "releng",
                    "signoffs_required": None,
                    "data_version": 1,
                    "signoffs": {"bill": "releng"},
                    "required_signoffs": {"releng": 1},
                },
            ],
        }
        self.assertEqual(ret.json(), expected)

    def testGetScheduledChangesWithArgs(self):
        ret = self._get("/scheduled_changes/required_signoffs/product", qs={"product": "fake", "channel": "a"})
        expected = {
            "count": 2,
            "scheduled_changes": [
                {
                    "sc_id": 1,
                    "when": 100000000,
                    "scheduled_by": "bill",
                    "change_type": "insert",
                    "complete": False,
                    "sc_data_version": 1,
                    "product": "fake",
                    "channel": "a",
                    "role": "relman",
                    "signoffs_required": 1,
                    "data_version": None,
                    "signoffs": {"bill": "releng"},
                    "required_signoffs": {"releng": 1},
                },
                {
                    "sc_id": 2,
                    "when": 200000000,
                    "scheduled_by": "bill",
                    "change_type": "update",
                    "complete": False,
                    "sc_data_version": 1,
                    "product": "fake",
                    "channel": "a",
                    "role": "releng",
                    "signoffs_required": 2,
                    "data_version": 1,
                    "signoffs": {"bill": "releng"},
                    "required_signoffs": {"releng": 1},
                },
            ],
        }
        self.assertEqual(ret.json(), expected)

    def testGetScheduledChangesWithCompleted(self):
        ret = self._get("/scheduled_changes/required_signoffs/product", qs={"all": 1})
        expected = {
            "count": 4,
            "scheduled_changes": [
                {
                    "sc_id": 1,
                    "when": 100000000,
                    "scheduled_by": "bill",
                    "change_type": "insert",
                    "complete": False,
                    "sc_data_version": 1,
                    "product": "fake",
                    "channel": "a",
                    "role": "relman",
                    "signoffs_required": 1,
                    "data_version": None,
                    "signoffs": {"bill": "releng"},
                    "required_signoffs": {"releng": 1},
                },
                {
                    "sc_id": 2,
                    "when": 200000000,
                    "scheduled_by": "bill",
                    "change_type": "update",
                    "complete": False,
                    "sc_data_version": 1,
                    "product": "fake",
                    "channel": "a",
                    "role": "releng",
                    "signoffs_required": 2,
                    "data_version": 1,
                    "signoffs": {"bill": "releng"},
                    "required_signoffs": {"releng": 1},
                },
                {
                    "sc_id": 3,
                    "when": 300000000,
                    "scheduled_by": "bill",
                    "change_type": "insert",
                    "complete": True,
                    "sc_data_version": 2,
                    "product": "fake",
                    "channel": "e",
                    "role": "releng",
                    "signoffs_required": 1,
                    "data_version": None,
                    "signoffs": {},
                    "required_signoffs": {},
                },
                {
                    "sc_id": 4,
                    "when": 400000000,
                    "scheduled_by": "bill",
                    "change_type": "delete",
                    "complete": False,
                    "sc_data_version": 1,
                    "product": "fake",
                    "channel": "j",
                    "role": "releng",
                    "signoffs_required": None,
                    "data_version": 1,
                    "signoffs": {"bill": "releng"},
                    "required_signoffs": {"releng": 1},
                },
            ],
        }
        self.assertEqual(ret.json(), expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeExistingRequiredSignoff(self):
        data = {"when": 400000000, "product": "fake", "channel": "k", "role": "relman", "signoffs_required": 2, "data_version": 2, "change_type": "update"}
        ret = self._post("/scheduled_changes/required_signoffs/product", data=data)
        self.assertEqual(ret.status_code, 200, ret.text)
        self.assertEqual(ret.json(), {"sc_id": 5, "signoffs": {}})
        r = dbo.productRequiredSignoffs.scheduled_changes.t.select().where(dbo.productRequiredSignoffs.scheduled_changes.sc_id == 5).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 5,
            "scheduled_by": "bill",
            "change_type": "update",
            "complete": False,
            "data_version": 1,
            "base_product": "fake",
            "base_channel": "k",
            "base_role": "relman",
            "base_signoffs_required": 2,
            "base_data_version": 2,
        }
        self.assertEqual(db_data, expected)
        cond = (
            dbo.productRequiredSignoffs.scheduled_changes.conditions.t.select()
            .where(dbo.productRequiredSignoffs.scheduled_changes.conditions.sc_id == 5)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 5, "data_version": 1, "when": 400000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeNewRequiredSignoff(self):
        data = {"when": 400000000, "product": "fake", "channel": "k", "role": "releng", "signoffs_required": 1, "change_type": "insert"}
        ret = self._post("/scheduled_changes/required_signoffs/product", data=data)
        self.assertEqual(ret.status_code, 200, ret.text)
        self.assertEqual(ret.json(), {"sc_id": 5, "signoffs": {}})
        r = dbo.productRequiredSignoffs.scheduled_changes.t.select().where(dbo.productRequiredSignoffs.scheduled_changes.sc_id == 5).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 5,
            "scheduled_by": "bill",
            "change_type": "insert",
            "complete": False,
            "data_version": 1,
            "base_product": "fake",
            "base_channel": "k",
            "base_role": "releng",
            "base_signoffs_required": 1,
            "base_data_version": None,
        }
        self.assertEqual(db_data, expected)
        cond = (
            dbo.productRequiredSignoffs.scheduled_changes.conditions.t.select()
            .where(dbo.productRequiredSignoffs.scheduled_changes.conditions.sc_id == 5)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 5, "data_version": 1, "when": 400000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeDeleteRequiredSignoff(self):
        data = {"when": 400000000, "product": "fake", "channel": "k", "role": "relman", "change_type": "delete", "data_version": 2}
        ret = self._post("/scheduled_changes/required_signoffs/product", data=data)
        self.assertEqual(ret.status_code, 200, ret.text)
        self.assertEqual(ret.json(), {"sc_id": 5, "signoffs": {}})
        r = dbo.productRequiredSignoffs.scheduled_changes.t.select().where(dbo.productRequiredSignoffs.scheduled_changes.sc_id == 5).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 5,
            "scheduled_by": "bill",
            "change_type": "delete",
            "complete": False,
            "data_version": 1,
            "base_product": "fake",
            "base_channel": "k",
            "base_role": "relman",
            "base_signoffs_required": None,
            "base_data_version": 2,
        }
        self.assertEqual(db_data, expected)
        cond = (
            dbo.productRequiredSignoffs.scheduled_changes.conditions.t.select()
            .where(dbo.productRequiredSignoffs.scheduled_changes.conditions.sc_id == 5)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 5, "data_version": 1, "when": 400000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledUnknownScheduledChangeID(self):
        data = {"signoffs_required": 1, "data_version": 1, "sc_data_version": 1, "when": 200000000}
        ret = self._post("/scheduled_changes/required_signoffs/product/98765432", data=data)
        self.assertEqual(ret.status_code, 404, ret.text)

        ret = self._post("/scheduled_changes/required_signoffs/permissions/98765432", data=data)
        self.assertEqual(ret.status_code, 404, ret.text)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeExistingRequiredSignoff(self):
        data = {"signoffs_required": 1, "data_version": 1, "sc_data_version": 1, "when": 200000000}
        ret = self._post("/scheduled_changes/required_signoffs/product/2", data=data)
        self.assertEqual(ret.status_code, 200, ret.text)
        self.assertEqual(ret.json(), {"new_data_version": 2, "signoffs": {"bill": "releng"}})

        r = dbo.productRequiredSignoffs.scheduled_changes.t.select().where(dbo.productRequiredSignoffs.scheduled_changes.sc_id == 2).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 2,
            "complete": False,
            "data_version": 2,
            "scheduled_by": "bill",
            "change_type": "update",
            "base_product": "fake",
            "base_channel": "a",
            "base_role": "releng",
            "base_signoffs_required": 1,
            "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)
        cond = (
            dbo.productRequiredSignoffs.scheduled_changes.conditions.t.select()
            .where(dbo.productRequiredSignoffs.scheduled_changes.conditions.sc_id == 2)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 2, "data_version": 2, "when": 200000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeNewRequiredSignoff(self):
        data = {"signoffs_required": 2, "sc_data_version": 1, "when": 450000000}
        ret = self._post("/scheduled_changes/required_signoffs/product/1", data=data)
        self.assertEqual(ret.status_code, 200, ret.text)
        self.assertEqual(ret.json(), {"new_data_version": 2, "signoffs": {"bill": "releng"}})

        r = dbo.productRequiredSignoffs.scheduled_changes.t.select().where(dbo.productRequiredSignoffs.scheduled_changes.sc_id == 1).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 1,
            "complete": False,
            "data_version": 2,
            "scheduled_by": "bill",
            "change_type": "insert",
            "base_product": "fake",
            "base_channel": "a",
            "base_role": "relman",
            "base_signoffs_required": 2,
            "base_data_version": None,
        }
        self.assertEqual(db_data, expected)
        cond = (
            dbo.productRequiredSignoffs.scheduled_changes.conditions.t.select()
            .where(dbo.productRequiredSignoffs.scheduled_changes.conditions.sc_id == 1)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 1, "data_version": 2, "when": 450000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    def testDeleteScheduledChange(self):
        ret = self._delete("/scheduled_changes/required_signoffs/product/1", qs={"data_version": 1})
        self.assertEqual(ret.status_code, 200, ret.text)
        got = dbo.productRequiredSignoffs.scheduled_changes.t.select().where(dbo.productRequiredSignoffs.scheduled_changes.sc_id == 1).execute().fetchall()
        self.assertEqual(got, [])
        cond_got = (
            dbo.productRequiredSignoffs.scheduled_changes.conditions.t.select()
            .where(dbo.productRequiredSignoffs.scheduled_changes.conditions.sc_id == 1)
            .execute()
            .fetchall()
        )
        self.assertEqual(cond_got, [])

    def testEnactScheduledChangeExistingRequiredSignoff(self):
        ret = self._post("/scheduled_changes/required_signoffs/product/2/enact")
        self.assertEqual(ret.status_code, 200, ret.text)

        r = dbo.productRequiredSignoffs.scheduled_changes.t.select().where(dbo.productRequiredSignoffs.scheduled_changes.sc_id == 2).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 2,
            "complete": True,
            "data_version": 2,
            "scheduled_by": "bill",
            "change_type": "update",
            "base_product": "fake",
            "base_channel": "a",
            "base_role": "releng",
            "base_signoffs_required": 2,
            "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)

        base_row = (
            dbo.productRequiredSignoffs.t.select()
            .where(dbo.productRequiredSignoffs.channel == "a")
            .where(dbo.productRequiredSignoffs.product == "fake")
            .where(dbo.productRequiredSignoffs.role == "releng")
            .execute()
            .fetchall()[0]
        )
        base_expected = {"product": "fake", "channel": "a", "role": "releng", "signoffs_required": 2, "data_version": 2}
        self.assertEqual(dict(base_row), base_expected)

    def testEnactScheduledChangeNewRequiredSignoff(self):
        ret = self._post("/scheduled_changes/required_signoffs/product/1/enact")
        self.assertEqual(ret.status_code, 200, ret.text)

        r = dbo.productRequiredSignoffs.scheduled_changes.t.select().where(dbo.productRequiredSignoffs.scheduled_changes.sc_id == 1).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 1,
            "complete": True,
            "data_version": 2,
            "scheduled_by": "bill",
            "change_type": "insert",
            "base_product": "fake",
            "base_channel": "a",
            "base_role": "relman",
            "base_signoffs_required": 1,
            "base_data_version": None,
        }
        self.assertEqual(db_data, expected)

        base_row = dict(
            dbo.productRequiredSignoffs.t.select()
            .where(dbo.productRequiredSignoffs.channel == "a")
            .where(dbo.productRequiredSignoffs.product == "fake")
            .where(dbo.productRequiredSignoffs.role == "relman")
            .execute()
            .fetchall()[0]
        )
        base_expected = {"product": "fake", "channel": "a", "role": "relman", "signoffs_required": 1, "data_version": 1}
        self.assertEqual(dict(base_row), base_expected)

    def testEnactScheduledChangeDeleteRequiredSignoff(self):
        ret = self._post("/scheduled_changes/required_signoffs/product/4/enact")
        self.assertEqual(ret.status_code, 200, ret.text)

        r = dbo.productRequiredSignoffs.scheduled_changes.t.select().where(dbo.productRequiredSignoffs.scheduled_changes.sc_id == 4).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 4,
            "complete": True,
            "data_version": 2,
            "scheduled_by": "bill",
            "change_type": "delete",
            "base_product": "fake",
            "base_channel": "j",
            "base_role": "releng",
            "base_signoffs_required": None,
            "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)

        base_row = (
            dbo.productRequiredSignoffs.t.select()
            .where(dbo.productRequiredSignoffs.channel == "j")
            .where(dbo.productRequiredSignoffs.product == "fake")
            .where(dbo.productRequiredSignoffs.role == "releng")
            .execute()
            .fetchall()
        )
        self.assertEqual(len(base_row), 0)

    def testGetScheduledChangeHistoryRevisions(self):
        ret = self._get("/scheduled_changes/required_signoffs/product/3/revisions")
        self.assertEqual(ret.status_code, 200, ret.text)
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
                    "product": "fake",
                    "channel": "e",
                    "role": "releng",
                    "signoffs_required": 1,
                    "when": 300000000,
                    "complete": True,
                    "sc_data_version": 2,
                },
                {
                    "change_id": 6,
                    "changed_by": "bill",
                    "timestamp": 81,
                    "sc_id": 3,
                    "scheduled_by": "bill",
                    "change_type": "insert",
                    "data_version": None,
                    "product": "fake",
                    "channel": "e",
                    "role": "releng",
                    "signoffs_required": 2,
                    "when": 300000000,
                    "complete": False,
                    "sc_data_version": 1,
                },
            ],
        }
        self.assertEqual(ret.json(), expected)

    @mock.patch("time.time", mock.MagicMock(return_value=100))
    def testSignoffWithPermission(self):
        ret = self._post("/scheduled_changes/required_signoffs/product/2/signoffs", data=dict(role="relman"), username="bob")
        self.assertEqual(ret.status_code, 200, ret.text)
        r = (
            dbo.productRequiredSignoffs.scheduled_changes.signoffs.t.select()
            .where(dbo.productRequiredSignoffs.scheduled_changes.signoffs.sc_id == 2)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(r), 2)
        self.assertEqual(dict(r[0]), {"sc_id": 2, "username": "bill", "role": "releng"})
        self.assertEqual(dict(r[1]), {"sc_id": 2, "username": "bob", "role": "relman"})
        r = (
            dbo.productRequiredSignoffs.scheduled_changes.signoffs.history.t.select()
            .where(dbo.productRequiredSignoffs.scheduled_changes.signoffs.history.sc_id == 2)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(r), 4)
        self.assertEqual(dict(r[0]), {"change_id": 3, "changed_by": "bill", "timestamp": 60, "sc_id": 2, "username": "bill", "role": None})
        self.assertEqual(dict(r[1]), {"change_id": 4, "changed_by": "bill", "timestamp": 61, "sc_id": 2, "username": "bill", "role": "releng"})
        self.assertEqual(dict(r[2]), {"change_id": 10, "changed_by": "bob", "timestamp": 99999, "sc_id": 2, "username": "bob", "role": None})
        self.assertEqual(dict(r[3]), {"change_id": 11, "changed_by": "bob", "timestamp": 100000, "sc_id": 2, "username": "bob", "role": "relman"})

    def testSignoffWithoutPermission(self):
        ret = self._post("/scheduled_changes/required_signoffs/product/2/signoffs", data=dict(role="relman"), username="bill")
        self.assertEqual(ret.status_code, 403, ret.text)

    def testRevokeSignoff(self):
        ret = self._delete("/scheduled_changes/required_signoffs/product/1/signoffs", username="bill")
        self.assertEqual(ret.status_code, 200, ret.text)
        r = (
            dbo.productRequiredSignoffs.scheduled_changes.signoffs.t.select()
            .where(dbo.productRequiredSignoffs.scheduled_changes.signoffs.sc_id == 1)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(r), 0)


class TestPermissionsRequiredSignoffs(ViewTest):
    def testGetRequiredSignoffs(self):
        ret = self._get("/required_signoffs/permissions")
        got = ret.json()
        self.assertEqual(got["count"], 5)
        expected = [
            {"product": "fake", "role": "releng", "signoffs_required": 1, "data_version": 1},
            {"product": "bar", "role": "releng", "signoffs_required": 1, "data_version": 1},
            {"product": "blah", "role": "releng", "signoffs_required": 1, "data_version": 1},
            {"product": "doop", "role": "releng", "signoffs_required": 1, "data_version": 2},
            {"product": "superfake", "role": "relman", "signoffs_required": 1, "data_version": 1},
        ]
        self.assertEqual(got["required_signoffs"], expected)

    def testAddRequiredSignoff(self):
        ret = self._post("/required_signoffs/permissions", data=dict(product="super", role="releng", signoffs_required=1))
        self.assertStatusCode(ret, 201)
        rs = (
            dbo.permissionsRequiredSignoffs.t.select()
            .where(dbo.permissionsRequiredSignoffs.product == "super")
            .where(dbo.permissionsRequiredSignoffs.role == "releng")
            .execute()
            .fetchall()
        )
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0]["signoffs_required"], 1)
        self.assertEqual(rs[0]["data_version"], 1)

    def testAddRequiredSignoffWithoutEnoughUsersInRole(self):
        ret = self._post("/required_signoffs/permissions", data=dict(product="super", role="releng", signoffs_required=3))
        self.assertStatusCode(ret, 400)
        self.assertIn("Cannot require 3 signoffs", ret.text)

    def testAddRequiredSignoffThatRequiresSignoff(self):
        ret = self._post("/required_signoffs/permissions", data=dict(product="fake", role="relman", signoffs_required=1))
        self.assertStatusCode(ret, 400)
        self.assertIn("No Signoffs given", ret.text)

    def testAddRequiredSignoffWithoutPermission(self):
        ret = self._post("/required_signoffs/permissions", data=dict(product="super", role="releng", signoffs_required=1), username="janet")
        self.assertStatusCode(ret, 403)

    def testModifyRequiredSignoff(self):
        ret = self._post("/required_signoffs/permissions", data=dict(product="fake", role="releng", signoffs_required=2, data_version=1))
        self.assertStatusCode(ret, 400)
        self.assertIn("Required Signoffs cannot be", ret.text)

    def testDeleteRequiredSignoff(self):
        ret = self._delete("/required_signoffs/permissions", qs=dict(product="fake", role="releng", data_version=1))
        self.assertStatusCode(ret, 400)


class TestPermissionsRequiredSignoffsHistoryView(ViewTest):
    maxDiff = 1000

    def testGetRevisions(self):
        ret = self._get("/required_signoffs/permissions/revisions", qs={"product": "doop", "role": "releng"})
        self.assertStatusCode(ret, 200)

        got = ret.json()
        expected = [
            {"change_id": 3, "changed_by": "bill", "timestamp": 25, "product": "doop", "role": "releng", "signoffs_required": 1, "data_version": 2},
            {"change_id": 2, "changed_by": "bill", "timestamp": 11, "product": "doop", "role": "releng", "signoffs_required": 2, "data_version": 1},
        ]
        self.assertEqual(got["count"], 2)
        self.assertEqual(got["required_signoffs"], expected)

    def testGetPermissionsRequiredSignoffsHistoryWithinTimeRange(self):
        ret = self._get("/required_signoffs/permissions/history", qs={"timestamp_from": 20, "timestamp_to": 30})
        self.assertStatusCode(ret, 200)

        got = ret.json()
        expected = [{"change_id": 3, "changed_by": "bill", "timestamp": 25, "product": "doop", "role": "releng", "signoffs_required": 1, "data_version": 2}]
        self.assertEqual(got["Permissions Required Signoffs"]["count"], 1)
        self.assertEqual(got["Permissions Required Signoffs"]["required_signoffs"], expected)


class TestPermissionsRequiredSignoffsScheduledChanges(ViewTest):
    maxDiff = 10000

    def setUp(self):
        super(TestPermissionsRequiredSignoffsScheduledChanges, self).setUp()
        dbo.permissionsRequiredSignoffs.scheduled_changes.t.insert().execute(
            sc_id=1, scheduled_by="bill", change_type="insert", data_version=1, base_product="superfake", base_role="releng", base_signoffs_required=1
        )
        dbo.permissionsRequiredSignoffs.scheduled_changes.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=20, sc_id=1)
        dbo.permissionsRequiredSignoffs.scheduled_changes.history.t.insert().execute(
            change_id=2,
            changed_by="bill",
            timestamp=21,
            sc_id=1,
            scheduled_by="bill",
            change_type="insert",
            data_version=1,
            base_product="superfake",
            base_role="releng",
            base_signoffs_required=1,
        )
        dbo.permissionsRequiredSignoffs.scheduled_changes.signoffs.t.insert().execute(sc_id=1, username="bob", role="relman")
        dbo.permissionsRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(
            change_id=1, changed_by="bob", timestamp=30, sc_id=1, username="bob"
        )
        dbo.permissionsRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(
            change_id=2, changed_by="bob", timestamp=31, sc_id=1, username="bob", role="relman"
        )
        dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.t.insert().execute(sc_id=1, when=100000000, data_version=1)
        dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=20, sc_id=1)
        dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(
            change_id=2, changed_by="bill", timestamp=21, sc_id=1, when=100000000, data_version=1
        )

        dbo.permissionsRequiredSignoffs.scheduled_changes.t.insert().execute(
            sc_id=2,
            scheduled_by="bill",
            change_type="update",
            data_version=1,
            base_product="fake",
            base_role="releng",
            base_signoffs_required=2,
            base_data_version=1,
        )
        dbo.permissionsRequiredSignoffs.scheduled_changes.history.t.insert().execute(change_id=3, changed_by="bill", timestamp=40, sc_id=2)
        dbo.permissionsRequiredSignoffs.scheduled_changes.history.t.insert().execute(
            change_id=4,
            changed_by="bill",
            timestamp=41,
            sc_id=2,
            scheduled_by="bill",
            change_type="update",
            data_version=1,
            base_product="fake",
            base_role="releng",
            base_signoffs_required=2,
            base_data_version=1,
        )
        dbo.permissionsRequiredSignoffs.scheduled_changes.signoffs.t.insert().execute(sc_id=2, username="bill", role="releng")
        dbo.permissionsRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(
            change_id=3, changed_by="bill", timestamp=60, sc_id=2, username="bill"
        )
        dbo.permissionsRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(
            change_id=4, changed_by="bill", timestamp=61, sc_id=2, username="bill", role="releng"
        )
        dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.t.insert().execute(sc_id=2, when=200000000, data_version=1)
        dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(change_id=3, changed_by="bill", timestamp=40, sc_id=2)
        dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(
            change_id=4, changed_by="bill", timestamp=41, sc_id=2, when=200000000, data_version=1
        )

        dbo.permissionsRequiredSignoffs.scheduled_changes.t.insert().execute(
            sc_id=3, scheduled_by="bill", change_type="insert", data_version=2, base_product="bar", base_role="releng", base_signoffs_required=1, complete=True
        )
        dbo.permissionsRequiredSignoffs.scheduled_changes.history.t.insert().execute(change_id=5, changed_by="bill", timestamp=80, sc_id=3)
        dbo.permissionsRequiredSignoffs.scheduled_changes.history.t.insert().execute(
            change_id=6,
            changed_by="bill",
            timestamp=81,
            sc_id=3,
            scheduled_by="bill",
            change_type="insert",
            data_version=1,
            base_product="bar",
            base_role="releng",
            base_signoffs_required=2,
            complete=False,
        )
        dbo.permissionsRequiredSignoffs.scheduled_changes.history.t.insert().execute(
            change_id=7,
            changed_by="bill",
            timestamp=100,
            sc_id=3,
            scheduled_by="bill",
            change_type="insert",
            data_version=2,
            base_product="bar",
            base_role="releng",
            base_signoffs_required=1,
            complete=True,
        )
        dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.t.insert().execute(sc_id=3, when=300000000, data_version=2)
        dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(change_id=5, changed_by="bill", timestamp=80, sc_id=3)
        dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(
            change_id=6, changed_by="bill", timestamp=81, sc_id=3, when=300000000, data_version=1
        )
        dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(
            change_id=7, changed_by="bill", timestamp=100, sc_id=3, when=300000000, data_version=2
        )

        dbo.permissionsRequiredSignoffs.scheduled_changes.t.insert().execute(
            sc_id=4, scheduled_by="bill", change_type="delete", data_version=1, base_product="blah", base_role="releng", base_data_version=1
        )
        dbo.permissionsRequiredSignoffs.scheduled_changes.history.t.insert().execute(change_id=8, changed_by="bill", timestamp=200, sc_id=4)
        dbo.permissionsRequiredSignoffs.scheduled_changes.history.t.insert().execute(
            change_id=9,
            changed_by="bill",
            timestamp=201,
            sc_id=4,
            scheduled_by="bill",
            change_type="delete",
            data_version=1,
            base_product="blah",
            base_role="releng",
            base_data_version=1,
        )
        dbo.permissionsRequiredSignoffs.scheduled_changes.signoffs.t.insert().execute(sc_id=4, username="bill", role="releng")
        dbo.permissionsRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(
            change_id=8, changed_by="bill", timestamp=300, sc_id=1, username="bill"
        )
        dbo.permissionsRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(
            change_id=9, changed_by="bill", timestamp=301, sc_id=1, username="bill", role="releng"
        )
        dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.t.insert().execute(sc_id=4, when=400000000, data_version=1)
        dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(change_id=8, changed_by="bill", timestamp=200, sc_id=4)
        dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(
            change_id=9, changed_by="bill", timestamp=201, sc_id=4, when=400000000, data_version=1
        )

    def testGetScheduledChanges(self):
        ret = self._get("/scheduled_changes/required_signoffs/permissions")
        expected = {
            "count": 3,
            "scheduled_changes": [
                {
                    "sc_id": 1,
                    "when": 100000000,
                    "scheduled_by": "bill",
                    "change_type": "insert",
                    "complete": False,
                    "sc_data_version": 1,
                    "product": "superfake",
                    "role": "releng",
                    "signoffs_required": 1,
                    "data_version": None,
                    "signoffs": {"bob": "relman"},
                    "required_signoffs": {"relman": 1},
                },
                {
                    "sc_id": 2,
                    "when": 200000000,
                    "scheduled_by": "bill",
                    "change_type": "update",
                    "complete": False,
                    "sc_data_version": 1,
                    "product": "fake",
                    "role": "releng",
                    "signoffs_required": 2,
                    "data_version": 1,
                    "signoffs": {"bill": "releng"},
                    "required_signoffs": {"releng": 1},
                },
                {
                    "sc_id": 4,
                    "when": 400000000,
                    "scheduled_by": "bill",
                    "change_type": "delete",
                    "complete": False,
                    "sc_data_version": 1,
                    "product": "blah",
                    "role": "releng",
                    "signoffs_required": None,
                    "data_version": 1,
                    "signoffs": {"bill": "releng"},
                    "required_signoffs": {"releng": 1},
                },
            ],
        }
        self.assertEqual(ret.json(), expected)

    def testGetScheduledChangesWithCompleted(self):
        ret = self._get("/scheduled_changes/required_signoffs/permissions", qs={"all": 1})
        expected = {
            "count": 4,
            "scheduled_changes": [
                {
                    "sc_id": 1,
                    "when": 100000000,
                    "scheduled_by": "bill",
                    "change_type": "insert",
                    "complete": False,
                    "sc_data_version": 1,
                    "product": "superfake",
                    "role": "releng",
                    "signoffs_required": 1,
                    "data_version": None,
                    "signoffs": {"bob": "relman"},
                    "required_signoffs": {"relman": 1},
                },
                {
                    "sc_id": 2,
                    "when": 200000000,
                    "scheduled_by": "bill",
                    "change_type": "update",
                    "complete": False,
                    "sc_data_version": 1,
                    "product": "fake",
                    "role": "releng",
                    "signoffs_required": 2,
                    "data_version": 1,
                    "signoffs": {"bill": "releng"},
                    "required_signoffs": {"releng": 1},
                },
                {
                    "sc_id": 3,
                    "when": 300000000,
                    "scheduled_by": "bill",
                    "change_type": "insert",
                    "complete": True,
                    "sc_data_version": 2,
                    "product": "bar",
                    "role": "releng",
                    "signoffs_required": 1,
                    "data_version": None,
                    "signoffs": {},
                    "required_signoffs": {},
                },
                {
                    "sc_id": 4,
                    "when": 400000000,
                    "scheduled_by": "bill",
                    "change_type": "delete",
                    "complete": False,
                    "sc_data_version": 1,
                    "product": "blah",
                    "role": "releng",
                    "signoffs_required": None,
                    "data_version": 1,
                    "signoffs": {"bill": "releng"},
                    "required_signoffs": {"releng": 1},
                },
            ],
        }
        self.assertEqual(ret.json(), expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeExistingRequiredSignoff(self):
        data = {"when": 400000000, "product": "doop", "role": "releng", "signoffs_required": 2, "data_version": 2, "change_type": "update"}
        ret = self._post("/scheduled_changes/required_signoffs/permissions", data=data)
        self.assertEqual(ret.status_code, 200, ret.text)
        self.assertEqual(ret.json(), {"sc_id": 5, "signoffs": {"bill": "releng"}})
        r = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.sc_id == 5)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 5,
            "scheduled_by": "bill",
            "change_type": "update",
            "complete": False,
            "data_version": 1,
            "base_product": "doop",
            "base_role": "releng",
            "base_signoffs_required": 2,
            "base_data_version": 2,
        }
        self.assertEqual(db_data, expected)
        cond = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.sc_id == 5)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 5, "data_version": 1, "when": 400000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeNewRequiredSignoff(self):
        data = {"when": 400000000, "product": "foo", "role": "relman", "signoffs_required": 1, "change_type": "insert"}
        ret = self._post("/scheduled_changes/required_signoffs/permissions", data=data)
        self.assertEqual(ret.status_code, 200, ret.text)
        self.assertEqual(ret.json(), {"sc_id": 5, "signoffs": {}})
        r = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.sc_id == 5)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 5,
            "scheduled_by": "bill",
            "change_type": "insert",
            "complete": False,
            "data_version": 1,
            "base_product": "foo",
            "base_role": "relman",
            "base_signoffs_required": 1,
            "base_data_version": None,
        }
        self.assertEqual(db_data, expected)
        cond = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.sc_id == 5)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 5, "data_version": 1, "when": 400000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeDeleteRequiredSignoff(self):
        data = {"when": 400000000, "product": "doop", "role": "releng", "change_type": "delete", "data_version": 2}
        ret = self._post("/scheduled_changes/required_signoffs/permissions", data=data)
        self.assertEqual(ret.status_code, 200, ret.text)
        self.assertEqual(ret.json(), {"sc_id": 5, "signoffs": {"bill": "releng"}})
        r = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.sc_id == 5)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 5,
            "scheduled_by": "bill",
            "change_type": "delete",
            "complete": False,
            "data_version": 1,
            "base_product": "doop",
            "base_role": "releng",
            "base_signoffs_required": None,
            "base_data_version": 2,
        }
        self.assertEqual(db_data, expected)
        cond = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.sc_id == 5)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 5, "data_version": 1, "when": 400000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeExistingRequiredSignoff(self):
        data = {"signoffs_required": 1, "data_version": 1, "sc_data_version": 1, "when": 200000000}
        ret = self._post("/scheduled_changes/required_signoffs/permissions/2", data=data)
        self.assertEqual(ret.status_code, 200, ret.text)
        self.assertEqual(ret.json(), {"new_data_version": 2, "signoffs": {"bill": "releng"}})

        r = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.sc_id == 2)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 2,
            "complete": False,
            "data_version": 2,
            "scheduled_by": "bill",
            "change_type": "update",
            "base_product": "fake",
            "base_role": "releng",
            "base_signoffs_required": 1,
            "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)
        cond = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.sc_id == 2)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 2, "data_version": 2, "when": 200000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeNewRequiredSignoff(self):
        data = {"signoffs_required": 2, "sc_data_version": 1, "when": 450000000}
        ret = self._post("/scheduled_changes/required_signoffs/permissions/1", data=data)
        self.assertEqual(ret.status_code, 200, ret.text)
        self.assertEqual(ret.json(), {"new_data_version": 2, "signoffs": {}})

        r = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.sc_id == 1)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 1,
            "complete": False,
            "data_version": 2,
            "scheduled_by": "bill",
            "change_type": "insert",
            "base_product": "superfake",
            "base_role": "releng",
            "base_signoffs_required": 2,
            "base_data_version": None,
        }
        self.assertEqual(db_data, expected)
        cond = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.sc_id == 1)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 1, "data_version": 2, "when": 450000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    def testDeleteScheduledChange(self):
        ret = self._delete("/scheduled_changes/required_signoffs/permissions/1", qs={"data_version": 1})
        self.assertEqual(ret.status_code, 200, ret.text)
        got = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.sc_id == 1)
            .execute()
            .fetchall()
        )
        self.assertEqual(got, [])
        cond_got = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.conditions.sc_id == 1)
            .execute()
            .fetchall()
        )
        self.assertEqual(cond_got, [])

    def testEnactScheduledChangeExistingRequiredSignoff(self):
        ret = self._post("/scheduled_changes/required_signoffs/permissions/2/enact")
        self.assertEqual(ret.status_code, 200, ret.text)

        r = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.sc_id == 2)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 2,
            "complete": True,
            "data_version": 2,
            "scheduled_by": "bill",
            "change_type": "update",
            "base_product": "fake",
            "base_role": "releng",
            "base_signoffs_required": 2,
            "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)

        base_row = (
            dbo.permissionsRequiredSignoffs.t.select()
            .where(dbo.permissionsRequiredSignoffs.product == "fake")
            .where(dbo.permissionsRequiredSignoffs.role == "releng")
            .execute()
            .fetchall()[0]
        )
        base_expected = {"product": "fake", "role": "releng", "signoffs_required": 2, "data_version": 2}
        self.assertEqual(dict(base_row), base_expected)

    def testEnactScheduledChangeNewRequiredSignoff(self):
        ret = self._post("/scheduled_changes/required_signoffs/permissions/1/enact")
        self.assertEqual(ret.status_code, 200, ret.text)

        r = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.sc_id == 1)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 1,
            "complete": True,
            "data_version": 2,
            "scheduled_by": "bill",
            "change_type": "insert",
            "base_product": "superfake",
            "base_role": "releng",
            "base_signoffs_required": 1,
            "base_data_version": None,
        }
        self.assertEqual(db_data, expected)

        base_row = dict(
            dbo.permissionsRequiredSignoffs.t.select()
            .where(dbo.permissionsRequiredSignoffs.product == "superfake")
            .where(dbo.permissionsRequiredSignoffs.role == "releng")
            .execute()
            .fetchall()[0]
        )
        base_expected = {"product": "superfake", "role": "releng", "signoffs_required": 1, "data_version": 1}
        self.assertEqual(dict(base_row), base_expected)

    def testEnactScheduledChangeDeleteRequiredSignoff(self):
        ret = self._post("/scheduled_changes/required_signoffs/permissions/4/enact")
        self.assertEqual(ret.status_code, 200, ret.text)

        r = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.sc_id == 4)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 4,
            "complete": True,
            "data_version": 2,
            "scheduled_by": "bill",
            "change_type": "delete",
            "base_product": "blah",
            "base_role": "releng",
            "base_signoffs_required": None,
            "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)

        base_row = (
            dbo.permissionsRequiredSignoffs.t.select()
            .where(dbo.permissionsRequiredSignoffs.product == "blah")
            .where(dbo.permissionsRequiredSignoffs.role == "releng")
            .execute()
            .fetchall()
        )
        self.assertEqual(len(base_row), 0)

    def testGetScheduledChangeHistoryRevisions(self):
        ret = self._get("/scheduled_changes/required_signoffs/permissions/3/revisions")
        self.assertEqual(ret.status_code, 200, ret.text)
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
                    "product": "bar",
                    "role": "releng",
                    "signoffs_required": 1,
                    "when": 300000000,
                    "complete": True,
                    "sc_data_version": 2,
                },
                {
                    "change_id": 6,
                    "changed_by": "bill",
                    "timestamp": 81,
                    "sc_id": 3,
                    "scheduled_by": "bill",
                    "change_type": "insert",
                    "data_version": None,
                    "product": "bar",
                    "role": "releng",
                    "signoffs_required": 2,
                    "when": 300000000,
                    "complete": False,
                    "sc_data_version": 1,
                },
            ],
        }
        self.assertEqual(ret.json(), expected)

    def testGetPermissionsRequiredSignoffsHistory(self):
        ret = self._get("/required_signoffs/permissions/history")
        self.assertEqual(ret.status_code, 200, ret.text)
        expected = {
            "count": 2,
            "required_signoffs": [
                {"data_version": 2, "changed_by": "bill", "product": "doop", "change_id": 3, "role": "releng", "signoffs_required": 1, "timestamp": 25},
                {"data_version": 1, "changed_by": "bill", "product": "doop", "change_id": 2, "role": "releng", "signoffs_required": 2, "timestamp": 11},
            ],
        }
        data = ret.json()
        revisions = data["Permissions Required Signoffs"]["required_signoffs"]
        expected_revisions = expected["required_signoffs"]
        for index in range(len(revisions)):
            self.assertEqual(revisions[index]["product"], expected_revisions[index]["product"])
            self.assertEqual(revisions[index]["timestamp"], expected_revisions[index]["timestamp"])
            self.assertEqual(revisions[index]["change_id"], expected_revisions[index]["change_id"])
            self.assertEqual(revisions[index]["data_version"], expected_revisions[index]["data_version"])
            self.assertEqual(revisions[index]["changed_by"], expected_revisions[index]["changed_by"])
        self.assertEqual(len(data["Permissions Required Signoffs"]["required_signoffs"]), 2)
        self.assertEqual(ret.json()["Permissions Required Signoffs"], expected)

    @mock.patch("time.time", mock.MagicMock(return_value=100))
    def testSignoffWithPermission(self):
        ret = self._post("/scheduled_changes/required_signoffs/permissions/2/signoffs", data=dict(role="relman"), username="bob")
        self.assertEqual(ret.status_code, 200, ret.text)
        r = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.signoffs.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.signoffs.sc_id == 2)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(r), 2)
        self.assertEqual(dict(r[0]), {"sc_id": 2, "username": "bill", "role": "releng"})
        self.assertEqual(dict(r[1]), {"sc_id": 2, "username": "bob", "role": "relman"})
        r = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.signoffs.history.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.signoffs.history.sc_id == 2)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(r), 4)
        self.assertEqual(dict(r[0]), {"change_id": 3, "changed_by": "bill", "timestamp": 60, "sc_id": 2, "username": "bill", "role": None})
        self.assertEqual(dict(r[1]), {"change_id": 4, "changed_by": "bill", "timestamp": 61, "sc_id": 2, "username": "bill", "role": "releng"})
        self.assertEqual(dict(r[2]), {"change_id": 10, "changed_by": "bob", "timestamp": 99999, "sc_id": 2, "username": "bob", "role": None})
        self.assertEqual(dict(r[3]), {"change_id": 11, "changed_by": "bob", "timestamp": 100000, "sc_id": 2, "username": "bob", "role": "relman"})

    def testSignoffWithoutPermission(self):
        ret = self._post("/scheduled_changes/required_signoffs/permissions/2/signoffs", data=dict(role="relman"), username="bill")
        self.assertEqual(ret.status_code, 403, ret.text)

    def testSignoffWithoutRole(self):
        ret = self._post("/scheduled_changes/required_signoffs/permissions/2/signoffs", data=dict(lorem="random"), username="bill")
        self.assertEqual(ret.status_code, 400, ret.text)

    def testRevokeSignoff(self):
        ret = self._delete("/scheduled_changes/required_signoffs/permissions/1/signoffs", username="bob")
        self.assertEqual(ret.status_code, 200, ret.text)
        r = (
            dbo.permissionsRequiredSignoffs.scheduled_changes.signoffs.t.select()
            .where(dbo.permissionsRequiredSignoffs.scheduled_changes.signoffs.sc_id == 1)
            .execute()
            .fetchall()
        )
        self.assertEqual(len(r), 0)
