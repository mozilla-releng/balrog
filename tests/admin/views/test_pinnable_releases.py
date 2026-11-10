from auslib.global_state import dbo

from .base import ViewTest


class TestRuleScheduledChanges(ViewTest):
    maxDiff = 50000

    def setUp(self):
        super(TestRuleScheduledChanges, self).setUp()
        with dbo.engine.begin() as conn:
            conn.execute(
                dbo.pinnable_releases.scheduled_changes.t.insert(),
                {
                    "sc_id": 1,
                    "scheduled_by": "bill",
                    "data_version": 1,
                    "change_type": "insert",
                    "base_product": "a",
                    "base_channel": "c",
                    "base_version": "1.",
                    "base_mapping": "a",
                    "base_data_version": 1,
                },
            )
            conn.execute(dbo.pinnable_releases.scheduled_changes.conditions.t.insert(), {"sc_id": 1, "when": 1000000, "data_version": 1})

    def testGetScheduledChanges(self):
        ret = self._get("/scheduled_changes/pinnable_releases")
        expected = {
            "count": 1,
            "scheduled_changes": [
                {
                    "sc_id": 1,
                    "when": 1000000,
                    "scheduled_by": "bill",
                    "sc_data_version": 1,
                    "data_version": 1,
                    "change_type": "insert",
                    "product": "a",
                    "channel": "c",
                    "version": "1.",
                    "mapping": "a",
                    "complete": False,
                    "required_signoffs": {},
                    "signoffs": {},
                },
            ],
        }
        self.assertEqual(ret.get_json(), expected)

    def testEnactScheduledChange(self):
        ret = self._post("/scheduled_changes/pinnable_releases/1/enact", username="mary")
        self.assertEqual(ret.mimetype, "application/json")
        self.assertEqual(ret.status_code, 200, ret.get_data())

        with dbo.engine.connect() as conn:
            sc_row = conn.execute(dbo.pinnable_releases.scheduled_changes.t.select().where(dbo.pinnable_releases.scheduled_changes.sc_id == 1)).fetchall()[0]
            self.assertEqual(sc_row._mapping["complete"], True)

            row = conn.execute(dbo.pinnable_releases.t.select().where(dbo.pinnable_releases.mapping == "a")).fetchall()[0]
        expected = {
            "product": "a",
            "channel": "c",
            "version": "1.",
            "mapping": "a",
            "data_version": 1,
        }
        self.assertEqual(dict(row._mapping), expected)
