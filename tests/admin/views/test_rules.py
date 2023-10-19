# This Python file uses the following encoding: utf-8
import mock

from auslib.global_state import dbo
from auslib.util.comparison import operators

from .base import ViewTest


class TestRulesAPI_JSON(ViewTest):
    maxDiff = 1000

    def testGetRules(self):
        ret = self._get("/rules")
        got = ret.get_json()
        self.assertEqual(got["count"], 9)

    def testGetRulesWithProductFilter(self):
        ret = self._get("/rules", qs={"product": "fake"})
        self.assertEqual(ret.status_code, 200, ret.data)
        got = ret.get_json()
        expected = [
            {
                "rule_id": 4,
                "product": "fake",
                "priority": 80,
                "buildTarget": "d",
                "backgroundRate": 100,
                "mapping": "a",
                "update_type": "minor",
                "channel": "a",
                "data_version": 1,
                "comment": None,
                "fallbackMapping": None,
                "version": None,
                "buildID": None,
                "locale": None,
                "distribution": None,
                "osVersion": None,
                "instructionSet": None,
                "distVersion": None,
                "headerArchitecture": None,
                "alias": None,
                "memory": None,
                "mig64": None,
                "jaws": None,
            },
            {
                "rule_id": 6,
                "product": "fake",
                "priority": 40,
                "backgroundRate": 50,
                "mapping": "a",
                "update_type": "minor",
                "channel": "e",
                "data_version": 1,
                "buildTarget": None,
                "comment": None,
                "fallbackMapping": None,
                "version": None,
                "buildID": None,
                "locale": None,
                "distribution": None,
                "osVersion": None,
                "instructionSet": None,
                "distVersion": None,
                "headerArchitecture": None,
                "alias": None,
                "memory": None,
                "mig64": None,
                "jaws": None,
            },
            {
                "rule_id": 7,
                "product": "fake",
                "priority": 30,
                "backgroundRate": 85,
                "mapping": "a",
                "update_type": "minor",
                "channel": "c",
                "data_version": 1,
                "buildTarget": None,
                "comment": None,
                "fallbackMapping": None,
                "version": None,
                "buildID": None,
                "locale": None,
                "distribution": None,
                "osVersion": None,
                "instructionSet": None,
                "distVersion": None,
                "headerArchitecture": None,
                "alias": None,
                "memory": None,
                "mig64": None,
                "jaws": None,
            },
        ]
        self.assertEqual(got["count"], 3)
        rules = sorted(got["rules"], key=lambda r: r["rule_id"])
        self.assertEqual(rules, expected)

    def testGetRulesWithTimestampFilter(self):
        ret = self._get("/rules", qs={"timestamp": 75})
        expected = (
            {
                "change_id": 3,
                "timestamp": 65,
                "changed_by": "bill",
                "rule_id": 1,
                "product": "a",
                "priority": 100,
                "backgroundRate": 100,
                "mapping": "c",
                "update_type": "minor",
                "channel": "a",
                "data_version": 2,
                "buildTarget": "d",
                "version": "3.5",
                "comment": None,
                "fallbackMapping": None,
                "buildID": None,
                "locale": None,
                "distribution": None,
                "osVersion": None,
                "instructionSet": None,
                "distVersion": None,
                "headerArchitecture": None,
                "alias": None,
                "memory": None,
                "mig64": None,
                "jaws": None,
            },
            {
                "change_id": 5,
                "timestamp": 61,
                "changed_by": "bill",
                "rule_id": 2,
                "product": "a",
                "priority": 100,
                "backgroundRate": 100,
                "mapping": "b",
                "update_type": "minor",
                "channel": "a",
                "data_version": 1,
                "buildTarget": "d",
                "version": "3.3",
                "alias": "frodo",
                "comment": None,
                "fallbackMapping": None,
                "buildID": None,
                "locale": None,
                "distribution": None,
                "osVersion": None,
                "instructionSet": None,
                "distVersion": None,
                "headerArchitecture": None,
                "memory": None,
                "mig64": None,
                "jaws": None,
            },
            {
                "change_id": 7,
                "timestamp": 73,
                "changed_by": "bill",
                "rule_id": 3,
                "product": "a",
                "priority": 50,
                "backgroundRate": 100,
                "mapping": "a",
                "update_type": "minor",
                "channel": "a",
                "data_version": 1,
                "buildTarget": "a",
                "version": "3.5",
                "alias": None,
                "comment": None,
                "fallbackMapping": None,
                "buildID": None,
                "locale": None,
                "distribution": None,
                "osVersion": None,
                "instructionSet": None,
                "distVersion": None,
                "headerArchitecture": None,
                "memory": None,
                "mig64": None,
                "jaws": None,
            },
        )
        got = ret.get_json()
        rules = sorted(got["rules"], key=lambda r: r["rule_id"])
        self.assertSequenceEqual(rules, expected)

    def testGetRulesWithVariousTimestampFilter(self):
        times_and_results = (
            (50, []),
            (70, [{"change_id": 3, "timestamp": 65, "rule_id": 1}, {"change_id": 5, "timestamp": 61, "rule_id": 2}]),
            (
                90,
                [
                    {"change_id": 3, "timestamp": 65, "rule_id": 1},
                    {"change_id": 5, "timestamp": 61, "rule_id": 2},
                    {"change_id": 7, "timestamp": 73, "rule_id": 3},
                    {"change_id": 10, "timestamp": 81, "rule_id": 4},
                ],
            ),
            (
                110,
                [
                    {"change_id": 3, "timestamp": 65, "rule_id": 1},
                    {"change_id": 5, "timestamp": 61, "rule_id": 2},
                    {"change_id": 8, "timestamp": 105, "rule_id": 3},
                    {"change_id": 10, "timestamp": 81, "rule_id": 4},
                    {"change_id": 12, "timestamp": 91, "rule_id": 5},
                ],
            ),
            (
                130,
                [
                    {"change_id": 3, "timestamp": 65, "rule_id": 1},
                    {"change_id": 5, "timestamp": 61, "rule_id": 2},
                    {"change_id": 8, "timestamp": 105, "rule_id": 3},
                    {"change_id": 10, "timestamp": 81, "rule_id": 4},
                    {"change_id": 12, "timestamp": 91, "rule_id": 5},
                    {"change_id": 14, "timestamp": 111, "rule_id": 6},
                    {"change_id": 16, "timestamp": 116, "rule_id": 7},
                ],
            ),
            (
                170,
                [
                    {"change_id": 3, "timestamp": 65, "rule_id": 1},
                    {"change_id": 5, "timestamp": 61, "rule_id": 2},
                    {"change_id": 8, "timestamp": 105, "rule_id": 3},
                    {"change_id": 10, "timestamp": 81, "rule_id": 4},
                    {"change_id": 12, "timestamp": 91, "rule_id": 5},
                    {"change_id": 14, "timestamp": 111, "rule_id": 6},
                    {"change_id": 16, "timestamp": 116, "rule_id": 7},
                    {"change_id": 18, "timestamp": 151, "rule_id": 8},
                    {"change_id": 20, "timestamp": 161, "rule_id": 9},
                ],
            ),
        )

        for timestamp, expected in times_and_results:
            ret = self._get("/rules", qs={"timestamp": timestamp})
            self.assertEqual(ret.status_code, 200, ret.data)
            got = ret.get_json()
            rules = sorted(got["rules"], key=lambda r: r["rule_id"])
            important_values = [{k: r[k] for k in ("change_id", "timestamp", "rule_id")} for r in rules]
            self.assertSequenceEqual(important_values, expected)

    def testGetRulesWithProductAndTimestampFilter(self):
        ret = self._get("/rules", qs={"product": "a", "timestamp": 23456789})
        self.assertEqual(ret.status_code, 400, ret.data)

    def testNewRulePost(self):
        ret = self._post("/rules", data=dict(backgroundRate=31, mapping="c", priority=33, product="Firefox", update_type="minor", channel="nightly"))
        rule_id = int(ret.get_data())
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, rule_id))
        r = dbo.rules.t.select().where(dbo.rules.rule_id == rule_id).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["mapping"], "c")
        self.assertEqual(r[0]["backgroundRate"], 31)
        self.assertEqual(r[0]["priority"], 33)
        self.assertEqual(r[0]["data_version"], 1)

    def testNewRulePostWithUnicode(self):
        ret = self._post("/rules", data=dict(backgroundRate=31, mapping="c", priority=33, product="Firefox", update_type="minor", channel="nightlyÁ"))
        self.assertEqual(ret.status_code, 400, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))

    def testNewRulePostWithGlob(self):
        ret = self._post("/rules", data=dict(backgroundRate=31, mapping="c", priority=33, product="Firefox", update_type="minor", version="99.98.*"))
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))

    def testBackgroundRateZero(self):
        ret = self._post("/rules", data=dict(backgroundRate=0, mapping="c", priority=33, product="Firefox", update_type="minor", channel="nightly"))
        rule_id = int(ret.get_data())
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, rule_id))
        r = dbo.rules.t.select().where(dbo.rules.rule_id == rule_id).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["mapping"], "c")
        self.assertEqual(r[0]["backgroundRate"], 0)
        self.assertEqual(r[0]["priority"], 33)
        self.assertEqual(r[0]["data_version"], 1)

    def testPriorityZero(self):
        ret = self._post("/rules", data=dict(backgroundRate=33, mapping="c", priority=0, product="Firefox", update_type="minor", channel="nightly"))
        rule_id = int(ret.get_data())
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, rule_id))
        r = dbo.rules.t.select().where(dbo.rules.rule_id == rule_id).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["mapping"], "c")
        self.assertEqual(r[0]["backgroundRate"], 33)
        self.assertEqual(r[0]["priority"], 0)
        self.assertEqual(r[0]["data_version"], 1)

    def testCreateRuleWithMemory(self):
        ret = self._post(
            "/rules", data=dict(backgroundRate=33, mapping="c", priority=0, memory="<7373", product="Firefox", update_type="minor", channel="nightly")
        )
        rule_id = int(ret.get_data())
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, rule_id))
        r = dbo.rules.t.select().where(dbo.rules.rule_id == rule_id).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["mapping"], "c")
        self.assertEqual(r[0]["backgroundRate"], 33)
        self.assertEqual(r[0]["priority"], 0)
        self.assertEqual(r[0]["memory"], "<7373")
        self.assertEqual(r[0]["data_version"], 1)

    def testCreateRuleWithMig64(self):
        ret = self._post("/rules", data=dict(backgroundRate=33, mapping="c", priority=0, mig64=True, product="Firefox", update_type="minor", channel="nightly"))
        rule_id = int(ret.get_data())
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, rule_id))
        r = dbo.rules.t.select().where(dbo.rules.rule_id == rule_id).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["mapping"], "c")
        self.assertEqual(r[0]["backgroundRate"], 33)
        self.assertEqual(r[0]["priority"], 0)
        self.assertEqual(r[0]["mig64"], True)
        self.assertEqual(r[0]["data_version"], 1)

    def testCreateRuleWithJaws(self):
        ret = self._post("/rules", data=dict(backgroundRate=33, mapping="c", priority=0, jaws=True, product="Firefox", update_type="minor", channel="nightly"))
        rule_id = int(ret.get_data())
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, rule_id))
        r = dbo.rules.t.select().where(dbo.rules.rule_id == rule_id).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["mapping"], "c")
        self.assertEqual(r[0]["backgroundRate"], 33)
        self.assertEqual(r[0]["priority"], 0)
        self.assertEqual(r[0]["jaws"], True)
        self.assertEqual(r[0]["data_version"], 1)

    def testVersionMaxFieldLength(self):
        # Max field length of rules.version is 75
        version = "3.3,3.4,3.5,3.6,3.8,3.9,3.10,3.11,3.12,3.13,3.14,3.15"
        ret = self._post(
            "/rules/1",
            data=dict(
                backgroundRate=71,
                mapping="d",
                version="{}".format(version),
                priority=73,
                data_version=2,
                product="Firefox",
                update_type="minor",
                channel="nightly",
                buildID="1234",
                osVersion="10.5",
                headerArchitecture="INTEL",
                distVersion="19",
                buildTarget="MAC",
            ),
        )
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        ret = dbo.rules.select(where={"rule_id": 1}, columns=["version"])
        self.assertEqual(ret[0].get("version"), version)
        self.assertEqual(len(ret[0].get("version")), len(version))

    def testNewRuleWithoutProductAdminPermission(self):
        data = dict(backgroundRate=31, mapping="a", priority=33, product="Firefox", update_type="minor", channel="nightly")
        ret = self._post("/rules", data=data, username="billy")
        self.assertStatusCode(ret, 403)

    def testNewRuleWithProductAdminPermission(self):
        data = dict(backgroundRate=31, mapping="a", priority=33, product="a", update_type="minor", channel="nightly")
        ret = self._post("/rules", data=data, username="billy")
        self.assertStatusCode(ret, 200)

    def testNewRuleWithoutPermission(self):
        data = dict(backgroundRate=31, mapping="c", priority=33, product="Firefox", update_type="minor", channel="nightly")
        ret = self._post("/rules", data=data, username="jack")
        self.assertEqual(ret.status_code, 403, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))

    def testNewRuleWithWhitespaceInLocale(self):
        data = dict(backgroundRate=31, mapping="a", priority=33, product="a", update_type="minor", channel="nightly", locale="de, en-US, hu, it, zh-TW")
        ret = self._post("/rules", data=data, username="billy")
        rule_id = int(ret.get_data())
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, rule_id))
        r = dbo.rules.t.select().where(dbo.rules.rule_id == rule_id).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["mapping"], "a")
        self.assertEqual(r[0]["backgroundRate"], 31)
        self.assertEqual(r[0]["priority"], 33)
        self.assertEqual(r[0]["data_version"], 1)
        self.assertEqual(r[0]["locale"], "de,en-US,hu,it,zh-TW")

    # A POST without the required fields shouldn't be valid
    def testMissingFields(self):
        # But we still need to pass product, because permission checking
        # is done before what we're testing
        post_data = {"product": "a"}
        ret = self._post("/rules", data=post_data)
        self.assertEqual(ret.status_code, 400, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        # Connexion and manual request.json validation methods will preempt and throw 400 error as
        # soon as the first field invalidates. Only one field may be present in the response.get_data() depending
        # upon the order of fields sorted in swagger yaml file and in views.
        post_data["update_type"] = "minor"
        ret = self._post("/rules", data=post_data)

        self.assertEqual(ret.status_code, 400, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        self.assertTrue("backgroundRate" in ret.get_data(as_text=True), msg=ret.get_data())
        post_data["backgroundRate"] = 10
        ret = self._post("/rules", data=post_data)

        self.assertEqual(ret.status_code, 400, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        self.assertTrue("priority" in ret.get_data(as_text=True), msg=ret.get_data())

    def testVersionValidation(self):
        for op in operators:
            ret = self._post(
                "/rules",
                data=dict(backgroundRate=42, mapping="d", priority=50, product="Firefox", channel="nightly", update_type="minor", version="%s4.0" % op),
            )
            rule_id = int(ret.get_data())
            self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s, Operator: %s" % (ret.status_code, rule_id, op))
            r = dbo.rules.t.select().where(dbo.rules.rule_id == rule_id).execute().fetchall()
            self.assertEqual(len(r), 1)
            self.assertEqual(r[0]["version"], "%s4.0" % op)

    def testVersionValidationRequiresAtLeastTwoPartVersion(self):
        ret = self._post(
            "/rules", data=dict(backgroundRate=42, mapping="d", priority=50, product="Firefox", channel="nightly", update_type="minor", version="5")
        )
        self.assertEqual(ret.status_code, 400)

    def testVersionValidationRequiresAtLeastTwoPartVersionWithOperator(self):
        for op in operators:
            ret = self._post(
                "/rules", data=dict(backgroundRate=42, mapping="d", priority=50, product="Firefox", channel="nightly", update_type="minor", version="%s5" % op)
            )
            self.assertEqual(ret.status_code, 400)

    def testVersionValidationAlphaTagsAllowedForModernVersions(self):
        ret = self._post(
            "/rules", data=dict(backgroundRate=42, mapping="d", priority=50, product="Firefox", channel="nightly", update_type="minor", version="5.0a1")
        )
        rule_id = int(ret.get_data())
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, rule_id))
        r = dbo.rules.t.select().where(dbo.rules.rule_id == rule_id).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["version"], "5.0a1")

    def testVersionValidationNoBetaTagsAllowedForModernVersions(self):
        ret = self._post(
            "/rules", data=dict(backgroundRate=42, mapping="d", priority=50, product="Firefox", channel="nightly", update_type="minor", version="5.0b4")
        )
        self.assertEqual(ret.status_code, 400)

    def testBuildIDValidation(self):
        for op in operators:
            ret = self._post(
                "/rules",
                data=dict(
                    backgroundRate=42, mapping="d", priority=50, product="Firefox", channel="nightly", update_type="minor", buildID="%s20010101000000" % op
                ),
            )
            rule_id = int(ret.get_data())
            self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s, Operator: %s" % (ret.status_code, rule_id, op))
            r = dbo.rules.t.select().where(dbo.rules.rule_id == rule_id).execute().fetchall()
            self.assertEqual(len(r), 1)
            self.assertEqual(r[0]["buildID"], "%s20010101000000" % op)

    def testBuildIDDoesntAcceptStrings(self):
        for buildid in ("abcdef", "<abcdef"):
            ret = self._post(
                "/rules", data=dict(backgroundRate=42, mapping="d", priority=50, product="Firefox", channel="nightly", update_type="minor", buildID=buildid)
            )
            self.assertEqual(ret.status_code, 400, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))

    def testVersionListValidInput(self):
        for validVersionList in ("3.3,4.2", "3.1.3,4.2"):
            ret = self._post(
                "/rules",
                data=dict(backgroundRate=42, mapping="d", priority=50, product="Firefox", channel="nightly", update_type="minor", version=validVersionList),
            )
            self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s, Input: %s" % (ret.status_code, ret.get_data(), validVersionList))

    def testVersionValidationBogusInput(self):
        for bogus in (
            "<= 4.0",
            " <=4.0",
            "<>4.0",
            "<=-4.0",
            "=4.0",
            "> 4.0",
            ">= 4.0",
            " >=4.0",
            " 4.0 ",
            "<=4.0,3.0",
            ">=4.0,3.0",
            "4.0,<3.0",
            "4.0,>3.0",
            "=4.0,3.0",
            "=4.0,=3.0",
            "4.0,=3.0",
        ):
            ret = self._post(
                "/rules", data=dict(backgroundRate=42, mapping="d", priority=50, product="Firefox", channel="nightly", update_type="minor", version=bogus)
            )
            self.assertEqual(ret.status_code, 400, "Status Code: %d, Data: %s, Input: %s" % (ret.status_code, ret.get_data(), bogus))
            self.assertTrue("version" in ret.get_data(as_text=True), msg=ret.get_data())

    def testBuilIDValidationBogusInput(self):
        for bogus in ("<= 4120", " <=4120", "<>4120", "<=-4120", "=41230", "> 41210", ">= 41220", " >=41220", " 41220 "):
            ret = self._post(
                "/rules", data=dict(backgroundRate=42, mapping="d", priority=50, product="Firefox", channel="nightly", update_type="minor", buildID=bogus)
            )
            self.assertEqual(ret.status_code, 400, "Status Code: %d, Data: %s, Input: %s" % (ret.status_code, ret.get_data(), bogus))
            self.assertTrue("buildID" in ret.get_data(as_text=True), msg=ret.get_data())

    def testValidationEmptyInput(self):
        ret = self._post(
            "/rules", data=dict(backgroundRate=42, mapping="d", priority=50, product="Firefox", channel="nightly", update_type="minor", version="", buildID="")
        )
        rule_id = int(ret.get_data())
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, rule_id))
        r = dbo.rules.t.select().where(dbo.rules.rule_id == rule_id).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["buildID"], None)
        self.assertEqual(r[0]["version"], None)

    def testInvalidMapping(self):
        data_dict = dict(backgroundRate=31, mapping="random", priority=33, product="a", update_type="minor")
        ret = self._post("/rules", data=data_dict)
        self.assertEqual(ret.status_code, 400, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        self.assertIn("mapping", ret.get_data(as_text=True), "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))

    def testPutDataVersionLessThanOne(self):
        # Throw 400 error when data_version is less than 1.
        ret = self._put(
            "/rules/1", data=dict(backgroundRate=71, mapping="d", priority=73, data_version=0, product="Firefox", channel="nightly", update_type="minor")
        )
        self.assertEqual(ret.status_code, 400, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))

    def testDuplicateAlias(self):
        ret = self._post(
            "/rules", data=dict(backgroundRate=31, mapping="c", priority=33, product="Firefox", update_type="minor", channel="nightly", alias="test")
        )
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))

        ret = self._post(
            "/rules", data=dict(backgroundRate=31, mapping="c", priority=33, product="Firefox", update_type="minor", channel="nightly", alias="test")
        )
        self.assertEqual(ret.status_code, 400, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))

    def testNewRulePostWithDistributionList(self):
        data = dict(
            backgroundRate=31,
            mapping="c",
            priority=33,
            product="Firefox",
            update_type="minor",
            channel="nightly",
            distribution="  mozilla1, mozilla2, mozilla3,mozilla4 ",
        )
        ret = self._post("/rules", data=data)
        rule_id = int(ret.get_data())
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, rule_id))
        r = dbo.rules.t.select().where(dbo.rules.rule_id == rule_id).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["distribution"], "mozilla1,mozilla2,mozilla3,mozilla4")


class TestSingleRuleView_JSON(ViewTest):
    def testGetRule(self):
        ret = self._get("/rules/1")
        expected = dict(
            backgroundRate=100,
            mapping="c",
            fallbackMapping=None,
            priority=100,
            product="a",
            version="3.5",
            buildID=None,
            channel="a",
            locale=None,
            distribution=None,
            buildTarget="d",
            osVersion=None,
            instructionSet=None,
            distVersion=None,
            comment=None,
            update_type="minor",
            headerArchitecture=None,
            data_version=2,
            rule_id=1,
            alias=None,
            memory=None,
            mig64=None,
            jaws=None,
        )
        self.assertEqual(ret.get_json(), expected)

    def testGetRuleByAlias(self):
        ret = self._get("/rules/frodo")
        expected = dict(
            backgroundRate=100,
            mapping="b",
            fallbackMapping=None,
            priority=100,
            product="a",
            version="3.3",
            buildID=None,
            channel="a",
            locale=None,
            distribution=None,
            buildTarget="d",
            osVersion=None,
            instructionSet=None,
            distVersion=None,
            comment=None,
            update_type="minor",
            headerArchitecture=None,
            data_version=1,
            rule_id=2,
            alias="frodo",
            memory=None,
            mig64=None,
            jaws=None,
        )
        self.assertEqual(ret.get_json(), expected)

    def testGetRule404(self):
        ret = self.client.get("/rules/123")
        self.assertEqual(ret.status_code, 404)

    def testPost(self):
        # Make some changes to a rule
        ret = self._post(
            "/rules/1",
            data=dict(
                backgroundRate=71,
                mapping="d",
                update_type="minor",
                fallbackMapping="b",
                priority=73,
                data_version=2,
                product="Firefox",
                channel="nightly",
                instructionSet="SSE",
            ),
        )
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        load = ret.get_json()
        self.assertEqual(load["new_data_version"], 3)

        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 1).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["mapping"], "d")
        self.assertEqual(r[0]["fallbackMapping"], "b")
        self.assertEqual(r[0]["backgroundRate"], 71)
        self.assertEqual(r[0]["instructionSet"], "SSE")
        self.assertEqual(r[0]["priority"], 73)
        self.assertEqual(r[0]["data_version"], 3)
        # And that we didn't modify other fields
        self.assertEqual(r[0]["update_type"], "minor")
        self.assertEqual(r[0]["version"], "3.5")
        self.assertEqual(r[0]["buildTarget"], "d")

    def testPostChangeToMemory(self):
        # Make some changes to a rule
        ret = self._post("/rules/1", data=dict(memory="42", data_version=2))
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        load = ret.get_json()
        self.assertEqual(load["new_data_version"], 3)

        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 1).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["memory"], "42")
        self.assertEqual(r[0]["data_version"], 3)
        # And that we didn't modify other fields
        self.assertEqual(r[0]["update_type"], "minor")
        self.assertEqual(r[0]["version"], "3.5")
        self.assertEqual(r[0]["buildTarget"], "d")

    def testPostChangeToMig64(self):
        # Make some changes to a rule
        ret = self._post("/rules/1", data=dict(mig64=True, data_version=2))
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        load = ret.get_json()
        self.assertEqual(load["new_data_version"], 3)

        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 1).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["mig64"], True)
        self.assertEqual(r[0]["data_version"], 3)
        # And that we didn't modify other fields
        self.assertEqual(r[0]["update_type"], "minor")
        self.assertEqual(r[0]["version"], "3.5")
        self.assertEqual(r[0]["buildTarget"], "d")

    def testPostChangeToJaws(self):
        # Make some changes to a rule
        ret = self._post("/rules/1", data=dict(jaws=True, data_version=2))
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        load = ret.get_json()
        self.assertEqual(load["new_data_version"], 3)

        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 1).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["jaws"], True)
        self.assertEqual(r[0]["data_version"], 3)
        # And that we didn't modify other fields
        self.assertEqual(r[0]["update_type"], "minor")
        self.assertEqual(r[0]["version"], "3.5")
        self.assertEqual(r[0]["buildTarget"], "d")

    def testPostUnsetMig64(self):
        # Make some changes to a rule
        ret = self._post("/rules/8", data=dict(mig64=None, data_version=1))
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        load = ret.get_json()
        self.assertEqual(load["new_data_version"], 2)

        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 8).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["mig64"], None)
        self.assertEqual(r[0]["data_version"], 2)
        # And that we didn't modify other fields
        self.assertEqual(r[0]["update_type"], "minor")
        self.assertEqual(r[0]["priority"], 25)

    def testPostUnsetJaws(self):
        # Make some changes to a rule
        ret = self._post("/rules/9", data=dict(jaws=None, data_version=1))
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        load = ret.get_json()
        self.assertEqual(load["new_data_version"], 2)

        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 9).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["jaws"], None)
        self.assertEqual(r[0]["data_version"], 2)
        # And that we didn't modify other fields
        self.assertEqual(r[0]["update_type"], "minor")
        self.assertEqual(r[0]["priority"], 25)

    def testPutRuleOutdatedData(self):
        # Make changes to a rule
        ret = self._put("/rules/1", data=dict(backgroundRate=71, mapping="d", priority=73, data_version=2, product="Firefox", channel="nightly"))
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        load = ret.get_json()
        self.assertEqual(load["new_data_version"], 3)
        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 1).execute().fetchall()
        self.assertEqual(r[0]["data_version"], 3)

        # OutdatedDataVersion Request
        ret2 = self._put("/rules/1", data=dict(backgroundRate=71, mapping="d", priority=73, data_version=1, product="Firefox", channel="nightly"))
        self.assertEqual(ret2.status_code, 400, "Status Code: %d, Data: %s" % (ret2.status_code, ret2.get_data()))

    def testPostRuleOutdatedData(self):
        # Make changes to a rule
        ret = self._post("/rules/1", data=dict(backgroundRate=71, mapping="d", priority=73, data_version=2, product="Firefox", channel="nightly"))
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        load = ret.get_json()
        self.assertEqual(load["new_data_version"], 3)
        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 1).execute().fetchall()
        self.assertEqual(r[0]["data_version"], 3)

        # OutdatedDataVersion Request
        ret2 = self._put("/rules/1", data=dict(backgroundRate=71, mapping="d", priority=73, data_version=2, product="Firefox", channel="nightly"))
        self.assertEqual(ret2.status_code, 400, "Status Code: %d, Data: %s" % (ret2.status_code, ret2.get_data()))

    def testPostByAlias(self):
        # Make some changes to a rule
        ret = self._post("/rules/frodo", data=dict(backgroundRate=71, mapping="d", priority=73, data_version=1, product="Firefox", channel="nightly"))
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        load = ret.get_json()
        self.assertEqual(load["new_data_version"], 2)

        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 2).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["mapping"], "d")
        self.assertEqual(r[0]["backgroundRate"], 71)
        self.assertEqual(r[0]["priority"], 73)
        self.assertEqual(r[0]["data_version"], 2)
        # And that we didn't modify other fields
        self.assertEqual(r[0]["update_type"], "minor")
        self.assertEqual(r[0]["version"], "3.3")
        self.assertEqual(r[0]["buildTarget"], "d")

    def testPostJSON(self):
        data = dict(backgroundRate=71, mapping="d", priority=73, data_version=2, product="Firefox", channel="nightly")
        ret = self._post("/rules/1", data=data)
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        load = ret.get_json()
        self.assertEqual(load["new_data_version"], 3)

        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 1).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["mapping"], "d")
        self.assertEqual(r[0]["backgroundRate"], 71)
        self.assertEqual(r[0]["priority"], 73)
        self.assertEqual(r[0]["data_version"], 3)
        # And that we didn't modify other fields
        self.assertEqual(r[0]["update_type"], "minor")
        self.assertEqual(r[0]["version"], "3.5")
        self.assertEqual(r[0]["buildTarget"], "d")

    def testPostAddAlias(self):
        # Make some changes to a rule
        ret = self._post("/rules/1", data=dict(alias="sam", data_version=2))
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        load = ret.get_json()
        self.assertEqual(load["new_data_version"], 3)

        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 1).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["alias"], "sam")
        self.assertEqual(r[0]["data_version"], 3)
        # And that we didn"t modify other fields
        self.assertEqual(r[0]["update_type"], "minor")
        self.assertEqual(r[0]["version"], "3.5")
        self.assertEqual(r[0]["buildTarget"], "d")

    def testPostAddBadAlias(self):
        ret = self._post("/rules/1", data=dict(alias="abc#$%", data_version=1))
        self.assertEqual(ret.status_code, 400, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))

    def testPostWithoutProduct(self):
        ret = self._post("/rules/2", username="bob", data=dict(backgroundRate=71, mapping="d", priority=73, data_version=1, channel="nightly"))
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        load = ret.get_json()
        self.assertEqual(load["new_data_version"], 2)
        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 2).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["mapping"], "d")
        self.assertEqual(r[0]["backgroundRate"], 71)
        self.assertEqual(r[0]["priority"], 73)
        self.assertEqual(r[0]["data_version"], 2)
        self.assertEqual(r[0]["channel"], "nightly")
        # And that we didn't modify other fields
        self.assertEqual(r[0]["update_type"], "minor")
        self.assertEqual(r[0]["buildTarget"], "d")
        self.assertEqual(r[0]["product"], "a")

    def testPostSetBackgroundRateTo0(self):
        ret = self._post("/rules/3", data=dict(backgroundRate=0, data_version=2))
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        load = ret.get_json()
        self.assertEqual(load["new_data_version"], 3)
        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 3).execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["backgroundRate"], 0)
        self.assertEqual(r[0]["data_version"], 3)
        # And that we didn't modify other fields
        self.assertEqual(r[0]["update_type"], "minor")
        self.assertEqual(r[0]["mapping"], "a")
        self.assertEqual(r[0]["priority"], 100)
        self.assertEqual(r[0]["buildTarget"], "a")
        self.assertEqual(r[0]["product"], "a")

    def testPostRemoveRestriction(self):
        ret = self._post("/rules/5", data=dict(buildTarget="", data_version=1))
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        load = ret.get_json()
        self.assertEqual(load["new_data_version"], 2)
        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 5).execute().fetchall()
        self.assertEqual(len(r), 1)
        r = r[0]
        self.assertEqual(r["buildTarget"], None)
        # ...and that other fields weren't modified
        self.assertEqual(r["priority"], 80)
        self.assertEqual(r["version"], "3.3")
        self.assertEqual(r["backgroundRate"], 0)
        self.assertEqual(r["mapping"], "c")
        self.assertEqual(r["update_type"], "minor")
        self.assertEqual(r["product"], "a")

    def testPost404(self):
        ret = self._post("/rules/555", data=dict(mapping="d", data_version=1))
        self.assertEqual(ret.status_code, 404)

    def testPostWithBadData(self):
        ret = self._post("/rules/1", data=dict(mapping="uhet"))
        self.assertEqual(ret.status_code, 400)

    def testPostWithBadAlias(self):
        ret = self._post("/rules/1", data=dict(alias="3", data_version=1))
        self.assertEqual(ret.status_code, 400)

    def testPostWithRequiredSignoff(self):
        ret = self._post("/rules/4", data=dict(product="c", channel="c", data_version=1))
        self.assertEqual(ret.status_code, 400)
        self.assertIn("No Signoffs given", ret.get_data(as_text=True))

    # Regression test for https://bugzilla.mozilla.org/show_bug.cgi?id=1375670
    def testPostWithRequiredSignoffForProductOnly(self):
        ret = self._post("/rules/7", data=dict(osVersion="Darwin", data_version=1))
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        load = ret.get_json()
        self.assertEqual(load["new_data_version"], 2)
        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 7).execute().fetchall()
        self.assertEqual(len(r), 1)
        r = r[0]
        self.assertEqual(r["osVersion"], "Darwin")
        # ...and that other fields weren't modified
        self.assertEqual(r["priority"], 30)
        self.assertEqual(r["backgroundRate"], 85)
        self.assertEqual(r["mapping"], "a")
        self.assertEqual(r["update_type"], "minor")
        self.assertEqual(r["product"], "fake")
        self.assertEqual(r["channel"], "c")

    def testBadAuthPost(self):
        ret = self._post("/rules/1", data=dict(backgroundRate=100, mapping="c", priority=100, data_version=1), username="bad!")
        self.assertEqual(ret.status_code, 403, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))

    def testNoPermissionToAlterExistingProduct(self):
        ret = self._post("/rules/4", data=dict(backgroundRate=71, data_version=1), username="bob")
        self.assertEqual(ret.status_code, 403)

    def testNoPermissionToAlterNewProduct(self):
        ret = self._post(
            "/rules/4", data=dict(product="protected", mapping="a", backgroundRate=71, priority=50, update_type="minor", data_version=1), username="bob"
        )
        self.assertEqual(ret.status_code, 403)

    def testGetSingleRule(self):
        ret = self._get("/rules/1")
        self.assertEqual(ret.status_code, 200)
        self.assertTrue("c" in ret.get_data(as_text=True), msg=ret.get_data())
        for h in ("X-Data-Version",):
            self.assertTrue(h in ret.headers, msg=ret.headers)

    def testDeleteRule(self):
        ret = self._delete("/rules/1", qs=dict(data_version=2))
        self.assertEqual(ret.status_code, 200, msg=ret.get_data())

    def testDeleteRuleOutdatedData(self):
        ret = self._get("/rules/1")
        self.assertEqual(ret.status_code, 200, msg=ret.get_data())
        ret = self._delete("/rules/1", qs=dict(data_version=7))
        self.assertEqual(ret.status_code, 400, msg=ret.get_data())

    def testDeleteRuleByAlias(self):
        ret = self._delete("/rules/frodo", qs={"data_version": 1})
        self.assertEqual(ret.status_code, 200, msg=ret.get_data())

    def testDeleteRule404(self):
        ret = self._delete("/rules/112", qs={"data_version": 25})
        self.assertEqual(ret.status_code, 404)

    def testDeleteWithProductAdminPermission(self):
        ret = self._delete("/rules/3", username="billy", qs=dict(data_version=2))
        self.assertEqual(ret.status_code, 200)

    def testDeleteWithoutProductAdminPermission(self):
        ret = self._delete("/rules/4", username="billy", qs=dict(data_version=1))
        self.assertEqual(ret.status_code, 403)

    def testDeleteWithoutPermission(self):
        ret = self._delete("/rules/2", username="tony", qs=dict(data_version=1))
        self.assertEqual(ret.status_code, 403)


class TestRuleHistoryView(ViewTest):
    def testGetRefusesAlias(self):
        ret = self._get("/rules/frodo/revisions")
        self.assertEqual(ret.status_code, 404)

    def testGetRevisions(self):
        # Make some changes to a rule
        ret = self._post(
            "/rules/1", data=dict(backgroundRate=71, mapping="d", priority=73, data_version=2, product="Firefox", update_type="minor", channel="nightly")
        )
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        # and again
        ret = self._post(
            "/rules/1", data=dict(backgroundRate=72, mapping="d", priority=73, data_version=3, product="Firefux", update_type="minor", channel="nightly")
        )
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))

        url = "/rules/1/revisions"
        ret = self._get(url)
        got = ret.get_json()
        self.assertEqual(ret.status_code, 200, msg=ret.get_data())
        self.assertEqual(got["count"], 4)
        self.assertTrue("rule_id" in got["rules"][0])
        self.assertTrue("backgroundRate" in got["rules"][0])

    def testGetHistory(self):
        # Make some changes to a rule
        ret = self._post(
            "/rules/1", data=dict(backgroundRate=71, mapping="d", priority=73, data_version=2, product="Firefox", update_type="minor", channel="nightly")
        )
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        # and again
        ret = self._post(
            "/rules/1", data=dict(backgroundRate=72, mapping="d", priority=73, data_version=3, product="Firefux", update_type="minor", channel="nightly")
        )
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))

        url = "/rules/history"
        ret = self._get(url)
        got = ret.get_json()
        self.assertEqual(ret.status_code, 200, msg=ret.get_data())
        self.assertEqual(got["Rules"]["count"], 13)
        self.assertTrue("rule_id" in got["Rules"]["revisions"][0])
        self.assertTrue("backgroundRate" in got["Rules"]["revisions"][0])
        self.assertTrue("timestamp" in got["Rules"]["revisions"][0])

    def testVersionMaxFieldLength(self):
        # Max field length of rules.version is 75
        version = "3.3,3.4,3.5,3.6,3.8,3.9,3.10,3.11"
        ret = self._post(
            "/rules/1",
            data=dict(
                backgroundRate=71,
                mapping="d",
                version="{}".format(version),
                priority=73,
                data_version=2,
                product="Firefox",
                update_type="minor",
                channel="nightly",
                buildID="1234",
                osVersion="10.5",
                headerArchitecture="INTEL",
                distVersion="19",
                buildTarget="MAC",
            ),
        )
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        ret = dbo.rules.history.select(where={"rule_id": 1, "data_version": 3}, columns=["version"])
        self.assertEqual(ret[0].get("version"), version)
        self.assertEqual(len(ret[0].get("version")), len(version))

    def testPostRevisionRollback(self):
        # Make some changes to a rule
        ret = self._post(
            "/rules/1",
            data=dict(
                backgroundRate=71,
                mapping="d",
                priority=73,
                data_version=2,
                product="Firefox",
                update_type="minor",
                channel="nightly",
                buildID="1234",
                osVersion="10.5",
                headerArchitecture="INTEL",
                distVersion="19",
                buildTarget="MAC",
            ),
        )
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        # and again
        ret = self._post(
            "/rules/1", data=dict(backgroundRate=72, mapping="d", priority=73, data_version=3, product="Firefux", update_type="minor", channel="nightly")
        )
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))

        table = dbo.rules
        (row,) = table.select(where=[table.rule_id == 1])
        self.assertEqual(row["backgroundRate"], 72)
        self.assertEqual(row["data_version"], 4)

        count = table.history.count()
        self.assertEqual(count, 22)

        # Oh no! We prefer the product=Firefox, backgroundRate=71 one better
        (row,) = table.history.select(where=[table.history.product == "Firefox", table.history.backgroundRate == 71], limit=1)
        change_id = row["change_id"]
        assert row["rule_id"] == 1  # one of the fixtures

        url = "/rules/1/revisions"
        ret = self._post(url, {"change_id": change_id})
        self.assertEqual(ret.status_code, 200, ret.get_data())

        count = table.history.count()
        self.assertEqual(count, 23)

        (row,) = table.select(where=[table.rule_id == 1])
        self.assertEqual(row["backgroundRate"], 71)
        self.assertEqual(row["product"], "Firefox")
        self.assertEqual(row["data_version"], 5)
        self.assertEqual(row["buildID"], "1234")
        self.assertEqual(row["osVersion"], "10.5")
        self.assertEqual(row["headerArchitecture"], "INTEL")
        self.assertEqual(row["distVersion"], "19")
        self.assertEqual(row["buildTarget"], "MAC")

    def testRollbackWithoutPermission(self):
        ret = self._post(
            "/rules/1",
            data=dict(
                backgroundRate=71,
                mapping="d",
                priority=73,
                data_version=1,
                product="foo",
                update_type="minor",
                channel="nightly",
                buildID="1234",
                osVersion="10.5",
                headerArchitecture="INTEL",
                distVersion="19",
                buildTarget="MAC",
            ),
        )
        ret = self._post(
            "/rules/1", data=dict(backgroundRate=72, mapping="d", priority=73, product="foo", data_version=2, update_type="minor", channel="nightly")
        )
        (row,) = dbo.rules.history.select(where=[dbo.rules.history.backgroundRate == 72], limit=1)
        change_id = row["change_id"]

        url = "/rules/1/revisions"
        ret = self._post(url, {"change_id": change_id}, username="bob")
        self.assertEqual(ret.status_code, 403)

    def testPostRevisionRollbackBadRequests(self):
        ret = self._post(
            "/rules/1",
            data=dict(
                backgroundRate=71,
                mapping="d",
                priority=73,
                data_version=2,
                product="Firefox",
                update_type="minor",
                channel="nightly",
                buildID="1234",
                osVersion="10.5",
                headerArchitecture="INTEL",
                distVersion="19",
                buildTarget="MAC",
            ),
        )
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        # when posting you need both the rule_id and the change_id
        wrong_url = "/rules/999/revisions"
        # not found rule_id
        ret = self._post(wrong_url, {"change_id": 10})
        self.assertEqual(ret.status_code, 404, ret.get_data())

        url = "/rules/1/revisions"
        ret = self._post(url, {"change_id": 999})
        # not found change_id
        self.assertEqual(ret.status_code, 400)

        url = "/rules/1/revisions"
        ret = self._post(url)  # no change_id posted
        self.assertEqual(ret.status_code, 400)


class TestSingleColumn_JSON(ViewTest):
    def testGetRules(self):
        expected_product = ["fake", "fake2", "fake3", "a"]
        expected = dict(count=4, product=expected_product)
        ret = self._get("/rules/columns/product")
        returned_data = ret.get_json()
        self.assertEqual(returned_data["count"], expected["count"])
        self.assertCountEqual(returned_data["product"], expected["product"])

    def testGetRuleColumn404(self):
        ret = self.client.get("/rules/columns/blah")
        self.assertEqual(ret.status_code, 404)


class TestRuleScheduledChanges(ViewTest):
    maxDiff = 50000

    def setUp(self):
        super(TestRuleScheduledChanges, self).setUp()
        dbo.rules.scheduled_changes.t.insert().execute(
            sc_id=1,
            scheduled_by="bill",
            data_version=1,
            base_rule_id=1,
            base_priority=100,
            base_version="3.5",
            base_buildTarget="d",
            base_backgroundRate=100,
            base_mapping="b",
            base_update_type="minor",
            base_data_version=2,
            change_type="update",
            base_product="a",
            base_channel="a",
        )
        dbo.rules.scheduled_changes.conditions.t.insert().execute(sc_id=1, when=1000000, data_version=1)

        dbo.rules.scheduled_changes.t.insert().execute(
            sc_id=2,
            scheduled_by="bill",
            data_version=1,
            base_priority=50,
            base_backgroundRate=100,
            base_product="baz",
            base_mapping="ab",
            base_update_type="minor",
            change_type="insert",
        )
        dbo.rules.scheduled_changes.history.t.insert().execute(change_id=4, changed_by="bill", timestamp=15, sc_id=2)
        dbo.rules.scheduled_changes.history.t.insert().execute(
            change_id=5,
            changed_by="bill",
            timestamp=16,
            sc_id=2,
            scheduled_by="bill",
            data_version=1,
            base_priority=50,
            base_backgroundRate=100,
            base_product="baz",
            base_mapping="ab",
            base_update_type="minor",
            change_type="insert",
        )
        dbo.rules.scheduled_changes.conditions.t.insert().execute(sc_id=2, when=1500000, data_version=1)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=4, changed_by="bill", timestamp=15, sc_id=2)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=5, changed_by="bill", timestamp=16, sc_id=2, when=1500000, data_version=1)

        dbo.rules.scheduled_changes.t.insert().execute(
            sc_id=3,
            scheduled_by="bill",
            data_version=2,
            base_priority=150,
            base_backgroundRate=100,
            base_channel="a",
            base_mapping="ghi",
            base_update_type="minor",
            change_type="insert",
        )
        dbo.rules.scheduled_changes.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=5, sc_id=3)
        dbo.rules.scheduled_changes.history.t.insert().execute(
            change_id=2,
            changed_by="bill",
            timestamp=6,
            sc_id=3,
            scheduled_by="bill",
            data_version=1,
            base_priority=150,
            base_backgroundRate=100,
            base_channel="a",
            base_mapping="def",
            base_update_type="minor",
            change_type="insert",
        )
        dbo.rules.scheduled_changes.history.t.insert().execute(
            change_id=3,
            changed_by="bill",
            timestamp=10,
            sc_id=3,
            scheduled_by="bill",
            data_version=2,
            base_priority=150,
            base_backgroundRate=100,
            base_channel="a",
            base_mapping="ghi",
            base_update_type="minor",
            change_type="insert",
        )
        dbo.rules.scheduled_changes.conditions.t.insert().execute(sc_id=3, when=2900000, data_version=2)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=5, sc_id=3)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=2, changed_by="bill", timestamp=6, sc_id=3, when=2000000, data_version=1)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=3, changed_by="bill", timestamp=10, sc_id=3, when=2900000, data_version=2)
        dbo.rules.scheduled_changes.signoffs.t.insert().execute(sc_id=3, username="bill", role="releng")
        dbo.rules.scheduled_changes.signoffs.t.insert().execute(sc_id=3, username="mary", role="relman")

        dbo.rules.scheduled_changes.t.insert().execute(
            sc_id=4,
            scheduled_by="bill",
            data_version=2,
            complete=True,
            base_rule_id=5,
            base_priority=80,
            base_version="3.3",
            base_buildTarget="d",
            base_backgroundRate=0,
            base_mapping="c",
            base_update_type="minor",
            base_data_version=1,
            change_type="update",
        )
        dbo.rules.scheduled_changes.history.t.insert().execute(change_id=6, changed_by="bill", timestamp=5, sc_id=4)
        dbo.rules.scheduled_changes.history.t.insert().execute(change_id=7, changed_by="bill", timestamp=5, sc_id=4)
        dbo.rules.scheduled_changes.history.t.insert().execute(
            change_id=8,
            changed_by="bill",
            timestamp=6,
            sc_id=4,
            scheduled_by="bill",
            data_version=1,
            base_priority=80,
            base_version="3.3",
            base_buildTarget="d",
            base_backgroundRate=0,
            base_mapping="c",
            base_update_type="minor",
            base_data_version=1,
            change_type="update",
        )
        dbo.rules.scheduled_changes.history.t.insert().execute(
            change_id=9,
            changed_by="bill",
            timestamp=7,
            sc_id=4,
            scheduled_by="bill",
            data_version=2,
            complete=True,
            base_rule_id=5,
            base_priority=80,
            base_version="3.3",
            base_buildTarget="d",
            base_backgroundRate=0,
            base_mapping="c",
            base_update_type="minor",
            base_data_version=1,
            change_type="update",
        )
        dbo.rules.scheduled_changes.conditions.t.insert().execute(sc_id=4, when=500000, data_version=2)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=6, changed_by="bill", timestamp=5, sc_id=4)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=7, changed_by="bill", timestamp=5, sc_id=4)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=8, changed_by="bill", timestamp=6, sc_id=4, when=500000, data_version=1)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=9, changed_by="bill", timestamp=7, sc_id=4, when=500000, data_version=2)

        dbo.rules.scheduled_changes.t.insert().execute(
            sc_id=5, scheduled_by="bill", data_version=1, complete=False, change_type="delete", base_rule_id=4, base_data_version=1
        )
        dbo.rules.scheduled_changes.history.t.insert().execute(change_id=10, changed_by="bill", timestamp=50, sc_id=5)
        dbo.rules.scheduled_changes.history.t.insert().execute(
            change_id=11, changed_by="bill", timestamp=51, sc_id=5, scheduled_by="bill", data_version=1, complete=False, base_rule_id=4, base_data_version=1
        )
        dbo.rules.scheduled_changes.conditions.t.insert().execute(sc_id=5, when=600000, data_version=1)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=10, changed_by="bill", timestamp=50, sc_id=5)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=11, changed_by="bill", timestamp=50, sc_id=5, when=600000, data_version=1)

        dbo.rules.scheduled_changes.t.insert().execute(
            sc_id=6,
            scheduled_by="bill",
            data_version=1,
            base_priority=100,
            base_backgroundRate=100,
            base_product="fake",
            base_channel="k",
            base_mapping="ab",
            base_update_type="minor",
            change_type="insert",
        )
        dbo.rules.scheduled_changes.history.t.insert().execute(change_id=12, changed_by="bill", timestamp=75, sc_id=6)
        dbo.rules.scheduled_changes.history.t.insert().execute(
            change_id=13,
            changed_by="bill",
            timestamp=76,
            sc_id=6,
            scheduled_by="bill",
            data_version=1,
            base_priority=100,
            base_backgroundRate=100,
            base_product="fake",
            base_channel="k",
            base_mapping="ab",
            base_update_type="minor",
            change_type="insert",
        )
        dbo.rules.scheduled_changes.conditions.t.insert().execute(sc_id=6, when=5500000, data_version=1)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=12, changed_by="bill", timestamp=75, sc_id=6)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=13, changed_by="bill", timestamp=76, sc_id=6, when=5500000, data_version=1)
        dbo.rules.scheduled_changes.signoffs.t.insert().execute(sc_id=6, username="bill", role="releng")
        dbo.rules.scheduled_changes.signoffs.t.insert().execute(sc_id=6, username="mary", role="relman")

        dbo.rules.scheduled_changes.t.insert().execute(
            sc_id=7,
            scheduled_by="bill",
            data_version=1,
            base_priority=40,
            base_backgroundRate=50,
            base_mapping="a",
            base_update_type="minor",
            base_channel="k",
            base_product="fake",
            base_rule_id=6,
            change_type="update",
        )
        dbo.rules.scheduled_changes.history.t.insert().execute(change_id=14, changed_by="bill", timestamp=123, sc_id=7)
        dbo.rules.scheduled_changes.history.t.insert().execute(
            change_id=15,
            changed_by="bill",
            timestamp=124,
            sc_id=7,
            scheduled_by="bill",
            data_version=1,
            base_priority=40,
            base_backgroundRate=50,
            base_mapping="a",
            base_update_type="minor",
            base_channel="k",
            base_product="fake",
            base_rule_id=6,
            change_type="update",
        )
        dbo.rules.scheduled_changes.conditions.t.insert().execute(sc_id=7, when=7500000, data_version=1)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=14, changed_by="bill", timestamp=123, sc_id=7)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=15, changed_by="bill", timestamp=124, sc_id=7, when=7500000, data_version=1)

    def testGetScheduledChanges(self):
        ret = self._get("/scheduled_changes/rules")
        expected = {
            "count": 6,
            "scheduled_changes": [
                {
                    "sc_id": 1,
                    "when": 1000000,
                    "scheduled_by": "bill",
                    "complete": False,
                    "sc_data_version": 1,
                    "rule_id": 1,
                    "priority": 100,
                    "version": "3.5",
                    "buildTarget": "d",
                    "backgroundRate": 100,
                    "mapping": "b",
                    "update_type": "minor",
                    "data_version": 2,
                    "alias": None,
                    "product": "a",
                    "channel": "a",
                    "buildID": None,
                    "locale": None,
                    "memory": None,
                    "mig64": None,
                    "osVersion": None,
                    "distribution": None,
                    "fallbackMapping": None,
                    "distVersion": None,
                    "headerArchitecture": None,
                    "comment": None,
                    "instructionSet": None,
                    "telemetry_product": None,
                    "telemetry_channel": None,
                    "telemetry_uptake": None,
                    "jaws": None,
                    "change_type": "update",
                    "signoffs": {},
                    "required_signoffs": {},
                },
                {
                    "sc_id": 2,
                    "when": 1500000,
                    "scheduled_by": "bill",
                    "complete": False,
                    "sc_data_version": 1,
                    "rule_id": None,
                    "priority": 50,
                    "backgroundRate": 100,
                    "product": "baz",
                    "mapping": "ab",
                    "update_type": "minor",
                    "version": None,
                    "buildTarget": None,
                    "alias": None,
                    "channel": None,
                    "buildID": None,
                    "locale": None,
                    "osVersion": None,
                    "memory": None,
                    "mig64": None,
                    "distribution": None,
                    "fallbackMapping": None,
                    "distVersion": None,
                    "headerArchitecture": None,
                    "comment": None,
                    "jaws": None,
                    "data_version": None,
                    "instructionSet": None,
                    "telemetry_product": None,
                    "telemetry_channel": None,
                    "telemetry_uptake": None,
                    "change_type": "insert",
                    "signoffs": {},
                    "required_signoffs": {},
                },
                {
                    "sc_id": 3,
                    "when": 2900000,
                    "scheduled_by": "bill",
                    "complete": False,
                    "sc_data_version": 2,
                    "rule_id": None,
                    "priority": 150,
                    "backgroundRate": 100,
                    "channel": "a",
                    "mapping": "ghi",
                    "update_type": "minor",
                    "version": None,
                    "memory": None,
                    "mig64": None,
                    "buildTarget": None,
                    "alias": None,
                    "product": None,
                    "buildID": None,
                    "locale": None,
                    "osVersion": None,
                    "jaws": None,
                    "distribution": None,
                    "fallbackMapping": None,
                    "distVersion": None,
                    "headerArchitecture": None,
                    "comment": None,
                    "data_version": None,
                    "instructionSet": None,
                    "telemetry_product": None,
                    "telemetry_channel": None,
                    "telemetry_uptake": None,
                    "change_type": "insert",
                    "signoffs": {"bill": "releng", "mary": "relman"},
                    "required_signoffs": {"releng": 1},
                },
                {
                    "sc_id": 5,
                    "when": 600000,
                    "scheduled_by": "bill",
                    "complete": False,
                    "sc_data_version": 1,
                    "rule_id": 4,
                    "priority": None,
                    "backgroundRate": None,
                    "channel": None,
                    "mapping": None,
                    "update_type": None,
                    "version": None,
                    "jaws": None,
                    "buildTarget": None,
                    "alias": None,
                    "product": None,
                    "buildID": None,
                    "locale": None,
                    "osVersion": None,
                    "memory": None,
                    "mig64": None,
                    "distribution": None,
                    "fallbackMapping": None,
                    "distVersion": None,
                    "headerArchitecture": None,
                    "comment": None,
                    "data_version": 1,
                    "instructionSet": None,
                    "telemetry_product": None,
                    "telemetry_channel": None,
                    "telemetry_uptake": None,
                    "change_type": "delete",
                    "signoffs": {},
                    "required_signoffs": {"releng": 1},
                },
                {
                    "sc_id": 6,
                    "when": 5500000,
                    "scheduled_by": "bill",
                    "complete": False,
                    "sc_data_version": 1,
                    "rule_id": None,
                    "priority": 100,
                    "backgroundRate": 100,
                    "product": "fake",
                    "mapping": "ab",
                    "update_type": "minor",
                    "version": None,
                    "jaws": None,
                    "buildTarget": None,
                    "alias": None,
                    "channel": "k",
                    "buildID": None,
                    "locale": None,
                    "osVersion": None,
                    "memory": None,
                    "mig64": None,
                    "distribution": None,
                    "fallbackMapping": None,
                    "distVersion": None,
                    "headerArchitecture": None,
                    "comment": None,
                    "data_version": None,
                    "instructionSet": None,
                    "telemetry_product": None,
                    "telemetry_channel": None,
                    "telemetry_uptake": None,
                    "change_type": "insert",
                    "signoffs": {"bill": "releng", "mary": "relman"},
                    "required_signoffs": {"relman": 1},
                },
                {
                    "sc_id": 7,
                    "when": 7500000,
                    "scheduled_by": "bill",
                    "complete": False,
                    "sc_data_version": 1,
                    "rule_id": 6,
                    "priority": 40,
                    "backgroundRate": 50,
                    "product": "fake",
                    "mapping": "a",
                    "update_type": "minor",
                    "version": None,
                    "jaws": None,
                    "buildTarget": None,
                    "alias": None,
                    "channel": "k",
                    "buildID": None,
                    "locale": None,
                    "osVersion": None,
                    "memory": None,
                    "mig64": None,
                    "distribution": None,
                    "fallbackMapping": None,
                    "distVersion": None,
                    "headerArchitecture": None,
                    "comment": None,
                    "data_version": None,
                    "instructionSet": None,
                    "telemetry_product": None,
                    "telemetry_channel": None,
                    "telemetry_uptake": None,
                    "change_type": "update",
                    "signoffs": {},
                    "required_signoffs": {"releng": 1, "relman": 1},
                },
            ],
        }
        self.assertEqual(ret.get_json(), expected)

    def testGetScheduledChangesByRuleId(self):
        ret = self._get("/scheduled_changes/rules", qs={"rule_id": 1})
        expected = {
            "count": 1,
            "scheduled_changes": [
                {
                    "sc_id": 1,
                    "when": 1000000,
                    "scheduled_by": "bill",
                    "complete": False,
                    "sc_data_version": 1,
                    "rule_id": 1,
                    "priority": 100,
                    "version": "3.5",
                    "buildTarget": "d",
                    "backgroundRate": 100,
                    "mapping": "b",
                    "update_type": "minor",
                    "data_version": 2,
                    "alias": None,
                    "product": "a",
                    "channel": "a",
                    "buildID": None,
                    "locale": None,
                    "memory": None,
                    "mig64": None,
                    "osVersion": None,
                    "distribution": None,
                    "fallbackMapping": None,
                    "distVersion": None,
                    "headerArchitecture": None,
                    "comment": None,
                    "instructionSet": None,
                    "telemetry_product": None,
                    "telemetry_channel": None,
                    "telemetry_uptake": None,
                    "jaws": None,
                    "change_type": "update",
                    "signoffs": {},
                    "required_signoffs": {},
                }
            ],
        }
        self.assertEqual(ret.get_json(), expected)

    def testGetScheduledChangesWithCompleted(self):
        ret = self._get("/scheduled_changes/rules", qs={"all": 1})
        expected = {
            "count": 7,
            "scheduled_changes": [
                {
                    "sc_id": 1,
                    "when": 1000000,
                    "scheduled_by": "bill",
                    "complete": False,
                    "sc_data_version": 1,
                    "rule_id": 1,
                    "priority": 100,
                    "version": "3.5",
                    "buildTarget": "d",
                    "backgroundRate": 100,
                    "mapping": "b",
                    "update_type": "minor",
                    "data_version": 2,
                    "alias": None,
                    "product": "a",
                    "channel": "a",
                    "buildID": None,
                    "locale": None,
                    "memory": None,
                    "mig64": None,
                    "osVersion": None,
                    "distribution": None,
                    "fallbackMapping": None,
                    "distVersion": None,
                    "headerArchitecture": None,
                    "comment": None,
                    "instructionSet": None,
                    "telemetry_product": None,
                    "telemetry_channel": None,
                    "telemetry_uptake": None,
                    "jaws": None,
                    "change_type": "update",
                    "signoffs": {},
                    "required_signoffs": {},
                },
                {
                    "sc_id": 2,
                    "when": 1500000,
                    "scheduled_by": "bill",
                    "complete": False,
                    "sc_data_version": 1,
                    "rule_id": None,
                    "priority": 50,
                    "backgroundRate": 100,
                    "product": "baz",
                    "mapping": "ab",
                    "update_type": "minor",
                    "version": None,
                    "jaws": None,
                    "buildTarget": None,
                    "alias": None,
                    "channel": None,
                    "buildID": None,
                    "locale": None,
                    "osVersion": None,
                    "memory": None,
                    "mig64": None,
                    "distribution": None,
                    "fallbackMapping": None,
                    "distVersion": None,
                    "headerArchitecture": None,
                    "comment": None,
                    "data_version": None,
                    "instructionSet": None,
                    "telemetry_product": None,
                    "telemetry_channel": None,
                    "telemetry_uptake": None,
                    "change_type": "insert",
                    "signoffs": {},
                    "required_signoffs": {},
                },
                {
                    "sc_id": 3,
                    "when": 2900000,
                    "scheduled_by": "bill",
                    "complete": False,
                    "sc_data_version": 2,
                    "rule_id": None,
                    "priority": 150,
                    "backgroundRate": 100,
                    "channel": "a",
                    "mapping": "ghi",
                    "update_type": "minor",
                    "version": None,
                    "jaws": None,
                    "buildTarget": None,
                    "alias": None,
                    "product": None,
                    "buildID": None,
                    "locale": None,
                    "osVersion": None,
                    "memory": None,
                    "mig64": None,
                    "distribution": None,
                    "fallbackMapping": None,
                    "distVersion": None,
                    "headerArchitecture": None,
                    "comment": None,
                    "data_version": None,
                    "instructionSet": None,
                    "telemetry_product": None,
                    "telemetry_channel": None,
                    "telemetry_uptake": None,
                    "change_type": "insert",
                    "signoffs": {"bill": "releng", "mary": "relman"},
                    "required_signoffs": {"releng": 1},
                },
                {
                    "sc_id": 4,
                    "when": 500000,
                    "scheduled_by": "bill",
                    "complete": True,
                    "sc_data_version": 2,
                    "rule_id": 5,
                    "priority": 80,
                    "version": "3.3",
                    "buildTarget": "d",
                    "backgroundRate": 0,
                    "mapping": "c",
                    "update_type": "minor",
                    "data_version": 1,
                    "alias": None,
                    "product": None,
                    "channel": None,
                    "buildID": None,
                    "locale": None,
                    "memory": None,
                    "mig64": None,
                    "osVersion": None,
                    "distribution": None,
                    "fallbackMapping": None,
                    "distVersion": None,
                    "headerArchitecture": None,
                    "comment": None,
                    "instructionSet": None,
                    "telemetry_product": None,
                    "telemetry_channel": None,
                    "telemetry_uptake": None,
                    "jaws": None,
                    "change_type": "update",
                    "signoffs": {},
                    "required_signoffs": {},
                    # No original row on "complete"
                },
                {
                    "sc_id": 5,
                    "when": 600000,
                    "scheduled_by": "bill",
                    "complete": False,
                    "sc_data_version": 1,
                    "rule_id": 4,
                    "priority": None,
                    "backgroundRate": None,
                    "channel": None,
                    "mapping": None,
                    "update_type": None,
                    "version": None,
                    "jaws": None,
                    "buildTarget": None,
                    "alias": None,
                    "product": None,
                    "buildID": None,
                    "locale": None,
                    "osVersion": None,
                    "memory": None,
                    "mig64": None,
                    "distribution": None,
                    "fallbackMapping": None,
                    "distVersion": None,
                    "headerArchitecture": None,
                    "comment": None,
                    "data_version": 1,
                    "instructionSet": None,
                    "telemetry_product": None,
                    "telemetry_channel": None,
                    "telemetry_uptake": None,
                    "change_type": "delete",
                    "signoffs": {},
                    "required_signoffs": {"releng": 1},
                },
                {
                    "sc_id": 6,
                    "when": 5500000,
                    "scheduled_by": "bill",
                    "complete": False,
                    "sc_data_version": 1,
                    "rule_id": None,
                    "priority": 100,
                    "backgroundRate": 100,
                    "product": "fake",
                    "mapping": "ab",
                    "update_type": "minor",
                    "version": None,
                    "jaws": None,
                    "buildTarget": None,
                    "alias": None,
                    "channel": "k",
                    "buildID": None,
                    "locale": None,
                    "osVersion": None,
                    "memory": None,
                    "mig64": None,
                    "distribution": None,
                    "fallbackMapping": None,
                    "distVersion": None,
                    "headerArchitecture": None,
                    "comment": None,
                    "data_version": None,
                    "instructionSet": None,
                    "telemetry_product": None,
                    "telemetry_channel": None,
                    "telemetry_uptake": None,
                    "change_type": "insert",
                    "signoffs": {"bill": "releng", "mary": "relman"},
                    "required_signoffs": {"relman": 1},
                },
                {
                    "sc_id": 7,
                    "when": 7500000,
                    "scheduled_by": "bill",
                    "complete": False,
                    "sc_data_version": 1,
                    "rule_id": 6,
                    "priority": 40,
                    "backgroundRate": 50,
                    "product": "fake",
                    "mapping": "a",
                    "update_type": "minor",
                    "version": None,
                    "jaws": None,
                    "buildTarget": None,
                    "alias": None,
                    "channel": "k",
                    "buildID": None,
                    "locale": None,
                    "osVersion": None,
                    "memory": None,
                    "mig64": None,
                    "distribution": None,
                    "fallbackMapping": None,
                    "distVersion": None,
                    "headerArchitecture": None,
                    "comment": None,
                    "data_version": None,
                    "instructionSet": None,
                    "telemetry_product": None,
                    "telemetry_channel": None,
                    "telemetry_uptake": None,
                    "change_type": "update",
                    "signoffs": {},
                    "required_signoffs": {"releng": 1, "relman": 1},
                },
            ],
        }
        self.assertEqual(ret.get_json(), expected)

    def testGetScheduledChangeByScId(self):
        ret = self._get("/scheduled_changes/rules/3")
        expected = {
            "scheduled_change": {
                "sc_id": 3,
                "when": 2900000,
                "scheduled_by": "bill",
                "complete": False,
                "sc_data_version": 2,
                "rule_id": None,
                "priority": 150,
                "backgroundRate": 100,
                "channel": "a",
                "mapping": "ghi",
                "update_type": "minor",
                "version": None,
                "jaws": None,
                "buildTarget": None,
                "alias": None,
                "product": None,
                "buildID": None,
                "locale": None,
                "osVersion": None,
                "memory": None,
                "mig64": None,
                "distribution": None,
                "fallbackMapping": None,
                "distVersion": None,
                "headerArchitecture": None,
                "comment": None,
                "data_version": None,
                "instructionSet": None,
                "telemetry_product": None,
                "telemetry_channel": None,
                "telemetry_uptake": None,
                "change_type": "insert",
                "signoffs": {"bill": "releng", "mary": "relman"},
                "required_signoffs": {"releng": 1},
            }
        }
        self.assertEqual(ret.get_json(), expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeExistingRule(self):
        data = {
            "rule_id": 5,
            "telemetry_product": None,
            "telemetry_channel": None,
            "telemetry_uptake": None,
            "priority": 80,
            "buildTarget": "d",
            "version": "3.3",
            "backgroundRate": 100,
            "mapping": "c",
            "update_type": "minor",
            "data_version": 1,
            "change_type": "update",
            "when": 1234567,
        }
        ret = self._post("/scheduled_changes/rules", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"sc_id": 8, "signoffs": {"bill": "releng"}})

        r = dbo.rules.scheduled_changes.t.select().where(dbo.rules.scheduled_changes.sc_id == 8).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "scheduled_by": "bill",
            "base_rule_id": 5,
            "base_priority": 80,
            "base_buildTarget": "d",
            "base_version": "3.3",
            "base_backgroundRate": 100,
            "base_mapping": "c",
            "base_update_type": "minor",
            "base_data_version": 1,
            "data_version": 1,
            "sc_id": 8,
            "complete": False,
            "base_alias": None,
            "base_product": None,
            "base_channel": None,
            "base_buildID": None,
            "base_locale": None,
            "base_osVersion": None,
            "base_distribution": None,
            "base_fallbackMapping": None,
            "base_distVersion": None,
            "base_headerArchitecture": None,
            "base_comment": None,
            "base_memory": None,
            "base_mig64": None,
            "base_instructionSet": None,
            "base_jaws": None,
            "change_type": "update",
        }
        self.assertEqual(db_data, expected)
        cond = dbo.rules.scheduled_changes.conditions.t.select().where(dbo.rules.scheduled_changes.conditions.sc_id == 8).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 8, "data_version": 1, "telemetry_product": None, "telemetry_channel": None, "telemetry_uptake": None, "when": 1234567}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeExistingDeletingRule(self):
        data = {
            "rule_id": 5,
            "telemetry_product": None,
            "telemetry_channel": None,
            "telemetry_uptake": None,
            "data_version": 1,
            "change_type": "delete",
            "when": 1234567,
        }
        ret = self._post("/scheduled_changes/rules", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"sc_id": 8, "signoffs": {"bill": "releng"}})

        r = dbo.rules.scheduled_changes.t.select().where(dbo.rules.scheduled_changes.sc_id == 8).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "scheduled_by": "bill",
            "base_rule_id": 5,
            "base_priority": None,
            "base_buildTarget": None,
            "base_version": None,
            "base_backgroundRate": None,
            "base_mapping": None,
            "base_update_type": None,
            "base_data_version": 1,
            "data_version": 1,
            "sc_id": 8,
            "complete": False,
            "base_alias": None,
            "base_product": None,
            "base_channel": None,
            "base_buildID": None,
            "base_locale": None,
            "base_osVersion": None,
            "base_distribution": None,
            "base_fallbackMapping": None,
            "base_distVersion": None,
            "base_headerArchitecture": None,
            "base_comment": None,
            "base_memory": None,
            "base_mig64": None,
            "base_instructionSet": None,
            "base_jaws": None,
            "change_type": "delete",
        }
        self.assertEqual(db_data, expected)
        cond = dbo.rules.scheduled_changes.conditions.t.select().where(dbo.rules.scheduled_changes.conditions.sc_id == 8).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 8, "data_version": 1, "telemetry_product": None, "telemetry_channel": None, "telemetry_uptake": None, "when": 1234567}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeNewRule(self):
        data = {
            "when": 1234567,
            "priority": 120,
            "backgroundRate": 100,
            "product": "blah",
            "channel": "blah",
            "update_type": "minor",
            "mapping": "a",
            "change_type": "insert",
        }
        ret = self._post("/scheduled_changes/rules", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"sc_id": 8, "signoffs": {}})

        r = dbo.rules.scheduled_changes.t.select().where(dbo.rules.scheduled_changes.sc_id == 8).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "scheduled_by": "bill",
            "base_priority": 120,
            "base_backgroundRate": 100,
            "base_product": "blah",
            "base_channel": "blah",
            "base_update_type": "minor",
            "base_mapping": "a",
            "sc_id": 8,
            "data_version": 1,
            "complete": False,
            "base_data_version": None,
            "base_rule_id": None,
            "base_buildTarget": None,
            "base_version": None,
            "base_alias": None,
            "base_buildID": None,
            "base_locale": None,
            "base_osVersion": None,
            "base_distribution": None,
            "base_fallbackMapping": None,
            "base_distVersion": None,
            "base_headerArchitecture": None,
            "base_comment": None,
            "base_instructionSet": None,
            "change_type": "insert",
            "base_memory": None,
            "base_mig64": None,
            "base_jaws": None,
        }
        self.assertEqual(db_data, expected)
        cond = dbo.rules.scheduled_changes.conditions.t.select().where(dbo.rules.scheduled_changes.conditions.sc_id == 8).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 8, "data_version": 1, "when": 1234567, "telemetry_product": None, "telemetry_channel": None, "telemetry_uptake": None}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeNewRuleWithoutUpdateType(self):
        data = {"when": 1234567, "priority": 120, "backgroundRate": 100, "product": "blah", "channel": "blah", "mapping": "a", "change_type": "insert"}
        ret = self._post("/scheduled_changes/rules", data=data)
        self.assertEqual(ret.status_code, 400, ret.get_data())

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeUpdateRuleRuleWithoutUpdateType(self):
        data = {
            "when": 1234567,
            "priority": 120,
            "backgroundRate": 100,
            "product": "blah",
            "channel": "blah",
            "mapping": "a",
            "change_type": "insert",
            "data_version": 1,
        }
        ret = self._post("/scheduled_changes/rules", data=data)
        self.assertEqual(ret.status_code, 400, ret.get_data())

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeInThePast(self):
        data = {
            "when": 67,
            "priority": 120,
            "backgroundRate": 100,
            "product": "blah",
            "channel": "blah",
            "update_type": "minor",
            "mapping": "a",
            "change_type": "insert",
        }
        ret = self._post("/scheduled_changes/rules", data=data)
        self.assertEqual(ret.status_code, 400, ret.get_data())

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeNoPermissionsToSchedule(self):
        data = {
            "when": 1234567,
            "priority": 120,
            "backgroundRate": 100,
            "product": "blah",
            "channel": "blah",
            "update_type": "minor",
            "mapping": "a",
            "change_type": "insert",
        }
        ret = self._post("/scheduled_changes/rules", data=data, username="bob")
        self.assertEqual(ret.status_code, 403, ret.get_data())

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeNoPermissionsToMakeChange(self):
        data = {
            "when": 1234567,
            "priority": 120,
            "backgroundRate": 100,
            "product": "foo",
            "channel": "blah",
            "update_type": "minor",
            "mapping": "a",
            "change_type": "insert",
        }
        ret = self._post("/scheduled_changes/rules", data=data, username="mary")
        self.assertEqual(ret.status_code, 403, ret.get_data())

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeMultipleConditions(self):
        data = {
            "when": 23893254,
            "telemetry_product": "foo",
            "telemetry_channel": "foo",
            "telemetry_uptake": 5,
            "priority": 120,
            "backgroundRate": 100,
            "update_type": "minor",
            "change_type": "insert",
        }
        ret = self._post("scheduled_changes/rules", data=data)
        self.assertEqual(ret.status_code, 400)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeRuleWithDuplicateAlias(self):
        ret = self._post(
            "/rules", data=dict(backgroundRate=31, mapping="c", priority=33, product="Firefox", update_type="minor", channel="nightly", alias="test")
        )
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))

        data1 = {
            "when": 1234567,
            "priority": 120,
            "backgroundRate": 100,
            "product": "blah",
            "channel": "blah",
            "mapping": "a",
            "change_type": "insert",
            "alias": "test",
        }
        ret1 = self._post("/scheduled_changes/rules", data=data1)
        self.assertEqual(ret1.status_code, 400, ret1.get_data())

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeWithAliasAlreadyPresent(self):
        data = {
            "when": 2000000,
            "data_version": 1,
            "rule_id": 1,
            "priority": 100,
            "version": "3.5",
            "buildTarget": "d",
            "backgroundRate": 100,
            "mapping": "c",
            "update_type": "minor",
            "sc_data_version": 1,
            "scheduled_by": "test",
        }
        ret = self._post("/scheduled_changes/rules/4", data=data)
        self.assertEqual(ret.status_code, 400, ret.get_data())

    def testAddScheduledChangeMissingRequiredTelemetryFields(self):
        data = {"telemetry_product": "foo", "priority": 120, "backgroundRate": 100, "update_type": "minor", "change_type": "insert"}
        ret = self._post("scheduled_changes/rules", data=data)
        self.assertEqual(ret.status_code, 400)

    def testAddScheduledChangeForDeletionMissingRequiredPKColumns(self):
        data = {"telemetry_product": "foo", "telemetry_channel": "bar", "telemetry_uptake": 42, "data_version": 1, "change_type": "delete"}
        ret = self._post("/scheduled_changes/rules", data=data)
        self.assertEqual(ret.status_code, 400)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateCompletedScheduleChange(self):
        data = {
            "when": 2000000,
            "data_version": 1,
            "rule_id": 1,
            "priority": 100,
            "version": "3.5",
            "buildTarget": "d",
            "backgroundRate": 100,
            "mapping": "c",
            "update_type": "minor",
            "sc_data_version": 1,
        }
        ret = self._post("/scheduled_changes/rules/4", data=data)
        self.assertEqual(ret.status_code, 400, ret.get_data())

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateUnknownScheduledChangeID(self):
        data = {
            "when": 2000000,
            "data_version": 1,
            "rule_id": 1,
            "priority": 100,
            "version": "3.5",
            "buildTarget": "d",
            "backgroundRate": 100,
            "mapping": "c",
            "update_type": "minor",
            "sc_data_version": 1,
        }
        ret = self._post("/scheduled_changes/rules/9876", data=data)
        self.assertEqual(ret.status_code, 404, ret.get_data())

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChange(self):
        data = {
            "when": 2000000,
            "data_version": 2,
            "rule_id": 1,
            "priority": 100,
            "version": "3.5",
            "buildTarget": "d",
            "backgroundRate": 100,
            "mapping": "c",
            "update_type": "minor",
            "sc_data_version": 1,
            "memory": "888",
        }
        ret = self._post("/scheduled_changes/rules/1", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"new_data_version": 2, "signoffs": {}})

        r = dbo.rules.scheduled_changes.t.select().where(dbo.rules.scheduled_changes.sc_id == 1).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 1,
            "scheduled_by": "bill",
            "data_version": 2,
            "complete": False,
            "base_rule_id": 1,
            "base_priority": 100,
            "base_version": "3.5",
            "base_buildTarget": "d",
            "base_backgroundRate": 100,
            "base_mapping": "c",
            "base_update_type": "minor",
            "base_data_version": 2,
            "base_alias": None,
            "base_product": "a",
            "base_channel": "a",
            "base_buildID": None,
            "base_locale": None,
            "base_osVersion": None,
            "base_distribution": None,
            "base_fallbackMapping": None,
            "base_distVersion": None,
            "base_headerArchitecture": None,
            "base_comment": None,
            "base_instructionSet": None,
            "base_memory": "888",
            "base_mig64": None,
            "base_jaws": None,
            "change_type": "update",
        }
        self.assertEqual(db_data, expected)
        cond = dbo.rules.scheduled_changes.conditions.t.select().where(dbo.rules.scheduled_changes.conditions.sc_id == 1).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 1, "data_version": 2, "when": 2000000, "telemetry_product": None, "telemetry_channel": None, "telemetry_uptake": None}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeVersionFieldLength(self):
        version = "3.3,3.4,3.5,3.6,3.8,3.9,3.10,3.11"
        data = {
            "when": 2000000,
            "data_version": 2,
            "rule_id": 1,
            "priority": 100,
            "version": "{}".format(version),
            "buildTarget": "d",
            "backgroundRate": 100,
            "mapping": "c",
            "update_type": "minor",
            "sc_data_version": 1,
        }
        ret = self._post("/scheduled_changes/rules/1", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"new_data_version": 2, "signoffs": {}})

        ret = dbo.rules.scheduled_changes.t.select().where(dbo.rules.scheduled_changes.sc_id == 1).execute().fetchall()
        self.assertEqual(len(ret), 1)
        db_data = dict(ret[0])
        expected = {
            "sc_id": 1,
            "scheduled_by": "bill",
            "data_version": 2,
            "complete": False,
            "base_rule_id": 1,
            "base_priority": 100,
            "base_version": "{}".format(version),
            "base_buildTarget": "d",
            "base_backgroundRate": 100,
            "base_mapping": "c",
            "base_update_type": "minor",
            "base_data_version": 2,
            "base_alias": None,
            "base_product": "a",
            "base_channel": "a",
            "base_buildID": None,
            "base_locale": None,
            "base_osVersion": None,
            "base_distribution": None,
            "base_fallbackMapping": None,
            "base_distVersion": None,
            "base_memory": None,
            "base_mig64": None,
            "base_headerArchitecture": None,
            "base_comment": None,
            "base_instructionSet": None,
            "change_type": "update",
            "base_jaws": None,
        }
        self.assertEqual(db_data, expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeHistoryVersionFieldLength(self):
        version = "3.3,3.4,3.5,3.6,3.8,3.9,3.10,3.11"
        data = {
            "when": 2000000,
            "data_version": 2,
            "rule_id": 1,
            "priority": 100,
            "version": "{}".format(version),
            "buildTarget": "d",
            "backgroundRate": 100,
            "mapping": "c",
            "update_type": "minor",
            "sc_data_version": 1,
        }
        ret = self._post("/scheduled_changes/rules/1", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"new_data_version": 2, "signoffs": {}})

        ret = dbo.rules.scheduled_changes.history.t.select().where(dbo.rules.scheduled_changes.history.sc_id == 1).execute().fetchall()
        self.assertEqual(len(ret), 1)
        db_data = dict(ret[0])
        expected = {"base_version": "{}".format(version)}
        self.assertEqual(db_data["base_version"], expected["base_version"])
        self.assertEqual(len(db_data["base_version"]), len(expected["base_version"]))

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeResetSignOffs(self):
        data = {"when": 2900000, "priority": 150, "backgroundRate": 100, "mapping": "c", "channel": "a", "update_type": "minor", "sc_data_version": 2}
        rows = dbo.rules.scheduled_changes.signoffs.t.select().where(dbo.rules.scheduled_changes.signoffs.sc_id == 3).execute().fetchall()
        self.assertEqual(len(rows), 2)
        ret = self._post("/scheduled_changes/rules/3", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"new_data_version": 3, "signoffs": {"bill": "releng"}})

        r = dbo.rules.scheduled_changes.t.select().where(dbo.rules.scheduled_changes.sc_id == 3).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 3,
            "scheduled_by": "bill",
            "data_version": 3,
            "complete": False,
            "base_priority": 150,
            "base_backgroundRate": 100,
            "base_mapping": "c",
            "base_update_type": "minor",
            "base_channel": "a",
            "base_buildID": None,
            "base_locale": None,
            "base_osVersion": None,
            "base_product": None,
            "base_data_version": None,
            "base_alias": None,
            "base_distribution": None,
            "base_fallbackMapping": None,
            "base_distVersion": None,
            "base_headerArchitecture": None,
            "base_comment": None,
            "base_memory": None,
            "base_mig64": None,
            "base_jaws": None,
            "base_instructionSet": None,
            "base_version": None,
            "base_rule_id": None,
            "base_buildTarget": None,
            "change_type": "insert",
        }
        self.assertEqual(db_data, expected)
        rows = dbo.rules.scheduled_changes.signoffs.t.select().where(dbo.rules.scheduled_changes.signoffs.sc_id == 3).execute().fetchall()
        self.assertEqual(len(rows), 1)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeDiffUserResetSignOffs(self):
        data = {"when": 2900000, "priority": 150, "backgroundRate": 50, "update_type": "minor", "sc_data_version": 1, "channel": "j"}
        rows = dbo.rules.scheduled_changes.signoffs.t.select().where(dbo.rules.scheduled_changes.signoffs.sc_id == 6).execute().fetchall()
        self.assertEqual(len(rows), 2)
        ret = self._post("/scheduled_changes/rules/6", data=data, username="julie")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"new_data_version": 2, "signoffs": {"julie": "releng"}})
        r = dbo.rules.scheduled_changes.t.select().where(dbo.rules.scheduled_changes.sc_id == 6).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 6,
            "scheduled_by": "julie",
            "data_version": 2,
            "complete": False,
            "base_priority": 150,
            "base_backgroundRate": 50,
            "base_mapping": "ab",
            "base_update_type": "minor",
            "base_channel": "j",
            "base_buildID": None,
            "base_locale": None,
            "base_osVersion": None,
            "base_product": "fake",
            "base_data_version": None,
            "base_alias": None,
            "base_distribution": None,
            "base_fallbackMapping": None,
            "base_distVersion": None,
            "base_headerArchitecture": None,
            "base_comment": None,
            "base_memory": None,
            "base_mig64": None,
            "base_jaws": None,
            "base_instructionSet": None,
            "base_version": None,
            "base_rule_id": None,
            "base_buildTarget": None,
            "change_type": "insert",
        }
        self.assertEqual(db_data, expected)
        rows = dbo.rules.scheduled_changes.signoffs.t.select().where(dbo.rules.scheduled_changes.signoffs.sc_id == 6).execute().fetchall()
        self.assertEqual(len(rows), 1)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeCantRemoveProductWithoutPermission(self):
        data = {"data_version": 1, "product": None, "sc_data_version": 1}
        ret = self._post("/scheduled_changes/rules/2", username="bob", data=data)
        self.assertEqual(ret.status_code, 403, ret.get_data())

    def testUpdateRuleWithMergeError(self):
        data = {"mapping": "a", "data_version": 2}
        ret = self._post("/rules/1", data=data)
        self.assertEqual(ret.status_code, 400, ret.get_data())
        self.assertIn("Is there a scheduled change", ret.get_data(as_text=True))

    def testDeleteRuleWithScheduledChange(self):
        ret = self._delete("/rules/1", qs=dict(data_version=2))
        self.assertEqual(ret.status_code, 400, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")
        self.assertIn("Cannot delete rows that have", ret.get_data(as_text=True))

    def testDeleteScheduledChange(self):
        ret = self._delete("/scheduled_changes/rules/1", qs=dict(data_version=1))
        self.assertEqual(ret.mimetype, "application/json")
        self.assertEqual(ret.status_code, 200, msg=ret.get_data())

    def testDeleteCompletedScheduledChange(self):
        ret = self._delete("/scheduled_changes/rules/4", qs=dict(data_version=1))
        self.assertEqual(ret.mimetype, "application/json")
        self.assertEqual(ret.status_code, 400, msg=ret.get_data())

    def testDeleteScheduledChangeWrongDataVersion(self):
        ret = self._delete("/scheduled_changes/rules/1", qs=dict(data_version=5))
        self.assertEqual(ret.status_code, 400, msg=ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")
        self.assertIn("Outdated Data Version", ret.get_data(as_text=True))

    def testDeleteScheduledChangeWithoutPermission(self):
        ret = self._delete("/scheduled_changes/rules/1", username="rex", qs=dict(data_version=1))
        self.assertEqual(ret.mimetype, "application/json")
        self.assertEqual(ret.status_code, 403, msg=ret.get_data())

    def testDeleteNonExistentScheduledChange(self):
        ret = self._delete("/scheduled_changes/rules/62", qs=dict(data_version=1))
        self.assertEqual(ret.mimetype, "application/json")
        self.assertEqual(ret.status_code, 404, msg=ret.get_data())

    def testEnactScheduledChangeExistingRule(self):
        ret = self._post("/scheduled_changes/rules/1/enact", username="mary")
        self.assertEqual(ret.mimetype, "application/json")
        self.assertEqual(ret.status_code, 200, ret.get_data())

        sc_row = dbo.rules.scheduled_changes.t.select().where(dbo.rules.scheduled_changes.sc_id == 1).execute().fetchall()[0]
        self.assertEqual(sc_row["complete"], True)

        row = dbo.rules.t.select().where(dbo.rules.rule_id == 1).execute().fetchall()[0]
        expected = {
            "rule_id": 1,
            "priority": 100,
            "version": "3.5",
            "buildTarget": "d",
            "backgroundRate": 100,
            "mapping": "b",
            "fallbackMapping": None,
            "update_type": "minor",
            "data_version": 3,
            "alias": None,
            "product": "a",
            "channel": "a",
            "buildID": None,
            "locale": None,
            "osVersion": None,
            "distribution": None,
            "distVersion": None,
            "headerArchitecture": None,
            "comment": None,
            "instructionSet": None,
            "memory": None,
            "mig64": None,
            "jaws": None,
        }
        self.assertEqual(dict(row), expected)

    def testEnactScheduledChangeNewRule(self):
        ret = self._post("/scheduled_changes/rules/2/enact", username="mary")
        self.assertEqual(ret.mimetype, "application/json")
        self.assertEqual(ret.status_code, 200, ret.get_data())

        sc_row = dbo.rules.scheduled_changes.t.select().where(dbo.rules.scheduled_changes.sc_id == 2).execute().fetchall()[0]
        self.assertEqual(sc_row["complete"], True)

        row = dbo.rules.t.select().where(dbo.rules.rule_id == 10).execute().fetchall()[0]
        expected = {
            "rule_id": 10,
            "priority": 50,
            "version": None,
            "buildTarget": None,
            "backgroundRate": 100,
            "mapping": "ab",
            "fallbackMapping": None,
            "update_type": "minor",
            "data_version": 1,
            "alias": None,
            "product": "baz",
            "channel": None,
            "buildID": None,
            "locale": None,
            "osVersion": None,
            "distribution": None,
            "distVersion": None,
            "headerArchitecture": None,
            "comment": None,
            "instructionSet": None,
            "memory": None,
            "mig64": None,
            "jaws": None,
        }
        self.assertEqual(dict(row), expected)

    def testEnactScheduledChangeNoPermissions(self):
        ret = self._post("/scheduled_changes/rules/2/enact", username="bob")
        self.assertEqual(ret.mimetype, "application/json")
        self.assertEqual(ret.status_code, 403, ret.get_data())

    def testGetScheduledChangeHistoryRevisions(self):
        ret = self._get("/scheduled_changes/rules/3/revisions")
        self.assertEqual(ret.status_code, 200)
        expected = {
            "count": 2,
            "revisions": [
                {
                    "change_id": 3,
                    "changed_by": "bill",
                    "timestamp": 10,
                    "sc_id": 3,
                    "scheduled_by": "bill",
                    "when": 2900000,
                    "sc_data_version": 2,
                    "priority": 150,
                    "backgroundRate": 100,
                    "channel": "a",
                    "mapping": "ghi",
                    "fallbackMapping": None,
                    "update_type": "minor",
                    "complete": False,
                    "telemetry_product": None,
                    "telemetry_channel": None,
                    "telemetry_uptake": None,
                    "rule_id": None,
                    "version": None,
                    "product": None,
                    "buildTarget": None,
                    "buildID": None,
                    "locale": None,
                    "osVersion": None,
                    "instructionSet": None,
                    "distribution": None,
                    "distVersion": None,
                    "memory": None,
                    "mig64": None,
                    "jaws": None,
                    "headerArchitecture": None,
                    "comment": None,
                    "alias": None,
                    "data_version": None,
                    "change_type": "insert",
                },
                {
                    "change_id": 2,
                    "changed_by": "bill",
                    "timestamp": 6,
                    "sc_id": 3,
                    "scheduled_by": "bill",
                    "when": 2000000,
                    "sc_data_version": 1,
                    "priority": 150,
                    "backgroundRate": 100,
                    "channel": "a",
                    "mapping": "def",
                    "fallbackMapping": None,
                    "update_type": "minor",
                    "complete": False,
                    "telemetry_product": None,
                    "telemetry_channel": None,
                    "telemetry_uptake": None,
                    "rule_id": None,
                    "version": None,
                    "product": None,
                    "buildTarget": None,
                    "buildID": None,
                    "locale": None,
                    "osVersion": None,
                    "instructionSet": None,
                    "distribution": None,
                    "distVersion": None,
                    "memory": None,
                    "mig64": None,
                    "jaws": None,
                    "headerArchitecture": None,
                    "comment": None,
                    "alias": None,
                    "data_version": None,
                    "change_type": "insert",
                },
            ],
        }
        self.assertEqual(ret.get_json(), expected)

    def testGetRulesHistory(self):
        ret = self._get("/rules/history")
        got = ret.get_json()
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.status_code, 200, msg=ret.get_data())
        self.assertEqual(got["Rules scheduled change"]["count"], 8)
        self.assertTrue("rule_id" in got["Rules scheduled change"]["revisions"][0])
        self.assertTrue("backgroundRate" in got["Rules scheduled change"]["revisions"][0])
        self.assertTrue("timestamp" in got["Rules scheduled change"]["revisions"][0])

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testRevertScheduledChange(self):
        ret = self._post("/scheduled_changes/rules/3/revisions", data={"change_id": 2})
        self.assertEqual(ret.status_code, 200, ret.get_data())

        self.assertEqual(dbo.rules.scheduled_changes.history.count(), 16)
        r = dbo.rules.scheduled_changes.t.select().where(dbo.rules.scheduled_changes.sc_id == 3).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 3,
            "scheduled_by": "bill",
            "complete": False,
            "data_version": 3,
            "base_rule_id": None,
            "base_priority": 150,
            "base_backgroundRate": 100,
            "base_channel": "a",
            "base_mapping": "def",
            "base_update_type": "minor",
            "base_version": None,
            "base_buildTarget": None,
            "base_alias": None,
            "base_product": None,
            "base_buildID": None,
            "base_locale": None,
            "base_osVersion": None,
            "base_distribution": None,
            "base_fallbackMapping": None,
            "base_distVersion": None,
            "base_headerArchitecture": None,
            "base_comment": None,
            "base_data_version": None,
            "base_instructionSet": None,
            "base_memory": None,
            "base_mig64": None,
            "base_jaws": None,
            "change_type": "insert",
        }
        self.assertEqual(db_data, expected)
        self.assertEqual(dbo.rules.scheduled_changes.conditions.history.count(), 16)
        cond = dbo.rules.scheduled_changes.conditions.t.select().where(dbo.rules.scheduled_changes.conditions.sc_id == 3).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 3, "data_version": 3, "when": 2000000, "telemetry_product": None, "telemetry_channel": None, "telemetry_uptake": None}
        self.assertEqual(dict(cond[0]), cond_expected)

    def testRevertScheduledChangeBadChangeId(self):
        ret = self._post("/scheduled_changes/rules/3/revisions", data={"change_id": 43})
        self.assertEqual(ret.status_code, 400, ret.get_data())

    def testRevertScheduledChangeChangeIdDoesntMatchScId(self):
        ret = self._post("/scheduled_changes/rules/3/revisions", data={"change_id": 4})
        self.assertEqual(ret.status_code, 400, ret.get_data())

    def testSignoffWithPermission(self):
        ret = self._post("/scheduled_changes/rules/2/signoffs", data=dict(role="qa"), username="bill")
        self.assertEqual(ret.mimetype, "application/json")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        r = dbo.rules.scheduled_changes.signoffs.t.select().where(dbo.rules.scheduled_changes.signoffs.sc_id == 2).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        self.assertEqual(db_data, {"sc_id": 2, "username": "bill", "role": "qa"})

    def testSignoffWithoutPermission(self):
        ret = self._post("/scheduled_changes/rules/2/signoffs", data=dict(role="relman"), username="bill")
        self.assertEqual(ret.mimetype, "application/json")
        self.assertEqual(ret.status_code, 403, ret.get_data())

    def testSignoffASecondTimeWithSameRole(self):
        ret = self._post("/scheduled_changes/rules/3/signoffs", data=dict(role="releng"), username="bill")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")
        r = dbo.rules.scheduled_changes.signoffs.t.select().where(dbo.rules.scheduled_changes.signoffs.sc_id == 3).execute().fetchall()
        self.assertEqual(len(r), 2)
        db_data = [dict(row) for row in r]
        self.assertIn({"sc_id": 3, "username": "bill", "role": "releng"}, db_data)
        self.assertIn({"sc_id": 3, "username": "mary", "role": "relman"}, db_data)

    def testSignoffWithSecondRole(self):
        ret = self._post("/scheduled_changes/rules/3/signoffs", data=dict(role="qa"), username="bill")
        self.assertEqual(ret.status_code, 403, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")

    def testSignoffWithoutRole(self):
        ret = self._post("/scheduled_changes/rules/3/signoffs", data=dict(lorem_ipso="random"), username="bill")
        self.assertEqual(ret.status_code, 400, ret.get_data())
        self.assertEqual(ret.mimetype, "application/problem+json")

    def testRevokeSignoff(self):
        ret = self._delete("/scheduled_changes/rules/3/signoffs", username="bill")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")
        r = dbo.rules.scheduled_changes.signoffs.t.select().where(dbo.rules.scheduled_changes.signoffs.sc_id == 3).execute().fetchall()
        self.assertEqual(len(r), 1)

    def testRevokeOtherUsersSignoffAsAdmin(self):
        # The username passed to _delete is the user performing the action.
        # The username in the query string is the person who's signoff we want to revoke.
        ret = self._delete("/scheduled_changes/rules/3/signoffs", username="bill", qs={"username": "mary"})
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")

    def testCannotRevokeOtherUsersSignoffAsNormalUser(self):
        # The username passed to _delete is the user performing the action.
        # The username in the query string is the person who's signoff we want to revoke.
        ret = self._delete("/scheduled_changes/rules/3/signoffs", username="julie", qs={"username": "mary"})
        self.assertEqual(ret.status_code, 403, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")
