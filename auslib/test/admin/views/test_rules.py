import json
import mock

from auslib.global_state import dbo
from auslib.test.admin.views.base import ViewTest
from auslib.util.comparison import operators


class TestRulesAPI_JSON(ViewTest):
    maxDiff = 1000

    def testGetRules(self):
        ret = self._get("/rules")
        got = json.loads(ret.data)
        self.assertEquals(got["count"], 5)

    def testGetRulesWithProductFilter(self):
        ret = self._get("/rules", qs={"product": "fake"})
        got = json.loads(ret.data)
        expected = {
            "rule_id": 4, "product": "fake", "priority": 80, "buildTarget": "d", "backgroundRate": 100, "mapping": "a",
            "update_type": "minor", "data_version": 1
        }
        self.assertEquals(got["count"], 1)
        for k, v in expected.iteritems():
            self.assertEquals(got["rules"][0][k], v)

    def testNewRulePost(self):
        ret = self._post('/rules', data=dict(backgroundRate=31, mapping='c', priority=33,
                                             product='Firefox', update_type='minor', channel='nightly'))
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        r = dbo.rules.t.select().where(dbo.rules.rule_id == ret.data).execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['mapping'], 'c')
        self.assertEquals(r[0]['backgroundRate'], 31)
        self.assertEquals(r[0]['priority'], 33)
        self.assertEquals(r[0]['data_version'], 1)

    def testNewRulePostJSON(self):
        data = dict(
            backgroundRate=31, mapping="c", priority=33, product="Firefox",
            update_type="minor", channel="nightly"
        )
        ret = self._post("/rules", data=data)
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        r = dbo.rules.t.select().where(dbo.rules.rule_id == ret.data).execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['mapping'], 'c')
        self.assertEquals(r[0]['backgroundRate'], 31)
        self.assertEquals(r[0]['priority'], 33)
        self.assertEquals(r[0]['data_version'], 1)

    def testNewRuleWithoutProductAdminPermission(self):
        data = dict(
            backgroundRate=31, mapping="a", priority=33, product="Firefox",
            update_type="minor", channel="nightly"
        )
        ret = self._post("/rules", data=data, username="billy")
        self.assertStatusCode(ret, 403)

    def testNewRuleWithProductAdminPermission(self):
        data = dict(
            backgroundRate=31, mapping="a", priority=33, product="a",
            update_type="minor", channel="nightly"
        )
        ret = self._post("/rules", data=data, username="billy")
        self.assertStatusCode(ret, 200)

    def testNewRuleWithoutPermission(self):
        data = dict(
            backgroundRate=31, mapping="c", priority=33, product="Firefox",
            update_type="minor", channel="nightly"
        )
        ret = self._post("/rules", data=data, username="jack")
        self.assertEquals(ret.status_code, 403, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))

    # A POST without the required fields shouldn't be valid
    def testMissingFields(self):
        # But we still need to pass product, because permission checking
        # is done before what we're testing
        ret = self._post('/rules', data=dict({'product': 'a'}))
        self.assertEquals(ret.status_code, 400, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        self.assertTrue('backgroundRate' in ret.data, msg=ret.data)
        self.assertTrue('priority' in ret.data, msg=ret.data)

    def testVersionValidation(self):
        for op in operators:
            ret = self._post('/rules', data=dict(backgroundRate=42, mapping='d', priority=50,
                             product='Firefox', update_type='minor', version='%s4.0' % op))
            self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s, Operator: %s" % (ret.status_code, ret.data, op))
            r = dbo.rules.t.select().where(dbo.rules.rule_id == ret.data).execute().fetchall()
            self.assertEquals(len(r), 1)
            self.assertEquals(r[0]['version'], '%s4.0' % op)

    def testBuildIDValidation(self):
        for op in operators:
            ret = self._post('/rules', data=dict(backgroundRate=42, mapping='d', priority=50,
                             product='Firefox', update_type='minor', buildID='%s20010101000000' % op))
            self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s, Operator: %s" % (ret.status_code, ret.data, op))
            r = dbo.rules.t.select().where(dbo.rules.rule_id == ret.data).execute().fetchall()
            self.assertEquals(len(r), 1)
            self.assertEquals(r[0]['buildID'], '%s20010101000000' % op)

    def testVersionValidationBogusInput(self):
        for bogus in ('<= 4.0', ' <=4.0', '<>4.0', '<=-4.0', '=4.0', '> 4.0', '>= 4.0', ' >=4.0', ' 4.0 '):
            ret = self._post('/rules', data=dict(backgroundRate=42, mapping='d', priority=50,
                             product='Firefox', update_type='minor', version=bogus))
            self.assertEquals(ret.status_code, 400, "Status Code: %d, Data: %s, Input: %s" % (ret.status_code, ret.data, bogus))
            self.assertTrue('version' in ret.data, msg=ret.data)

    def testBuilIDValidationBogusInput(self):
        for bogus in ('<= 4120', ' <=4120', '<>4120', '<=-4120', '=41230', '> 41210', '>= 41220', ' >=41220', ' 41220 '):
            ret = self._post('/rules', data=dict(backgroundRate=42, mapping='d', priority=50,
                             product='Firefox', update_type='minor', buildID=bogus))
            self.assertEquals(ret.status_code, 400, "Status Code: %d, Data: %s, Input: %s" % (ret.status_code, ret.data, bogus))
            self.assertTrue('buildID' in ret.data, msg=ret.data)

    def testValidationEmptyInput(self):
        ret = self._post('/rules', data=dict(backgroundRate=42, mapping='d', priority=50,
                         product='Firefox', update_type='minor', version='', buildID=''))
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        r = dbo.rules.t.select().where(dbo.rules.rule_id == ret.data).execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['buildID'], None)
        self.assertEquals(r[0]['version'], None)


class TestSingleRuleView_JSON(ViewTest):

    def testGetRule(self):
        ret = self._get("/rules/1")
        expected = dict(
            backgroundRate=100,
            mapping="c",
            fallbackMapping=None,
            priority=100,
            product=None,
            version="3.5",
            buildID=None,
            channel=None,
            locale=None,
            distribution=None,
            buildTarget="d",
            osVersion=None,
            systemCapabilities=None,
            distVersion=None,
            comment=None,
            update_type="minor",
            headerArchitecture=None,
            data_version=1,
            rule_id=1,
            alias=None,
            whitelist=None,
        )
        self.assertEquals(json.loads(ret.data), expected)

    def testGetRuleByAlias(self):
        ret = self._get("/rules/frodo")
        expected = dict(
            backgroundRate=100,
            mapping="b",
            fallbackMapping=None,
            priority=100,
            product=None,
            version="3.3",
            buildID=None,
            channel=None,
            locale=None,
            distribution=None,
            buildTarget="d",
            osVersion=None,
            systemCapabilities=None,
            distVersion=None,
            comment=None,
            update_type="minor",
            headerArchitecture=None,
            data_version=1,
            rule_id=2,
            alias="frodo",
            whitelist=None,
        )
        self.assertEquals(json.loads(ret.data), expected)

    def testGetRule404(self):
        ret = self.client.get("/rules/123")
        self.assertEquals(ret.status_code, 404)

    def testPost(self):
        # Make some changes to a rule
        ret = self._post('/rules/1', data=dict(backgroundRate=71, mapping='d',
                                               fallbackMapping="fallback_d", priority=73, data_version=1,
                                               product='Firefox', channel='nightly', systemCapabilities="SSE"))
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        load = json.loads(ret.data)
        self.assertEquals(load['new_data_version'], 2)

        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 1).execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['mapping'], 'd')
        self.assertEquals(r[0]['fallbackMapping'], 'fallback_d')
        self.assertEquals(r[0]['backgroundRate'], 71)
        self.assertEquals(r[0]['systemCapabilities'], "SSE")
        self.assertEquals(r[0]['priority'], 73)
        self.assertEquals(r[0]['data_version'], 2)
        # And that we didn't modify other fields
        self.assertEquals(r[0]['update_type'], 'minor')
        self.assertEquals(r[0]['version'], '3.5')
        self.assertEquals(r[0]['buildTarget'], 'd')

    def testPutRuleOutdatedData(self):
        # Make changes to a rule
        ret = self._put('/rules/1', data=dict(backgroundRate=71, mapping='d', priority=73, data_version=1, product='Firefox', channel='nightly'))
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        load = json.loads(ret.data)
        self.assertEquals(load['new_data_version'], 2)
        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 1).execute().fetchall()
        self.assertEquals(r[0]['data_version'], 2)

        # OutdatedDataVersion Request
        ret2 = self._put('/rules/1', data=dict(backgroundRate=71, mapping='d', priority=73, data_version=1, product='Firefox', channel='nightly'))
        self.assertEquals(ret2.status_code, 400, "Status Code: %d, Data: %s" % (ret2.status_code, ret2.data))

    def testPostRuleOutdatedData(self):
        # Make changes to a rule
        ret = self._post('/rules/1', data=dict(backgroundRate=71, mapping='d', priority=73, data_version=1, product='Firefox', channel='nightly'))
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        load = json.loads(ret.data)
        self.assertEquals(load['new_data_version'], 2)
        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 1).execute().fetchall()
        self.assertEquals(r[0]['data_version'], 2)

        # OutdatedDataVersion Request
        ret2 = self._put('/rules/1', data=dict(backgroundRate=71, mapping='d', priority=73, data_version=1, product='Firefox', channel='nightly'))
        self.assertEquals(ret2.status_code, 400, "Status Code: %d, Data: %s" % (ret2.status_code, ret2.data))

    def testPostByAlias(self):
        # Make some changes to a rule
        ret = self._post('/rules/frodo', data=dict(backgroundRate=71, mapping='d', priority=73, data_version=1,
                                                   product='Firefox', channel='nightly'))
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        load = json.loads(ret.data)
        self.assertEquals(load['new_data_version'], 2)

        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 2).execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['mapping'], 'd')
        self.assertEquals(r[0]['backgroundRate'], 71)
        self.assertEquals(r[0]['priority'], 73)
        self.assertEquals(r[0]['data_version'], 2)
        # And that we didn't modify other fields
        self.assertEquals(r[0]['update_type'], 'minor')
        self.assertEquals(r[0]['version'], '3.3')
        self.assertEquals(r[0]['buildTarget'], 'd')

    def testPostJSON(self):
        data = dict(
            backgroundRate=71, mapping="d", priority=73, data_version=1,
            product="Firefox", channel="nightly"
        )
        ret = self._post("/rules/1", data=data)
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        load = json.loads(ret.data)
        self.assertEquals(load['new_data_version'], 2)

        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 1).execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['mapping'], 'd')
        self.assertEquals(r[0]['backgroundRate'], 71)
        self.assertEquals(r[0]['priority'], 73)
        self.assertEquals(r[0]['data_version'], 2)
        # And that we didn't modify other fields
        self.assertEquals(r[0]['update_type'], 'minor')
        self.assertEquals(r[0]['version'], '3.5')
        self.assertEquals(r[0]['buildTarget'], 'd')

    def testPostAddAlias(self):
        # Make some changes to a rule
        ret = self._post("/rules/1", data=dict(alias="sam", data_version=1))
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        load = json.loads(ret.data)
        self.assertEquals(load["new_data_version"], 2)

        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 1).execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]["alias"], "sam")
        self.assertEquals(r[0]["data_version"], 2)
        # And that we didn"t modify other fields
        self.assertEquals(r[0]["update_type"], "minor")
        self.assertEquals(r[0]["version"], "3.5")
        self.assertEquals(r[0]["buildTarget"], "d")

    def testPostAddBadAlias(self):
        ret = self._post("/rules/1", data=dict(alias="abc#$%", data_version=1))
        self.assertEquals(ret.status_code, 400, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))

    def testPostWithoutProduct(self):
        ret = self._post('/rules/4', username='bob',
                         data=dict(backgroundRate=71, mapping='d', priority=73, data_version=1,
                                   channel='nightly'))
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        load = json.loads(ret.data)
        self.assertEquals(load['new_data_version'], 2)
        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 4).execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['mapping'], 'd')
        self.assertEquals(r[0]['backgroundRate'], 71)
        self.assertEquals(r[0]['priority'], 73)
        self.assertEquals(r[0]['data_version'], 2)
        self.assertEquals(r[0]['channel'], 'nightly')
        # And that we didn't modify other fields
        self.assertEquals(r[0]['update_type'], 'minor')
        self.assertEquals(r[0]['buildTarget'], 'd')
        self.assertEquals(r[0]['product'], 'fake')

    def testPostSetBackgroundRateTo0(self):
        ret = self._post("/rules/4", data=dict(backgroundRate=0, data_version=1))
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        load = json.loads(ret.data)
        self.assertEquals(load['new_data_version'], 2)
        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 4).execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['backgroundRate'], 0)
        self.assertEquals(r[0]['data_version'], 2)
        # And that we didn't modify other fields
        self.assertEquals(r[0]['update_type'], 'minor')
        self.assertEquals(r[0]['mapping'], 'a')
        self.assertEquals(r[0]['priority'], 80)
        self.assertEquals(r[0]['buildTarget'], 'd')
        self.assertEquals(r[0]['product'], 'fake')

    def testPostRemoveRestriction(self):
        ret = self._post("/rules/5", data=dict(buildTarget="", data_version=1))
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        load = json.loads(ret.data)
        self.assertEquals(load['new_data_version'], 2)
        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 5).execute().fetchall()
        self.assertEquals(len(r), 1)
        r = r[0]
        self.assertEquals(r["buildTarget"], None)
        # ...and that other fields weren't modified
        self.assertEquals(r["priority"], 80)
        self.assertEquals(r["version"], "3.3")
        self.assertEquals(r["backgroundRate"], 0)
        self.assertEquals(r["mapping"], "c")
        self.assertEquals(r["update_type"], "minor")
        self.assertEquals(r["product"], None)

    def testPost404(self):
        ret = self._post("/rules/555", data=dict(mapping="d"))
        self.assertEquals(ret.status_code, 404)

    def testPostWithBadData(self):
        ret = self._post("/rules/1", data=dict(mapping="uhet"))
        self.assertEquals(ret.status_code, 400)

    def testPostWithBadAlias(self):
        ret = self._post("/rules/1", data=dict(alias="3", data_version=1))
        self.assertEquals(ret.status_code, 400)

    def testBadAuthPost(self):
        ret = self._badAuthPost('/rules/1', data=dict(backgroundRate=100, mapping='c', priority=100, data_version=1))
        self.assertEquals(ret.status_code, 403, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))

    def testHttpRemoteUserAuth(self):
        # Make some changes to a rule
        ret = self._httpRemoteUserPost('/rules/1', data=dict(backgroundRate=71, mapping='d', priority=73, data_version=1,
                                                             product='Firefox', channel='nightly'))
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        load = json.loads(ret.data)
        self.assertEquals(load['new_data_version'], 2)

        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 1).execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['mapping'], 'd')
        self.assertEquals(r[0]['backgroundRate'], 71)
        self.assertEquals(r[0]['priority'], 73)
        self.assertEquals(r[0]['data_version'], 2)
        # And that we didn't modify other fields
        self.assertEquals(r[0]['update_type'], 'minor')
        self.assertEquals(r[0]['version'], '3.5')
        self.assertEquals(r[0]['buildTarget'], 'd')

    def testNoPermissionToAlterExistingProduct(self):
        ret = self._post('/rules/1', data=dict(backgroundRate=71, data_version=1), username='bob')
        self.assertEquals(ret.status_code, 403)

    def testNoPermissionToAlterNewProduct(self):
        ret = self._post(
            '/rules/4', data=dict(product='protected', mapping='a', backgroundRate=71, priority=50, update_type='minor', data_version=1), username='bob')
        self.assertEquals(ret.status_code, 403)

    def testGetSingleRule(self):
        ret = self._get('/rules/1')
        self.assertEquals(ret.status_code, 200)
        self.assertTrue("c" in ret.data, msg=ret.data)
        for h in ("X-CSRF-Token", "X-Data-Version"):
            self.assertTrue(h in ret.headers, msg=ret.headers)

    def testDeleteRule(self):
        ret = self._delete('/rules/1', qs=dict(data_version=1))
        self.assertEquals(ret.status_code, 200, msg=ret.data)

    def testDeleteRuleOutdatedData(self):
        ret = self._get('/rules/1')
        self.assertEquals(ret.status_code, 200, msg=ret.data)
        ret = self._delete('/rules/1', qs=dict(data_version=7))
        self.assertEquals(ret.status_code, 400, msg=ret.data)

    def testDeleteRuleByAlias(self):
        ret = self._delete('/rules/frodo', qs=dict(data_version=1))
        self.assertEquals(ret.status_code, 200, msg=ret.data)

    def testDeleteRule404(self):
        ret = self._delete("/rules/112")
        self.assertEquals(ret.status_code, 404)

    def testDeleteWithProductAdminPermission(self):
        ret = self._delete("/rules/3", username="billy",
                           qs=dict(data_version=1))
        self.assertEquals(ret.status_code, 200)

    def testDeleteWithoutProductAdminPermission(self):
        ret = self._delete("/rules/4", username="billy",
                           qs=dict(data_version=1))
        self.assertEquals(ret.status_code, 403)

    def testDeleteWithoutPermission(self):
        ret = self._delete("/rules/2", username="tony", qs=dict(data_version=1))
        self.assertEquals(ret.status_code, 403)


class TestRuleHistoryView(ViewTest):

    def testGetNoRevisions(self):
        url = '/rules/1/revisions'
        ret = self._get(url)
        self.assertEquals(ret.status_code, 200, msg=ret.data)
        got = json.loads(ret.data)
        self.assertEquals(got["count"], 0)

    def testGetRefusesAlias(self):
        ret = self._get("/rules/frodo/revisions")
        self.assertEquals(ret.status_code, 404)

    def testGetRevisions(self):
        # Make some changes to a rule
        ret = self._post(
            '/rules/1',
            data=dict(
                backgroundRate=71,
                mapping='d',
                priority=73,
                data_version=1,
                product='Firefox',
                update_type='minor',
                channel='nightly',
            )
        )
        self.assertEquals(
            ret.status_code,
            200,
            "Status Code: %d, Data: %s" % (ret.status_code, ret.data)
        )
        # and again
        ret = self._post(
            '/rules/1',
            data=dict(
                backgroundRate=72,
                mapping='d',
                priority=73,
                data_version=2,
                product='Firefux',
                update_type='minor',
                channel='nightly',
            )
        )
        self.assertEquals(
            ret.status_code,
            200,
            "Status Code: %d, Data: %s" % (ret.status_code, ret.data)
        )

        url = '/rules/1/revisions'
        ret = self._get(url)
        got = json.loads(ret.data)
        self.assertEquals(ret.status_code, 200, msg=ret.data)
        self.assertEquals(got["count"], 2)
        self.assertTrue(u"rule_id" in got["rules"][0])
        self.assertTrue(u"backgroundRate" in got["rules"][0])

    def testPostRevisionRollback(self):
        # Make some changes to a rule
        ret = self._post(
            '/rules/1',
            data=dict(
                backgroundRate=71,
                mapping='d',
                priority=73,
                data_version=1,
                product='Firefox',
                update_type='minor',
                channel='nightly',
                buildID='1234',
                osVersion='10.5',
                headerArchitecture='INTEL',
                distVersion='19',
                buildTarget='MAC',
            )
        )
        self.assertEquals(
            ret.status_code,
            200,
            "Status Code: %d, Data: %s" % (ret.status_code, ret.data)
        )
        # and again
        ret = self._post(
            '/rules/1',
            data=dict(
                backgroundRate=72,
                mapping='d',
                priority=73,
                data_version=2,
                product='Firefux',
                update_type='minor',
                channel='nightly',
            )
        )
        self.assertEquals(
            ret.status_code,
            200,
            "Status Code: %d, Data: %s" % (ret.status_code, ret.data)
        )

        table = dbo.rules
        row, = table.select(where=[table.rule_id == 1])
        self.assertEqual(row['backgroundRate'], 72)
        self.assertEqual(row['data_version'], 3)

        query = table.history.t.count()
        count, = query.execute().first()
        self.assertEqual(count, 2)

        # Oh no! We prefer the product=Firefox, backgroundRate=71 one better
        row, = table.history.select(
            where=[table.history.product == 'Firefox',
                   table.history.backgroundRate == 71],
            limit=1
        )
        change_id = row['change_id']
        assert row['rule_id'] == 1  # one of the fixtures

        url = '/rules/1/revisions'
        ret = self._post(url, {'change_id': change_id})
        self.assertEquals(ret.status_code, 200, ret.data)

        query = table.history.t.count()
        count, = query.execute().first()
        self.assertEqual(count, 3)

        row, = table.select(where=[table.rule_id == 1])
        self.assertEqual(row['backgroundRate'], 71)
        self.assertEqual(row['product'], 'Firefox')
        self.assertEqual(row['data_version'], 4)
        self.assertEqual(row['buildID'], '1234')
        self.assertEqual(row['osVersion'], '10.5')
        self.assertEqual(row['headerArchitecture'], 'INTEL')
        self.assertEqual(row['distVersion'], '19')
        self.assertEqual(row['buildTarget'], 'MAC')

    def testRollbackWithoutPermission(self):
        ret = self._post(
            '/rules/1',
            data=dict(
                backgroundRate=71,
                mapping='d',
                priority=73,
                data_version=1,
                product='',
                update_type='minor',
                channel='nightly',
                buildID='1234',
                osVersion='10.5',
                headerArchitecture='INTEL',
                distVersion='19',
                buildTarget='MAC',
            )
        )
        ret = self._post(
            '/rules/1',
            data=dict(
                backgroundRate=72,
                mapping='d',
                priority=73,
                product='',
                data_version=2,
                update_type='minor',
                channel='nightly',
            )
        )
        row, = dbo.rules.history.select(
            where=[dbo.rules.history.backgroundRate == 72],
            limit=1
        )
        change_id = row['change_id']

        url = '/rules/1/revisions'
        ret = self._post(url, {'change_id': change_id}, username='bob')
        self.assertEquals(ret.status_code, 403)

    def testPostRevisionRollbackBadRequests(self):
        ret = self._post(
            '/rules/1',
            data=dict(
                backgroundRate=71,
                mapping='d',
                priority=73,
                data_version=1,
                product='Firefox',
                update_type='minor',
                channel='nightly',
                buildID='1234',
                osVersion='10.5',
                headerArchitecture='INTEL',
                distVersion='19',
                buildTarget='MAC',
            )
        )
        self.assertEquals(
            ret.status_code,
            200,
            "Status Code: %d, Data: %s" % (ret.status_code, ret.data)
        )
        # when posting you need both the rule_id and the change_id
        wrong_url = '/rules/999/revisions'
        # not found rule_id
        ret = self._post(wrong_url, {'change_id': 10})
        self.assertEquals(ret.status_code, 404, ret.data)

        url = '/rules/1/revisions'
        ret = self._post(url, {'change_id': 999})
        # not found change_id
        self.assertEquals(ret.status_code, 400)

        url = '/rules/1/revisions'
        ret = self._post(url)  # no change_id posted
        self.assertEquals(ret.status_code, 400)


class TestSingleColumn_JSON(ViewTest):

    def testGetRules(self):
        expected_product = ["fake", "a"]
        expected = dict(count=2, product=expected_product)
        ret = self._get("/rules/columns/product")
        returned_data = json.loads(ret.data)
        self.assertEquals(returned_data['count'], expected['count'])
        self.assertItemsEqual(returned_data['product'], expected['product'])

    def testGetRuleColumn404(self):
        ret = self.client.get("/rules/columns/blah")
        self.assertEquals(ret.status_code, 404)


class TestRuleScheduledChanges(ViewTest):
    maxDiff = 15000

    def setUp(self):
        super(TestRuleScheduledChanges, self).setUp()
        dbo.rules.scheduled_changes.t.insert().execute(
            sc_id=1, scheduled_by="bill", data_version=1, base_rule_id=1, base_priority=100, base_version="3.5", base_buildTarget="d",
            base_backgroundRate=100, base_mapping="b", base_update_type="minor", base_data_version=1,
        )
        dbo.rules.scheduled_changes.conditions.t.insert().execute(sc_id=1, when=1000000, data_version=1)
        dbo.rules.scheduled_changes.t.insert().execute(
            sc_id=2, scheduled_by="bill", data_version=1, base_priority=50, base_backgroundRate=100, base_product="baz",
            base_mapping="ab", base_update_type="minor",
        )
        dbo.rules.scheduled_changes.conditions.t.insert().execute(sc_id=2, when=1500000, data_version=1)
        dbo.rules.scheduled_changes.t.insert().execute(
            sc_id=3, scheduled_by="bill", data_version=2, base_priority=150, base_backgroundRate=100, base_product="ff",
            base_mapping="ghi", base_update_type="minor",
        )
        dbo.rules.scheduled_changes.conditions.t.insert().execute(sc_id=3, when=2900000, data_version=2)
        dbo.rules.scheduled_changes.t.insert().execute(
            sc_id=4, scheduled_by="bill", data_version=2, complete=True, base_rule_id=5, base_priority=80, base_version="3.3",
            base_buildTarget="d", base_backgroundRate=0, base_mapping="c", base_update_type="minor", base_data_version=1,
        )
        dbo.rules.scheduled_changes.conditions.t.insert().execute(sc_id=4, when=500000, data_version=2)

        dbo.rules.scheduled_changes.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=5, sc_id=3)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=5, sc_id=3)

        dbo.rules.scheduled_changes.history.t.insert().execute(
            change_id=2, changed_by="bill", timestamp=6, sc_id=3, scheduled_by="bill", data_version=1, base_priority=150,
            base_backgroundRate=100, base_product="ff", base_mapping="def", base_update_type="minor",
        )
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=2, changed_by="bill", timestamp=6, sc_id=3, when=2000000, data_version=1)

        dbo.rules.scheduled_changes.history.t.insert().execute(
            change_id=3, changed_by="bill", timestamp=10, sc_id=3, scheduled_by="bill", data_version=2, base_priority=150,
            base_backgroundRate=100, base_product="ff", base_mapping="ghi", base_update_type="minor",
        )
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=3, changed_by="bill", timestamp=10, sc_id=3, when=2900000, data_version=2)

        dbo.rules.scheduled_changes.history.t.insert().execute(change_id=4, changed_by="bill", timestamp=15, sc_id=2)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=4, changed_by="bill", timestamp=15, sc_id=2)

        dbo.rules.scheduled_changes.history.t.insert().execute(
            change_id=5, changed_by="bill", timestamp=16, sc_id=2, scheduled_by="bill", data_version=1, base_priority=50,
            base_backgroundRate=100, base_product="baz", base_mapping="ab", base_update_type="minor"
        )
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=5, changed_by="bill", timestamp=16, sc_id=2, when=1500000, data_version=1)

        dbo.rules.scheduled_changes.history.t.insert().execute(change_id=6, changed_by="bill", timestamp=5, sc_id=4)
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=6, changed_by="bill", timestamp=5, sc_id=4)

        dbo.rules.scheduled_changes.history.t.insert().execute(
            change_id=7, changed_by="bill", timestamp=6, sc_id=4, scheduled_by="bill", data_version=1, base_priority=80,
            base_version="3.3", base_buildTarget="d", base_backgroundRate=0, base_mapping="c", base_update_type="minor", base_data_version=1
        )
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=7, changed_by="bill", timestamp=6, sc_id=4, when=500000, data_version=1)

        dbo.rules.scheduled_changes.history.t.insert().execute(
            change_id=8, changed_by="bill", timestamp=7, sc_id=4, scheduled_by="bill", data_version=2, complete=True, base_rule_id=5,
            base_priority=80, base_version="3.3", base_buildTarget="d", base_backgroundRate=0, base_mapping="c", base_update_type="minor", base_data_version=1
        )
        dbo.rules.scheduled_changes.conditions.history.t.insert().execute(change_id=8, changed_by="bill", timestamp=7, sc_id=4, when=500000, data_version=2)

    def testGetScheduledChanges(self):
        ret = self._get("/scheduled_changes/rules")
        expected = {
            "count": 3,
            "scheduled_changes": [
                {
                    "sc_id": 1, "when": 1000000, "scheduled_by": "bill", "complete": False, "sc_data_version": 1, "rule_id": 1, "priority": 100,
                    "version": "3.5", "buildTarget": "d", "backgroundRate": 100, "mapping": "b", "update_type": "minor",
                    "data_version": 1, "alias": None, "product": None, "channel": None, "buildID": None, "locale": None,
                    "osVersion": None, "distribution": None, "fallbackMapping": None, "distVersion": None, "headerArchitecture": None, "comment": None,
                    "whitelist": None, "systemCapabilities": None, "telemetry_product": None, "telemetry_channel": None, "telemetry_uptake": None,
                },
                {
                    "sc_id": 2, "when": 1500000, "scheduled_by": "bill", "complete": False, "sc_data_version": 1, "rule_id": None, "priority": 50,
                    "backgroundRate": 100, "product": "baz", "mapping": "ab", "update_type": "minor", "version": None,
                    "buildTarget": None, "alias": None, "channel": None, "buildID": None, "locale": None, "osVersion": None,
                    "distribution": None, "fallbackMapping": None, "distVersion": None, "headerArchitecture": None, "comment": None, "whitelist": None,
                    "data_version": None, "systemCapabilities": None, "telemetry_product": None, "telemetry_channel": None, "telemetry_uptake": None,
                },
                {
                    "sc_id": 3, "when": 2900000, "scheduled_by": "bill", "complete": False, "sc_data_version": 2, "rule_id": None, "priority": 150,
                    "backgroundRate": 100, "product": "ff", "mapping": "ghi", "update_type": "minor", "version": None,
                    "buildTarget": None, "alias": None, "channel": None, "buildID": None, "locale": None, "osVersion": None,
                    "distribution": None, "fallbackMapping": None, "distVersion": None, "headerArchitecture": None, "comment": None, "whitelist": None,
                    "data_version": None, "systemCapabilities": None, "telemetry_product": None, "telemetry_channel": None, "telemetry_uptake": None,
                },
            ],
        }
        self.assertEquals(json.loads(ret.data), expected)

    def testGetScheduledChangesWithCompleted(self):
        ret = self._get("/scheduled_changes/rules", qs={"all": 1})
        expected = {
            "count": 4,
            "scheduled_changes": [
                {
                    "sc_id": 1, "when": 1000000, "scheduled_by": "bill", "complete": False, "sc_data_version": 1, "rule_id": 1, "priority": 100,
                    "version": "3.5", "buildTarget": "d", "backgroundRate": 100, "mapping": "b", "update_type": "minor",
                    "data_version": 1, "alias": None, "product": None, "channel": None, "buildID": None, "locale": None,
                    "osVersion": None, "distribution": None, "fallbackMapping": None, "distVersion": None, "headerArchitecture": None, "comment": None,
                    "whitelist": None, "systemCapabilities": None, "telemetry_product": None, "telemetry_channel": None, "telemetry_uptake": None,
                },
                {
                    "sc_id": 2, "when": 1500000, "scheduled_by": "bill", "complete": False, "sc_data_version": 1, "rule_id": None, "priority": 50,
                    "backgroundRate": 100, "product": "baz", "mapping": "ab", "update_type": "minor", "version": None,
                    "buildTarget": None, "alias": None, "channel": None, "buildID": None, "locale": None, "osVersion": None,
                    "distribution": None, "fallbackMapping": None, "distVersion": None, "headerArchitecture": None, "comment": None, "whitelist": None,
                    "data_version": None, "systemCapabilities": None, "telemetry_product": None, "telemetry_channel": None, "telemetry_uptake": None,
                },
                {
                    "sc_id": 3, "when": 2900000, "scheduled_by": "bill", "complete": False, "sc_data_version": 2, "rule_id": None, "priority": 150,
                    "backgroundRate": 100, "product": "ff", "mapping": "ghi", "update_type": "minor", "version": None,
                    "buildTarget": None, "alias": None, "channel": None, "buildID": None, "locale": None, "osVersion": None,
                    "distribution": None, "fallbackMapping": None, "distVersion": None, "headerArchitecture": None, "comment": None, "whitelist": None,
                    "data_version": None, "systemCapabilities": None, "telemetry_product": None, "telemetry_channel": None, "telemetry_uptake": None,
                },
                {
                    "sc_id": 4, "when": 500000, "scheduled_by": "bill", "complete": True, "sc_data_version": 2, "rule_id": 5, "priority": 80,
                    "version": "3.3", "buildTarget": "d", "backgroundRate": 0, "mapping": "c", "update_type": "minor",
                    "data_version": 1, "alias": None, "product": None, "channel": None, "buildID": None, "locale": None,
                    "osVersion": None, "distribution": None, "fallbackMapping": None, "distVersion": None, "headerArchitecture": None, "comment": None,
                    "whitelist": None, "systemCapabilities": None, "telemetry_product": None, "telemetry_channel": None, "telemetry_uptake": None,
                },
            ],
        }
        self.assertEquals(json.loads(ret.data), expected)

    def testAddScheduledChangeExistingRule(self):
        data = {
            "telemetry_product": "foo", "telemetry_channel": "bar", "telemetry_uptake": 42, "rule_id": 5,
            "priority": 80, "buildTarget": "d", "version": "3.3", "backgroundRate": 100, "mapping": "c", "update_type": "minor",
            "data_version": 1
        }
        ret = self._post("/scheduled_changes/rules", data=data)
        self.assertEquals(ret.status_code, 200, ret.data)
        self.assertEquals(json.loads(ret.data), {"sc_id": 5})

        r = dbo.rules.scheduled_changes.t.select().where(dbo.rules.scheduled_changes.sc_id == 5).execute().fetchall()
        self.assertEquals(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "scheduled_by": "bill", "base_rule_id": 5, "base_priority": 80, "base_buildTarget": "d", "base_version": "3.3", "base_backgroundRate": 100,
            "base_mapping": "c", "base_update_type": "minor", "base_data_version": 1, "data_version": 1, "sc_id": 5, "complete": False, "base_alias": None,
            "base_product": None, "base_channel": None, "base_buildID": None, "base_locale": None, "base_osVersion": None, "base_distribution": None,
            "base_fallbackMapping": None, "base_distVersion": None, "base_headerArchitecture": None, "base_comment": None, "base_whitelist": None,
            "base_systemCapabilities": None,
        }
        self.assertEquals(db_data, expected)
        cond = dbo.rules.scheduled_changes.conditions.t.select().where(dbo.rules.scheduled_changes.conditions.sc_id == 5).execute().fetchall()
        self.assertEquals(len(cond), 1)
        cond_expected = {"sc_id": 5, "data_version": 1, "telemetry_product": "foo", "telemetry_channel": "bar", "telemetry_uptake": 42, "when": None}
        self.assertEquals(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeNewRule(self):
        data = {
            "when": 1234567, "priority": 120, "backgroundRate": 100, "product": "blah", "channel": "blah",
            "update_type": "minor", "mapping": "a",
        }
        ret = self._post("/scheduled_changes/rules", data=data)
        self.assertEquals(ret.status_code, 200, ret.data)
        self.assertEquals(json.loads(ret.data), {"sc_id": 5})

        r = dbo.rules.scheduled_changes.t.select().where(dbo.rules.scheduled_changes.sc_id == 5).execute().fetchall()
        self.assertEquals(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "scheduled_by": "bill", "base_priority": 120, "base_backgroundRate": 100, "base_product": "blah", "base_channel": "blah",
            "base_update_type": "minor", "base_mapping": "a", "sc_id": 5, "data_version": 1, "complete": False, "base_data_version": None,
            "base_rule_id": None, "base_buildTarget": None, "base_version": None, "base_alias": None, "base_buildID": None, "base_locale": None,
            "base_osVersion": None, "base_distribution": None, "base_fallbackMapping": None, "base_distVersion": None, "base_headerArchitecture": None,
            "base_comment": None, "base_whitelist": None, "base_systemCapabilities": None,
        }
        self.assertEquals(db_data, expected)
        cond = dbo.rules.scheduled_changes.conditions.t.select().where(dbo.rules.scheduled_changes.conditions.sc_id == 5).execute().fetchall()
        self.assertEquals(len(cond), 1)
        cond_expected = {"sc_id": 5, "data_version": 1, "when": 1234567, "telemetry_product": None, "telemetry_channel": None, "telemetry_uptake": None}
        self.assertEquals(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeInThePast(self):
        data = {
            "when": 67, "priority": 120, "backgroundRate": 100, "product": "blah", "channel": "blah",
            "update_type": "minor", "mapping": "a",
        }
        ret = self._post("/scheduled_changes/rules", data=data)
        self.assertEquals(ret.status_code, 400, ret.data)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeNoPermissionsToSchedule(self):
        data = {
            "when": 1234567, "priority": 120, "backgroundRate": 100, "product": "blah", "channel": "blah",
            "update_type": "minor", "mapping": "a",
        }
        ret = self._post("/scheduled_changes/rules", data=data, username="bob")
        self.assertEquals(ret.status_code, 403, ret.data)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeNoPermissionsToMakeChange(self):
        data = {
            "when": 1234567, "priority": 120, "backgroundRate": 100, "product": "foo", "channel": "blah",
            "update_type": "minor", "mapping": "a",
        }
        ret = self._post("/scheduled_changes/rules", data=data, username="mary")
        self.assertEquals(ret.status_code, 403, ret.data)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeMultipleConditions(self):
        data = {
            "when": 23893254, "telemetry_product": "foo", "telemetry_channel": "foo", "telemetry_uptake": 5,
            "priority": 120, "backgroundRate": 100, "update_type": "minor",
        }
        ret = self._post("scheduled_changes/rules", data=data)
        self.assertEquals(ret.status_code, 400)

    def testAddScheduledChangeMissingRequiredTelemetryFields(self):
        data = {
            "telemetry_product": "foo", "priority": 120, "backgroundRate": 100, "update_type": "minor",
        }
        ret = self._post("scheduled_changes/rules", data=data)
        self.assertEquals(ret.status_code, 400)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChange(self):
        data = {
            "when": 2000000, "data_version": 1, "rule_id": 1, "priority": 100, "version": "3.5", "buildTarget": "d",
            "backgroundRate": 100, "mapping": "c", "update_type": "minor", "sc_data_version": 1
        }
        ret = self._post("/scheduled_changes/rules/1", data=data)
        self.assertEquals(ret.status_code, 200, ret.data)

        r = dbo.rules.scheduled_changes.t.select().where(dbo.rules.scheduled_changes.sc_id == 1).execute().fetchall()
        self.assertEquals(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 1, "scheduled_by": "bill", "data_version": 2, "complete": False, "base_rule_id": 1,
            "base_priority": 100, "base_version": "3.5", "base_buildTarget": "d", "base_backgroundRate": 100,
            "base_mapping": "c", "base_update_type": "minor", "base_data_version": 1, "base_alias": None,
            "base_product": None, "base_channel": None, "base_buildID": None, "base_locale": None, "base_osVersion": None,
            "base_distribution": None, "base_fallbackMapping": None, "base_distVersion": None,
            "base_headerArchitecture": None, "base_comment": None, "base_whitelist": None, "base_systemCapabilities": None,
        }
        self.assertEquals(db_data, expected)
        cond = dbo.rules.scheduled_changes.conditions.t.select().where(dbo.rules.scheduled_changes.conditions.sc_id == 1).execute().fetchall()
        self.assertEquals(len(cond), 1)
        cond_expected = {"sc_id": 1, "data_version": 2, "when": 2000000, "telemetry_product": None, "telemetry_channel": None, "telemetry_uptake": None}
        self.assertEquals(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeCantRemoveProductWithoutPermission(self):
        data = {"data_version": 1, "product": None, "sc_data_version": 1}
        ret = self._post("/scheduled_changes/rules/2", username="bob", data=data)
        self.assertEquals(ret.status_code, 403, ret.data)

    def testUpdateRuleWithMergeError(self):
        data = {"mapping": "a", "data_version": 1}
        ret = self._post("/rules/1", data=data)
        self.assertEquals(ret.status_code, 400, ret.data)
        self.assertIn("Is there a scheduled change", ret.data)

    def testDeleteRuleWithScheduledChange(self):
        ret = self._delete("/rules/1", qs=dict(data_version=1))
        self.assertEquals(ret.status_code, 400, ret.data)
        self.assertIn("Cannot delete rows that have", ret.data)

    def testDeleteScheduledChange(self):
        ret = self._delete("/scheduled_changes/rules/1", qs=dict(data_version=1))
        self.assertEquals(ret.status_code, 200, msg=ret.data)

    def testDeleteScheduledChangeWrongDataVersion(self):
        ret = self._delete("/scheduled_changes/rules/1", qs=dict(data_version=5))
        self.assertEquals(ret.status_code, 400, msg=ret.data)
        self.assertIn("Outdated Data Version", ret.data)

    def testDeleteScheduledChangeWithoutPermission(self):
        ret = self._delete("/scheduled_changes/rules/1", username="rex", qs=dict(data_version=1))
        self.assertEquals(ret.status_code, 403, msg=ret.data)

    def testDeleteNonExistentScheduledChange(self):
        ret = self._delete("/scheduled_changes/rules/5", qs=dict(data_version=1))
        self.assertEquals(ret.status_code, 404, msg=ret.data)

    def testEnactScheduledChangeExistingRule(self):
        ret = self._post("/scheduled_changes/rules/1/enact", username="mary")
        self.assertEquals(ret.status_code, 200, ret.data)

        sc_row = dbo.rules.scheduled_changes.t.select().where(dbo.rules.scheduled_changes.sc_id == 1).execute().fetchall()[0]
        self.assertEquals(sc_row["complete"], True)

        row = dbo.rules.t.select().where(dbo.rules.rule_id == 1).execute().fetchall()[0]
        expected = {
            "rule_id": 1, "priority": 100, "version": "3.5", "buildTarget": "d", "backgroundRate": 100, "mapping": "b", "fallbackMapping": None,
            "update_type": "minor", "data_version": 2, "alias": None, "product": None, "channel": None, "buildID": None,
            "locale": None, "osVersion": None, "distribution": None, "distVersion": None, "headerArchitecture": None,
            "comment": None, "whitelist": None, "systemCapabilities": None,
        }
        self.assertEquals(dict(row), expected)

    def testEnactScheduledChangeNewRule(self):
        ret = self._post("/scheduled_changes/rules/2/enact", username="mary")
        self.assertEquals(ret.status_code, 200, ret.data)

        sc_row = dbo.rules.scheduled_changes.t.select().where(dbo.rules.scheduled_changes.sc_id == 2).execute().fetchall()[0]
        self.assertEquals(sc_row["complete"], True)

        row = dbo.rules.t.select().where(dbo.rules.rule_id == 6).execute().fetchall()[0]
        expected = {
            "rule_id": 6, "priority": 50, "version": None, "buildTarget": None, "backgroundRate": 100, "mapping": "ab", "fallbackMapping": None,
            "update_type": "minor", "data_version": 1, "alias": None, "product": "baz", "channel": None, "buildID": None,
            "locale": None, "osVersion": None, "distribution": None, "distVersion": None, "headerArchitecture": None,
            "comment": None, "whitelist": None, "systemCapabilities": None,
        }
        self.assertEquals(dict(row), expected)

    def testEnactScheduledChangeNoPermissions(self):
        ret = self._post("/scheduled_changes/rules/2/enact", username="bob")
        self.assertEquals(ret.status_code, 403, ret.data)

    def testGetScheduledChangeHistoryRevisions(self):
        ret = self._get("/scheduled_changes/rules/3/revisions")
        self.assertEquals(ret.status_code, 200)
        expected = {
            "count": 2,
            "revisions": [
                {
                    "change_id": 3, "changed_by": "bill", "timestamp": 10, "sc_id": 3, "scheduled_by": "bill", "when": 2900000, "sc_data_version": 2,
                    "priority": 150, "backgroundRate": 100, "product": "ff", "mapping": "ghi", "fallbackMapping": None, "update_type": "minor",
                    "complete": False, "telemetry_product": None, "telemetry_channel": None, "telemetry_uptake": None, "rule_id": None,
                    "version": None, "channel": None, "buildTarget": None, "buildID": None, "locale": None,
                    "osVersion": None, "systemCapabilities": None, "distribution": None, "distVersion": None,
                    "headerArchitecture": None, "comment": None, "whitelist": None, "alias": None, "data_version": None,
                },
                {
                    "change_id": 2, "changed_by": "bill", "timestamp": 6, "sc_id": 3, "scheduled_by": "bill", "when": 2000000, "sc_data_version": 1,
                    "priority": 150, "backgroundRate": 100, "product": "ff", "mapping": "def", "fallbackMapping": None, "update_type": "minor",
                    "complete": False, "telemetry_product": None, "telemetry_channel": None, "telemetry_uptake": None, "rule_id": None,
                    "version": None, "channel": None, "buildTarget": None, "buildID": None, "locale": None,
                    "osVersion": None, "systemCapabilities": None, "distribution": None, "distVersion": None,
                    "headerArchitecture": None, "comment": None, "whitelist": None, "alias": None, "data_version": None,
                },
            ],
        }
        self.assertEquals(json.loads(ret.data), expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testRevertScheduledChange(self):
        ret = self._post("/scheduled_changes/rules/3/revisions", data={"change_id": 2})
        self.assertEquals(ret.status_code, 200, ret.data)

        self.assertEquals(dbo.rules.scheduled_changes.history.t.count().execute().first()[0], 9)
        r = dbo.rules.scheduled_changes.t.select().where(dbo.rules.scheduled_changes.sc_id == 3).execute().fetchall()
        self.assertEquals(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 3, "scheduled_by": "bill", "complete": False, "data_version": 3, "base_rule_id": None, "base_priority": 150,
            "base_backgroundRate": 100, "base_product": "ff", "base_mapping": "def", "base_update_type": "minor", "base_version": None,
            "base_buildTarget": None, "base_alias": None, "base_channel": None, "base_buildID": None, "base_locale": None, "base_osVersion": None,
            "base_distribution": None, 'base_fallbackMapping': None, "base_distVersion": None, "base_headerArchitecture": None, "base_comment": None,
            "base_whitelist": None, "base_data_version": None, "base_systemCapabilities": None
        }
        self.assertEquals(db_data, expected)
        self.assertEquals(dbo.rules.scheduled_changes.conditions.history.t.count().execute().first()[0], 9)
        cond = dbo.rules.scheduled_changes.conditions.t.select().where(dbo.rules.scheduled_changes.conditions.sc_id == 3).execute().fetchall()
        self.assertEquals(len(cond), 1)
        cond_expected = {"sc_id": 3, "data_version": 3, "when": 2000000, "telemetry_product": None, "telemetry_channel": None, "telemetry_uptake": None}
        self.assertEquals(dict(cond[0]), cond_expected)

    def testRevertScheduledChangeBadChangeId(self):
        ret = self._post("/scheduled_changes/rules/3/revisions", data={"change_id": 43})
        self.assertEquals(ret.status_code, 400, ret.data)

    def testRevertScheduledChangeChangeIdDoesntMatchScId(self):
        ret = self._post("/scheduled_changes/rules/3/revisions", data={"change_id": 4})
        self.assertEquals(ret.status_code, 400, ret.data)
