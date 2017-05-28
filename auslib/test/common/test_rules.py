import json
from auslib.test.common.base import CommonTestBase


class TestPublicRulesAPI(CommonTestBase):
    def test_get_rules(self):
        ret = self.public_client.get("/rules")
        got = json.loads(ret.data)
        self.assertEquals(got["count"], 3)

    def test_get_rule_by_id(self):
        ret = self.public_client.get("/rules/1")
        self.assertEqual(ret.status_code, 200, ret.data)
        got = json.loads(ret.data)
        self.assertTrue(got, "Empty dict")

    def test_get_rule_by_alias(self):
        expected = dict(priority=90, backgroundRate=100, mapping="b",
                        update_type="minor", product="b", data_version=1,
                        alias="moz-releng", buildID=None, buildTarget=None,
                        channel=None, comment=None, distVersion=None,
                        distribution=None, fallbackMapping=None,
                        headerArchitecture=None, locale=None, version=None,
                        systemCapabilities=None, osVersion=None)
        ret = self.public_client.get("/rules/moz-releng")
        self.assertEqual(ret.status_code, 200, ret.data)
        got = json.loads(ret.data)
        del got["rule_id"]
        self.assertEqual(got, expected)

    def test_rule_not_found(self):
        ret = self.public_client.get("/rules/404")
        self.assertEqual(ret.status_code, 404)

    def test_get_revisions(self):
        user = {'REMOTE_USER': 'bill'}
        changes = dict(data_version=1, channel="nightly")
        ret = self.admin_client.post("/rules/1",
                                     data=json.dumps(changes),
                                     content_type="application/json",
                                     environ_base=user)
        self.assertEqual(ret.status_code, 200, ret.data)

        changes = dict(data_version=2, backgroundRate=42)
        ret = self.admin_client.post("/rules/1",
                                     data=json.dumps(changes),
                                     content_type="application/json",
                                     environ_base=user)
        self.assertEqual(ret.status_code, 200, ret.data)

        ret = self.public_client.get("/rules/1/revisions")
        self.assertEqual(ret.status_code, 200, ret.data)
        got = json.loads(ret.data)
        self.assertEqual(got["count"], 2)
