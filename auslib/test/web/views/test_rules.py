import simplejson as json

from auslib.web.base import db
from auslib.test.web.views.base import ViewTest, JSONTestMixin, HTMLTestMixin

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
        self.assertTrue('<input id="1-throttle" name="1-throttle" type="text" value="100" />' in ret.data, msg=ret.data)
        self.assertTrue('<input id="1-priority" name="1-priority" type="text" value="100" />' in ret.data, msg=ret.data)

