from auslib.admin.base import db
from auslib.test.admin.views.base import ViewTest, HTMLTestMixin

class TestRulesAPI_HTML(ViewTest, HTMLTestMixin):
    def testNewRulePost(self):
        ret = self._post('/rules', data=dict(throttle=31, mapping='c', priority=33,
                                                product='Firefox', update_type='minor', channel='nightly'))
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        r = db.rules.t.select().where(db.rules.rule_id==ret.data).execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['mapping'], 'c')
        self.assertEquals(r[0]['throttle'], 31)
        self.assertEquals(r[0]['priority'], 33)
        self.assertEquals(r[0]['data_version'], 1)

    # A POST without the required fields shouldn't be valid
    def testMissingFields(self):
        ret = self._post('/rules', data=dict( ))
        self.assertEquals(ret.status_code, 400, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        self.assertTrue('throttle' in  ret.data, msg=ret.data)
        self.assertTrue('priority' in  ret.data, msg=ret.data)

class TestSingleRuleView_HTML(ViewTest, HTMLTestMixin):
    def testPost(self):
        # Make some changes to a rule
        ret = self._post('/rules/1', data=dict(throttle=71, mapping='d', priority=73, data_version=1,
                                                product='Firefox', update_type='minor', channel='nightly'))
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))

        # Assure the changes made it into the database
        r = db.rules.t.select().where(db.rules.rule_id==1).execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['mapping'], 'd')
        self.assertEquals(r[0]['throttle'], 71)
        self.assertEquals(r[0]['priority'], 73)
        self.assertEquals(r[0]['data_version'], 2)

    def testBadAuthPost(self):
        ret = self._badAuthPost('/rules/1', data=dict(throttle=100, mapping='c', priority=100, data_version=1))
        self.assertEquals(ret.status_code, 401, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        self.assertTrue("not allowed to access" in ret.data, msg=ret.data)

    def testGetSingleRule(self):
        ret = self._get('/rules/1')
        self.assertEquals(ret.status_code, 200)
        self.assertTrue("c" in ret.data, msg=ret.data)


class TestRulesView_HTML(ViewTest, HTMLTestMixin):
    def testGetRules(self):
        ret = self._get('/rules.html')
        self.assertEquals(ret.status_code, 200, msg=ret.data)
        self.assertTrue("<form id='rules_form'" in ret.data, msg=ret.data)
        self.assertTrue('<input id="1-throttle" name="1-throttle" type="text" value="100">' in ret.data, msg=ret.data)
        self.assertTrue('<input id="1-priority" name="1-priority" type="text" value="100">' in ret.data, msg=ret.data)


class TestRuleHistoryView(ViewTest, HTMLTestMixin):
    def testGetNoRevisions(self):
        url = '/rules/1/revisions/'
        ret = self._get(url)
        self.assertEquals(ret.status_code, 200, msg=ret.data)
        self.assertTrue('There were no previous revisions' in ret.data)

    def testGetRevisions(self):
        # Make some changes to a rule
        ret = self._post(
            '/rules/1',
            data=dict(
                throttle=71,
                mapping='d',
                priority=73,
                data_version=1,
                product='Firefox',
                update_type='minor',
                channel='nightly'
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
                throttle=72,
                mapping='d',
                priority=73,
                data_version=2,
                product='Firefux',
                update_type='minor',
                channel='nightly'
            )
        )
        self.assertEquals(
            ret.status_code,
            200,
            "Status Code: %d, Data: %s" % (ret.status_code, ret.data)
        )

        url = '/rules/1/revisions/'
        ret = self._get(url)
        self.assertEquals(ret.status_code, 200, msg=ret.data)
        self.assertTrue('There were no previous revisions' not in ret.data)
        self.assertTrue('Firefox' in ret.data and 'Firefux' in ret.data)
        self.assertTrue('71' in ret.data and '72' in ret.data)

    def testPostRevisionRollback(self):
        # Make some changes to a rule
        ret = self._post(
            '/rules/1',
            data=dict(
                throttle=71,
                mapping='d',
                priority=73,
                data_version=1,
                product='Firefox',
                update_type='minor',
                channel='nightly'
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
                throttle=72,
                mapping='d',
                priority=73,
                data_version=2,
                product='Firefux',
                update_type='minor',
                channel='nightly'
            )
        )
        self.assertEquals(
            ret.status_code,
            200,
            "Status Code: %d, Data: %s" % (ret.status_code, ret.data)
        )

        table = db.rules
        row, = table.select(where=[table.rule_id == 1])
        self.assertEqual(row['throttle'], 72)
        self.assertEqual(row['data_version'], 3)

        query = table.history.t.count()
        count, = query.execute().first()
        self.assertEqual(count, 2)

        # Oh no! We prefer the product=Firefox, throttle=71 one better
        row, = table.history.select(
            where=[table.history.product == 'Firefox',
                   table.history.throttle == 71],
            limit=1
        )
        change_id = row['change_id']
        assert row['rule_id'] == 1  # one of the fixtures

        url = '/rules/1/revisions/'
        ret = self._post(url, {'change_id': change_id})
        self.assertEquals(ret.status_code, 200, ret.data)

        query = table.history.t.count()
        count, = query.execute().first()
        self.assertEqual(count, 3)

        row, = table.select(where=[table.rule_id == 1])
        self.assertEqual(row['throttle'], 71)
        self.assertEqual(row['data_version'], 4)

    def testPostRevisionRollbackBadRequests(self):
        # when posting you need both the rule_id and the change_id
        wrong_url = '/rules/999/revisions/'
        # not found rule_id
        ret = self._post(wrong_url, {'change_id': 10})
        self.assertEquals(ret.status_code, 404)

        url = '/rules/1/revisions/'
        ret = self._post(url, {'change_id': 999})
        # not found change_id
        self.assertEquals(ret.status_code, 404)

        url = '/rules/1/revisions/'
        ret = self._post(url)  # no change_id posted
        self.assertEquals(ret.status_code, 400)

    def testGetRevisionsWithPagination(self):
        # Make some changes to a rule
        for i in range(33):  # some largish number
            ret = self._post(
                '/rules/1',
                data=dict(
                    throttle=1 + i,
                    mapping='d',
                    priority=73,
                    data_version=1 + i,
                    product='Firefox',
                    update_type='minor',
                    channel='nightly'
                )
            )
            self.assertEquals(
                ret.status_code,
                200,
                "Status Code: %d, Data: %s" % (ret.status_code, ret.data)
            )

        url = '/rules/1/revisions/'
        ret = self._get(url)
        self.assertEquals(ret.status_code, 200, msg=ret.data)
        self.assertTrue('There were no previous revisions' not in ret.data)
        self.assertTrue('?page=2' in ret.data)

        ret2 = self._get(url + '?page=2')
        self.assertEquals(ret.status_code, 200, msg=ret.data)
        self.assertTrue(ret.data != ret2.data)
