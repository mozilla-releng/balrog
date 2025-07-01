from .base import CommonTestBase


class TestPublicRulesAPI(CommonTestBase):
    def test_get_rules(self):
        ret = self.public_client.get("/api/v1/rules")
        got = ret.json()
        self.assertEqual(got["count"], 4)
        rules = [(rule["mapping"], rule["product"]) for rule in got["rules"]]
        self.assertIn(("Fennec.55.0a1", "Fennec"), rules)
        self.assertIn(("Firefox.55.0a1", "Firefox"), rules)
        self.assertIn(("q", "q"), rules)

    def test_get_rules_by_product(self):
        product = "Fennec"
        ret = self.public_client.get("/api/v1/rules?product={}".format(product))
        self.assertEqual(ret.status_code, 200, ret.text)
        got = ret.json()
        self.assertTrue(got, "No rules returned for product {}".format(product))
        self.assertEqual(got["count"], 1)
        self.assertEqual(got["rules"][0]["product"], product)

    def test_get_rule_by_id(self):
        rule_id = 2
        ret = self.public_client.get("/api/v1/rules/{}".format(rule_id))
        self.assertEqual(ret.status_code, 200, ret.text)
        got = ret.json()
        self.assertTrue(got, "Rule not found by rule_id={}".format(rule_id))
        self.assertEqual(ret.headers["X-Data-Version"], "1")
        self.assertEqual(got["rule_id"], rule_id)
        self.assertEqual(got["mapping"], "Firefox.55.0a1")
        self.assertEqual(got["product"], "Firefox")

    def test_get_rule_by_alias(self):
        expected = dict(
            rule_id=1,
            priority=90,
            backgroundRate=100,
            mapping="Fennec.55.0a1",
            update_type="minor",
            product="Fennec",
            data_version=1,
            alias="moz-releng",
            buildID=None,
            buildTarget=None,
            channel=None,
            comment=None,
            distVersion=None,
            distribution=None,
            fallbackMapping=None,
            headerArchitecture=None,
            locale=None,
            version=None,
            osVersion=None,
            memory=None,
            instructionSet=None,
            mig64=None,
            jaws=None,
        )
        ret = self.public_client.get("/api/v1/rules/moz-releng")
        self.assertEqual(ret.status_code, 200, ret.text)
        got = ret.json()
        self.assertEqual(got, expected)
        self.assertEqual(ret.headers["X-Data-Version"], "1")

    def test_rule_not_found(self):
        ret = self.public_client.get("/api/v1/rules/404")
        self.assertEqual(ret.status_code, 404)

    def test_get_revisions(self):
        ret = self.public_client.get("/api/v1/rules/3/revisions")
        self.assertEqual(ret.status_code, 200, ret.text)
        got = ret.json()
        self.assertEqual(got["count"], 2)
        rules = [(rule["mapping"], rule["product"], rule["data_version"]) for rule in got["rules"]]
        self.assertIn(("z", "z", 1), rules)
        self.assertIn(("y", "y", 2), rules)
