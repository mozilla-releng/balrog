import json

from auslib.global_state import dbo
from auslib.test.admin.views.base import ViewTest, JSONTestMixin
from auslib.util.comparison import operators


class TestRulesAPI_JSON(ViewTest, JSONTestMixin):
    maxDiff = 1000

    def testGetRules(self):
        ret = self._get("/rules")
        got = json.loads(ret.data)
        self.assertEquals(got["count"], 5)

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
        data = json.dumps(dict(
            backgroundRate=31, mapping="c", priority=33, product="Firefox",
            update_type="minor", channel="nightly"
        ))
        ret = self._post("/rules", data=data, headers={"Content-Type": "application/json"})
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        r = dbo.rules.t.select().where(dbo.rules.rule_id == ret.data).execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['mapping'], 'c')
        self.assertEquals(r[0]['backgroundRate'], 31)
        self.assertEquals(r[0]['priority'], 33)
        self.assertEquals(r[0]['data_version'], 1)

    def testNewRuleWithoutPermission(self):
        data = json.dumps(dict(
            backgroundRate=31, mapping="c", priority=33, product="Firefox",
            update_type="minor", channel="nightly"
        ))
        ret = self._post("/rules", data=data, headers={"Content-Type": "application/json"}, username="jack")
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


class TestSingleRuleView_JSON(ViewTest, JSONTestMixin):

    def testGetRule(self):
        ret = self._get("/rules/1")
        expected = dict(
            backgroundRate=100,
            mapping="c",
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
        ret = self._post('/rules/1', data=dict(backgroundRate=71, mapping='d', priority=73, data_version=1,
                                               product='Firefox', channel='nightly', systemCapabilities="SSE"))
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        load = json.loads(ret.data)
        self.assertEquals(load['new_data_version'], 2)

        # Assure the changes made it into the database
        r = dbo.rules.t.select().where(dbo.rules.rule_id == 1).execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['mapping'], 'd')
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
        data = json.dumps(dict(
            backgroundRate=71, mapping="d", priority=73, data_version=1,
            product="Firefox", channel="nightly"
        ))
        ret = self._post("/rules/1", data=data, headers={"Content-Type": "application/json"})
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

    def testDeleteWithoutPermission(self):
        ret = self._delete("/rules/2", username="tony", qs=dict(data_version=1))
        self.assertEquals(ret.status_code, 403)


class TestRuleHistoryView(ViewTest, JSONTestMixin):

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
        ret = self._post(url, json.dumps({'change_id': change_id}), content_type="application/json")
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
        ret = self._post(url, json.dumps({'change_id': change_id}), content_type="application/json", username='bob')
        self.assertEquals(ret.status_code, 403)

    def testPostRevisionRollbackBadRequests(self):
        # when posting you need both the rule_id and the change_id
        wrong_url = '/rules/999/revisions'
        # not found rule_id
        ret = self._post(wrong_url, json.dumps({'change_id': 10}), content_type="application/json")
        self.assertEquals(ret.status_code, 404)

        url = '/rules/1/revisions'
        ret = self._post(url, json.dumps({'change_id': 999}), content_type="application/json")
        # not found change_id
        self.assertEquals(ret.status_code, 404)

        url = '/rules/1/revisions'
        ret = self._post(url)  # no change_id posted
        self.assertEquals(ret.status_code, 400)


class TestSingleColumn_JSON(ViewTest, JSONTestMixin):

    def testGetRules(self):
        expected_product = ["fake"]
        expected = dict(count=1, product=expected_product)
        ret = self._get("/rules/columns/product")
        self.assertEquals(json.loads(ret.data), expected)

    def testGetRuleColumn404(self):
        ret = self.client.get("/rules/columns/blah")
        self.assertEquals(ret.status_code, 404)
