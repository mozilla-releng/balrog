import json

from auslib.global_state import dbo
from auslib.test.admin.views.base import ViewTest


# TODO: everything for permission required signoffs
class TestProductRequiredSignoffs(ViewTest):

    def testGetRequiredSignoffs(self):
        ret = self._get("/required_signoffs/product")
        got = json.loads(ret.data)
        self.assertEquals(got["count"], 2)
        expected = [
            {"product": "fake", "channel": "a", "role": "releng", "signoffs_required": 1, "data_version": 1},
            {"product": "fake", "channel": "j", "role": "releng", "signoffs_required": 1, "data_version": 1},
        ]
        self.assertEquals(got["required_signoffs"], expected)

    def testAddRequiredSignoff(self):
        ret = self._post("/required_signoffs/product", data=dict(product="fake", channel="b", role="releng", signoffs_required=1))
        self.assertStatusCode(ret, 201)
        rs = dbo.productRequiredSignoffs.t.select().where(dbo.productRequiredSignoffs.product == "fake")\
                                                   .where(dbo.productRequiredSignoffs.channel == "b")\
                                                   .where(dbo.productRequiredSignoffs.role == "releng")\
                                                   .execute().fetchall()
        self.assertEquals(len(rs), 1)
        self.assertEquals(rs[0]["signoffs_required"], 1)
        self.assertEquals(rs[0]["data_version"], 1)

    def testAddRequiredSignoffWithoutEnoughUsersInRole(self):
        ret = self._post("/required_signoffs/product", data=dict(product="fake", channel="b", role="releng", signoffs_required=3))
        self.assertStatusCode(ret, 400)
        self.assertIn("Cannot require 3 signoffs", ret.data)

    def testAddRequiredSignoffThatRequiresSignoff(self):
        ret = self._post("/required_signoffs/product", data=dict(product="fake", channel="a", role="relman", signoffs_required=1))
        self.assertStatusCode(ret, 400)
        self.assertIn("This change requires signoff", ret.data)

    def testAddRequiredSignoffWithoutPermission(self):
        ret = self._post("/required_signoffs/product", data=dict(product="fake", channel="b", role="releng", signoffs_required=1), username="janet")
        self.assertStatusCode(ret, 403)

    def testModifyRequiredSignoff(self):
        ret = self._post("/required_signoffs/product", data=dict(product="fake", channel="a", role="relman", signoffs_required=1, data_version=1))
        self.assertStatusCode(ret, 400)
        self.assertIn("This change requires signoff", ret.data)

    def testDeleteRequiredSignoff(self):
        ret = self._delete("/required_signoffs/product", qs=dict(product="fake", channel="a", role="relman", data_version=1))
        self.assertStatusCode(ret, 400)
        self.assertIn("This change requires signoff", ret.data)


class TestProductRequiredSignoffsScheduledChanges(ViewTest):
    maxDiff = 10000

    def setUp(self):
        super(TestProductRequiredSignoffsScheduledChanges, self).setUp()
        dbo.productRequiredSignoffs.scheduled_changes.t.insert().execute(
            sc_id=1, scheduled_by="bill", change_type="insert", data_version=1, base_product="fake", base_channel="c", base_role="releng",
            base_signoffs_required=1
        )
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=20, sc_id=1)
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(
            change_id=2, changed_by="bill", timestamp=21, sc_id=1, scheduled_by="bill", change_type="insert", data_version=1,
            base_product="fake", base_channel="c", base_role="releng", base_signoffs_required=1
        )
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.t.insert().execute(sc_id=1, username="bill", role="releng")
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=30, sc_id=1,
                                                                                          username="bill")
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(change_id=2, changed_by="bill", timestamp=31, sc_id=1,
                                                                                          username="bill", role="releng")
        dbo.productRequiredSignoffs.scheduled_changes.conditions.t.insert().execute(sc_id=1, when=100000000, data_version=1)
        dbo.productRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=20, sc_id=1)
        dbo.productRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(
            change_id=2, changed_by="bill", timestamp=21, sc_id=1, when=100000000, data_version=1
        )

        dbo.productRequiredSignoffs.scheduled_changes.t.insert().execute(
            sc_id=2, scheduled_by="bill", change_type="update", data_version=1, base_product="fake", base_channel="a", base_role="releng",
            base_signoffs_required=2, base_data_version=1
        )
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(change_id=3, changed_by="bill", timestamp=40, sc_id=2)
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(
            change_id=4, changed_by="bill", timestamp=41, sc_id=2, scheduled_by="bill", change_type="update", data_version=1,
            base_product="fake", base_channel="a", base_role="releng", base_signoffs_required=2, base_data_version=1
        )
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.t.insert().execute(sc_id=2, username="bill", role="releng")
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(change_id=3, changed_by="bill", timestamp=60, sc_id=2,
                                                                                          username="bill")
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(change_id=4, changed_by="bill", timestamp=61, sc_id=2,
                                                                                          username="bill", role="releng")
        dbo.productRequiredSignoffs.scheduled_changes.conditions.t.insert().execute(sc_id=2, when=200000000, data_version=1)
        dbo.productRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(change_id=3, changed_by="bill", timestamp=40, sc_id=2)
        dbo.productRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(
            change_id=4, changed_by="bill", timestamp=41, sc_id=2, when=200000000, data_version=1
        )

        dbo.productRequiredSignoffs.scheduled_changes.t.insert().execute(
            sc_id=3, scheduled_by="bill", change_type="insert", data_version=2, base_product="fake", base_channel="e", base_role="releng",
            base_signoffs_required=1, complete=True
        )
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(change_id=5, changed_by="bill", timestamp=80, sc_id=3)
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(
            change_id=6, changed_by="bill", timestamp=81, sc_id=3, scheduled_by="bill", change_type="insert", data_version=1,
            base_product="fake", base_channel="e", base_role="releng", base_signoffs_required=2, complete=False
        )
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(
            change_id=7, changed_by="bill", timestamp=100, sc_id=3, scheduled_by="bill", change_type="insert", data_version=2,
            base_product="fake", base_channel="e", base_role="releng", base_signoffs_required=1, complete=True
        )
        dbo.productRequiredSignoffs.scheduled_changes.conditions.t.insert().execute(sc_id=3, when=300000000, data_version=2)
        dbo.productRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(change_id=5, changed_by="bill", timestamp=80, sc_id=3)
        dbo.productRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(
            change_id=6, changed_by="bill", timestamp=81, sc_id=3, when=300000000, data_version=1
        )
        dbo.productRequiredSignoffs.scheduled_changes.conditions.history.t.insert().execute(
            change_id=7, changed_by="bill", timestamp=81, sc_id=3, when=300000000, data_version=2
        )

        dbo.productRequiredSignoffs.scheduled_changes.t.insert().execute(
            sc_id=4, scheduled_by="bill", change_type="delete", data_version=1, base_product="fake", base_channel="j", base_role="releng",
            base_data_version=1,
        )
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(change_id=8, changed_by="bill", timestamp=200, sc_id=4)
        dbo.productRequiredSignoffs.scheduled_changes.history.t.insert().execute(
            change_id=9, changed_by="bill", timestamp=201, sc_id=4, scheduled_by="bill", change_type="delete", data_version=1,
            base_product="fake", base_channel="j", base_role="releng", base_data_version=1
        )
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.t.insert().execute(sc_id=4, username="bill", role="releng")
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(change_id=8, changed_by="bill", timestamp=300, sc_id=1,
                                                                                          username="bill")
        dbo.productRequiredSignoffs.scheduled_changes.signoffs.history.t.insert().execute(change_id=9, changed_by="bill", timestamp=301, sc_id=1,
                                                                                          username="bill", role="releng")
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
                    "sc_id": 1, "when": 100000000, "scheduled_by": "bill", "change_type": "insert", "complete": False, "sc_data_version": 1,
                    "product": "fake", "channel": "c", "role": "releng", "signoffs_required": 1, "data_version": None,
                    "signoffs": {"bill": "releng"},
                },
                {
                    "sc_id": 2, "when": 200000000, "scheduled_by": "bill", "change_type": "update", "complete": False, "sc_data_version": 1,
                    "product": "fake", "channel": "a", "role": "releng", "signoffs_required": 2, "data_version": 1,
                    "signoffs": {"bill": "releng"},
                },
                {
                    "sc_id": 4, "when": 400000000, "scheduled_by": "bill", "change_type": "delete", "complete": False, "sc_data_version": 1,
                    "product": "fake", "channel": "j", "role": "releng", "signoffs_required": None, "data_version": 1,
                    "signoffs": {"bill": "releng"},
                },
            ],
        }
        self.assertEquals(json.loads(ret.data), expected)

    def testGetScheduledChangesWithCompleted(self):
        ret = self._get("/scheduled_changes/required_signoffs/product", qs={"all": 1})
        expected = {
            "count": 4,
            "scheduled_changes": [
                {
                    "sc_id": 1, "when": 100000000, "scheduled_by": "bill", "change_type": "insert", "complete": False, "sc_data_version": 1,
                    "product": "fake", "channel": "c", "role": "releng", "signoffs_required": 1, "data_version": None,
                    "signoffs": {"bill": "releng"},
                },
                {
                    "sc_id": 2, "when": 200000000, "scheduled_by": "bill", "change_type": "update", "complete": False, "sc_data_version": 1,
                    "product": "fake", "channel": "a", "role": "releng", "signoffs_required": 2, "data_version": 1,
                    "signoffs": {"bill": "releng"},
                },
                {
                    "sc_id": 3, "when": 300000000, "scheduled_by": "bill", "change_type": "insert", "complete": True, "sc_data_version": 2,
                    "product": "fake", "channel": "e", "role": "releng", "signoffs_required": 1, "data_version": None,
                    "signoffs": {},
                },
                {
                    "sc_id": 4, "when": 400000000, "scheduled_by": "bill", "change_type": "delete", "complete": False, "sc_data_version": 1,
                    "product": "fake", "channel": "j", "role": "releng", "signoffs_required": None, "data_version": 1,
                    "signoffs": {"bill": "releng"},
                },
            ],
        }
        self.assertEquals(json.loads(ret.data), expected)

