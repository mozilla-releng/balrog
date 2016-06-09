import logging
import mock
import os
from os import path
import simplejson as json
import sys
from tempfile import mkstemp
import unittest

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, select, String
from sqlalchemy.engine.reflection import Inspector

import migrate.versioning.api

from auslib.global_state import cache, dbo
from auslib.db import AUSDatabase, AUSTable, AlreadySetupError, \
    AUSTransaction, TransactionError, OutdatedDataError, UpdateMergeError, \
    ReadOnlyError, PermissionDeniedError
from auslib.blobs.base import BlobValidationError
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

            def __init__(self, db, metadata):
                self.table = Table('test', metadata, Column('id', Integer, primary_key=True, autoincrement=True),
                                   Column('foo', Integer))
                AUSTable.__init__(self, db, 'sqlite')

        class TestAutoincrementTable(AUSTable):

            def __init__(self, db, metadata):
                self.table = Table('test-autoincrement', metadata,
                                   Column('id', Integer, primary_key=True, autoincrement=True),
                                   Column('foo', Integer))
                AUSTable.__init__(self, db, 'sqlite')
        self.test = TestTable("fake", self.metadata)
        self.testAutoincrement = TestAutoincrementTable("fake", self.metadata)
        self.metadata.create_all()
        self.test.t.insert().execute(id=1, foo=33, data_version=1)
        self.test.t.insert().execute(id=2, foo=22, data_version=1)
        self.test.t.insert().execute(id=3, foo=11, data_version=2)


class TestMultiplePrimaryTableMixin(object):

    def setUp(self):
        self.engine = create_engine(self.dburi)
        self.metadata = MetaData(self.engine)

        class TestTable(AUSTable):

            def __init__(self, db, metadata):
                self.table = Table('test', metadata, Column('id1', Integer, primary_key=True),
                                   Column('id2', Integer, primary_key=True),
                                   Column('foo', Integer))
                AUSTable.__init__(self, db, 'sqlite')
        self.test = TestTable("fake", self.metadata)
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
        # insert adds data_version to the query, so we need to add that before comparing
        what["data_version"] = 1
        self.assertEquals(shared[0], self.test)
        self.assertEquals(shared[1], "INSERT")
        self.assertEquals(shared[2], "bob")
        self.assertEquals(shared[3].parameters, what)

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
        # update adds data_version and id to the query, so we need to add that before comparing
        self.assertEquals(shared[0], self.test)
        self.assertEquals(shared[1], "DELETE")
        self.assertEquals(shared[2], "bob")
        # There should be two WHERE clauses, because AUSTable adds a data_version one in addition
        # to the id condition above.
        self.assertEquals(len(shared[3]._whereclause.get_children()), 2)

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
        # update adds data_version and id to the query, so we need to add that before comparing
        what["data_version"] = 2
        what["id"] = 1
        self.assertEquals(shared[0], self.test)
        self.assertEquals(shared[1], "UPDATE")
        self.assertEquals(shared[2], "bob")
        self.assertEquals(shared[3].parameters, what)
        # There should be two WHERE clauses, because AUSTable adds a data_version one in addition
        # to the id condition above.
        self.assertEquals(len(shared[3]._whereclause.get_children()), 2)


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

    def testHistoryGetChangeWithChangeID(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0

            self.test.insert(changed_by='george', id=4, foo=0)
            ret = self.test.history.getChange(change_id=1)
            self.assertEquals(ret, {u'data_version': None,
                                    u'changed_by': u'george',
                                    u'foo': None, u'timestamp': 999,
                                    u'change_id': 1, u'id': 4})

    def testHistoryGetChangeWithDataVersion(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0

            self.test.insert(changed_by='george', id=4, foo=0)
            ret = self.test.history.getChange(data_version=1,
                                              column_values={'id': 4})
            self.assertEquals(ret, {u'data_version': 1,
                                    u'changed_by': u'george',
                                    u'foo': 0, u'timestamp': 1000,
                                    u'change_id': 2, u'id': 4})

    def testHistoryGetChangeWithDataVersionReturnNone(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0

            self.test.insert(changed_by='george', id=4, foo=0)
            ret = self.test.history.getChange(data_version=1,
                                              column_values={'id': 5})
            self.assertEquals(ret, None)

    def testHistoryGetChangeWithDataVersionWithNonPrimaryKeyColumn(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0

            self.test.insert(changed_by='george', id=4, foo=0)
            self.assertRaises(ValueError, self.test.history.getChange, data_version=1,
                              column_values={'foo': 4})


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

    def testMultiplePrimaryKeyHistoryGetChangeWithDataVersion(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0

            self.test.insert(changed_by='george', id1=4, id2=5, foo=0)
            ret = self.test.history.getChange(data_version=1,
                                              column_values={'id1': 4, 'id2': 5})
            self.assertEquals(ret, {u'data_version': 1,
                                    u'changed_by': u'george',
                                    u'foo': 0, u'timestamp': 1000,
                                    u'change_id': 2, u'id1': 4, u'id2': 5})

    def testMultiplePrimaryKeyHistoryGetChangeWithDataVersionReturnNone(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0

            self.test.insert(changed_by='george', id1=4, id2=5, foo=0)
            ret = self.test.history.getChange(data_version=1,
                                              column_values={'id1': 4,
                                                             'id2': 55})
            self.assertEquals(ret, None)

    def testHistoryGetChangeWithDataVersionWithNonPrimaryKeyColumn(self):
        with mock.patch('time.time') as t:
            t.return_value = 1.0

            self.test.insert(changed_by='george', id1=4, id2=5, foo=0)
            self.assertRaises(ValueError, self.test.history.getChange, data_version=1,
                              column_values={'id1': 4, 'foo': 4})


class ScheduledChangesTableMixin(object):

    def setUp(self):
        self.db = AUSDatabase(self.dburi)
        self.db.create()
        self.engine = self.db.engine
        self.metadata = self.db.metadata

        class TestTable(AUSTable):

            def __init__(self, db, metadata):
                self.table = Table("test_table", metadata, Column("fooid", Integer, primary_key=True, autoincrement=True),
                                   Column("foo", String(15)),
                                   Column("bar", String(15)))
                super(TestTable, self).__init__(db, "sqlite", scheduled_changes=True, history=True, versioned=True)

            def insert(self, changed_by, transaction=None, dryrun=False, **columns):
                if not self.db.hasPermission(changed_by, "test", "create", transaction=transaction):
                    raise PermissionDeniedError("fail")
                if not dryrun:
                    super(TestTable, self).insert(changed_by, transaction, **columns)

            def update(self, where, what, changed_by, old_data_version, transaction=None, dryrun=False):
                # Although our test table doesn't need it, real tables do some extra permission
                # checks based on "where". To make sure we catch bugs around the "where" arg
                # being broken, we use it similarly here.
                for row in self.select(where=where, transaction=transaction):
                    if not self.db.hasPermission(changed_by, "test", "modify", transaction=transaction):
                        raise PermissionDeniedError("fail")
                if not dryrun:
                    super(TestTable, self).update(where, what, changed_by, old_data_version, transaction)

            def delete(self, where, changed_by, old_data_version, transaction=None, dryrun=False):
                if not self.db.hasPermission(changed_by, "test", "delete", transaction=transaction):
                    raise PermissionDeniedError("fail")

                if not dryrun:
                    super(TestTable, self).delete(where, changed_by, old_data_version, transaction)

        self.table = TestTable(self.db, self.metadata)
        self.sc_table = self.table.scheduled_changes
        self.metadata.create_all()
        self.table.t.insert().execute(fooid=1, foo="a", data_version=1)
        self.table.t.insert().execute(fooid=2, foo="b", bar="bb", data_version=2)
        self.table.t.insert().execute(fooid=3, foo="c", data_version=1)
        self.sc_table.t.insert().execute(sc_id=1, when=234, scheduled_by="bob", base_fooid=1, base_foo="aa", base_bar="barbar", base_data_version=1,
                                         data_version=1)
        self.sc_table.t.insert().execute(sc_id=2, when=567, scheduled_by="bob", base_foo="cc", base_bar="ceecee", data_version=1)
        self.sc_table.t.insert().execute(sc_id=3, when=1, scheduled_by="bob", complete=True, base_fooid=2, base_foo="b", base_bar="bb", base_data_version=1,
                                         data_version=1)
        self.sc_table.t.insert().execute(sc_id=4, when=333, scheduled_by="bob", base_fooid=2, base_foo="dd", base_bar="bb", base_data_version=2, data_version=1)
        self.db.permissions.t.insert().execute(permission="admin", username="bob", data_version=1)
        self.db.permissions.t.insert().execute(permission="admin", username="mary", data_version=1)
        self.db.permissions.t.insert().execute(permission="scheduled_change", username="nancy", options='{"actions": ["enact"]}', data_version=1)


class TestScheduledChangesTable(unittest.TestCase, ScheduledChangesTableMixin, MemoryDatabaseMixin):

    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        ScheduledChangesTableMixin.setUp(self)

    def testAllTablesCreated(self):
        self.assertTrue(self.table)
        self.assertTrue(self.table.history)
        self.assertTrue(self.table.scheduled_changes)
        self.assertTrue(self.table.scheduled_changes.history)

    def testSCTableHasAllColumns(self):
        columns = [c.name for c in self.table.scheduled_changes.t.get_children()]
        self.assertTrue("sc_id" in columns)
        self.assertTrue("scheduled_by" in columns)
        self.assertTrue("complete" in columns)
        self.assertTrue("telemetry_product" in columns)
        self.assertTrue("telemetry_channel" in columns)
        self.assertTrue("telemetry_uptake" in columns)
        self.assertTrue("when" in columns)
        self.assertTrue("data_version" in columns)
        self.assertTrue("base_fooid" in columns)
        self.assertTrue("base_foo" in columns)
        self.assertTrue("base_bar" in columns)
        self.assertTrue("base_data_version" in columns)

    def testValidateConditionsNone(self):
        self.assertRaisesRegexp(ValueError, "No conditions found", self.sc_table._validateConditions, {})

    def testValidateConditionsNoneValue(self):
        self.assertRaisesRegexp(ValueError, "No conditions found", self.sc_table._validateConditions, {"when": None})

    def testValdiateConditionsInvalid(self):
        self.assertRaisesRegexp(ValueError, "Invalid condition", self.sc_table._validateConditions, {"blah": "blah"})

    def testValidateConditionsJustWhen(self):
        self.sc_table._validateConditions({"when": 12345678})

    def testValidateConditionsBadWhen(self):
        self.assertRaisesRegexp(ValueError, "Cannot parse", self.sc_table._validateConditions, {"when": "abc"})

    def testValidateConditionsJustTelemetry(self):
        self.sc_table._validateConditions({
            "telemetry_product": "Firefox",
            "telemetry_channel": "nightly",
            "telemetry_uptake": "200000",
        })

    def testValidateConditionsNotAllowedWhenAndOther(self):
        self.assertRaisesRegexp(ValueError, "Invalid combination of conditions", self.sc_table._validateConditions,
                                {"when": "12345", "telemetry_product": "foo"})

    def testValidateConditionsMissingTelemetryValue(self):
        self.assertRaisesRegexp(ValueError, "Invalid combination of conditions", self.sc_table._validateConditions, {"telemetry_product": "foo"})

    def testInsertForExistingRow(self):
        what = {"fooid": 2, "foo": "thing", "bar": "thing2", "data_version": 2, "when": 999}
        self.sc_table.insert(changed_by="bob", **what)
        row = self.sc_table.t.select().where(self.sc_table.sc_id == 5).execute().fetchall()[0]
        self.assertEquals(row.scheduled_by, "bob")
        self.assertEquals(row.when, 999)
        self.assertEquals(row.data_version, 1)
        self.assertEquals(row.base_fooid, 2)
        self.assertEquals(row.base_foo, "thing")
        self.assertEquals(row.base_bar, "thing2")
        self.assertEquals(row.base_data_version, 2)

    def testInsertForNewRow(self):
        what = {"foo": "newthing1", "when": 888}
        self.sc_table.insert(changed_by="bob", **what)
        row = self.sc_table.t.select().where(self.sc_table.sc_id == 5).execute().fetchall()[0]
        self.assertEquals(row.scheduled_by, "bob")
        self.assertEquals(row.when, 888)
        self.assertEquals(row.data_version, 1)
        self.assertEquals(row.base_fooid, None)
        self.assertEquals(row.base_foo, "newthing1")
        self.assertEquals(row.base_bar, None)
        self.assertEquals(row.base_data_version, None)

    def testInsertWithNonAutoincrement(self):
        class TestTable2(AUSTable):

            def __init__(self, db, metadata):
                self.table = Table("test_table2", metadata, Column("foo_name", String(15), primary_key=True),
                                   Column("foo", String(15)),
                                   Column("bar", String(15)))
                super(TestTable2, self).__init__(db, "sqlite", scheduled_changes=True, history=True, versioned=True)

        table = TestTable2(self.db, self.metadata)
        self.metadata.create_all()
        what = {"foo_name": "i'm a foo", "foo": "123", "bar": "456", "when": 876}
        table.scheduled_changes.insert(changed_by="mary", **what)
        row = table.scheduled_changes.t.select().where(table.scheduled_changes.sc_id == 1).execute().fetchall()[0]
        self.assertEquals(row.scheduled_by, "mary")
        self.assertEquals(row.when, 876)
        self.assertEquals(row.data_version, 1)
        self.assertEquals(row.base_foo_name, "i'm a foo")
        self.assertEquals(row.base_foo, "123")
        self.assertEquals(row.base_bar, "456")
        self.assertEquals(row.base_data_version, None)

    def testInsertForExistingNoSuchRow(self):
        what = {"fooid": 10, "foo": "thing", "data_version": 1, "when": 999}
        self.assertRaisesRegexp(ValueError, "Cannot create scheduled change with data_version for non-existent row", self.sc_table.insert, changed_by="bob",
                                **what)

    def testInsertMissingRequiredPartOfPK(self):
        class TestTable2(AUSTable):

            def __init__(self, db, metadata):
                self.table = Table("test_table2", metadata, Column("fooid", Integer, primary_key=True, autoincrement=True),
                                   Column("foo", String(15), primary_key=True),
                                   Column("bar", String(15)))
                super(TestTable2, self).__init__(db, "sqlite", scheduled_changes=True, history=True, versioned=True)

        table = TestTable2("fake", self.metadata)
        self.metadata.create_all()
        what = {"fooid": 2, "when": 4532}
        self.assertRaisesRegexp(ValueError, "Missing primary key column", table.scheduled_changes.insert, changed_by="bob", **what)

    def testInsertWithIncompatibleConditions(self):
        what = {"foo": "blah", "when": "abc"}
        self.assertRaisesRegexp(ValueError, "Cannot parse", self.sc_table.insert, changed_by="bob", **what)

    def testInsertDataVersionChanged(self):
        """Tests to make sure a scheduled change update is rejected if data
        version changes between grabbing the row to create a change, and
        submitting the scheduled change."""
        self.table.update([self.table.fooid == 3], what={"foo": "bb"}, changed_by="bob", old_data_version=1)
        what = {"fooid": 3, "data_version": 1, "bar": "blah", "when": 456}
        self.assertRaises(OutdatedDataError, self.sc_table.insert, changed_by="bob", **what)

    def testInsertWithoutPermissionOnBaseTable(self):
        what = {"fooid": 4, "bar": "blah", "when": 343}
        self.assertRaises(PermissionDeniedError, self.sc_table.insert, changed_by="nancy", **what)

    def testInsertWithoutPermissionOnBaseTableForUpdate(self):
        what = {"fooid": 3, "bar": "blah", "when": 343, "data_version": 1}
        self.assertRaises(PermissionDeniedError, self.sc_table.insert, changed_by="nancy", **what)

    def testUpdateNoChangesSinceCreation(self):
        where = [self.sc_table.sc_id == 1]
        what = {"when": 888, "foo": "bb"}
        self.sc_table.update(where, what, changed_by="bob", old_data_version=1)
        row = self.sc_table.t.select().where(self.sc_table.sc_id == 1).execute().fetchall()[0]
        history_row = self.sc_table.history.t.select().where(self.sc_table.history.sc_id == 1).execute().fetchall()[0]
        self.assertEquals(row.scheduled_by, "bob")
        self.assertEquals(row.when, 888)
        self.assertEquals(row.data_version, 2)
        self.assertEquals(row.base_fooid, 1)
        self.assertEquals(row.base_foo, "bb")
        self.assertEquals(row.base_bar, "barbar")
        self.assertEquals(row.base_data_version, 1)
        self.assertEquals(history_row.changed_by, "bob")
        self.assertEquals(history_row.scheduled_by, "bob")
        self.assertEquals(history_row.when, 888)
        self.assertEquals(history_row.data_version, 2)
        self.assertEquals(history_row.base_fooid, 1)
        self.assertEquals(history_row.base_foo, "bb")
        self.assertEquals(history_row.base_bar, "barbar")
        self.assertEquals(history_row.base_data_version, 1)

    def testUpdateNoChangesSinceCreationWithDict(self):
        where = {"sc_id": 1}
        what = {"when": 888, "foo": "bb", "data_version": 1, "fooid": 1}
        self.sc_table.update(where, what, changed_by="bob", old_data_version=1)
        row = self.sc_table.t.select().where(self.sc_table.sc_id == 1).execute().fetchall()[0]
        history_row = self.sc_table.history.t.select().where(self.sc_table.history.sc_id == 1).execute().fetchall()[0]
        self.assertEquals(row.scheduled_by, "bob")
        self.assertEquals(row.when, 888)
        self.assertEquals(row.data_version, 2)
        self.assertEquals(row.base_fooid, 1)
        self.assertEquals(row.base_foo, "bb")
        self.assertEquals(row.base_bar, "barbar")
        self.assertEquals(row.base_data_version, 1)
        self.assertEquals(history_row.changed_by, "bob")
        self.assertEquals(history_row.scheduled_by, "bob")
        self.assertEquals(history_row.when, 888)
        self.assertEquals(history_row.data_version, 2)
        self.assertEquals(history_row.base_fooid, 1)
        self.assertEquals(history_row.base_foo, "bb")
        self.assertEquals(history_row.base_bar, "barbar")
        self.assertEquals(history_row.base_data_version, 1)

    def testUpdateWithBadConditions(self):
        where = [self.sc_table.sc_id == 1]
        what = {"telemetry_product": "boop", "telemetry_channel": "boop", "telemetry_uptake": 99}
        self.assertRaisesRegexp(ValueError, "Invalid combination of conditions", self.sc_table.update, where, what, changed_by="bob", old_data_version=1)

    def testUpdateRemoveConditions(self):
        where = [self.sc_table.sc_id == 2]
        what = {"when": None}
        self.assertRaisesRegexp(ValueError, "No conditions found", self.sc_table.update, where, what, changed_by="bob", old_data_version=1)

    def testUpdateWithoutPermissionOnBaseTable(self):
        with mock.patch.object(self.sc_table.db, "hasPermission", return_value=False, create=True):
            where = [self.sc_table.sc_id == 2]
            what = {"when": 777}
            self.assertRaises(PermissionDeniedError, self.sc_table.update, where, what, changed_by="sue", old_data_version=1)

    def testUpdateBaseTableNoConflictWithChanges(self):
        """Tests to make sure a scheduled change is properly updated when an
        UPDATE is made to the row the scheduled change is for."""
        # fooid 2 has a change scheduled that would update its "foo" column
        # we'll change "bar" underneath it. This doesn't conflict with the
        # scheduled change, so it should simply be updated with the new "bar"
        # value.
        self.table.update([self.table.fooid == 2], what={"bar": "bar"}, changed_by="bob", old_data_version=2)
        row = self.table.t.select().where(self.table.fooid == 2).execute().fetchall()[0]
        sc_row = self.sc_table.t.select().where(self.sc_table.sc_id == 4).execute().fetchall()[0]
        history_row = self.sc_table.history.t.select().where(self.sc_table.history.sc_id == 4).execute().fetchall()[0]
        self.assertEquals(row.fooid, 2)
        self.assertEquals(row.foo, "b")
        self.assertEquals(row.bar, "bar")
        self.assertEquals(row.data_version, 3)
        # This should end up with the scheduled changed incorporating our new
        # value for "foo" as well as the new "bar" value.
        self.assertEquals(sc_row.scheduled_by, "bob")
        self.assertEquals(sc_row.when, 333)
        self.assertEquals(sc_row.data_version, 2)
        self.assertEquals(sc_row.base_fooid, 2)
        self.assertEquals(sc_row.base_foo, "dd")
        self.assertEquals(sc_row.base_bar, "bar")
        self.assertEquals(sc_row.base_data_version, 3)
        # ...As well as a new history table entry.
        self.assertEquals(history_row.changed_by, "bob")
        self.assertEquals(history_row.scheduled_by, "bob")
        self.assertEquals(history_row.when, 333)
        self.assertEquals(history_row.data_version, 2)
        self.assertEquals(history_row.base_fooid, 2)
        self.assertEquals(history_row.base_foo, "dd")
        self.assertEquals(history_row.base_bar, "bar")
        self.assertEquals(history_row.base_data_version, 3)

    def testUpdateBaseTableConflictWithRecentChanges(self):
        where = [self.table.fooid == 1]
        what = {"bar": "bar"}
        self.assertRaises(UpdateMergeError, self.table.update, where=where, what=what, changed_by="bob", old_data_version=1)

    def testDeleteChange(self):
        self.sc_table.delete(where=[self.sc_table.sc_id == 2], changed_by="bob", old_data_version=1)
        ret = self.sc_table.t.select().where(self.sc_table.sc_id == 2).execute().fetchall()
        self.assertEquals(len(ret), 0)

    def testDeleteChangeWithoutPermission(self):
        self.assertRaises(PermissionDeniedError, self.sc_table.delete, where=[self.sc_table.sc_id == 2], changed_by="nicole", old_data_version=1)

    def testBaseTableDeletesFailsWithScheduledChange(self):
        self.assertRaises(UpdateMergeError, self.table.delete, where=[self.table.fooid == 2], changed_by="bob", old_data_version=2)

    def testEnactChangeNewRow(self):
        self.table.scheduled_changes.enactChange(2, "nancy")
        row = self.table.t.select().where(self.table.fooid == 4).execute().fetchall()[0]
        history_rows = self.table.history.t.select().where(self.table.history.fooid == 4).execute().fetchall()
        sc_row = self.sc_table.t.select().where(self.sc_table.sc_id == 2).execute().fetchall()[0]
        self.assertEquals(row.fooid, 4)
        self.assertEquals(row.foo, "cc")
        self.assertEquals(row.bar, "ceecee")
        self.assertEquals(row.data_version, 1)
        self.assertEquals(history_rows[0].fooid, 4)
        self.assertEquals(history_rows[0].foo, None)
        self.assertEquals(history_rows[0].bar, None)
        self.assertEquals(history_rows[0].changed_by, "bob")
        self.assertEquals(history_rows[0].data_version, None)
        self.assertEquals(history_rows[1].fooid, 4)
        self.assertEquals(history_rows[1].foo, "cc")
        self.assertEquals(history_rows[1].bar, "ceecee")
        self.assertEquals(history_rows[1].changed_by, "bob")
        self.assertEquals(history_rows[1].data_version, 1)
        self.assertEquals(sc_row.complete, True)

    def testEnactChangeExistingRow(self):
        self.table.scheduled_changes.enactChange(1, "nancy")
        row = self.table.t.select().where(self.table.fooid == 1).execute().fetchall()[0]
        history_row = self.table.history.t.select().where(self.table.history.fooid == 1).where(self.table.history.data_version == 2).execute().fetchall()[0]
        sc_row = self.sc_table.t.select().where(self.sc_table.sc_id == 1).execute().fetchall()[0]
        self.assertEquals(row.foo, "aa")
        self.assertEquals(row.bar, "barbar")
        self.assertEquals(row.data_version, 2)
        self.assertEquals(history_row.foo, "aa")
        self.assertEquals(history_row.bar, "barbar")
        self.assertEquals(history_row.changed_by, "bob")
        self.assertEquals(history_row.data_version, 2)
        self.assertEquals(sc_row.complete, True)

    def testEnactChangeNoPermissions(self):
        # TODO: May want to add something to permissions api/ui that warns if a user has a scheduled change when changing their permissions
        self.assertRaises(PermissionDeniedError, self.table.scheduled_changes.enactChange, 1, "jeremy")

    def testMergeUpdateNoConflict(self):
        old_row = self.table.select(where=[self.table.fooid == 2])[0]
        what = {"fooid": 2, "bar": "bar", "data_version": 3}
        self.sc_table.mergeUpdate(old_row, what, changed_by="bob")
        sc_row = self.sc_table.t.select().where(self.sc_table.sc_id == 4).execute().fetchall()[0]
        self.assertEquals(sc_row.base_foo, "dd")
        self.assertEquals(sc_row.base_bar, "bar")
        self.assertEquals(sc_row.base_data_version, 3)

    def testMergeUpdateNoConflictChangingToNull(self):
        old_row = self.table.select(where=[self.table.fooid == 2])[0]
        what = {"fooid": 2, "bar": None, "data_version": 3}
        self.sc_table.mergeUpdate(old_row, what, changed_by="bob")
        sc_row = self.sc_table.t.select().where(self.sc_table.sc_id == 4).execute().fetchall()[0]
        self.assertEquals(sc_row.base_foo, "dd")
        self.assertEquals(sc_row.base_bar, None)
        self.assertEquals(sc_row.base_data_version, 3)

    def testMergeUpdateWithConflict(self):
        old_row = self.table.select(where=[self.table.fooid == 1])[0]
        what = {"fooid": 1, "bar": "abc", "data_version": 1}
        self.assertRaises(UpdateMergeError, self.sc_table.mergeUpdate, old_row, what, changed_by="bob")


class TestSampleData(unittest.TestCase, MemoryDatabaseMixin):
    """Tests to ensure that the current sample data (used by Docker) is
    compatible with the current schema."""
    sample_data = path.join(path.dirname(__file__), "..", "..", "scripts", "sample-data.sql")

    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.db.create()

    def testSampleDataImport(self):
        with self.db.begin() as trans:
            with open(self.sample_data) as f:
                for q in f:
                    trans.execute(q)


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
        self.paths.t.insert().execute(rule_id=1, priority=100, version='3.5', buildTarget='d', backgroundRate=100, mapping='c', update_type='z', data_version=1)
        self.paths.t.insert().execute(rule_id=2, priority=100, version='3.3', buildTarget='d', backgroundRate=100, mapping='b', update_type='z', data_version=1)
        self.paths.t.insert().execute(rule_id=3, priority=100, version='3.5', buildTarget='a', backgroundRate=100, mapping='a', update_type='z', data_version=1)
        self.paths.t.insert().execute(rule_id=4, alias="gandalf", priority=80, buildTarget='d', backgroundRate=100, mapping='a', update_type='z',
                                      data_version=1)
        self.paths.t.insert().execute(rule_id=5, priority=80, buildTarget='d', version='3.3', backgroundRate=0, mapping='c', update_type='z', data_version=1)
        self.paths.t.insert().execute(rule_id=6, priority=100, buildTarget='d', mapping='a', backgroundRate=100, osVersion='foo 1', update_type='z',
                                      data_version=1)
        self.paths.t.insert().execute(
            rule_id=7, priority=100, buildTarget='d', mapping='a', backgroundRate=100, osVersion='foo 2,blah 6', update_type='z', data_version=1)
        self.paths.t.insert().execute(
            rule_id=8, priority=100, buildTarget='e', mapping='d', backgroundRate=100, locale='foo,bar-baz', update_type='z', data_version=1)
        self.paths.t.insert().execute(rule_id=9, priority=100, buildTarget="f", mapping="f", backgroundRate=100, systemCapabilities="S", update_type="z",
                                      data_version=1)
        self.db.permissions.t.insert().execute(permission="admin", username="bill", data_version=1)

    def testGetOrderedRules(self):
        rules = self._stripNullColumns(self.paths.getOrderedRules())
        expected = [
            dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget='d', mapping='a', update_type='z', data_version=1),
            dict(rule_id=5, priority=80, backgroundRate=0, version='3.3', buildTarget='d', mapping='c', update_type='z', data_version=1),
            dict(rule_id=6, priority=100, buildTarget='d', mapping='a', backgroundRate=100, osVersion='foo 1', update_type='z', data_version=1),
            dict(rule_id=7, priority=100, buildTarget='d', mapping='a', backgroundRate=100, osVersion='foo 2,blah 6', update_type='z', data_version=1),
            dict(rule_id=8, priority=100, buildTarget='e', mapping='d', backgroundRate=100, locale='foo,bar-baz', update_type='z', data_version=1),
            dict(rule_id=9, priority=100, buildTarget="f", mapping="f", backgroundRate=100, systemCapabilities="S", update_type="z", data_version=1),
            dict(rule_id=2, priority=100, backgroundRate=100, version='3.3', buildTarget='d', mapping='b', update_type='z', data_version=1),
            dict(rule_id=3, priority=100, backgroundRate=100, version='3.5', buildTarget='a', mapping='a', update_type='z', data_version=1),
            dict(rule_id=1, priority=100, backgroundRate=100, version='3.5', buildTarget='d', mapping='c', update_type='z', data_version=1),
        ]
        self.assertEquals(rules, expected)

    def testGetRulesMatchingQuery(self):
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

    def testGetRulesMatchingQuerySystemCapabilities(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(product="", version="5.0", channel="", buildTarget="f",
                 buildID="", locale="", osVersion="", distribution="",
                 distVersion="", headerArchitecture="", force=False,
                 queryVersion=6, systemCapabilities="S"
                 ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(rule_id=9, priority=100, buildTarget="f", mapping="f", backgroundRate=100, systemCapabilities="S", update_type="z", data_version=1),
        ]
        self.assertEquals(rules, expected)

    def testGetRulesMatchingQuerySystemCapabilitiesNoSubstringMatch(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(product="", version="5.0", channel="", buildTarget="f",
                 buildID="", locale="", osVersion="", distribution="",
                 distVersion="", headerArchitecture="", force=False,
                 queryVersion=6, systemCapabilities="SA"
                 ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        self.assertEquals(rules, [])

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
        rule_id = self.paths.insert(changed_by='bill', **what)
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
        self.paths.update(where={"rule_id": 1}, what=what, changed_by="bill", old_data_version=1)

        rules = self.paths.t.select().where(self.paths.rule_id == 1).execute().fetchall()
        copy_rule = dict(rules[0].items())
        rule = self._stripNullColumns([copy_rule])

        expected = [dict(rule_id=1, priority=100, backgroundRate=100, version='3.5', buildTarget='d', mapping='d', update_type='z', data_version=2)]
        self.assertEquals(rule, expected)

    def testUpdateRuleByAlias(self):
        rules = self.paths.t.select().where(self.paths.rule_id == 4).execute().fetchall()
        what = dict(rules[0].items())

        what['mapping'] = 'd'
        self.paths.update(where={"rule_id": "gandalf"}, what=what, changed_by="bill", old_data_version=1)

        rules = self.paths.t.select().where(self.paths.rule_id == 4).execute().fetchall()
        copy_rule = dict(rules[0].items())
        rule = self._stripNullColumns([copy_rule])

        expected = [dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget='d', mapping='d', update_type='z', data_version=2)]
        self.assertEquals(rule, expected)

    def testDeleteRule(self):
        self.paths.delete({"rule_id": 2}, changed_by="bill", old_data_version=1)
        rule = self.paths.t.select().where(self.paths.rule_id == 2).execute().fetchall()
        self.assertEquals(rule, [])

    def testDeleteRuleByAlias(self):
        self.paths.delete({"rule_id": "gandalf"}, changed_by="bill", old_data_version=1)
        rule = self.paths.t.select().where(self.paths.rule_id == 4).execute().fetchall()
        self.assertEquals(rule, [])

    def testGetNumberOfRules(self):
        self.assertEquals(self.paths.countRules(), 9)


class TestRulesSpecial(unittest.TestCase, RulesTestMixin, MemoryDatabaseMixin):

    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.db.create()
        self.rules = self.db.rules
        self.rules.t.insert().execute(rule_id=1, priority=100, version='>=4.0b1', backgroundRate=100, update_type='z', data_version=1)
        self.rules.t.insert().execute(rule_id=2, priority=100, channel='release*', backgroundRate=100, update_type='z', data_version=1)
        self.rules.t.insert().execute(rule_id=3, priority=100, buildID='>=20010101222222', backgroundRate=100, update_type='z', data_version=1)

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
        dbo.setDb(self.dburi)
        dbo.create()
        self.rules = dbo.rules
        self.releases = dbo.releases
        self.permissions = dbo.permissions
        self.releases.t.insert().execute(name='a', product='a', data=json.dumps(dict(name="a", schema_version=1, hashFunction="sha512")),
                                         data_version=1)
        self.releases.t.insert().execute(name='ab', product='a', data=json.dumps(dict(name="ab", schema_version=1, hashFunction="sha512")),
                                         data_version=1)
        self.releases.t.insert().execute(name='b', product='b', data=json.dumps(dict(name="b", schema_version=1, hashFunction="sha512")),
                                         data_version=1)
        self.releases.t.insert().execute(name='c', product='c', data=json.dumps(dict(name="c", schema_version=1, hashFunction="sha512")),
                                         data_version=1)
        self.permissions.t.insert().execute(permission="admin", username="bill", data_version=1)
        self.permissions.t.insert().execute(permission="admin", username="me", data_version=1)
        self.permissions.t.insert().execute(permission="release", username="bob", options=json.dumps(dict(products=["c"])), data_version=1)

    def tearDown(self):
        dbo.reset()

    def testGetReleases(self):
        self.assertEquals(len(self.releases.getReleases()), 4)

    def testGetReleasesWithLimit(self):
        self.assertEquals(len(self.releases.getReleases(limit=1)), 1)

    def testGetReleasesWithWhere(self):
        expected = [dict(product='b', name='b', data=dict(name="b", schema_version=1, hashFunction="sha512"), data_version=1)]
        self.assertEquals(self.releases.getReleases(name='b'), expected)

    def testGetReleaseBlob(self):
        expected = dict(name="c", schema_version=1, hashFunction="sha512")
        self.assertEquals(self.releases.getReleaseBlob(name='c'), expected)

    def testGetReleaseBlobNonExistentRelease(self):
        self.assertRaises(KeyError, self.releases.getReleaseBlob, name='z')

    def testGetReleaseInfoAll(self):
        releases = self.releases.getReleaseInfo()
        expected = [dict(name='a', product='a', data_version=1, read_only=False, rule_ids=[]),
                    dict(name='ab', product='a', data_version=1, read_only=False, rule_ids=[]),
                    dict(name='b', product='b', data_version=1, read_only=False, rule_ids=[]),
                    dict(name='c', product='c', data_version=1, read_only=False, rule_ids=[])]
        self.assertEquals(releases, expected)

    def testGetReleaseInfoProduct(self):
        releases = self.releases.getReleaseInfo(product='a')
        expected = [dict(name='a', product='a', data_version=1, read_only=False, rule_ids=[]),
                    dict(name='ab', product='a', data_version=1, read_only=False, rule_ids=[])]
        self.assertEquals(releases, expected)

    def testGetReleaseInfoNoMatch(self):
        releases = self.releases.getReleaseInfo(product='ue')
        expected = []
        self.assertEquals(releases, expected)

    def testGetReleaseInfoNamePrefix(self):
        releases = self.releases.getReleaseInfo(name_prefix='a')
        expected = [dict(name='a', product='a', data_version=1, read_only=False, rule_ids=[]),
                    dict(name='ab', product='a', data_version=1, read_only=False, rule_ids=[])]
        self.assertEquals(releases, expected)

    def testGetReleaseInfoNamePrefixNameOnly(self):
        releases = self.releases.getReleaseInfo(name_prefix='a', nameOnly=True)
        expected = [{'name': 'a'}, {'name': 'ab'}]
        self.assertEquals(releases, expected)

    def testPresentRuleIdField(self):
        releases = self.releases.getReleaseInfo()
        self.assertTrue('rule_ids' in releases[0])

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

    def testGetReleaseNamesNoMatch(self):
        releases = self.releases.getReleaseNames(product='oo')
        expected = []
        self.assertEquals(releases, expected)

    def testGetNumberOfReleases(self):
        # because 4 releases were set up in the setUp()
        self.assertEquals(self.releases.countReleases(), 4)

    def testDeleteRelease(self):
        self.releases.delete({"name": "a"}, changed_by="bill", old_data_version=1)
        release = self.releases.t.select().where(self.releases.name == 'a').execute().fetchall()
        self.assertEquals(release, [])

    def testDeleteReleaseWhenReadOnly(self):
        self.releases.t.update(values=dict(read_only=True, data_version=2)).where(self.releases.name == "a").execute()
        self.assertRaises(ReadOnlyError, self.releases.delete, {"name": "a"}, changed_by='me', old_data_version=2)

    def testAddReleaseWithNameMismatch(self):
        blob = ReleaseBlobV1(name="f", schema_version=1, hashFunction="sha512")
        self.assertRaises(ValueError, self.releases.insert, "bill", name="g", product="g", data=blob)

    def testUpdateReleaseNoPermissionForNewProduct(self):
        self.assertRaises(PermissionDeniedError, self.releases.update, {"name": "c"}, {"product": "d"}, "bob", 1)

    def testUpdateReleaseWithNameMismatch(self):
        newBlob = ReleaseBlobV1(name="c", schema_version=1, hashFunction="sha512")
        self.assertRaises(ValueError, self.releases.update, {"name": "a"}, {"data": newBlob}, "bill", 1)

    def testUpdateReleaseChangeReadOnly(self):
        self.releases.t.update(values=dict(read_only=True, data_version=2)).where(self.releases.name == "a").execute()
        self.assertEqual(select([self.releases.read_only]).where(self.releases.name == 'a').execute().fetchone()[0], True)

    def testUpdateReleaseNoPermissionToSetReadOnly(self):
        self.assertRaises(PermissionDeniedError, self.releases.update, {"name": "c"}, {"read_only": True}, "bob", 1)

    def testIsReadOnly(self):
        self.releases.t.update(values=dict(read_only=True, data_version=2)).where(self.releases.name == "a").execute()
        self.assertEqual(self.releases.isReadOnly('a'), True)

    def testProceedIfNotReadOnly(self):
        self.releases.t.update(values=dict(read_only=True, data_version=2)).where(self.releases.name == "a").execute()
        self.assertRaises(ReadOnlyError, self.releases._proceedIfNotReadOnly, 'a')


class TestBlobCaching(unittest.TestCase, MemoryDatabaseMixin):

    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        cache.reset()
        cache.make_copies = True
        cache.make_cache("blob", 10, 10)
        cache.make_cache("blob_version", 10, 4)
        self.db = AUSDatabase(self.dburi)
        self.db.create()
        self.releases = self.db.releases
        self.releases.t.insert().execute(name='a', product='a', data=json.dumps(dict(name="a", schema_version=1, hashFunction="sha512")),
                                         data_version=1)
        self.releases.t.insert().execute(name='b', product='b', data=json.dumps(dict(name="b", schema_version=1, hashFunction="sha512")),
                                         data_version=1)
        self.db.permissions.t.insert().execute(permission="admin", username="bill", data_version=1)
        self.db.permissions.t.insert().execute(permission="admin", username="bob", data_version=1)
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
            self.releases.update({"name": "b"}, {"data": newBlob}, "bob", 1)

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
            # update doesn't affect the stats at all (but it updates
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
            self.releases.insert(
                changed_by="bill",
                name="abc",
                product="bbb",
                data=ReleaseBlobV1(name="abc", schema_version=1, hashFunction="sha512"),
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
            self.releases.delete({"name": "b"}, changed_by="bob", old_data_version=1)
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
            self.releases.addLocaleToRelease("b", "b", "win", "zu", dict(buildID=123), 1, "bob")
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
        self.releases.t.insert().execute(name='a', product='a', data_version=1, data="""
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
        self.releases.t.insert().execute(name='b', product='b', data_version=1, data="""
{
    "name": "b",
    "hashFunction": "sha512",
    "schema_version": 1
}
""")
        self.db.permissions.t.insert().execute(permission="admin", username="bill", data_version=1)
        self.db.permissions.t.insert().execute(permission="admin", username="me", data_version=1)

    def testAddRelease(self):
        blob = ReleaseBlobV1(name="d", hashFunction="sha512")
        self.releases.insert(changed_by="bill", name='d', product='d', data=blob)
        expected = [('d', 'd', False, json.dumps(dict(name="d", schema_version=1, hashFunction="sha512")), 1)]
        self.assertEquals(self.releases.t.select().where(self.releases.name == 'd').execute().fetchall(), expected)

    def testAddReleaseAlreadyExists(self):
        blob = ReleaseBlobV1(name="a", hashFunction="sha512")
        self.assertRaises(TransactionError, self.releases.insert, changed_by="bill", name='a', product='a', data=blob)

    def testUpdateRelease(self):
        blob = ReleaseBlobV1(name='a', hashFunction="sha512")
        self.releases.update({"name": "a"}, {"product": "z", "data": blob}, "bill", 1)
        expected = [('a', 'z', False, json.dumps(dict(name='a', schema_version=1, hashFunction="sha512")), 2)]
        self.assertEquals(self.releases.t.select().where(self.releases.name == 'a').execute().fetchall(), expected)

    def testUpdateReleaseWhenReadOnly(self):
        blob = ReleaseBlobV1(name='a', hashFunction="sha512")
        # set release 'a' to read-only
        self.releases.t.update(values=dict(read_only=True, data_version=2)).where(self.releases.name == "a").execute()
        self.assertRaises(ReadOnlyError, self.releases.update, {"name": "a"}, {"product": "z", "data": blob}, "me", 2)

    def testUpdateReleaseWithBlob(self):
        blob = ReleaseBlobV1(name='b', schema_version=1, hashFunction="sha512")
        self.releases.update({"name": "b"}, {"product": "z", "data": blob}, "bill", 1)
        expected = [('b', 'z', False, json.dumps(dict(name='b', schema_version=1, hashFunction="sha512")), 2)]
        self.assertEquals(self.releases.t.select().where(self.releases.name == 'b').execute().fetchall(), expected)

    def testUpdateReleaseInvalidBlob(self):
        blob = ReleaseBlobV1(name="2", hashFunction="sha512")
        blob['foo'] = 'bar'
        self.assertRaises(BlobValidationError, self.releases.update, where={"name": "b"}, what={"data": blob}, changed_by='bill', old_data_version=1)

    def testAddLocaleToRelease(self):
        data = {
            "complete": {
                "filesize": 1,
                "from": "*",
                "hashValue": "abc",
            }
        }
        self.releases.addLocaleToRelease(name='a', product='a', platform='p', locale='c', data=data, old_data_version=1, changed_by='bill')
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
        self.releases.addLocaleToRelease(name='a', product='a', platform='p', locale='c', data=data, old_data_version=1, changed_by='bill', alias=['p4'])
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
        self.releases.addLocaleToRelease(name='a', product='a', platform='p', locale='l', data=data, old_data_version=1, changed_by='bill')
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
        self.releases.addLocaleToRelease(name='b', product='b', platform='q', locale='l', data=data, old_data_version=1, changed_by='bill')
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
        self.releases.addLocaleToRelease(name='a', product='a', platform='p3', locale='l', data=data, old_data_version=1, changed_by='bill')
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
        self.releases.addLocaleToRelease(name='a', product='a', platform='q', locale='l', data=data, old_data_version=1, changed_by='bill')
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
        self.releases.addLocaleToRelease(name='a', product='a', platform='p2', locale='j', data=data, old_data_version=1, changed_by='bill')
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

    def testAddLocaleWhenReadOnly(self):
        data = {
            "complete": {
                "filesize": 1,
                "from": "*",
                "hashValue": "abc",
            }
        }
        self.releases.t.update(values=dict(read_only=True, data_version=2)).where(self.releases.name == "a").execute()
        self.assertRaises(ReadOnlyError, self.releases.addLocaleToRelease, name='a', product='a', platform='p', locale='c', data=data, old_data_version=1,
                          changed_by='bill')


class TestPermissions(unittest.TestCase, MemoryDatabaseMixin):

    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.db.create()
        self.permissions = self.db.permissions
        self.permissions.t.insert().execute(permission='admin', username='bill', data_version=1)
        self.permissions.t.insert().execute(permission="permission", username="bob", data_version=1)
        self.permissions.t.insert().execute(permission="release", username="bob", options=json.dumps(dict(products=["fake"])), data_version=1)
        self.permissions.t.insert().execute(permission="rule", username="cathy", data_version=1)
        self.permissions.t.insert().execute(permission="rule", username="bob", options=json.dumps(dict(actions=["modify"])), data_version=1)
        self.permissions.t.insert().execute(permission="rule", username="fred", options=json.dumps(dict(products=["foo", "bar"], actions=["modify"])),
                                            data_version=1)

    def testGrantPermissions(self):
        query = self.permissions.t.select().where(self.permissions.username == "jess")
        self.assertEquals(len(query.execute().fetchall()), 0)
        self.permissions.insert("bob", username="jess", permission="rule")
        self.assertEquals(query.execute().fetchall(), [("rule", "jess", None, 1)])

    def testGrantPermissionsWithOptions(self):
        self.permissions.insert("bob", username="cathy", permission="release", options=dict(products=["SeaMonkey"]))
        query = self.permissions.t.select().where(self.permissions.username == "cathy")
        query = query.where(self.permissions.permission == "release")
        self.assertEquals(query.execute().fetchall(), [("release", "cathy", json.dumps(dict(products=["SeaMonkey"])), 1)])

    def testGrantPermissionsUnknownPermission(self):
        self.assertRaises(ValueError, self.permissions.insert, changed_by="bob", username="bud", permission="bad")

    def testGrantPermissionsUnknownOption(self):
        self.assertRaises(ValueError, self.permissions.insert, changed_by="bob", username="bud", permission="rule",
                          options=dict(foo=1))

    def testRevokePermission(self):
        self.permissions.delete({"username": "bob", "permission": "release"}, changed_by="bill", old_data_version=1)
        query = self.permissions.t.select().where(self.permissions.username == "bob")
        query = query.where(self.permissions.permission == "release")
        self.assertEquals(len(query.execute().fetchall()), 0)

    def testGetAllUsers(self):
        self.assertEquals(set(self.permissions.getAllUsers()), set(["bill", "bob", "cathy", "fred"]))

    def testCountAllUsers(self):
        # bill, bob and cathy
        self.assertEquals(self.permissions.countAllUsers(), 4)

    def testGetPermission(self):
        expected = {
            "permission": "release",
            "username": "bob",
            "options": dict(products=["fake"]),
            "data_version": 1
        }
        self.assertEquals(self.permissions.getPermission("bob", "release"), expected)

    def testGetPermissionNonExistant(self):
        self.assertEquals(self.permissions.getPermission("cathy", "release"), {})

    def testGetUserPermissions(self):
        expected = {"permission": dict(options=None, data_version=1),
                    "release": dict(options=dict(products=["fake"]), data_version=1),
                    "rule": dict(options=dict(actions=["modify"]), data_version=1)}
        self.assertEquals(self.permissions.getUserPermissions("bob"), expected)

    def testGetOptions(self):
        expected = dict(products=["fake"])
        self.assertEquals(self.permissions.getOptions("bob", "release"), expected)

    def testGetOptionsPermissionDoesntExist(self):
        self.assertRaises(ValueError, self.permissions.getOptions, "fake", "fake")

    def testGetOptionsNoOptions(self):
        self.assertEquals(self.permissions.getOptions("cathy", "rule"), {})

    def testHasPermissionAdmin(self):
        self.assertTrue(self.permissions.hasPermission("bill", "rule", "delete"))

    def testHasPermissionGranular(self):
        self.assertTrue(self.permissions.hasPermission("cathy", "rule", "create"))

    def testHasPermissionWithDbOption(self):
        self.assertTrue(self.permissions.hasPermission("bob", "rule", "modify"))

    def testHasPermissionWithOption(self):
        self.assertTrue(self.permissions.hasPermission("bob", "release", "create", "fake"))

    def testHasPermissionWithUrlOptionMulti(self):
        self.assertTrue(self.permissions.hasPermission("fred", "rule", "modify", "foo"))
        self.assertTrue(self.permissions.hasPermission("fred", "rule", "modify", "bar"))

    def testHasPermissionNotAllowed(self):
        self.assertFalse(self.permissions.hasPermission("cathy", "release", "modify"))

    def testHasPermissionNotAllowedByAction(self):
        self.assertFalse(self.permissions.hasPermission("bob", "rule", "delete"))

    def testHasPermissionNotAllowedByProduct(self):
        self.assertFalse(self.permissions.hasPermission("bob", "release", "modify", "reallyfake"))


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


class PartialString(str):
    """Super hacky way to do partial string matches in mock's assert_called_with, because
    it doesn't provide a way to access individual arguments of a call."""

    def __eq__(self, other):
        return self in other

    def __repr__(self):
        return "Partial string of: '%s'" % self


class TestChangeNotifiers(unittest.TestCase):

    def setUp(self):
        self.db = AUSDatabase('sqlite:///:memory:')
        self.db.create()
        self.db.rules.t.insert().execute(rule_id=2, priority=100, channel='release', backgroundRate=100, update_type='z', data_version=1)
        self.db.permissions.t.insert().execute(permission="admin", username="bob", data_version=1)
        self.db.releases.t.insert().execute(name='a', product='a', read_only=True,
                                            data=json.dumps(dict(name="a", schema_version=1, hashFunction="sha512")),
                                            data_version=1)
        self.db.releases.t.insert().execute(name='b', product='b',
                                            read_only=False,
                                            data=json.dumps(dict(name="b", schema_version=1, hashFunction="sha512")),
                                            data_version=1)

    def _runTest(self, changer):
        with mock.patch("smtplib.SMTP") as smtp:
            mock_conn = mock.Mock()
            smtp.return_value = mock_conn
            self.db.setupChangeMonitors("fake", 25, "fake", "fake", "fake@to.com", "fake@from.com")
            changer()
            return mock_conn

    def testOnInsert(self):
        def doit():
            self.db.rules.insert("bob", product="foo", channel="bar", backgroundRate=100, priority=50, update_type="minor")
        mock_conn = self._runTest(doit)
        mock_conn.sendmail.assert_called_with("fake@from.com", "fake@to.com", PartialString("INSERT"))
        mock_conn.sendmail.assert_called_with("fake@from.com", "fake@to.com", PartialString("Row to be inserted:"))
        mock_conn.sendmail.assert_called_with("fake@from.com", "fake@to.com", PartialString("'channel': 'bar'"))

    def testOnUpdate(self):
        def doit():
            self.db.rules.update({"rule_id": 2}, {"product": "blah"}, "bob", 1)
        mock_conn = self._runTest(doit)
        mock_conn.sendmail.assert_called_with("fake@from.com", "fake@to.com", PartialString("UPDATE"))
        mock_conn.sendmail.assert_called_with("fake@from.com", "fake@to.com", PartialString("Row(s) to be updated as follows:"))
        mock_conn.sendmail.assert_called_with("fake@from.com", "fake@to.com", PartialString("'product': None ---> 'blah'"))
        mock_conn.sendmail.assert_called_with("fake@from.com", "fake@to.com", PartialString("'channel': u'release' (unchanged)"))

    def testOnDelete(self):
        def doit():
            self.db.rules.delete({"rule_id": 2}, changed_by="bob", old_data_version=1)
        mock_conn = self._runTest(doit)
        mock_conn.sendmail.assert_called_with("fake@from.com", "fake@to.com", PartialString("DELETE"))
        mock_conn.sendmail.assert_called_with("fake@from.com", "fake@to.com", PartialString("Row(s) to be removed:"))
        mock_conn.sendmail.assert_called_with("fake@from.com", "fake@to.com", PartialString("'rule_id': 2"))
        mock_conn.sendmail.assert_called_with("fake@from.com", "fake@to.com", PartialString("'channel': 'release'"))

    def testOnChangeReadOnly(self):
        def doit():
            self.db.releases.update({"name": "a"}, {"read_only": False}, changed_by='bob', old_data_version=1)
        mock_conn = self._runTest(doit)
        mock_conn.sendmail.assert_called_with("fake@from.com", "fake@to.com",
                                              PartialString("Read only release"
                                                            " u'a' changed to modifiable"))
        mock_conn.sendmail.assert_called_with("fake@from.com", "fake@to.com",
                                              PartialString("'name': u'a'"))
        mock_conn.sendmail.assert_called_with("fake@from.com", "fake@to.com",
                                              PartialString("'product': u'a'"))
        mock_conn.sendmail.assert_called_with("fake@from.com", "fake@to.com",
                                              PartialString("'read_only': True"
                                                            " ---> False"))

    def testOnChangeReadOnlySetUnmodifiable(self):
        def doit():
            self.db.releases.update({"name": "b"}, {"read_only": False}, changed_by='bob', old_data_version=1)
        mock_conn = self._runTest(doit)
        mock_conn.sendmail.assert_not_called()


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
