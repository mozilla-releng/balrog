from datetime import datetime
import simplejson as json
import unittest

from sqlalchemy import create_engine, MetaData, Table, Column, Integer
from sqlalchemy.engine.reflection import Inspector

from auslib.db import AUSDatabase, AUSTable, AlreadySetupError, PermissionDeniedError

class TestAUSTable(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.metadata = MetaData(self.engine)
        class TestTable(AUSTable):
            def __init__(self, metadata):
                self.table = Table('test', metadata, Column('id', Integer),
                                                     Column('foo', Integer))
                AUSTable.__init__(self)
        self.test = TestTable(self.metadata)
        self.metadata.create_all()
        self.test.t.insert().execute(id=1, foo=33)
        self.test.t.insert().execute(id=2, foo=22)
        self.test.t.insert().execute(id=3, foo=11)

    def testHasHistoryTable(self):
        self.assertIsNotNone(getattr(self.test, 'history', None))

    def testHistoryTableHasAllColumns(self):
        columns = [c.name for c in self.test.history.t.get_children()]
        self.assertIn('id', columns)
        self.assertIn('foo', columns)
        self.assertIn('changed_by', columns)
        self.assertIn('timestamp', columns)

    def testHistoryUponInsert(self):
        self.test.insert(changed_by='george', id=4, foo=0)
        ret = self.test.history.t.select().execute().fetchone()
        # XXX: How do we make make timestamps knowable ahead of time?
        ret = list(ret)
        ret[2] = None
        self.assertEquals(ret, [1, 'george', None, None, None])

    def testHistoryUponDelete(self):
        self.test.delete(changed_by='bobby', where=[self.test.id==1])
        ret = list(self.test.history.t.select().execute().fetchone())
        ret[2] = None
        self.assertEquals(ret, [1, 'bobby', None, 1, 33])

    def testHistoryUponUpdate(self):
        self.test.update(changed_by='heather', where=[self.test.id==2], what=dict(foo=99))
        ret = list(self.test.history.t.select().execute().fetchone())
        ret[2] = None
        self.assertEquals(ret, [1, 'heather', None, 2, 22])

    def testColumnMirroring(self):
        self.assertIn(self.test.id, self.test.table.get_children())
        self.assertIn(self.test.foo, self.test.table.get_children())

    def testSelect(self):
        expected = [dict(id=1, foo=33), dict(id=2, foo=22), dict(id=3, foo=11)]
        self.assertEquals(self.test.select(), expected)

    def testSelectWithColumns(self):
        expected = [dict(id=1), dict(id=2), dict(id=3)]
        self.assertEquals(self.test.select(columns=[self.test.id]), expected)

    def testSelectWithWhere(self):
        expected = [dict(id=2, foo=22), dict(id=3, foo=11)]
        self.assertEquals(self.test.select(where=[self.test.id >= 2]), expected)

    def testSelectWithOrder(self):
        expected = [dict(id=3, foo=11), dict(id=2, foo=22), dict(id=1, foo=33)]
        self.assertEquals(self.test.select(order_by=[self.test.foo]), expected)

    def testSelectWithLimit(self):
        self.assertEquals(self.test.select(limit=1), [dict(id=1, foo=33)])

    def testSelectCanModifyResult(self):
        ret = self.test.select()[0]
        # If we can't write to this, an Exception will be raised and the test will fail
        ret['foo'] = 3245

    def testInsert(self):
        self.test.insert(changed_by='bob', id=4, foo=0)
        self.assertEquals(len(self.test.t.select().execute().fetchall()), 4)

    def testDelete(self):
        ret = self.test.delete(changed_by='bill', where=[self.test.id==1, self.test.foo==33])
        self.assertEquals(ret.rowcount, 1)
        self.assertEquals(len(self.test.t.select().execute().fetchall()), 2)

    def testUpdate(self):
        ret = self.test.update(changed_by='bob', where=[self.test.id==1], what=dict(foo=123))
        self.assertEquals(ret.rowcount, 1)
        self.assertEquals(self.test.t.select(self.test.id==1).execute().fetchall()[0], (1, 123))

class TestUpdatePaths(object):
    def _stripNullColumns(self, rules):
        # We know a bunch of columns are going to be empty...easier to strip them out
        # than to be super verbose (also should let this test continue to work even
        # if the schema changes).
        for rule in rules:
            for key in rule.keys():
                if rule[key] == None:
                    del rule[key]
        return rules

class TestUpdatePathsSimple(unittest.TestCase, TestUpdatePaths):
    def setUp(self):
        self.db = AUSDatabase('sqlite:///:memory:')
        self.paths = self.db.updatePaths
        self.paths.t.insert().execute(id=1, priority=100, version='3.5', buildTarget='d', throttle=100, mapping='c')
        self.paths.t.insert().execute(id=2, priority=100, version='3.3', buildTarget='d', throttle=100, mapping='b')
        self.paths.t.insert().execute(id=3, priority=100, version='3.5', buildTarget='a', throttle=100, mapping='a')
        self.paths.t.insert().execute(id=4, priority=80, buildTarget='d', throttle=100, mapping='a')
        self.paths.t.insert().execute(id=5, priority=80, buildTarget='d', version='3.3', throttle=0, mapping='c')

    def testGetOrderedRules(self):
        rules = self._stripNullColumns(self.paths.getOrderedRules())
        expected = [
            dict(rule_id=4, priority=80, throttle=100, buildTarget='d', mapping='a'),
            dict(rule_id=5, priority=80, throttle=0, version='3.3', buildTarget='d', mapping='c'),
            dict(rule_id=2, priority=100, throttle=100, version='3.3', buildTarget='d', mapping='b'),
            dict(rule_id=3, priority=100, throttle=100, version='3.5', buildTarget='a', mapping='a'),
            dict(rule_id=1, priority=100, throttle=100, version='3.5', buildTarget='d', mapping='c'),
        ]
        self.assertEquals(rules, expected)

    def testGetRulesMatchingQuery(self):
        rules = self.paths.getRulesMatchingQuery(
            name='', product='', version='3.5', channel='', fallbackChannel='',
            buildTarget='a', buildID='', locale='', osVersion='',
            distribution='', distVersion='', headerArchitecture=''
        )
        rules = self._stripNullColumns(rules)
        expected = [dict(rule_id=3, priority=100, throttle=100, version='3.5', buildTarget='a', mapping='a')]
        self.assertEquals(rules, expected)

    def testGetRulesMatchingQueryWithNullColumn(self):
        rules = self.paths.getRulesMatchingQuery(
            name='', product='', version='3.5', channel='', fallbackChannel='',
            buildTarget='d', buildID='', locale='', osVersion='',
            distribution='', distVersion='', headerArchitecture=''
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(rule_id=1, priority=100, throttle=100, version='3.5', buildTarget='d', mapping='c'),
            dict(rule_id=4, priority=80, throttle=100, buildTarget='d', mapping='a'),
        ]
        self.assertEquals(rules, expected)

    def testGetRulesMatchingQueryDontReturnThrottled(self):
        rules = self.paths.getRulesMatchingQuery(
            name='', product='', version='3.3', channel='', fallbackChannel='',
            buildTarget='d', buildID='', locale='', osVersion='',
            distribution='', distVersion='', headerArchitecture=''
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(rule_id=2, priority=100, throttle=100, version='3.3', buildTarget='d', mapping='b'),
            dict(rule_id=4, priority=80, throttle=100, buildTarget='d', mapping='a'),
        ]
        self.assertEquals(rules, expected)

class TestUpdatePathsSpecial(unittest.TestCase, TestUpdatePaths):
    def setUp(self):
        self.db = AUSDatabase('sqlite:///:memory:')
        self.paths = self.db.updatePaths
        self.paths.t.insert().execute(id=1, priority=100, version='4.0*', throttle=100)
        self.paths.t.insert().execute(id=2, priority=100, channel='release*', throttle=100)

    def testGetRulesMatchingQueryVersionGlobbing(self):
        expected = [dict(rule_id=1, priority=100, throttle=100, version='4.0*')]
        rules = self.paths.getRulesMatchingQuery(
            name='', product='', version='4.0', channel='', fallbackChannel='',
            buildTarget='', buildID='', locale='', osVersion='',
            distribution='', distVersion='', headerArchitecture=''
        )
        rules = self._stripNullColumns(rules)
        self.assertEquals(rules, expected)
        rules = self.paths.getRulesMatchingQuery(
            name='', product='', version='4.0b2', channel='', fallbackChannel='',
            buildTarget='', buildID='', locale='', osVersion='',
            distribution='', distVersion='', headerArchitecture=''
        )
        rules = self._stripNullColumns(rules)
        self.assertEquals(rules, expected)
        rules = self.paths.getRulesMatchingQuery(
            name='', product='', version='4.0.1', channel='', fallbackChannel='',
            buildTarget='', buildID='', locale='', osVersion='',
            distribution='', distVersion='', headerArchitecture=''
        )
        rules = self._stripNullColumns(rules)
        self.assertEquals(rules, expected)

    def testGetRulesMatchingQueryChannelGlobbing(self):
        expected = [dict(rule_id=2, priority=100, throttle=100, channel='release*')]
        rules = self.paths.getRulesMatchingQuery(
            name='', product='', version='', channel='releasetest', fallbackChannel='releasetest',
            buildTarget='', buildID='', locale='', osVersion='', distribution='',
            distVersion='', headerArchitecture=''
        )
        rules = self._stripNullColumns(rules)
        self.assertEquals(rules, expected)
        rules = self.paths.getRulesMatchingQuery(
            name='', product='', version='', channel='releasetest-cck-blah',
            fallbackChannel='releasetest', buildTarget='', buildID='',
            locale='', osVersion='', distribution='', distVersion='',
            headerArchitecture=''
        )
        rules = self._stripNullColumns(rules)
        self.assertEquals(rules, expected)

class TestReleases(unittest.TestCase):
    def setUp(self):
        self.db = AUSDatabase('sqlite:///:memory:')
        self.releases = self.db.releases
        self.releases.t.insert().execute(name='a', product='a', version='a', data=json.dumps(dict(one=1)))
        self.releases.t.insert().execute(name='ab', product='a', version='a', data=json.dumps(dict(one=1)))
        self.releases.t.insert().execute(name='b', product='b', version='b', data=json.dumps(dict(two=2)))
        self.releases.t.insert().execute(name='c', product='c', version='c', data=json.dumps(dict(three=3)))

    def testGetReleases(self):
        self.assertEquals(len(self.releases.getReleases()), 4)

    def testGetReleasesWithLimit(self):
        self.assertEquals(len(self.releases.getReleases(limit=1)), 1)

    def testGetReleasesWithWhere(self):
        expected = [dict(product='b', version='b', name='b', data=dict(two=2))]
        self.assertEquals(self.releases.getReleases(name='b'), expected)

class TestPermissions(unittest.TestCase):
    def setUp(self):
        self.db = AUSDatabase('sqlite:///:memory:')
        self.permissions = self.db.permissions
        self.permissions.t.insert().execute(permission='admin', username='bill')
        self.permissions.t.insert().execute(permission='editusers', username='bob')
        self.permissions.t.insert().execute(permission='editproduct', username='bob', options='fake')

    def testGrantPermissions(self):
        query = self.permissions.t.select().where(self.permissions.username=='cathy')
        self.assertEquals(len(query.execute().fetchall()), 0)
        self.permissions.grantPermission('bob', 'cathy', '/releases')
        self.assertEquals(query.execute().fetchall(), [('/releases', 'cathy', None)])

    def testGrantPermissionsWithOptions(self):
        self.permissions.grantPermission('bob', 'cathy', 'editproduct', 'SeaMonkey')
        query = self.permissions.t.select().where(self.permissions.username=='cathy')
        self.assertEquals(query.execute().fetchall(), [('editproduct', 'cathy', 'SeaMonkey')])

    def testGrantPermissionsNotAllowed(self):
        self.assertRaises(PermissionDeniedError, self.permissions.grantPermission,
            'cathy', 'bob', '/abc'
        )

    def testRevokePermission(self):
        self.permissions.revokePermission(changed_by='bill', username='bob', permission='editproduct', options='fake')
        query = self.permissions.t.select().where(self.permissions.username=='cathy')
        query = query.where(self.permissions.permission=='editproduct')
        query = query.where(self.permissions.options=='fake')
        self.assertEquals(len(query.execute().fetchall()), 0)

    def testCanEditUsers(self):
        self.assertTrue(self.permissions.canEditUsers('bill'))
        self.assertTrue(self.permissions.canEditUsers('bob'))

    def testCanEditUsersFalse(self):
        self.assertFalse(self.permissions.canEditUsers('cathy'))

    def testGetAllUsers(self):
        self.assertEquals(self.permissions.getAllUsers(), ['bill', 'bob'])

    def testGetUserPermissions(self):
        expected = [dict(permission='editusers', options=None),
                    dict(permission='editproduct', options='fake')]
        self.assertEquals(self.permissions.getUserPermissions('bob'), expected)

    def testGetPermission(self):
        expected = dict(options='fake')
        self.assertEquals(self.permissions.getPermission('bob', 'editproduct'), expected)

class TestDB(unittest.TestCase):
    def testSetDburi(self):
        db = AUSDatabase()
        db.setDburi('sqlite:///:memory:')
        insp = Inspector.from_engine(db.engine)
        self.assertIsNot(insp.get_table_names(), [])

    def testSetDburiAlreadySetup(self):
        db = AUSDatabase('sqlite:///:memory:')
        self.assertRaises(AlreadySetupError, db.setDburi, 'sqlite:///:memory:')

    def testReset(self):
        db = AUSDatabase('sqlite:///:memory:')
        db.reset()
        # If we can set the dburi again, reset worked!
        db.setDburi('sqlite:///:memory:')
        insp = Inspector.from_engine(db.engine)
        self.assertIsNot(insp.get_table_names(), [])
