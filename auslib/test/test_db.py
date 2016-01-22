import logging
import mock
import os
import simplejson as json
import sys
from tempfile import mkstemp
import unittest

from jsonschema import ValidationError

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, select
from sqlalchemy.engine.reflection import Inspector

import migrate.versioning.api

from auslib.global_state import cache
from auslib.db import AUSDatabase, AUSTable, AlreadySetupError, \
    AUSTransaction, TransactionError, OutdatedDataError
from auslib.blobs.apprelease import ReleaseBlobV1


class MemoryDatabaseMixin(object):
    """Use this when writing tests that don't require multiple connections to
       the database."""

    def setUp(self):
        self.dburi = 'sqlite:///:memory:'


class NamedFileDatabaseMixin(object):
    """Use this when writing tests that *do* require multiple connections to
       the database. SQLite memory database don't support multiple connections
       to the same database. When you try to use them, you get weird behaviour
       like the second "connection" seeing the state of an in-progress
       transaction in the first. See the following links for more detail:
        http://www.sqlalchemy.org/docs/dialects/sqlite.html#threading-pooling-behavior
        http://www.sqlalchemy.org/trac/wiki/FAQ#IamusingmultipleconnectionswithaSQLitedatabasetypicallytotesttransactionoperationandmytestprogramisnotworking
       """

    def setUp(self):
        self.tmpfiles = []
        self.dburi = 'sqlite:///%s' % self.getTempfile()

    def tearDown(self):
        for fd, t in self.tmpfiles:
            os.close(fd)
            os.remove(t)

    def getTempfile(self):
        fd, t = mkstemp()
        self.tmpfiles.append((fd, t))
        return t


class TestAUSTransaction(unittest.TestCase, MemoryDatabaseMixin):

    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.engine = create_engine(self.dburi)
        self.metadata = MetaData(self.engine)
        self.table = Table('test', self.metadata, Column('id', Integer, primary_key=True),
                           Column('foo', Integer))
        self.metadata.create_all()
        self.table.insert().execute(id=1, foo=33)
        self.table.insert().execute(id=2, foo=22)
        self.table.insert().execute(id=3, foo=11)

    def testTransaction(self):
        trans = AUSTransaction(self.metadata.bind.connect())
        trans.execute(self.table.insert(values=dict(id=4, foo=55)))
        trans.execute(self.table.update(values=dict(foo=66)).where(self.table.c.id == 1))
        trans.commit()
        ret = self.table.select().execute().fetchall()
        self.assertEquals(ret, [(1, 66), (2, 22), (3, 11), (4, 55)])

    def testTransactionRaisesOnError(self):
        trans = AUSTransaction(self.metadata.bind.connect())
        self.assertRaises(TransactionError, trans.execute, "UPDATE test SET foo=123 WHERE fake=1")

    def testRollback(self):
        trans = AUSTransaction(self.metadata.bind.connect())
        trans.execute(self.table.update(values=dict(foo=66)).where(self.table.c.id == 1))
        trans.rollback()
        ret = self.table.select().execute().fetchall()
        self.assertEquals(ret, [(1, 33), (2, 22), (3, 11)])

    # bug 740360
    def testContextManagerClosesConnection(self):
        with AUSTransaction(self.metadata.bind.connect()) as trans:
            self.assertEqual(trans.conn.closed, False, "Connection closed at start of transaction, expected it to be open.")
            trans.execute(self.table.insert(values=dict(id=5, foo=41)))
        self.assertEqual(trans.conn.closed, True, "Connection not closed after __exit__ is called")


class TestAUSTransactionRequiresRealFile(unittest.TestCase, NamedFileDatabaseMixin):

    def setUp(self):
        NamedFileDatabaseMixin.setUp(self)
        self.engine = create_engine(self.dburi)
        self.metadata = MetaData(self.engine)
        self.table = Table('test', self.metadata, Column('id', Integer, primary_key=True),
                           Column('foo', Integer))
        self.metadata.create_all()
        self.table.insert().execute(id=1, foo=33)
        self.table.insert().execute(id=2, foo=22)
        self.table.insert().execute(id=3, foo=11)

    def testTransactionNotChangedUntilCommit(self):
        trans = AUSTransaction(self.metadata.bind.connect())
        trans.execute(self.table.update(values=dict(foo=66)).where(self.table.c.id == 1))
        # This select() runs in a different connection, so no changes should
        # be visible to it yet
        ret = self.table.select().execute().fetchall()
        self.assertEquals(ret, [(1, 33), (2, 22), (3, 11)])
        trans.commit()
        ret = self.table.select().execute().fetchall()
        self.assertEquals(ret, [(1, 66), (2, 22), (3, 11)])


class TestTableMixin(object):

    def setUp(self):
        self.engine = create_engine(self.dburi)
        self.metadata = MetaData(self.engine)

        class TestTable(AUSTable):

            def __init__(self, metadata):
                self.table = Table('test', metadata, Column('id', Integer, primary_key=True, autoincrement=True),
                                   Column('foo', Integer))
                AUSTable.__init__(self, 'sqlite')

        class TestAutoincrementTable(AUSTable):

            def __init__(self, metadata):
                self.table = Table('test-autoincrement', metadata,
                                   Column('id', Integer, primary_key=True, autoincrement=True),
                                   Column('foo', Integer))
                AUSTable.__init__(self, 'sqlite')
        self.test = TestTable(self.metadata)
        self.testAutoincrement = TestAutoincrementTable(self.metadata)
        self.metadata.create_all()
        self.test.t.insert().execute(id=1, foo=33, data_version=1)
        self.test.t.insert().execute(id=2, foo=22, data_version=1)
        self.test.t.insert().execute(id=3, foo=11, data_version=2)


class TestMultiplePrimaryTableMixin(object):

    def setUp(self):
        self.engine = create_engine(self.dburi)
        self.metadata = MetaData(self.engine)

        class TestTable(AUSTable):

            def __init__(self, metadata):
                self.table = Table('test', metadata, Column('id1', Integer, primary_key=True),
                                   Column('id2', Integer, primary_key=True),
                                   Column('foo', Integer))
                AUSTable.__init__(self, 'sqlite')
        self.test = TestTable(self.metadata)
        self.metadata.create_all()
        self.test.t.insert().execute(id1=1, id2=1, foo=33, data_version=1)
        self.test.t.insert().execute(id1=1, id2=2, foo=22, data_version=1)
        self.test.t.insert().execute(id1=2, id2=1, foo=11, data_version=1)
        self.test.t.insert().execute(id1=2, id2=2, foo=44, data_version=1)


class TestAUSTable(unittest.TestCase, TestTableMixin, MemoryDatabaseMixin):

    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        TestTableMixin.setUp(self)

    def testColumnMirroring(self):
        self.assertTrue(self.test.id in self.test.table.get_children())
        self.assertTrue(self.test.foo in self.test.table.get_children())

    def testSelect(self):
        expected = [dict(id=1, foo=33, data_version=1),
                    dict(id=2, foo=22, data_version=1),
                    dict(id=3, foo=11, data_version=2)]
        self.assertEquals(self.test.select(), expected)

    def testSelectWithColumns(self):
        expected = [dict(id=1), dict(id=2), dict(id=3)]
        self.assertEquals(self.test.select(columns=[self.test.id]), expected)

    def testSelectWithWhere(self):
        expected = [dict(id=2, foo=22, data_version=1),
                    dict(id=3, foo=11, data_version=2)]
        self.assertEquals(self.test.select(where=[self.test.id >= 2]), expected)

    def testSelectWithOrder(self):
        expected = [dict(id=3, foo=11, data_version=2),
                    dict(id=2, foo=22, data_version=1),
                    dict(id=1, foo=33, data_version=1)]
        self.assertEquals(self.test.select(order_by=[self.test.foo]), expected)

    def testSelectWithLimit(self):
        self.assertEquals(self.test.select(limit=1), [dict(id=1, foo=33, data_version=1)])

    def testSelectCanModifyResult(self):
        ret = self.test.select()[0]
        # If we can't write to this, an Exception will be raised and the test will fail
        ret['foo'] = 3245

    def testInsert(self):
        self.test.insert(changed_by='bob', id=4, foo=0)
        ret = self.test.t.select().execute().fetchall()
        self.assertEquals(len(ret), 4)
        self.assertEquals(ret[-1], (4, 0, 1))

    def testInsertClosesConnectionOnImplicitTransaction(self):
        with mock.patch('sqlalchemy.engine.base.Connection.close') as close:
            self.test.insert(changed_by='bob', id=5, foo=1)
            self.assertTrue(close.called, "Connection.close() never called by insert()")

    def testInsertClosesConnectionOnImplicitTransactionWithError(self):
        with mock.patch('sqlalchemy.engine.base.Connection.close') as close:
            try:
                self.test.insert(changed_by='bob', id=1, foo=1)
            except:
                pass
            self.assertTrue(close.called, "Connection.close() never called by insert()")

    def testInsertWithChangeCallback(self):
        shared = []
        self.test.onInsert = lambda *x: shared.extend(x)
        what = {'id': 4, 'foo': 1}
        self.test.insert(changed_by='bob', **what)
        self.assertEquals(shared, [self.test, 'bob', what])

    def testDelete(self):
        ret = self.test.delete(changed_by='bill', where=[self.test.id == 1, self.test.foo == 33],
                               old_data_version=1)
        self.assertEquals(ret.rowcount, 1)
        self.assertEquals(len(self.test.t.select().execute().fetchall()), 2)

    def testDeleteFailsOnVersionMismatch(self):
        self.assertRaises(OutdatedDataError, self.test.delete, changed_by='bill',
                          where=[self.test.id == 3], old_data_version=1)

    def testDeleteClosesConnectionOnImplicitTransaction(self):
        with mock.patch('sqlalchemy.engine.base.Connection.close') as close:
            self.test.delete(changed_by='bill', where=[self.test.id == 1], old_data_version=1)
            self.assertTrue(close.called, "Connection.close() never called by delete()")

    def testDeleteWithChangeCallback(self):
        shared = []
        self.test.onDelete = lambda *x: shared.extend(x)
        where = [self.test.id == 1]
        self.test.delete(changed_by='bob', where=where, old_data_version=1)
        self.assertEquals(shared, [self.test, 'bob', where])

    def testUpdate(self):
        ret = self.test.update(changed_by='bob', where=[self.test.id == 1], what=dict(foo=123),
                               old_data_version=1)
        self.assertEquals(ret.rowcount, 1)
        self.assertEquals(self.test.t.select(self.test.id == 1).execute().fetchone(), (1, 123, 2))

    def testUpdateFailsOnVersionMismatch(self):
        self.assertRaises(OutdatedDataError, self.test.update, changed_by='bill',
                          where=[self.test.id == 3], what=dict(foo=99), old_data_version=1)

    def testUpdateClosesConnectionOnImplicitTransaction(self):
        with mock.patch('sqlalchemy.engine.base.Connection.close') as close:
            self.test.update(changed_by='bob', where=[self.test.id == 1], what=dict(foo=432), old_data_version=1)
            self.assertTrue(close.called, "Connection.close() never called by update()")

    def testUpdateWithChangeCallback(self):
        shared = []
        self.test.onUpdate = lambda *x: shared.extend(x)
        where = [self.test.id == 1]
        what = dict(foo=123)
        self.test.update(changed_by='bob', where=where, what=what, old_data_version=1)
        self.assertEquals(shared, [self.test, 'bob', what, where])


class TestAUSTableRequiresRealFile(unittest.TestCase, TestTableMixin, NamedFileDatabaseMixin):

    def setUp(self):
        NamedFileDatabaseMixin.setUp(self)
        TestTableMixin.setUp(self)

    def testDeleteWithTransaction(self):
        trans = AUSTransaction(self.metadata.bind.connect())
        self.test.delete(changed_by='bill', transaction=trans, where=[self.test.id == 2], old_data_version=1)
        ret = self.test.t.select().execute().fetchall()
        self.assertEquals(len(ret), 3)
        trans.commit()
        ret = self.test.t.select().execute().fetchall()
        self.assertEquals(len(ret), 2)

    def testInsertWithTransaction(self):
        trans = AUSTransaction(self.metadata.bind.connect())
        self.test.insert(changed_by='bob', transaction=trans, id=5, foo=1)
        ret = self.test.t.select().execute().fetchall()
        self.assertEquals(len(ret), 3)
        trans.commit()
        ret = self.test.t.select().execute().fetchall()
        self.assertEquals(ret[-1], (5, 1, 1))

    def testUpdateWithTransaction(self):
        trans = AUSTransaction(self.metadata.bind.connect())
        self.test.update(changed_by='bill', transaction=trans, where=[self.test.id == 1], what=dict(foo=222),
                         old_data_version=1)
        ret = self.test.t.select(self.test.id == 1).execute().fetchone()
        self.assertEquals(ret, (1, 33, 1))
        trans.commit()
        ret = self.test.t.select(self.test.id == 1).execute().fetchone()
        self.assertEquals(ret, (1, 222, 2))

# TODO: Find some way of testing this with SQLite, or testing it with some other backend.
# Because it's impossible to have multiple simultaneous transaction with sqlite, you
# can't test the behaviour of concurrent transactions with it.
#    def testUpdateCollidingUpdateFails(self):
#        trans1 = AUSTransaction(self.test.getEngine().connect())
#        trans2 = AUSTransaction(self.test.getEngine().connect())
#        ret1 = self.test._prepareUpdate(trans1, where=[self.test.id==3], what=dict(foo=99), changed_by='bob')
#        ret2 = self.test._prepareUpdate(trans2, where=[self.test.id==3], what=dict(foo=66), changed_by='bob')
#        trans1.commit()
#        self.assertEquals(ret1.rowcount, 1)
#        self.assertEquals(self.test.t.select(self.test.id==3).execute().fetchone(), (1, 99, 2))
#        self.assertRaises(TransactionError, trans2.commit)


class TestHistoryTable(unittest.TestCase, TestTableMixin, MemoryDatabaseMixin):

    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        TestTableMixin.setUp(self)

    def testHasHistoryTable(self):
        self.assertTrue(self.test.history)

    def testHistoryTableHasAllColumns(self):
        columns = [c.name for c in self.test.history.t.get_children()]
        self.assertTrue('change_id' in columns)
        self.assertTrue('id' in columns)
        self.assertTrue('foo' in columns)
        self.assertTrue('changed_by' in columns)
        self.assertTrue('timestamp' in columns)

    def testHistoryUponInsert(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0
            self.test.insert(changed_by='george', id=4, foo=0)
            ret = self.test.history.t.select().execute().fetchall()
            self.assertEquals(ret, [(1, 'george', 999, 4, None, None),
                                    (2, 'george', 1000, 4, 0, 1)])

    def testHistoryUponAutoincrementInsert(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0
            self.test.insert(changed_by='george', foo=0)
            ret = self.test.history.t.select().execute().fetchall()
            self.assertEquals(ret, [(1, 'george', 999, 4, None, None),
                                    (2, 'george', 1000, 4, 0, 1)])

    def testHistoryUponDelete(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0
            self.test.delete(changed_by='bobby', where=[self.test.id == 1],
                             old_data_version=1)
            ret = self.test.history.t.select().execute().fetchone()
            self.assertEquals(ret, (1, 'bobby', 1000, 1, None, None))

    def testHistoryUponUpdate(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0
            self.test.update(changed_by='heather', where=[self.test.id == 2], what=dict(foo=99),
                             old_data_version=1)
            ret = self.test.history.t.select().execute().fetchone()
            self.assertEquals(ret, (1, 'heather', 1000, 2, 99, 2))

    def testHistoryTimestampMaintainsPrecision(self):
        with mock.patch('time.time') as t:
            t.return_value = 1234567890.123456
            self.test.insert(changed_by='bob', id=4)
            ret = select([self.test.history.timestamp]).where(self.test.history.id == 4).execute().fetchone()[0]
            # Insert decrements the timestamp
            self.assertEquals(ret, 1234567890122)

    def testHistoryUpdateRollback(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0

            # Update one of the rows
            self.test.t.update(values=dict(foo=99, data_version=2)).where(self.test.id == 2).execute()
            self.test.history.t.insert(values=dict(changed_by='heather', change_id=1, timestamp=1000, id=2, data_version=2, foo=99)).execute()

            # Update it again (this is the update we will rollback)
            self.test.t.update(values=dict(foo=100, data_version=3)).where(self.test.id == 2).execute()
            self.test.history.t.insert(values=dict(changed_by='heather', change_id=2, timestamp=1000, id=2, data_version=3, foo=100)).execute()

            # Rollback the second update
            self.test.history.rollbackChange(2, 'heather')

            ret = self.test.history.t.select().execute().fetchall()
            self.assertEquals(ret[-1], (3, 'heather', 1000, 2, 99, 4))

            ret = self.test.t.select().where(self.test.id == 2).execute().fetchall()
            self.assertEquals(ret, [(2, 99, 4)])

    def testHistoryInsertRollback(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0

            ret = self.test.t.select().execute().fetchall()

            # Insert the item
            self.test.t.insert(values=dict(foo=271, data_version=1, id=4)).execute()
            self.test.history.t.insert(values=dict(changed_by='george', change_id=1, timestamp=999, id=4, data_version=None, foo=None)).execute()
            self.test.history.t.insert(values=dict(changed_by='george', change_id=2, timestamp=1000, id=4, data_version=1, foo=271)).execute()

            # Rollback the 'insert'
            self.test.history.rollbackChange(2, 'george')

            ret = self.test.history.t.select().execute().fetchall()
            self.assertEquals(ret[-1], (3, 'george', 1000, 4, None, None))

            ret = self.test.t.select().execute().fetchall()
            self.assertEquals(len(ret), 3, msg=ret)

    def testHistoryDeleteRollback(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0

            ret = self.test.t.select().execute().fetchall()

            # Insert the thing we are going to delete
            self.test.t.insert(values=dict(foo=271, data_version=1, id=4)).execute()
            self.test.history.t.insert(values=dict(changed_by='george', change_id=1, timestamp=999, id=4, data_version=None, foo=None)).execute()
            self.test.history.t.insert(values=dict(changed_by='george', change_id=2, timestamp=1000, id=4, data_version=1, foo=271)).execute()

            # Delete it
            self.test.t.delete().where(self.test.id == 4).execute()
            self.test.history.t.insert(values=dict(changed_by='bobby', change_id=3, timestamp=1000, id=4, data_version=None, foo=None)).execute()

            # Rollback the 'delete'
            self.test.history.rollbackChange(3, 'george')

            ret = self.test.history.t.select().execute().fetchall()
            self.assertEquals(ret[-1], (5, 'george', 1000, 4, 271, 1))

            ret = self.test.t.select().execute().fetchall()
            self.assertEquals(len(ret), 4, msg=ret)


class TestMultiplePrimaryHistoryTable(unittest.TestCase, TestMultiplePrimaryTableMixin, MemoryDatabaseMixin):

    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        TestMultiplePrimaryTableMixin.setUp(self)

    def testHasHistoryTable(self):
        self.assertTrue(self.test.history)

    def testMultiplePrimaryHistoryTableHasAllColumns(self):
        columns = [c.name for c in self.test.history.t.get_children()]
        self.assertTrue('change_id' in columns)
        self.assertTrue('id1' in columns)
        self.assertTrue('id2' in columns)
        self.assertTrue('foo' in columns)
        self.assertTrue('changed_by' in columns)
        self.assertTrue('timestamp' in columns)

    def testMultiplePrimaryHistoryUponInsert(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0
            self.test.insert(changed_by='george', id1=4, id2=5, foo=0)
            ret = self.test.history.t.select().execute().fetchall()
            self.assertEquals(ret, [(1, 'george', 999, 4, 5, None, None),
                                    (2, 'george', 1000, 4, 5, 0, 1)])

    def testMultiplePrimaryHistoryUponDelete(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0
            self.test.delete(changed_by='bobby', where=[self.test.id1 == 1, self.test.id2 == 2],
                             old_data_version=1)
            ret = self.test.history.t.select().execute().fetchone()
            self.assertEquals(ret, (1, 'bobby', 1000, 1, 2, None, None))

    def testMultiplePrimaryHistoryUponUpdate(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0
            self.test.update(changed_by='heather', where=[self.test.id1 == 2, self.test.id2 == 1], what=dict(foo=99),
                             old_data_version=1)
            ret = self.test.history.t.select().execute().fetchone()
            self.assertEquals(ret, (1, 'heather', 1000, 2, 1, 99, 2))

    def testMultiplePrimaryHistoryUpdateRollback(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0
            self.test.t.update(values=dict(foo=99, data_version=2)).where(self.test.id1 == 2).where(self.test.id2 == 1).execute()
            self.test.history.t.insert(values=dict(changed_by='heather', change_id=1, timestamp=1000, id1=2, id2=1, data_version=2, foo=99)).execute()

            self.test.t.update(values=dict(foo=100, data_version=3)).where(self.test.id1 == 2).where(self.test.id2 == 1).execute()
            self.test.history.t.insert(values=dict(changed_by='heather', change_id=2, timestamp=1000, id1=2, id2=1, data_version=3, foo=100)).execute()

            self.test.history.rollbackChange(2, 'heather')

            ret = self.test.history.t.select().execute().fetchall()
            self.assertEquals(ret[-1], (3, 'heather', 1000, 2, 1, 99, 4))

            ret = self.test.t.select().where(self.test.id1 == 2).where(self.test.id2 == 1).execute().fetchall()
            self.assertEquals(ret, [(2, 1, 99, 4)])

    def testMultiplePrimaryHistoryInsertRollback(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0

            ret = self.test.t.select().execute().fetchall()

            self.test.t.insert(values=dict(foo=271, data_version=1, id1=4, id2=31)).execute()
            self.test.history.t.insert(values=dict(changed_by='george', change_id=1, timestamp=999, id1=4, id2=31, data_version=None, foo=None)).execute()
            self.test.history.t.insert(values=dict(changed_by='george', change_id=2, timestamp=1000, id1=4, id2=31, data_version=1, foo=271)).execute()

            self.test.history.rollbackChange(2, 'george')

            ret = self.test.history.t.select().execute().fetchall()
            self.assertEquals(ret[-1], (3, 'george', 1000, 4, 31, None, None))

            ret = self.test.t.select().execute().fetchall()
            self.assertEquals(len(ret), 4, msg=ret)

    def testMultiplePrimaryHistoryDeleteRollback(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0

            ret = self.test.t.select().execute().fetchall()

            self.test.t.insert(values=dict(foo=271, data_version=1, id1=4, id2=3)).execute()
            self.test.history.t.insert(values=dict(changed_by='george', change_id=1, timestamp=999, id1=4, id2=3, data_version=None, foo=None)).execute()
            self.test.history.t.insert(values=dict(changed_by='george', change_id=2, timestamp=1000, id1=4, id2=3, data_version=1, foo=271)).execute()

            self.test.t.delete().where(self.test.id1 == 4).where(self.test.id2 == 3).execute()
            self.test.history.t.insert(values=dict(changed_by='bobby', change_id=3, timestamp=1000, id1=4, id2=3, data_version=None, foo=None)).execute()

            self.test.history.rollbackChange(3, 'george')

            ret = self.test.history.t.select().execute().fetchall()
            self.assertEquals(ret[-1], (5, 'george', 1000, 4, 3, 271, 1))

            ret = self.test.t.select().execute().fetchall()
            self.assertEquals(len(ret), 5, msg=ret)


class RulesTestMixin(object):

    def _stripNullColumns(self, rules):
        # We know a bunch of columns are going to be empty...easier to strip them out
        # than to be super verbose (also should let this test continue to work even
        # if the schema changes).
        for rule in rules:
            for key in rule.keys():
                if rule[key] is None:
                    del rule[key]
        return rules


class TestRulesSimple(unittest.TestCase, RulesTestMixin, MemoryDatabaseMixin):

    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.db.create()
        self.paths = self.db.rules
        self.paths.t.insert().execute(id=1, priority=100, version='3.5', buildTarget='d', backgroundRate=100, mapping='c', update_type='z', data_version=1)
        self.paths.t.insert().execute(id=2, priority=100, version='3.3', buildTarget='d', backgroundRate=100, mapping='b', update_type='z', data_version=1)
        self.paths.t.insert().execute(id=3, priority=100, version='3.5', buildTarget='a', backgroundRate=100, mapping='a', update_type='z', data_version=1)
        self.paths.t.insert().execute(id=4, alias="gandalf", priority=80, buildTarget='d', backgroundRate=100, mapping='a', update_type='z', data_version=1)
        self.paths.t.insert().execute(id=5, priority=80, buildTarget='d', version='3.3', backgroundRate=0, mapping='c', update_type='z', data_version=1)
        self.paths.t.insert().execute(id=6, priority=100, buildTarget='d', mapping='a', backgroundRate=100, osVersion='foo 1', update_type='z', data_version=1)
        self.paths.t.insert().execute(
            id=7, priority=100, buildTarget='d', mapping='a', backgroundRate=100, osVersion='foo 2,blah 6', update_type='z', data_version=1)
        self.paths.t.insert().execute(
            id=8, priority=100, buildTarget='e', mapping='d', backgroundRate=100, locale='foo,bar-baz', update_type='z', data_version=1)

    def testGetOrderedRules(self):
        rules = self._stripNullColumns(self.paths.getOrderedRules())
        expected = [
            dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget='d', mapping='a', update_type='z', data_version=1),
            dict(rule_id=5, priority=80, backgroundRate=0, version='3.3', buildTarget='d', mapping='c', update_type='z', data_version=1),
            dict(rule_id=6, priority=100, buildTarget='d', mapping='a', backgroundRate=100, osVersion='foo 1', update_type='z', data_version=1),
            dict(rule_id=7, priority=100, buildTarget='d', mapping='a', backgroundRate=100, osVersion='foo 2,blah 6', update_type='z', data_version=1),
            dict(rule_id=8, priority=100, buildTarget='e', mapping='d', backgroundRate=100, locale='foo,bar-baz', update_type='z', data_version=1),
            dict(rule_id=2, priority=100, backgroundRate=100, version='3.3', buildTarget='d', mapping='b', update_type='z', data_version=1),
            dict(rule_id=3, priority=100, backgroundRate=100, version='3.5', buildTarget='a', mapping='a', update_type='z', data_version=1),
            dict(rule_id=1, priority=100, backgroundRate=100, version='3.5', buildTarget='d', mapping='c', update_type='z', data_version=1),
        ]
        self.assertEquals(rules, expected)

    def testGetRulesMatchingQuery(self):
        print self.paths.t.select().execute().fetchall()
        rules = self.paths.getRulesMatchingQuery(
            dict(product='', version='3.5', channel='',
                 buildTarget='a', buildID='', locale='', osVersion='',
                 distribution='', distVersion='', headerArchitecture='',
                 force=False, queryVersion=3,
                 ),
            fallbackChannel=''
        )
        rules = self._stripNullColumns(rules)
        expected = [dict(rule_id=3, priority=100, backgroundRate=100, version='3.5', buildTarget='a', mapping='a', update_type='z', data_version=1)]
        self.assertEquals(rules, expected)

    def testGetRulesMatchingQueryWithNullColumn(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(product='', version='3.5', channel='',
                 buildTarget='d', buildID='', locale='', osVersion='',
                 distribution='', distVersion='', headerArchitecture='',
                 force=False, queryVersion=3,
                 ),
            fallbackChannel=''
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(rule_id=1, priority=100, backgroundRate=100, version='3.5', buildTarget='d', mapping='c', update_type='z', data_version=1),
            dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget='d', mapping='a', update_type='z', data_version=1),
        ]
        self.assertEquals(rules, expected)

    def testGetRulesMatchingQueryDontReturnBackgroundThrottled(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(product='', version='3.3', channel='',
                 buildTarget='d', buildID='', locale='', osVersion='',
                 distribution='', distVersion='', headerArchitecture='',
                 force=False, queryVersion=3,
                 ),
            fallbackChannel=''
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(rule_id=2, priority=100, backgroundRate=100, version='3.3', buildTarget='d', mapping='b', update_type='z', data_version=1),
            dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget='d', mapping='a', update_type='z', data_version=1),
        ]
        self.assertEquals(rules, expected)

    def testGetRulesMatchingQueryReturnBackgroundThrottled(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(product='', version='3.3', channel='',
                 buildTarget='d', buildID='', locale='', osVersion='',
                 distribution='', distVersion='', headerArchitecture='',
                 force=True, queryVersion=3,
                 ),
            fallbackChannel=''
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(rule_id=2, priority=100, backgroundRate=100, version='3.3', buildTarget='d', mapping='b', update_type='z', data_version=1),
            dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget='d', mapping='a', update_type='z', data_version=1),
            dict(rule_id=5, priority=80, backgroundRate=0, version='3.3', buildTarget='d', mapping='c', update_type='z', data_version=1),
        ]
        self.assertEquals(rules, expected)

    def testGetRulesMatchingQueryOsVersionSubstring(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(product='', version='5.0', channel='', buildTarget='d',
                 buildID='', locale='', osVersion='foo 1.2.3', distribution='',
                 distVersion='', headerArchitecture='', force=False,
                 queryVersion=3,
                 ),
            fallbackChannel='',
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget='d', mapping='a', update_type='z', data_version=1),
            dict(rule_id=6, priority=100, buildTarget='d', mapping='a', backgroundRate=100, osVersion='foo 1', update_type='z', data_version=1)
        ]
        self.assertEquals(rules, expected)

    def testGetRulesMatchingQueryOsVersionSubstringNotAtStart(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(product='', version='5.0', channel='', buildTarget='d',
                 buildID='', locale='', osVersion='bbb foo 1.2.3', distribution='',
                 distVersion='', headerArchitecture='', force=False,
                 queryVersion=3,
                 ),
            fallbackChannel='',
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget='d', mapping='a', update_type='z', data_version=1),
            dict(rule_id=6, priority=100, buildTarget='d', mapping='a', backgroundRate=100, osVersion='foo 1', update_type='z', data_version=1)
        ]
        self.assertEquals(rules, expected)

    def testGetRulesMatchingQueryOsVersionMultipleSubstring(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(product='', version='5.0', channel='', buildTarget='d',
                 buildID='', locale='', osVersion='blah 6.3.2', distribution='',
                 distVersion='', headerArchitecture='', force=False,
                 queryVersion=3,
                 ),
            fallbackChannel='',
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget='d', mapping='a', update_type='z', data_version=1),
            dict(rule_id=7, priority=100, buildTarget='d', mapping='a', backgroundRate=100, osVersion='foo 2,blah 6', update_type='z', data_version=1)
        ]
        self.assertEquals(rules, expected)

    def testGetRulesMatchingQueryLocale(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(product='', version='', channel='', buildTarget='e',
                 buildID='', locale='foo', osVersion='', distribution='',
                 distVersion='', headerArchitecture='', force=False,
                 queryVersion=3,
                 ),
            fallbackChannel='',
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(rule_id=8, priority=100, buildTarget='e', mapping='d', backgroundRate=100, locale='foo,bar-baz', update_type='z', data_version=1)
        ]
        self.assertEquals(rules, expected)

    def testGetRulesMatchingQueryLocaleNoPartialMatch(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(product='', version='5', channel='', buildTarget='e',
                 buildID='', locale='bar', osVersion='', distribution='',
                 distVersion='', headerArchitecture='', force=False,
                 queryVersion=3,
                 ),
            fallbackChannel='',
        )
        rules = self._stripNullColumns(rules)
        expected = []
        self.assertEquals(rules, expected)

    def testGetRuleById(self):
        rule = self._stripNullColumns([self.paths.getRule(1)])
        expected = [dict(rule_id=1, priority=100, backgroundRate=100, version='3.5', buildTarget='d', mapping='c', update_type='z', data_version=1)]
        self.assertEquals(rule, expected)

    def testGetRuleByAlias(self):
        rule = self._stripNullColumns([self.paths.getRule(4)])
        expected = [dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget='d', mapping='a', update_type='z', data_version=1)]
        self.assertEquals(rule, expected)

    def testAddRule(self):
        what = dict(backgroundRate=11,
                    mapping='c',
                    update_type='z',
                    priority=60)
        rule_id = self.paths.addRule(changed_by='bill', what=what)
        rules = self.paths.t.select().where(self.paths.rule_id == rule_id).execute().fetchall()
        copy_rule = dict(rules[0].items())
        rule = self._stripNullColumns([copy_rule])
        what['rule_id'] = rule_id
        what['data_version'] = 1
        what = [what]
        self.assertEquals(rule, what)

    def testUpdateRule(self):
        rules = self.paths.t.select().where(self.paths.rule_id == 1).execute().fetchall()
        what = dict(rules[0].items())

        what['mapping'] = 'd'
        self.paths.updateRule(changed_by='bill', id_or_alias=1, what=what, old_data_version=1)

        rules = self.paths.t.select().where(self.paths.rule_id == 1).execute().fetchall()
        copy_rule = dict(rules[0].items())
        rule = self._stripNullColumns([copy_rule])

        expected = [dict(rule_id=1, priority=100, backgroundRate=100, version='3.5', buildTarget='d', mapping='d', update_type='z', data_version=1)]
        self.assertEquals(rule, expected)

    def testUpdateRuleByAlias(self):
        rules = self.paths.t.select().where(self.paths.rule_id == 4).execute().fetchall()
        what = dict(rules[0].items())

        what['mapping'] = 'd'
        self.paths.updateRule(changed_by='bill', id_or_alias="gandalf", what=what, old_data_version=1)

        rules = self.paths.t.select().where(self.paths.rule_id == 4).execute().fetchall()
        copy_rule = dict(rules[0].items())
        rule = self._stripNullColumns([copy_rule])

        expected = [dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget='d', mapping='d', update_type='z', data_version=1)]
        self.assertEquals(rule, expected)

    def testDeleteRule(self):
        self.paths.deleteRule(changed_by='bill', id_or_alias=2, old_data_version=1)
        rule = self.paths.t.select().where(self.paths.rule_id == 2).execute().fetchall()
        self.assertEquals(rule, [])

    def testDeleteRuleByAlias(self):
        self.paths.deleteRule(changed_by='bill', id_or_alias="gandalf", old_data_version=1)
        rule = self.paths.t.select().where(self.paths.rule_id == 4).execute().fetchall()
        self.assertEquals(rule, [])

    def testGetNumberOfRules(self):
        self.assertEquals(self.paths.countRules(), 8)


class TestRulesSpecial(unittest.TestCase, RulesTestMixin, MemoryDatabaseMixin):

    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.db.create()
        self.rules = self.db.rules
        self.rules.t.insert().execute(id=1, priority=100, version='>=4.0b1', backgroundRate=100, update_type='z', data_version=1)
        self.rules.t.insert().execute(id=2, priority=100, channel='release*', backgroundRate=100, update_type='z', data_version=1)
        self.rules.t.insert().execute(id=3, priority=100, buildID='>=20010101222222', backgroundRate=100, update_type='z', data_version=1)

    def testGetRulesMatchingQueryVersionComparison(self):
        expected = [dict(rule_id=1, priority=100, backgroundRate=100, version='>=4.0b1', update_type='z', data_version=1)]
        rules = self.rules.getRulesMatchingQuery(
            dict(name='', product='', version='4.0', channel='',
                 buildTarget='', buildID='', locale='', osVersion='',
                 distribution='', distVersion='', headerArchitecture='',
                 force=False, queryVersion=3,
                 ),
            fallbackChannel=''
        )
        rules = self._stripNullColumns(rules)
        self.assertEquals(rules, expected)

        rules = self.rules.getRulesMatchingQuery(
            dict(name='', product='', version='4.0b2', channel='',
                 buildTarget='', buildID='', locale='', osVersion='',
                 distribution='', distVersion='', headerArchitecture='',
                 force=False, queryVersion=3,
                 ),
            fallbackChannel=''
        )
        rules = self._stripNullColumns(rules)
        self.assertEquals(rules, expected)

        rules = self.rules.getRulesMatchingQuery(
            dict(name='', product='', version='4.0.1', channel='',
                 buildTarget='', buildID='', locale='', osVersion='',
                 distribution='', distVersion='', headerArchitecture='',
                 force=False, queryVersion=3,
                 ),
            fallbackChannel=''
        )
        rules = self._stripNullColumns(rules)
        self.assertEquals(rules, expected)

        rules = self.rules.getRulesMatchingQuery(
            dict(name='', product='', version='3.0', channel='',
                 buildTarget='', buildID='', locale='', osVersion='',
                 distribution='', distVersion='', headerArchitecture='',
                 force=False, queryVersion=3,
                 ),
            fallbackChannel=''
        )
        rules = self._stripNullColumns(rules)
        self.assertEquals(rules, [])

    def testGetRulesMatchingQueryChannelGlobbing(self):
        expected = [dict(rule_id=2, priority=100, backgroundRate=100, channel='release*', update_type='z', data_version=1)]
        rules = self.rules.getRulesMatchingQuery(
            dict(name='', product='', version='3.0', channel='releasetest',
                 buildTarget='', buildID='', locale='', osVersion='', distribution='',
                 distVersion='', headerArchitecture='',
                 force=False, queryVersion=3,
                 ),
            fallbackChannel='releasetest'
        )
        rules = self._stripNullColumns(rules)
        self.assertEquals(rules, expected)

        rules = self.rules.getRulesMatchingQuery(
            dict(name='', product='', version='3.0', channel='releasetest-cck-blah',
                 buildTarget='', buildID='', locale='', osVersion='',
                 distribution='', distVersion='', headerArchitecture='',
                 force=False, queryVersion=3,
                 ),
            fallbackChannel='releasetest'
        )
        rules = self._stripNullColumns(rules)
        self.assertEquals(rules, expected)

    def testGetRulesMatchingBuildIDComparison(self):
        expected = [dict(rule_id=3, priority=100, backgroundRate=100, buildID='>=20010101222222', update_type='z', data_version=1)]
        rules = self.rules.getRulesMatchingQuery(
            dict(name='', product='', version='3.0', channel='',
                 buildTarget='', buildID='20010101222222', locale='', osVersion='',
                 distribution='', distVersion='', headerArchitecture='',
                 force=False, queryVersion=3,
                 ),
            fallbackChannel=''
        )
        rules = self._stripNullColumns(rules)
        self.assertEquals(rules, expected)

        rules = self.rules.getRulesMatchingQuery(
            dict(name='', product='', version='3.0', channel='',
                 buildTarget='', buildID='20010101232323', locale='', osVersion='',
                 distribution='', distVersion='', headerArchitecture='',
                 force=False, queryVersion=3,
                 ),
            fallbackChannel=''
        )
        rules = self._stripNullColumns(rules)
        self.assertEquals(rules, expected)

        rules = self.rules.getRulesMatchingQuery(
            dict(name='', product='', version='3.0', channel='',
                 buildTarget='', buildID='20010101212121', locale='', osVersion='',
                 distribution='', distVersion='', headerArchitecture='',
                 force=False, queryVersion=3,
                 ),
            fallbackChannel=''
        )
        rules = self._stripNullColumns(rules)
        self.assertEquals(rules, [])


class TestReleases(unittest.TestCase, MemoryDatabaseMixin):

    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.db.create()
        self.releases = self.db.releases
        self.releases.t.insert().execute(name='a', product='a', version='a', data=json.dumps(dict(name="a", schema_version=1, hashFunction="sha512")),
                                         data_version=1)
        self.releases.t.insert().execute(name='ab', product='a', version='a', data=json.dumps(dict(name="ab", schema_version=1, hashFunction="sha512")),
                                         data_version=1)
        self.releases.t.insert().execute(name='b', product='b', version='b', data=json.dumps(dict(name="b", schema_version=1, hashFunction="sha512")),
                                         data_version=1)
        self.releases.t.insert().execute(name='c', product='c', version='c', data=json.dumps(dict(name="c", schema_version=1, hashFunction="sha512")),
                                         data_version=1)

    def testGetReleases(self):
        self.assertEquals(len(self.releases.getReleases()), 4)

    def testGetReleasesWithLimit(self):
        self.assertEquals(len(self.releases.getReleases(limit=1)), 1)

    def testGetReleasesWithWhere(self):
        expected = [dict(product='b', version='b', name='b', data=dict(name="b", schema_version=1, hashFunction="sha512"), data_version=1)]
        self.assertEquals(self.releases.getReleases(name='b'), expected)

    def testGetReleaseBlob(self):
        expected = dict(name="c", schema_version=1, hashFunction="sha512")
        self.assertEquals(self.releases.getReleaseBlob(name='c'), expected)

    def testGetReleaseBlobNonExistentRelease(self):
        self.assertRaises(KeyError, self.releases.getReleaseBlob, name='z')

    def testGetReleaseInfoAll(self):
        releases = self.releases.getReleaseInfo()
        expected = [dict(name='a', product='a', version='a', data_version=1),
                    dict(name='ab', product='a', version='a', data_version=1),
                    dict(name='b', product='b', version='b', data_version=1),
                    dict(name='c', product='c', version='c', data_version=1)]
        self.assertEquals(releases, expected)

    def testGetReleaseInfoProduct(self):
        releases = self.releases.getReleaseInfo(product='a')
        expected = [dict(name='a', product='a', version='a', data_version=1),
                    dict(name='ab', product='a', version='a', data_version=1)]
        self.assertEquals(releases, expected)

    def testGetReleaseInfoVersion(self):
        releases = self.releases.getReleaseInfo(version='b')
        expected = [dict(name='b', product='b', version='b', data_version=1), ]
        self.assertEquals(releases, expected)

    def testGetReleaseInfoNoMatch(self):
        releases = self.releases.getReleaseInfo(product='a', version='b')
        expected = []
        self.assertEquals(releases, expected)

    def testGetReleaseInfoNamePrefix(self):
        releases = self.releases.getReleaseInfo(name_prefix='a')
        expected = [dict(name='a', product='a', version='a', data_version=1),
                    dict(name='ab', product='a', version='a', data_version=1)]
        self.assertEquals(releases, expected)

    def testGetReleaseInfoNamePrefixNameOnly(self):
        releases = self.releases.getReleaseInfo(name_prefix='a', nameOnly=True)
        expected = [{'name': 'a'}, {'name': 'ab'}]
        self.assertEquals(releases, expected)

    def testGetReleaseNames(self):
        releases = self.releases.getReleaseNames()
        expected = [dict(name='a'),
                    dict(name='ab'),
                    dict(name='b'),
                    dict(name='c')]
        self.assertEquals(releases, expected)

    def testGetReleaseNamesProduct(self):
        releases = self.releases.getReleaseNames(product='a')
        expected = [dict(name='a'),
                    dict(name='ab')]
        self.assertEquals(releases, expected)

    def testGetReleaseNamesVersion(self):
        releases = self.releases.getReleaseNames(version='b')
        expected = [dict(name='b'), ]
        self.assertEquals(releases, expected)

    def testGetReleaseNamesNoMatch(self):
        releases = self.releases.getReleaseNames(product='a', version='b')
        expected = []
        self.assertEquals(releases, expected)

    def testGetNumberOfReleases(self):
        # because 4 releases were set up in the setUp()
        self.assertEquals(self.releases.countReleases(), 4)

    def testDeleteRelease(self):
        self.releases.deleteRelease(changed_by='bill', name='a', old_data_version=1)
        release = self.releases.t.select().where(self.releases.name == 'a').execute().fetchall()
        self.assertEquals(release, [])

    def testAddReleaseWithNameMismatch(self):
        blob = ReleaseBlobV1(name="f", schema_version=1, hashFunction="sha512")
        self.assertRaises(ValueError, self.releases.addRelease, "g", "g", "23.0", blob, "bill")

    def testUpdateReleaseWithNameMismatch(self):
        newBlob = ReleaseBlobV1(name="c", schema_version=1, hashFunction="sha512")
        self.assertRaises(ValueError, self.releases.updateRelease, "a", "bill", 1, blob=newBlob)


class TestBlobCaching(unittest.TestCase, MemoryDatabaseMixin):

    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        cache.reset()
        cache.make_cache("blob", 10, 10)
        cache.make_cache("blob_version", 10, 4)
        self.db = AUSDatabase(self.dburi)
        self.db.create()
        self.releases = self.db.releases
        self.releases.t.insert().execute(name='a', product='a', version='a', data=json.dumps(dict(name="a", schema_version=1, hashFunction="sha512")),
                                         data_version=1)
        self.releases.t.insert().execute(name='b', product='b', version='b', data=json.dumps(dict(name="b", schema_version=1, hashFunction="sha512")),
                                         data_version=1)
        # When we started copying objects that go in or out of the cache we
        # discovered that Blob objects were not copyable at the time, due to
        # deepycopy() trying to copy their instance-level "log" attribute.
        # Unit tests at the time didn't catch this because the logger used
        # in tests is copyable (whereas one that points at an actual file
        # stream is not). In order to make sure this doesn't regress, we
        # override the logging for these tests to make sure the loggers are
        # configured as they are in production.
        self.handler = logging.StreamHandler(sys.stderr)
        logger = logging.getLogger()
        logger.addHandler(self.handler)

    def tearDown(self):
        cache.reset()
        logger = logging.getLogger()
        logger.removeHandler(self.handler)

    def _checkCacheStats(self, cache, lookups, hits, misses):
        self.assertEquals(cache.lookups, lookups)
        self.assertEquals(cache.hits, hits)
        self.assertEquals(cache.misses, misses)

    def testGetReleaseBlobCaching(self):
        with mock.patch("time.time") as t:
            t.return_value = 0
            for i in range(5):
                self.releases.getReleaseBlob(name="a")
                t.return_value += 1

            # We've retrieved the blob and blob version 5 times.
            # The blob cache has a ttl of 10, so we're expecting the first one
            # to be a miss, and the rest to be hits.
            self._checkCacheStats(cache.caches["blob"], 5, 4, 1)
            # But blob version has a ttl of 4, so we should see the first one
            # miss, the next three hit, and then the last one miss again.
            self._checkCacheStats(cache.caches["blob_version"], 5, 3, 2)

    def testGetReleasesUsesBlobCache(self):
        with mock.patch("time.time") as t:
            t.return_value = 0
            for i in range(5):
                self.releases.getReleases()
                t.return_value += 1

            # We have the same hit rates as testGetReleaseBlobCaching, but
            # they're doubled because we're retrieving both releases instead
            # of just one.
            self._checkCacheStats(cache.caches["blob"], 10, 8, 2)
            self._checkCacheStats(cache.caches["blob_version"], 10, 6, 4)

    def testGetReleaseBlobCachingWithBlobCacheExpiry(self):
        with mock.patch("time.time") as t:
            t.return_value = 0
            # Because timeout is set to 10 and we increment by one second each
            # iteration, we should end up with the following per blob:
            # * One miss (initial lookup)
            # * Nine hits (t=1 through 9)
            # * One more miss (because the cache expired)
            #
            # Times two gives us 22 lookups, 18 hits, 4 misses
            #
            # The blob version is a bit different because of its 4 second ttl:
            # * One miss (initial lookup)
            # * Three hits (t=1 through 3)
            # * One miss (cache expired @ t=4)
            # * Three hits (t=5 through 8)
            # * One miss (cache expired @ t=9)
            # * Two hits (t=10 and 11)
            #
            # Times two gives us 22 lookups, 16 hits, 6 misses
            for i in range(11):
                self.releases.getReleaseBlob(name="a")
                self.releases.getReleaseBlob(name="b")
                t.return_value += 1

            self._checkCacheStats(cache.caches["blob"], 22, 18, 4)
            self._checkCacheStats(cache.caches["blob_version"], 22, 16, 6)

    def testGetReleaseBlobCachingWithDataVersionChange(self):
        with mock.patch("time.time") as t:
            t.return_value = 0
            # Retrieve the blob a few times to warm the cache.
            self.releases.getReleaseBlob(name="b")
            t.return_value += 1
            self.releases.getReleaseBlob(name="b")
            t.return_value += 1
            self.releases.getReleaseBlob(name="b")
            t.return_value += 1

            newBlob = ReleaseBlobV1(name="b", appv="2", hashFunction="sha512")
            self._checkCacheStats(cache.caches["blob"], 3, 2, 1)
            self._checkCacheStats(cache.caches["blob_version"], 3, 2, 1)

            # Now change it, which will change data_version.
            self.releases.updateRelease("b", "bob", 1, blob=newBlob)

            # Ensure that we have the updated version, not the originally
            # cached one.
            blob = self.releases.getReleaseBlob(name="b")
            self.assertEquals(blob["appv"], "2")
            t.return_value += 1

            # And retrieve it a few more times for good measure
            self.releases.getReleaseBlob(name="b")
            t.return_value += 1
            self.releases.getReleaseBlob(name="b")
            t.return_value += 1
            self.releases.getReleaseBlob(name="b")

            # The first 3 retrievals here cause a miss and then 2 hits.
            # updateRelease doesn't affect the stats at all (but it updates
            # the cache with the new version
            # Which means that all 4 subsequent retrievals should be hits.
            self._checkCacheStats(cache.caches["blob"], 7, 6, 1)
            # Because we updated the blob before the blob_version cache
            # expired at t=4, its expiry got reset, which means that its only
            # miss was the original lookup.
            self._checkCacheStats(cache.caches["blob_version"], 7, 6, 1)

    def testAddReleaseUpdatesCache(self):
        with mock.patch("time.time") as t:
            t.return_value = 0
            self.releases.addRelease(
                name="abc",
                product="bbb",
                version="3.2",
                blob=ReleaseBlobV1(name="abc", schema_version=1, hashFunction="sha512"),
                changed_by="bill",
            )
            t.return_value += 1
            self.releases.getReleaseBlob(name="abc")
            t.return_value += 1
            self.releases.getReleaseBlob(name="abc")

            # Adding the release should've caused the cache to get an initial
            # version of the blob without changing the stats. The two retrievals
            # should both be cache hits because of this.
            self._checkCacheStats(cache.caches["blob"], 2, 2, 0)
            self._checkCacheStats(cache.caches["blob_version"], 2, 2, 0)

    def testDeleteReleaseClobbersCache(self):
        with mock.patch("time.time") as t:
            t.return_value = 0
            self.releases.getReleaseBlob(name="b")
            t.return_value += 1
            self.releases.getReleaseBlob(name="b")
            t.return_value += 1
            self.releases.deleteRelease("bob", "b", 1)
            t.return_value += 1

            # We've just got two lookups here (one hit, one miss).
            # Deleting shouldn't cause any cache lookups...
            self._checkCacheStats(cache.caches["blob"], 2, 1, 1)
            self._checkCacheStats(cache.caches["blob_version"], 2, 1, 1)
            # ...but we do need to verify that the blob is no longer in the
            # cache or otherwise retrievable.
            self.assertRaises(KeyError, self.releases.getReleaseBlob, name="b")

    def testAddLocaleToReleaseUpdatesCaches(self):
        with mock.patch("time.time") as t:
            t.return_value = 0
            self.releases.getReleaseBlob(name="b")
            t.return_value += 1
            self.releases.addLocaleToRelease("b", "win", "zu", dict(buildID=123), 1, "bob")
            t.return_value += 1
            blob = self.releases.getReleaseBlob(name="b")

            newBlob = {
                "schema_version": 1,
                "name": "b",
                "hashFunction": "sha512",
                "platforms": {
                    "win": {
                        "locales": {
                            "zu": {
                                "buildID": 123,
                            }
                        }
                    }
                }
            }

            self.assertEquals(blob, newBlob)
            # The first getReleaseBlob call is a miss
            # addLocaleToRelease retrieve the blob (a hit) before updating it,
            # and updates the cache.
            # The second getReleaseBlob call will be a cache hit of the newly
            # updated contents.
            self._checkCacheStats(cache.caches["blob"], 3, 2, 1)
            self._checkCacheStats(cache.caches["blob_version"], 3, 2, 1)


class TestReleasesSchema1(unittest.TestCase, MemoryDatabaseMixin):
    """Tests for the Releases class that depend on version 1 of the blob schema."""

    maxDiff = 1000

    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.db.create()
        self.releases = self.db.releases
        self.releases.t.insert().execute(name='a', product='a', version='a', data_version=1, data="""
{
    "name": "a",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 1234,
                        "from": "*",
                        "hashValue": "def"
                    }
                }
            }
        },
        "p2": {
            "alias": "p"
        },
        "p3": {
        }
    }
}
""")
        self.releases.t.insert().execute(name='b', product='b', version='b', data_version=1, data="""
{
    "name": "b",
    "hashFunction": "sha512",
    "schema_version": 1
}
""")

    def testAddRelease(self):
        blob = ReleaseBlobV1(name="d", hashFunction="sha512")
        self.releases.addRelease(name='d', product='d', version='d', blob=blob, changed_by='bill')
        expected = [('d', 'd', 'd', json.dumps(dict(name="d", schema_version=1, hashFunction="sha512")), 1)]
        self.assertEquals(self.releases.t.select().where(self.releases.name == 'd').execute().fetchall(), expected)

    def testAddReleaseAlreadyExists(self):
        blob = ReleaseBlobV1(name="a", hashFunction="sha512")
        self.assertRaises(TransactionError, self.releases.addRelease, name='a', product='a', version='a', blob=blob, changed_by='bill')

    def testUpdateRelease(self):
        blob = ReleaseBlobV1(name='a', hashFunction="sha512")
        self.releases.updateRelease(name='a', product='z', version='y', blob=blob, changed_by='bill', old_data_version=1)
        expected = [('a', 'z', 'y', json.dumps(dict(name='a', schema_version=1, hashFunction="sha512")), 2)]
        self.assertEquals(self.releases.t.select().where(self.releases.name == 'a').execute().fetchall(), expected)

    def testUpdateReleaseWithBlob(self):
        blob = ReleaseBlobV1(name='b', schema_version=1, hashFunction="sha512")
        self.releases.updateRelease(name='b', product='z', version='y', changed_by='bill', blob=blob, old_data_version=1)
        expected = [('b', 'z', 'y', json.dumps(dict(name='b', schema_version=1, hashFunction="sha512")), 2)]
        self.assertEquals(self.releases.t.select().where(self.releases.name == 'b').execute().fetchall(), expected)

    def testUpdateReleaseInvalidBlob(self):
        blob = ReleaseBlobV1(name="2", hashFunction="sha512")
        blob['foo'] = 'bar'
        self.assertRaises(ValidationError, self.releases.updateRelease, changed_by='bill', name='b', blob=blob, old_data_version=1)

    def testAddLocaleToRelease(self):
        data = {
            "complete": {
                "filesize": 1,
                "from": "*",
                "hashValue": "abc",
            }
        }
        self.releases.addLocaleToRelease(name='a', platform='p', locale='c', data=data, old_data_version=1, changed_by='bill')
        ret = json.loads(select([self.releases.data]).where(self.releases.name == 'a').execute().fetchone()[0])
        expected = json.loads("""
{
    "name": "a",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "c": {
                    "complete": {
                        "filesize": 1,
                        "from": "*",
                        "hashValue": "abc"
                    }
                },
                "l": {
                    "complete": {
                        "filesize": 1234,
                        "from": "*",
                        "hashValue": "def"
                    }
                }
            }
        },
        "p2": {
            "alias": "p"
        },
        "p3": {
        }
    }
}
""")
        self.assertEqual(ret, expected)

    def testAddLocaleToReleaseWithAlias(self):
        data = {
            "complete": {
                "filesize": 123,
                "from": "*",
                "hashValue": "abc"
            }
        }
        self.releases.addLocaleToRelease(name='a', platform='p', locale='c', data=data, old_data_version=1, changed_by='bill', alias=['p4'])
        ret = json.loads(select([self.releases.data]).where(self.releases.name == 'a').execute().fetchone()[0])
        expected = json.loads("""
{
    "name": "a",
    "hashFunction": "sha512",
    "schema_version": 1,
    "platforms": {
        "p": {
            "locales": {
                "c": {
                    "complete": {
                        "filesize": 123,
                        "from": "*",
                        "hashValue": "abc"
                    }
                },
                "l": {
                    "complete": {
                        "filesize": 1234,
                        "from": "*",
                        "hashValue": "def"
                    }
                }
            }
        },
        "p2": {
            "alias": "p"
        },
        "p3": {
        },
        "p4": {
            "alias": "p"
        }
    }
}
""")
        self.assertEqual(ret, expected)

    def testAddLocaleToReleaseOverride(self):
        data = {
            "complete": {
                "filesize": 123,
                "from": "*",
                "hashValue": "789"
            }
        }
        self.releases.addLocaleToRelease(name='a', platform='p', locale='l', data=data, old_data_version=1, changed_by='bill')
        ret = json.loads(select([self.releases.data]).where(self.releases.name == 'a').execute().fetchone()[0])
        expected = json.loads("""
{
    "name": "a",
    "hashFunction": "sha512",
    "schema_version": 1,
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 123,
                        "from": "*",
                        "hashValue": "789"
                    }
                }
            }
        },
        "p2": {
            "alias": "p"
        },
        "p3": {
        }
    }
}
""")
        self.assertEqual(ret, expected)

    def testAddLocaleToReleasePlatformsDoesntExist(self):
        data = {
            "complete": {
                "filesize": 432,
                "from": "*",
                "hashValue": "abc"
            }
        }
        self.releases.addLocaleToRelease(name='b', platform='q', locale='l', data=data, old_data_version=1, changed_by='bill')
        ret = json.loads(select([self.releases.data]).where(self.releases.name == 'b').execute().fetchone()[0])
        expected = json.loads("""
{
    "name": "b",
    "hashFunction": "sha512",
    "schema_version": 1,
    "platforms": {
        "q": {
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 432,
                        "from": "*",
                        "hashValue": "abc"
                    }
                }
            }
        }
    }
}
""")
        self.assertEqual(ret, expected)

    def testAddLocaleToReleaseNoLocales(self):
        data = {
            "complete": {
                "filesize": 432,
                "from": "*",
                "hashValue": "abc",
            }
        }
        self.releases.addLocaleToRelease(name='a', platform='p3', locale='l', data=data, old_data_version=1, changed_by='bill')
        ret = json.loads(select([self.releases.data]).where(self.releases.name == 'a').execute().fetchone()[0])
        expected = json.loads("""
{
    "name": "a",
    "hashFunction": "sha512",
    "schema_version": 1,
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 1234,
                        "from": "*",
                        "hashValue": "def"
                    }
                }
            }
        },
        "p2": {
            "alias": "p"
        },
        "p3": {
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 432,
                        "from": "*",
                        "hashValue": "abc"
                    }
                }
            }
        }
    }
}
""")
        self.assertEqual(ret, expected)

    def testAddLocaleToReleaseSecondPlatform(self):
        data = {
            "complete": {
                "filesize": 324,
                "from": "*",
                "hashValue": "abc",
            }
        }
        self.releases.addLocaleToRelease(name='a', platform='q', locale='l', data=data, old_data_version=1, changed_by='bill')
        ret = json.loads(select([self.releases.data]).where(self.releases.name == 'a').execute().fetchone()[0])
        expected = json.loads("""
{
    "name": "a",
    "hashFunction": "sha512",
    "schema_version": 1,
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 1234,
                        "from": "*",
                        "hashValue": "def"
                    }
                }
            }
        },
        "p2": {
            "alias": "p"
        },
        "p3": {
        },
        "q": {
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 324,
                        "from": "*",
                        "hashValue": "abc"
                    }
                }
            }
        }
    }
}
""")
        self.assertEqual(ret, expected)

    def testAddLocaleToReleaseResolveAlias(self):
        data = {
            "complete": {
                "filesize": 444,
                "from": "*",
                "hashValue": "abc",
            }
        }
        self.releases.addLocaleToRelease(name='a', platform='p2', locale='j', data=data, old_data_version=1, changed_by='bill')
        ret = json.loads(select([self.releases.data]).where(self.releases.name == 'a').execute().fetchone()[0])
        expected = json.loads("""
{
    "name": "a",
    "hashFunction": "sha512",
    "schema_version": 1,
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 1234,
                        "from": "*",
                        "hashValue": "def"
                    }
                },
                "j": {
                    "complete": {
                        "filesize": 444,
                        "from": "*",
                        "hashValue": "abc"
                    }
                }
            }
        },
        "p2": {
            "alias": "p"
        },
        "p3": {
        }
    }
}
""")
        self.assertEqual(ret, expected)


class TestPermissions(unittest.TestCase, MemoryDatabaseMixin):

    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.db.create()
        self.permissions = self.db.permissions
        self.permissions.t.insert().execute(permission='admin', username='bill', data_version=1)
        self.permissions.t.insert().execute(permission='/users/:id/permissions/:permission', username='bob', data_version=1)
        self.permissions.t.insert().execute(permission='/releases/:name', username='bob', options=json.dumps(dict(product=['fake'])), data_version=1)
        self.permissions.t.insert().execute(permission='/rules', username='cathy', data_version=1)
        self.permissions.t.insert().execute(permission='/rules/:id', username='bob', options=json.dumps(dict(method='POST')), data_version=1)
        self.permissions.t.insert().execute(
            permission='/rules/:id', username='fred', options=json.dumps(dict(product=['foo', 'bar'], method='POST')), data_version=1)

    def testGrantPermissions(self):
        query = self.permissions.t.select().where(self.permissions.username == 'jess')
        self.assertEquals(len(query.execute().fetchall()), 0)
        self.permissions.grantPermission('bob', 'jess', '/rules/:id')
        self.assertEquals(query.execute().fetchall(), [('/rules/:id', 'jess', None, 1)])

    def testGrantPermissionsWithOptions(self):
        self.permissions.grantPermission('bob', 'cathy', '/releases/:name', options=dict(product=['SeaMonkey']))
        query = self.permissions.t.select().where(self.permissions.username == 'cathy')
        query = query.where(self.permissions.permission == '/releases/:name')
        self.assertEquals(query.execute().fetchall(), [('/releases/:name', 'cathy', json.dumps(dict(product=['SeaMonkey'])), 1)])

    def testGrantPermissionsUnknownPermission(self):
        self.assertRaises(ValueError, self.permissions.grantPermission,
                          'bob', 'bud', 'bad'
                          )

    def testGrantPermissionsUnknownOption(self):
        self.assertRaises(ValueError, self.permissions.grantPermission,
                          'bob', 'bud', '/rules/:id', dict(foo=1)
                          )

    def testRevokePermission(self):
        self.permissions.revokePermission(changed_by='bill', username='bob', permission='/releases/:name',
                                          old_data_version=1)
        query = self.permissions.t.select().where(self.permissions.username == 'bob')
        query = query.where(self.permissions.permission == '/releases/:name')
        self.assertEquals(len(query.execute().fetchall()), 0)

    def testGetAllUsers(self):
        self.assertEquals(set(self.permissions.getAllUsers()), set(['bill', 'bob', 'cathy', 'fred']))

    def testCountAllUsers(self):
        # bill, bob and cathy
        self.assertEquals(self.permissions.countAllUsers(), 4)

    def testGetPermission(self):
        expected = {
            'permission': '/releases/:name',
            'username': 'bob',
            'options': dict(product=['fake']),
            'data_version': 1
        }
        self.assertEquals(self.permissions.getPermission('bob', '/releases/:name'), expected)

    def testGetPermissionNonExistant(self):
        self.assertEquals(self.permissions.getPermission('bob', '/rules'), {})

    def testGetUserPermissions(self):
        expected = {'/users/:id/permissions/:permission': dict(options=None, data_version=1),
                    '/releases/:name': dict(options=dict(product=['fake']), data_version=1),
                    '/rules/:id': dict(options=dict(method='POST'), data_version=1)}
        self.assertEquals(self.permissions.getUserPermissions('bob'), expected)

    def testGetOptions(self):
        expected = dict(product=['fake'])
        self.assertEquals(self.permissions.getOptions('bob', '/releases/:name'), expected)

    def testGetOptionsPermissionDoesntExist(self):
        self.assertRaises(ValueError, self.permissions.getOptions, 'fake', 'fake')

    def testGetOptionsNoOptions(self):
        self.assertEquals(self.permissions.getOptions('cathy', '/rules'), {})

    def testHasUrlPermissionAdmin(self):
        self.assertTrue(self.permissions.hasUrlPermission('bill', '/rules', 'FOO'))

    def testHasUrlPermissionGranular(self):
        self.assertTrue(self.permissions.hasUrlPermission('cathy', '/rules', 'FOO'))

    def testHasUrlPermissionWithDbOption(self):
        self.assertTrue(self.permissions.hasUrlPermission('bob', '/rules/:id', 'POST'))

    def testHasUrlPermissionWithUrlOption(self):
        self.assertTrue(self.permissions.hasUrlPermission('bob', '/releases/:name', 'FOO', dict(product='fake')))

    def testHasUrlPermissionWithUrlOptionMulti(self):
        self.assertTrue(self.permissions.hasUrlPermission('fred', '/rules/:id', 'POST', dict(product='foo')))
        self.assertTrue(self.permissions.hasUrlPermission('fred', '/rules/:id', 'POST', dict(product='bar')))

    def testHasUrlPermissionNotAllowed(self):
        self.assertFalse(self.permissions.hasUrlPermission('cathy', '/rules/:id', 'FOO'))

    def testHasUrlPermissionNotAllowedWithDbOption(self):
        self.assertFalse(self.permissions.hasUrlPermission('bob', '/rules/:id', 'NOTPOST'))

    def testHasUrlPermissionNotAllowedWithUrlOption(self):
        self.assertFalse(self.permissions.hasUrlPermission('bob', '/releases/:name', 'FOO', dict(product='reallyfake')))


class TestDB(unittest.TestCase):

    def testSetDburiAlreadySetup(self):
        db = AUSDatabase('sqlite:///:memory:')
        self.assertRaises(AlreadySetupError, db.setDburi, 'sqlite:///:memory:')

    def testReset(self):
        db = AUSDatabase('sqlite:///:memory:')
        db.reset()
        # If we can set the dburi again, reset worked!
        db.setDburi('sqlite:///:memory:')
        db.create()
        insp = Inspector.from_engine(db.engine)
        self.assertNotEqual(insp.get_table_names(), [])


class TestDBUpgrade(unittest.TestCase, NamedFileDatabaseMixin):

    def setUp(self):
        NamedFileDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.db.metadata.create_all()

    def testModelIsSameAsRepository(self):
        db2 = AUSDatabase('sqlite:///' + self.getTempfile())
        db2.create()
        diff = migrate.versioning.api.compare_model_to_db(db2.engine, self.db.migrate_repo, self.db.metadata)
        if diff:
            self.fail(str(diff))
