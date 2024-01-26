import json
import logging
import os
import re
import sys
import unittest
from copy import deepcopy
from os import path
from tempfile import mkstemp

import migrate.versioning.api
import mock
import pytest
from migrate.versioning.api import version
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, select
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.testing.assertions import emits_warning

import auslib
from auslib.blobs.apprelease import ReleaseBlobV1
from auslib.blobs.base import createBlob
from auslib.db import (
    AlreadySetupError,
    AUSDatabase,
    AUSTable,
    AUSTransaction,
    ChangeScheduledError,
    HistoryTable,
    MismatchedDataVersionError,
    OutdatedDataError,
    PermissionDeniedError,
    SignoffRequiredError,
    SignoffsTable,
    TransactionError,
    UpdateMergeError,
    verify_signoffs,
)
from auslib.errors import BlobValidationError, ReadOnlyError
from auslib.global_state import cache, dbo
from auslib.services import releases

from .fakes import FakeGCSHistory, FakeGCSHistoryAsync


def setUpModule():
    # This is meant to silence the debug information coming from SQLAlchemy-Migrate since
    # AUSDatabase provides decent debugging logs by itself.
    logging.getLogger("migrate").setLevel(logging.CRITICAL)


class MemoryDatabaseMixin(object):
    """Use this when writing tests that don't require multiple connections to
    the database."""

    def setUp(self):
        self.dburi = "sqlite:///:memory:"


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
        self.dburi = "sqlite:///%s" % self.getTempfile()

    def tearDown(self):
        for fd, t in self.tmpfiles:
            os.close(fd)
            os.remove(t)

    def getTempfile(self):
        fd, t = mkstemp()
        self.tmpfiles.append((fd, t))
        return t


class TestVerifySignoffs(unittest.TestCase):
    def testNoRequiredSignoffs(self):
        verify_signoffs({}, {})

    def testNoRequiredSignoffsWithSignoffs(self):
        verify_signoffs({}, [{"role": "releng"}, {"role": "relman"}])

    def testNoSignoffsGiven(self):
        required = [{"role": "releng", "signoffs_required": 1}]
        signoffs = []
        self.assertRaises(SignoffRequiredError, verify_signoffs, required, signoffs)

    def testMissingSignoffFromOneRole(self):
        required = [{"role": "releng", "signoffs_required": 1}, {"role": "relman", "signoffs_required": 1}]
        signoffs = [{"role": "releng", "username": "joe"}]
        self.assertRaises(SignoffRequiredError, verify_signoffs, required, signoffs)

    def testNotEnoughSignoffsFromOneRole(self):
        required = [{"role": "releng", "signoffs_required": 2}, {"role": "relman", "signoffs_required": 1}]
        signoffs = [{"role": "releng", "username": "joe"}, {"role": "relman", "username": "jane"}]
        self.assertRaises(SignoffRequiredError, verify_signoffs, required, signoffs)

    def testExactlyEnoughSignoffsGiven(self):
        required = [{"role": "releng", "signoffs_required": 2}, {"role": "relman", "signoffs_required": 1}]
        signoffs = [{"role": "releng", "username": "joe"}, {"role": "releng", "username": "jane"}, {"role": "relman", "username": "nick"}]
        verify_signoffs(required, signoffs)

    def testMoreThanEnoughSignoffsGiven(self):
        required = [{"role": "releng", "signoffs_required": 2}, {"role": "relman", "signoffs_required": 1}]
        signoffs = [
            {"role": "releng", "username": "joe"},
            {"role": "releng", "username": "jane"},
            {"role": "relman", "username": "nick"},
            {"role": "relman", "username": "matt"},
        ]
        verify_signoffs(required, signoffs)

    def testMultiplePotentialSignoffsForOneGroupWithoutEnoughSignoffs(self):
        required = [{"role": "releng", "signoffs_required": 2}, {"role": "releng", "signoffs_required": 1}, {"role": "relman", "signoffs_required": 1}]
        signoffs = [{"role": "releng", "username": "joe"}, {"role": "relman", "username": "nick"}]
        self.assertRaises(SignoffRequiredError, verify_signoffs, required, signoffs)

    def testMultiplePotentialSignoffsForOneGroupWithEnoughSignoffs(self):
        required = [{"role": "releng", "signoffs_required": 2}, {"role": "releng", "signoffs_required": 1}, {"role": "relman", "signoffs_required": 1}]
        signoffs = [{"role": "releng", "username": "joe"}, {"role": "releng", "username": "jane"}, {"role": "relman", "username": "nick"}]
        verify_signoffs(required, signoffs)


class TestAUSTransaction(unittest.TestCase, MemoryDatabaseMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.engine = create_engine(self.dburi)
        self.metadata = MetaData(self.engine)
        self.table = Table("test", self.metadata, Column("id", Integer, primary_key=True), Column("foo", Integer))
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
        self.assertEqual(ret, [(1, 66), (2, 22), (3, 11), (4, 55)])

    def testTransactionRaisesOnError(self):
        trans = AUSTransaction(self.metadata.bind.connect())
        self.assertRaises(TransactionError, trans.execute, "UPDATE test SET foo=123 WHERE fake=1")

    def testRollback(self):
        trans = AUSTransaction(self.metadata.bind.connect())
        trans.execute(self.table.update(values=dict(foo=66)).where(self.table.c.id == 1))
        trans.rollback()
        ret = self.table.select().execute().fetchall()
        self.assertEqual(ret, [(1, 33), (2, 22), (3, 11)])

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
        self.table = Table("test", self.metadata, Column("id", Integer, primary_key=True), Column("foo", Integer))
        self.metadata.create_all()
        self.table.insert().execute(id=1, foo=33)
        self.table.insert().execute(id=2, foo=22)
        self.table.insert().execute(id=3, foo=11)

    def tearDown(self):
        NamedFileDatabaseMixin.tearDown(self)

    def testTransactionNotChangedUntilCommit(self):
        trans = AUSTransaction(self.metadata.bind.connect())
        trans.execute(self.table.update(values=dict(foo=66)).where(self.table.c.id == 1))
        # This select() runs in a different connection, so no changes should
        # be visible to it yet
        ret = self.table.select().execute().fetchall()
        self.assertEqual(ret, [(1, 33), (2, 22), (3, 11)])
        trans.commit()
        ret = self.table.select().execute().fetchall()
        self.assertEqual(ret, [(1, 66), (2, 22), (3, 11)])


class TestTableMixin(object):
    def setUp(self):
        self.engine = create_engine(self.dburi)
        self.metadata = MetaData(self.engine)

        class TestTable(AUSTable):
            def __init__(self, db, metadata):
                self.table = Table("test", metadata, Column("id", Integer, primary_key=True, autoincrement=True), Column("foo", Integer))
                AUSTable.__init__(self, db, "sqlite", historyClass=HistoryTable)

        class TestAutoincrementTable(AUSTable):
            def __init__(self, db, metadata):
                self.table = Table("test-autoincrement", metadata, Column("id", Integer, primary_key=True, autoincrement=True), Column("foo", Integer))
                AUSTable.__init__(self, db, "sqlite", historyClass=HistoryTable)

        self.test = TestTable("fake", self.metadata)
        self.testAutoincrement = TestAutoincrementTable("fake", self.metadata)
        self.metadata.create_all()
        self.test.t.insert().execute(id=1, foo=33, data_version=4)
        self.test.t.insert().execute(id=2, foo=22, data_version=5)
        self.test.t.insert().execute(id=3, foo=11, data_version=6)
        self.test.history.t.insert().execute(change_id=1, timestamp=9, changed_by="admin", id=1)
        self.test.history.t.insert().execute(change_id=2, timestamp=10, changed_by="admin", id=1, foo=30, data_version=1)
        self.test.history.t.insert().execute(change_id=3, timestamp=20, changed_by="admin", id=1, foo=31, data_version=2)
        self.test.history.t.insert().execute(change_id=4, timestamp=30, changed_by="admin", id=1, foo=32, data_version=3)
        self.test.history.t.insert().execute(change_id=5, timestamp=40, changed_by="admin", id=1, foo=33, data_version=4)
        self.test.history.t.insert().execute(change_id=6, timestamp=9, changed_by="admin", id=2)
        self.test.history.t.insert().execute(change_id=7, timestamp=10, changed_by="admin", id=2, foo=18, data_version=1)
        self.test.history.t.insert().execute(change_id=8, timestamp=15, changed_by="admin", id=2, foo=19, data_version=2)
        self.test.history.t.insert().execute(change_id=9, timestamp=20, changed_by="admin", id=2, foo=20, data_version=3)
        self.test.history.t.insert().execute(change_id=10, timestamp=25, changed_by="admin", id=2, foo=21, data_version=4)
        self.test.history.t.insert().execute(change_id=11, timestamp=30, changed_by="admin", id=2, foo=22, data_version=5)
        self.test.history.t.insert().execute(change_id=12, timestamp=22, changed_by="admin", id=3)
        self.test.history.t.insert().execute(change_id=13, timestamp=23, changed_by="admin", id=3, foo=6, data_version=1)
        self.test.history.t.insert().execute(change_id=14, timestamp=26, changed_by="admin", id=3, foo=7, data_version=2)
        self.test.history.t.insert().execute(change_id=15, timestamp=29, changed_by="admin", id=3, foo=8, data_version=3)
        self.test.history.t.insert().execute(change_id=16, timestamp=32, changed_by="admin", id=3, foo=9, data_version=4)
        self.test.history.t.insert().execute(change_id=17, timestamp=35, changed_by="admin", id=3, foo=10, data_version=5)
        self.test.history.t.insert().execute(change_id=18, timestamp=38, changed_by="admin", id=3, foo=11, data_version=6)
        self.test.history.t.insert().execute(change_id=19, timestamp=19, changed_by="admin", id=4)
        self.test.history.t.insert().execute(change_id=20, timestamp=20, changed_by="admin", id=4, foo=40, data_version=1)
        self.test.history.t.insert().execute(change_id=21, timestamp=25, changed_by="admin", id=4, foo=41, data_version=2)
        self.test.history.t.insert().execute(change_id=22, timestamp=30, changed_by="admin", id=4, foo=42, data_version=3)
        self.test.history.t.insert().execute(change_id=23, timestamp=35, changed_by="admin", id=4)


class TestMultiplePrimaryTableMixin(object):
    def setUp(self):
        self.engine = create_engine(self.dburi)
        self.metadata = MetaData(self.engine)

        class TestTable(AUSTable):
            def __init__(self, db, metadata):
                self.table = Table(
                    "test",
                    metadata,
                    Column("id1", Integer, primary_key=True, autoincrement=False),
                    Column("id2", Integer, primary_key=True, autoincrement=False),
                    Column("foo", Integer),
                )
                AUSTable.__init__(self, db, "sqlite", historyClass=HistoryTable)

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
        self.assertTrue(self.test.id in list(self.test.table.columns))
        self.assertTrue(self.test.foo in list(self.test.table.columns))

    def testSelect(self):
        expected = [dict(id=1, foo=33, data_version=4), dict(id=2, foo=22, data_version=5), dict(id=3, foo=11, data_version=6)]
        self.assertEqual(self.test.select(), expected)

    def testSelectWithColumns(self):
        expected = [dict(id=1), dict(id=2), dict(id=3)]
        self.assertEqual(self.test.select(columns=[self.test.id]), expected)

    def testSelectWithWhere(self):
        expected = [dict(id=2, foo=22, data_version=5), dict(id=3, foo=11, data_version=6)]
        self.assertEqual(self.test.select(where=[self.test.id >= 2]), expected)

    def testSelectWithOrder(self):
        expected = [dict(id=3, foo=11, data_version=6), dict(id=2, foo=22, data_version=5), dict(id=1, foo=33, data_version=4)]
        self.assertEqual(self.test.select(order_by=[self.test.foo]), expected)

    def testSelectWithLimit(self):
        self.assertEqual(self.test.select(limit=1), [dict(id=1, foo=33, data_version=4)])

    def testSelectCanModifyResult(self):
        ret = self.test.select()[0]
        # If we can't write to this, an Exception will be raised and the test will fail
        ret["foo"] = 3245

    def testInsert(self):
        self.test.insert(changed_by="bob", id=5, foo=0)
        ret = self.test.t.select().execute().fetchall()
        self.assertEqual(len(ret), 4)
        self.assertEqual(ret[-1], (5, 0, 1))

    def testInsertClosesConnectionOnImplicitTransaction(self):
        with mock.patch("sqlalchemy.engine.base.Connection.close") as close:
            self.test.insert(changed_by="bob", id=5, foo=1)
            self.assertTrue(close.called, "Connection.close() never called by insert()")

    def testInsertClosesConnectionOnImplicitTransactionWithError(self):
        with mock.patch("sqlalchemy.engine.base.Connection.close") as close:
            try:
                self.test.insert(changed_by="bob", id=1, foo=1)
            except Exception:
                pass
            self.assertTrue(close.called, "Connection.close() never called by insert()")

    def testDelete(self):
        ret = self.test.delete(changed_by="bill", where=[self.test.id == 1, self.test.foo == 33], old_data_version=4)
        self.assertEqual(ret.rowcount, 1)
        self.assertEqual(len(self.test.t.select().execute().fetchall()), 2)

    def testDeleteFailsOnVersionMismatch(self):
        self.assertRaises(OutdatedDataError, self.test.delete, changed_by="bill", where=[self.test.id == 3], old_data_version=1)

    def testDeleteClosesConnectionOnImplicitTransaction(self):
        with mock.patch("sqlalchemy.engine.base.Connection.close") as close:
            self.test.delete(changed_by="bill", where=[self.test.id == 1], old_data_version=4)
            self.assertTrue(close.called, "Connection.close() never called by delete()")

    def testUpdate(self):
        ret = self.test.update(changed_by="bob", where=[self.test.id == 1], what=dict(foo=123), old_data_version=4)
        self.assertEqual(ret.rowcount, 1)
        self.assertEqual(self.test.t.select(self.test.id == 1).execute().fetchone(), (1, 123, 5))

    def testUpdateFailsOnVersionMismatch(self):
        self.assertRaises(OutdatedDataError, self.test.update, changed_by="bill", where=[self.test.id == 3], what=dict(foo=99), old_data_version=1)

    def testUpdateClosesConnectionOnImplicitTransaction(self):
        with mock.patch("sqlalchemy.engine.base.Connection.close") as close:
            self.test.update(changed_by="bob", where=[self.test.id == 1], what=dict(foo=432), old_data_version=4)
            self.assertTrue(close.called, "Connection.close() never called by update()")

    def test_count(self):
        count = self.test.count()
        self.assertEqual(count, 3)
        where = [self.test.id == 2]
        count = self.test.count(where=where)
        self.assertEqual(count, 1)
        where = [self.test.id == -1]
        count = self.test.count(where=where)
        self.assertEqual(count, 0)


class TestAUSTableRequiresRealFile(unittest.TestCase, TestTableMixin, NamedFileDatabaseMixin):
    def setUp(self):
        NamedFileDatabaseMixin.setUp(self)
        TestTableMixin.setUp(self)

    def tearDown(self):
        NamedFileDatabaseMixin.tearDown(self)

    def testDeleteWithTransaction(self):
        trans = AUSTransaction(self.metadata.bind.connect())
        self.test.delete(changed_by="bill", transaction=trans, where=[self.test.id == 2], old_data_version=5)
        ret = self.test.t.select().execute().fetchall()
        self.assertEqual(len(ret), 3)
        trans.commit()
        ret = self.test.t.select().execute().fetchall()
        self.assertEqual(len(ret), 2)

    def testInsertWithTransaction(self):
        trans = AUSTransaction(self.metadata.bind.connect())
        self.test.insert(changed_by="bob", transaction=trans, id=5, foo=1)
        ret = self.test.t.select().execute().fetchall()
        self.assertEqual(len(ret), 3)
        trans.commit()
        ret = self.test.t.select().execute().fetchall()
        self.assertEqual(ret[-1], (5, 1, 1))

    def testUpdateWithTransaction(self):
        trans = AUSTransaction(self.metadata.bind.connect())
        self.test.update(changed_by="bill", transaction=trans, where=[self.test.id == 1], what=dict(foo=222), old_data_version=4)
        ret = self.test.t.select(self.test.id == 1).execute().fetchone()
        self.assertEqual(ret, (1, 33, 4))
        trans.commit()
        ret = self.test.t.select(self.test.id == 1).execute().fetchone()
        self.assertEqual(ret, (1, 222, 5))


# TODO: Find some way of testing this with SQLite, or testing it with some other backend.
# Because it's impossible to have multiple simultaneous transaction with sqlite, you
# can't test the behaviour of concurrent transactions with it.
#    def testUpdateCollidingUpdateFails(self):
#        trans1 = AUSTransaction(self.test.getEngine().connect())
#        trans2 = AUSTransaction(self.test.getEngine().connect())
#        ret1 = self.test._prepareUpdate(trans1, where=[self.test.id==3], what=dict(foo=99), changed_by='bob')
#        ret2 = self.test._prepareUpdate(trans2, where=[self.test.id==3], what=dict(foo=66), changed_by='bob')
#        trans1.commit()
#        self.assertEqual(ret1.rowcount, 1)
#        self.assertEqual(self.test.t.select(self.test.id==3).execute().fetchone(), (1, 99, 2))
#        self.assertRaises(TransactionError, trans2.commit)


class TestHistoryTable(unittest.TestCase, TestTableMixin, MemoryDatabaseMixin):
    maxDiff = 2000

    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        TestTableMixin.setUp(self)

    def testHasHistoryTable(self):
        self.assertTrue(self.test.history)

    def testHistoryTableHasAllColumns(self):
        columns = [c.name for c in self.test.history.t.columns]
        self.assertTrue("change_id" in columns)
        self.assertTrue("id" in columns)
        self.assertTrue("foo" in columns)
        self.assertTrue("changed_by" in columns)
        self.assertTrue("timestamp" in columns)
        self.assertTrue("data_version" in columns)

    @mock.patch("time.time", mock.MagicMock(return_value=1.0))
    def testHistoryUponInsert(self):
        self.test.insert(changed_by="george", id=5, foo=0)
        ret = self.test.history.t.select().where(self.test.history.id == 5).execute().fetchall()
        self.assertEqual(ret, [(24, "george", 999, 5, None, None), (25, "george", 1000, 5, 0, 1)])

    @mock.patch("time.time", mock.MagicMock(return_value=1.0))
    def testHistoryUponAutoincrementInsert(self):
        self.test.insert(changed_by="george", foo=0)
        # This actual generates history for a row we already have history for
        # because sqlite just uses max(id)+1 as the next available primary key.
        # Even if we insert and delete id 4 from the database, we still
        # get id=4 for the next autoincrement insert.
        ret = self.test.history.t.select().where(self.test.history.id == 4).execute().fetchall()[-2:]
        self.assertEqual(ret, [(24, "george", 999, 4, None, None), (25, "george", 1000, 4, 0, 1)])

    @mock.patch("time.time", mock.MagicMock(return_value=1.0))
    def testHistoryUponDelete(self):
        self.test.delete(changed_by="bobby", where=[self.test.id == 1], old_data_version=4)
        ret = self.test.history.t.select().where(self.test.history.id == 1).execute().fetchall()[-1]
        self.assertEqual(ret, (24, "bobby", 1000, 1, None, None))

    @mock.patch("time.time", mock.MagicMock(return_value=1.0))
    def testHistoryUponUpdate(self):
        self.test.update(changed_by="heather", where=[self.test.id == 2], what=dict(foo=99), old_data_version=5)
        ret = self.test.history.t.select().where(self.test.history.id == 2).execute().fetchall()[-1]
        self.assertEqual(ret, (24, "heather", 1000, 2, 99, 6))

    @mock.patch("time.time", mock.MagicMock(return_value=1234567890.123456))
    def testHistoryTimestampMaintainsPrecision(self):
        self.test.insert(changed_by="bob", id=5)
        ret = select([self.test.history.timestamp]).where(self.test.history.id == 5).execute().fetchone()[0]
        # Insert decrements the timestamp
        self.assertEqual(ret, 1234567890122)

    @mock.patch("time.time", mock.MagicMock(return_value=1.0))
    def testHistoryGetChangeWithChangeID(self):
        self.test.insert(changed_by="george", id=5, foo=0)
        ret = self.test.history.getChange(change_id=24)
        self.assertEqual(ret, {"data_version": None, "changed_by": "george", "foo": None, "timestamp": 999, "change_id": 24, "id": 5})

    @mock.patch("time.time", mock.MagicMock(return_value=1.0))
    def testHistoryGetChangeWithDataVersion(self):
        self.test.insert(changed_by="george", id=5, foo=0)
        ret = self.test.history.getChange(data_version=1, column_values={"id": 5})
        self.assertEqual(ret, {"data_version": 1, "changed_by": "george", "foo": 0, "timestamp": 1000, "change_id": 25, "id": 5})

    @mock.patch("time.time", mock.MagicMock(return_value=1.0))
    def testHistoryGetChangeWithDataVersionReturnNone(self):
        self.test.insert(changed_by="george", id=5, foo=0)
        ret = self.test.history.getChange(data_version=1, column_values={"id": 6})
        self.assertEqual(ret, None)

    @mock.patch("time.time", mock.MagicMock(return_value=1.0))
    def testHistoryGetChangeWithDataVersionWithNonPrimaryKeyColumn(self):
        self.test.insert(changed_by="george", id=5, foo=0)
        self.assertRaises(ValueError, self.test.history.getChange, data_version=1, column_values={"foo": 5})

    def testGetPointInTime(self):
        times_and_results = (
            (
                10,
                (
                    dict(change_id=2, timestamp=10, changed_by="admin", id=1, foo=30, data_version=1),
                    dict(change_id=7, timestamp=10, changed_by="admin", id=2, foo=18, data_version=1),
                ),
            ),
            (
                15,
                (
                    dict(change_id=2, timestamp=10, changed_by="admin", id=1, foo=30, data_version=1),
                    dict(change_id=8, timestamp=15, changed_by="admin", id=2, foo=19, data_version=2),
                ),
            ),
            (
                20,
                (
                    dict(change_id=3, timestamp=20, changed_by="admin", id=1, foo=31, data_version=2),
                    dict(change_id=9, timestamp=20, changed_by="admin", id=2, foo=20, data_version=3),
                    dict(change_id=20, timestamp=20, changed_by="admin", id=4, foo=40, data_version=1),
                ),
            ),
            (
                25,
                (
                    dict(change_id=3, timestamp=20, changed_by="admin", id=1, foo=31, data_version=2),
                    dict(change_id=10, timestamp=25, changed_by="admin", id=2, foo=21, data_version=4),
                    dict(change_id=13, timestamp=23, changed_by="admin", id=3, foo=6, data_version=1),
                    dict(change_id=21, timestamp=25, changed_by="admin", id=4, foo=41, data_version=2),
                ),
            ),
            (
                30,
                (
                    dict(change_id=4, timestamp=30, changed_by="admin", id=1, foo=32, data_version=3),
                    dict(change_id=11, timestamp=30, changed_by="admin", id=2, foo=22, data_version=5),
                    dict(change_id=15, timestamp=29, changed_by="admin", id=3, foo=8, data_version=3),
                    dict(change_id=22, timestamp=30, changed_by="admin", id=4, foo=42, data_version=3),
                ),
            ),
            (
                35,
                (
                    dict(change_id=4, timestamp=30, changed_by="admin", id=1, foo=32, data_version=3),
                    dict(change_id=11, timestamp=30, changed_by="admin", id=2, foo=22, data_version=5),
                    dict(change_id=17, timestamp=35, changed_by="admin", id=3, foo=10, data_version=5),
                ),
            ),
            (
                40,
                (
                    dict(change_id=5, timestamp=40, changed_by="admin", id=1, foo=33, data_version=4),
                    dict(change_id=11, timestamp=30, changed_by="admin", id=2, foo=22, data_version=5),
                    dict(change_id=18, timestamp=38, changed_by="admin", id=3, foo=11, data_version=6),
                ),
            ),
        )

        for timestamp, expected in times_and_results:
            ret = self.test.history.getPointInTime(timestamp)
            self.assertSequenceEqual(ret, expected)


class TestMultiplePrimaryHistoryTable(unittest.TestCase, TestMultiplePrimaryTableMixin, MemoryDatabaseMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        TestMultiplePrimaryTableMixin.setUp(self)

    def testHasHistoryTable(self):
        self.assertTrue(self.test.history)

    def testMultiplePrimaryHistoryTableHasAllColumns(self):
        columns = [c.name for c in self.test.history.t.columns]
        self.assertTrue("change_id" in columns)
        self.assertTrue("id1" in columns)
        self.assertTrue("id2" in columns)
        self.assertTrue("foo" in columns)
        self.assertTrue("changed_by" in columns)
        self.assertTrue("timestamp" in columns)
        self.assertTrue("data_version" in columns)

    @mock.patch("time.time", mock.MagicMock(return_value=1.0))
    def testMultiplePrimaryHistoryUponInsert(self):
        self.test.insert(changed_by="george", id1=4, id2=5, foo=0)
        ret = self.test.history.t.select().execute().fetchall()
        self.assertEqual(ret, [(1, "george", 999, 4, 5, None, None), (2, "george", 1000, 4, 5, 0, 1)])

    @mock.patch("time.time", mock.MagicMock(return_value=1.0))
    def testMultiplePrimaryHistoryUponDelete(self):
        self.test.delete(changed_by="bobby", where=[self.test.id1 == 1, self.test.id2 == 2], old_data_version=1)
        ret = self.test.history.t.select().execute().fetchone()
        self.assertEqual(ret, (1, "bobby", 1000, 1, 2, None, None))

    @mock.patch("time.time", mock.MagicMock(return_value=1.0))
    def testMultiplePrimaryHistoryUponUpdate(self):
        self.test.update(changed_by="heather", where=[self.test.id1 == 2, self.test.id2 == 1], what=dict(foo=99), old_data_version=1)
        ret = self.test.history.t.select().execute().fetchone()
        self.assertEqual(ret, (1, "heather", 1000, 2, 1, 99, 2))

    @mock.patch("time.time", mock.MagicMock(return_value=1.0))
    def testMultiplePrimaryKeyHistoryGetChangeWithDataVersion(self):
        self.test.insert(changed_by="george", id1=4, id2=5, foo=0)
        ret = self.test.history.getChange(data_version=1, column_values={"id1": 4, "id2": 5})
        self.assertEqual(ret, {"data_version": 1, "changed_by": "george", "foo": 0, "timestamp": 1000, "change_id": 2, "id1": 4, "id2": 5})

    @mock.patch("time.time", mock.MagicMock(return_value=1.0))
    def testMultiplePrimaryKeyHistoryGetChangeWithDataVersionReturnNone(self):
        self.test.insert(changed_by="george", id1=4, id2=5, foo=0)
        ret = self.test.history.getChange(data_version=1, column_values={"id1": 4, "id2": 55})
        self.assertEqual(ret, None)

    @mock.patch("time.time", mock.MagicMock(return_value=1.0))
    def testHistoryGetChangeWithDataVersionWithNonPrimaryKeyColumn(self):
        self.test.insert(changed_by="george", id1=4, id2=5, foo=0)
        self.assertRaises(ValueError, self.test.history.getChange, data_version=1, column_values={"id1": 4, "foo": 4})


@pytest.mark.usefixtures("current_db_schema")
class ScheduledChangesTableMixin(object):
    def setUp(self):
        self.db = AUSDatabase(self.dburi, releases_history_buckets={"*": "fake"}, releases_history_class=FakeGCSHistory)
        self.metadata.create_all(self.db.engine)
        self.engine = self.db.engine
        self.metadata = self.db.metadata

        class TestTable(AUSTable):
            def __init__(self, db, metadata):
                self.table = Table(
                    "test_table",
                    metadata,
                    Column("fooid", Integer, primary_key=True, autoincrement=True),
                    Column("foo", String(15), nullable=False),
                    Column("bar", String(15)),
                )
                super(TestTable, self).__init__(db, "sqlite", scheduled_changes=True, versioned=True, historyClass=HistoryTable)

            def getPotentialRequiredSignoffs(self, affected_rows, transaction=None):
                for row in affected_rows:
                    if row["foo"] == "signofftest":
                        return {"rs": [{"role": "releng", "signoffs_required": 1}]}

            def insert(self, changed_by, transaction=None, dryrun=False, signoffs=None, **columns):
                if not self.db.hasPermission(changed_by, "test", "create", transaction=transaction):
                    raise PermissionDeniedError("fail")
                if not dryrun:
                    super(TestTable, self).insert(changed_by, transaction, dryrun, **columns)

            def update(self, where, what, changed_by, old_data_version, transaction=None, dryrun=False, signoffs=None):
                # Although our test table doesn't need it, real tables do some extra permission
                # checks based on "where". To make sure we catch bugs around the "where" arg
                # being broken, we use it similarly here.
                for row in self.select(where=where, transaction=transaction):
                    if not self.db.hasPermission(changed_by, "test", "modify", transaction=transaction):
                        raise PermissionDeniedError("fail")
                if not dryrun:
                    super(TestTable, self).update(where, what, changed_by, old_data_version, transaction, dryrun)

            def delete(self, where, changed_by, old_data_version, transaction=None, dryrun=False, signoffs=None):
                if not self.db.hasPermission(changed_by, "test", "delete", transaction=transaction):
                    raise PermissionDeniedError("fail")

                if not dryrun:
                    super(TestTable, self).delete(where, changed_by, old_data_version, transaction, dryrun)

        self.table = TestTable(self.db, self.metadata)
        self.sc_table = self.table.scheduled_changes
        self.metadata.create_all()
        self.table.t.insert().execute(fooid=1, foo="a", data_version=1)
        self.table.t.insert().execute(fooid=2, foo="b", bar="bb", data_version=2)
        self.table.t.insert().execute(fooid=3, foo="c", data_version=2)
        self.table.t.insert().execute(fooid=4, foo="d", data_version=2)
        self.sc_table.t.insert().execute(
            sc_id=1, scheduled_by="bob", base_fooid=1, base_foo="aa", base_bar="barbar", base_data_version=1, data_version=1, change_type="update"
        )
        self.sc_table.conditions.t.insert().execute(sc_id=1, when=234000, data_version=1)
        self.sc_table.t.insert().execute(sc_id=2, scheduled_by="bob", base_foo="cc", base_bar="ceecee", data_version=1, change_type="insert")
        self.sc_table.conditions.t.insert().execute(sc_id=2, when=567000, data_version=1)
        self.sc_table.t.insert().execute(
            sc_id=3, scheduled_by="bob", complete=True, base_fooid=2, base_foo="b", base_bar="bb", base_data_version=1, data_version=1, change_type="update"
        )
        self.sc_table.conditions.t.insert().execute(sc_id=3, when=1000, data_version=1)
        self.sc_table.t.insert().execute(
            sc_id=4, scheduled_by="bob", base_fooid=2, base_foo="dd", base_bar="bb", base_data_version=2, data_version=1, change_type="update"
        )
        self.sc_table.conditions.t.insert().execute(sc_id=4, when=333000, data_version=1)
        self.sc_table.t.insert().execute(
            sc_id=5, scheduled_by="bob", complete=True, base_fooid=3, base_foo="c", base_bar="bb", base_data_version=1, data_version=1, change_type="update"
        )
        self.sc_table.conditions.t.insert().execute(sc_id=5, when=39000, data_version=1)
        self.sc_table.t.insert().execute(
            sc_id=6, scheduled_by="bob", complete=False, base_fooid=4, base_foo="d", base_bar=None, base_data_version=2, data_version=1, change_type="delete"
        )
        self.sc_table.conditions.t.insert().execute(sc_id=6, when=400000, data_version=1)
        self.db.permissions.t.insert().execute(permission="admin", username="bob", data_version=1)
        self.db.permissions.t.insert().execute(permission="admin", username="mary", data_version=1)
        self.db.permissions.t.insert().execute(permission="admin", username="jane", data_version=1)
        self.db.permissions.t.insert().execute(permission="scheduled_change", username="nancy", options={"actions": ["enact"]}, data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="bob", role="releng", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="mary", role="releng", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="mary", role="dev", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="jane", role="dev", data_version=1)


class TestScheduledChangesTable(unittest.TestCase, ScheduledChangesTableMixin, MemoryDatabaseMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        ScheduledChangesTableMixin.setUp(self)

    def testAllTablesCreated(self):
        self.assertTrue(self.table)
        self.assertTrue(self.table.history)
        self.assertTrue(self.table.scheduled_changes)
        self.assertTrue(self.table.scheduled_changes.history)
        self.assertTrue(self.table.scheduled_changes.conditions)
        self.assertTrue(self.table.scheduled_changes.conditions.history)
        self.assertTrue(self.table.scheduled_changes.signoffs)
        self.assertTrue(self.table.scheduled_changes.signoffs.history)

    def testTablesHaveCorrectColumns(self):
        sc_columns = [c.name for c in self.sc_table.t.columns]
        self.assertEqual(len(sc_columns), 9)
        self.assertTrue("sc_id" in sc_columns)
        self.assertTrue("scheduled_by" in sc_columns)
        self.assertTrue("complete" in sc_columns)
        self.assertTrue("data_version" in sc_columns)
        self.assertTrue("base_fooid" in sc_columns)
        self.assertTrue("base_foo" in sc_columns)
        self.assertTrue("base_bar" in sc_columns)
        self.assertTrue("base_data_version" in sc_columns)
        self.assertTrue("change_type" in sc_columns)
        self.assertTrue("telemetry_product" not in sc_columns)
        self.assertTrue("telemetry_channel" not in sc_columns)
        self.assertTrue("telemetry_uptake" not in sc_columns)
        self.assertTrue("when" not in sc_columns)

        cond_columns = [c.name for c in self.sc_table.conditions.t.columns]
        self.assertEqual(len(cond_columns), 6)
        self.assertTrue("sc_id" in cond_columns)
        self.assertTrue("telemetry_product" in cond_columns)
        self.assertTrue("telemetry_channel" in cond_columns)
        self.assertTrue("telemetry_uptake" in cond_columns)
        self.assertTrue("when" in cond_columns)
        self.assertTrue("data_version" in cond_columns)

        signoff_columns = [c.name for c in self.sc_table.signoffs.t.columns]
        self.assertTrue("sc_id" in signoff_columns)
        self.assertTrue("username" in signoff_columns)
        self.assertTrue("role" in signoff_columns)

    def testValidateConditionsNone(self):
        self.assertRaisesRegex(ValueError, "No conditions found", self.sc_table.conditions.validate, {})

    def testValidateConditionsNoneValue(self):
        self.assertRaisesRegex(ValueError, "No conditions found", self.sc_table.conditions.validate, {"when": None})

    def testValdiateConditionsInvalid(self):
        self.assertRaisesRegex(ValueError, "Invalid condition", self.sc_table.conditions.validate, {"blah": "blah"})

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testValidateConditionsJustWhen(self):
        self.sc_table.conditions.validate({"when": 12345678})

    def testValidateConditionsBadWhen(self):
        self.assertRaisesRegex(ValueError, "Cannot parse", self.sc_table.conditions.validate, {"when": "abc"})

    def testValidateConditionsWhenInThePast(self):
        self.assertRaisesRegex(ValueError, "Cannot schedule changes in the past", self.sc_table.conditions.validate, {"when": 1})

    def testValidateConditionsJustTelemetry(self):
        self.sc_table.conditions.validate({"telemetry_product": "Firefox", "telemetry_channel": "nightly", "telemetry_uptake": "200000"})

    def testValidateConditionsNotAllowedWhenAndOther(self):
        self.assertRaisesRegex(
            ValueError, "Invalid combination of conditions", self.sc_table.conditions.validate, {"when": "12345", "telemetry_product": "foo"}
        )

    def testValidateConditionsMissingTelemetryValue(self):
        self.assertRaisesRegex(ValueError, "Invalid combination of conditions", self.sc_table.conditions.validate, {"telemetry_product": "foo"})

    def testSelectIncludesConditionColumns(self):
        row = self.sc_table.select(where=[self.sc_table.sc_id == 2])[0]
        self.assertEqual(row["scheduled_by"], "bob")
        self.assertEqual(row["complete"], False)
        self.assertEqual(row["data_version"], 1)
        self.assertEqual(row["base_fooid"], None)
        self.assertEqual(row["base_foo"], "cc")
        self.assertEqual(row["base_bar"], "ceecee")
        self.assertEqual(row["base_data_version"], None)
        self.assertEqual(row["telemetry_product"], None)
        self.assertEqual(row["telemetry_channel"], None)
        self.assertEqual(row["telemetry_uptake"], None)
        self.assertEqual(row["when"], 567000)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testInsertForExistingRow(self):
        what = {"fooid": 3, "foo": "thing", "bar": "thing2", "data_version": 2, "when": 999000, "change_type": "update"}
        self.sc_table.insert(changed_by="bob", **what)
        sc_row = self.sc_table.t.select().where(self.sc_table.sc_id == 7).execute().fetchall()[0]
        cond_row = self.sc_table.conditions.t.select().where(self.sc_table.conditions.sc_id == 7).execute().fetchall()[0]
        self.assertEqual(sc_row.scheduled_by, "bob")
        self.assertEqual(sc_row.change_type, "update")
        self.assertEqual(sc_row.data_version, 1)
        self.assertEqual(sc_row.base_fooid, 3)
        self.assertEqual(sc_row.base_foo, "thing")
        self.assertEqual(sc_row.base_bar, "thing2")
        self.assertEqual(sc_row.base_data_version, 2)
        self.assertEqual(cond_row.when, 999000)
        self.assertEqual(cond_row.data_version, 1)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testInsertForNewRow(self):
        what = {"foo": "newthing1", "when": 888000, "change_type": "insert"}
        self.sc_table.insert(changed_by="bob", **what)
        sc_row = self.sc_table.t.select().where(self.sc_table.sc_id == 7).execute().fetchall()[0]
        cond_row = self.sc_table.conditions.t.select().where(self.sc_table.conditions.sc_id == 7).execute().fetchall()[0]
        self.assertEqual(sc_row.scheduled_by, "bob")
        self.assertEqual(sc_row.change_type, "insert")
        self.assertEqual(sc_row.data_version, 1)
        self.assertEqual(sc_row.base_fooid, None)
        self.assertEqual(sc_row.base_foo, "newthing1")
        self.assertEqual(sc_row.base_bar, None)
        self.assertEqual(sc_row.base_data_version, None)
        self.assertEqual(cond_row.when, 888000)
        self.assertEqual(cond_row.data_version, 1)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testInsertRecordSignOffForUserHavingSingleRole(self):
        what = {"fooid": 3, "foo": "signofftest", "bar": "thing2", "data_version": 2, "when": 999000, "change_type": "update"}
        self.sc_table.insert(changed_by="bob", **what)
        user_role_rows = self.table.scheduled_changes.signoffs.select(where={"username": "bob", "sc_id": 7})
        self.assertEqual(len(user_role_rows), 1)
        self.assertEqual(user_role_rows[0].get("username"), "bob")
        self.assertEqual(user_role_rows[0].get("role"), "releng")
        self.assertEqual(user_role_rows[0].get("sc_id"), 7)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testInsertRecordSignOffForUserHavingMultipleRoles(self):
        what = {"fooid": 3, "foo": "signofftest", "bar": "thing2", "data_version": 2, "when": 999000, "change_type": "update"}
        self.sc_table.insert(changed_by="mary", **what)
        user_role_rows = self.table.scheduled_changes.signoffs.select(where={"username": "mary", "sc_id": 7})
        self.assertEqual(len(user_role_rows), 1)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testInsertRecordSignOffUnneededRole(self):
        what = {"fooid": 3, "foo": "signofftest", "bar": "thing2", "data_version": 2, "when": 999000, "change_type": "update"}
        self.sc_table.insert(changed_by="jane", **what)
        user_role_rows = self.table.scheduled_changes.signoffs.select(where={"username": "jane", "sc_id": 7})
        self.assertEqual(len(user_role_rows), 0)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testInsertWithNonAutoincrement(self):
        class TestTable2(AUSTable):
            def __init__(self, db, metadata):
                self.table = Table(
                    "test_table2", metadata, Column("foo_name", String(15), primary_key=True), Column("foo", String(15)), Column("bar", String(15))
                )
                super(TestTable2, self).__init__(db, "sqlite", scheduled_changes=True, versioned=True)

            def getPotentialRequiredSignoffs(self, *args, **kwargs):
                return None

        table = TestTable2(self.db, self.metadata)
        self.metadata.create_all()
        what = {"foo_name": "i'm a foo", "foo": "123", "bar": "456", "when": 876000, "change_type": "insert"}
        table.scheduled_changes.insert(changed_by="mary", **what)
        sc_row = table.scheduled_changes.t.select().where(table.scheduled_changes.sc_id == 1).execute().fetchall()[0]
        cond_row = table.scheduled_changes.conditions.t.select().where(table.scheduled_changes.conditions.sc_id == 1).execute().fetchall()[0]
        self.assertEqual(sc_row.scheduled_by, "mary")
        self.assertEqual(sc_row.change_type, "insert")
        self.assertEqual(sc_row.data_version, 1)
        self.assertEqual(sc_row.base_foo_name, "i'm a foo")
        self.assertEqual(sc_row.base_foo, "123")
        self.assertEqual(sc_row.base_bar, "456")
        self.assertEqual(sc_row.base_data_version, None)
        self.assertEqual(cond_row.when, 876000)
        self.assertEqual(cond_row.data_version, 1)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testInsertWithNonNullablePKColumn(self):
        class TestTable(AUSTable):
            def __init__(self, db, metadata):
                self.table = Table(
                    "test_table_null_pk",
                    metadata,
                    Column("foo_id", Integer, primary_key=True),
                    Column("bar", String(15), primary_key=True, nullable=False),
                    Column("baz", String(15)),
                )
                super(TestTable, self).__init__(db, "sqlite", scheduled_changes=True, historyClass=None, versioned=True)

        table = TestTable(self.db, self.metadata)
        self.metadata.create_all()
        table_sc = table.scheduled_changes
        what = {"baz": "baz", "change_type": "insert", "when": 876000}
        self.assertRaisesRegex(ValueError, "Missing primary key column ", table_sc.insert, changed_by="alice", **what)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testInsertForExistingNoSuchRow(self):
        what = {"fooid": 10, "foo": "thing", "data_version": 1, "when": 999000, "change_type": "update"}
        self.assertRaisesRegex(
            ValueError, "Cannot create scheduled change with data_version for non-existent row", self.sc_table.insert, changed_by="bob", **what
        )

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testInsertMissingRequiredPartOfPK(self):
        class TestTable2(AUSTable):
            def __init__(self, db, metadata):
                self.table = Table(
                    "test_table2", metadata, Column("fooid", Integer, primary_key=True), Column("foo", String(15), primary_key=True), Column("bar", String(15))
                )
                super(TestTable2, self).__init__(db, "sqlite", scheduled_changes=True, versioned=True)

            def getPotentialRequiredSignoffs(self, *args, **kwargs):
                return None

        table = TestTable2("fake", self.metadata)
        self.metadata.create_all()
        what = {"fooid": 2, "when": 4532000, "change_type": "insert"}
        self.assertRaisesRegex(ValueError, "Missing primary key column", table.scheduled_changes.insert, changed_by="bob", **what)

    def testInsertWithMalformedTimestamp(self):
        what = {"foo": "blah", "when": "abc", "change_type": "insert"}
        self.assertRaisesRegex(ValueError, "Cannot parse", self.sc_table.insert, changed_by="bob", **what)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testInsertDataVersionChanged(self):
        """Tests to make sure a scheduled change update is rejected if data
        version changes between grabbing the row to create a change, and
        submitting the scheduled change."""
        self.table.update([self.table.fooid == 3], what={"foo": "bb"}, changed_by="bob", old_data_version=2)
        what = {"fooid": 3, "data_version": 2, "bar": "blah", "when": 456000, "change_type": "update"}
        self.assertRaises(OutdatedDataError, self.sc_table.insert, changed_by="bob", **what)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testInsertWithoutPermissionOnBaseTable(self):
        what = {"fooid": 5, "bar": "blah", "when": 343000, "change_type": "insert"}
        self.assertRaises(PermissionDeniedError, self.sc_table.insert, changed_by="nancy", **what)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testInsertWithoutPermissionOnBaseTableForUpdate(self):
        what = {"fooid": 3, "bar": "blah", "when": 343000, "data_version": 2, "change_type": "update"}
        self.assertRaises(PermissionDeniedError, self.sc_table.insert, changed_by="nancy", **what)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testInsertRejectedWithAlreadyScheduledChange(self):
        what = {"fooid": 2, "foo": "b", "bar": "thing2", "data_version": 2, "when": 929000, "change_type": "update"}
        self.assertRaises(ChangeScheduledError, self.sc_table.insert, changed_by="bob", **what)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testInsertRaisesErrorOnDataVersionBetweenCoreAndConditions(self):
        # We need to fake out the conditions table insert so we do it ourselves
        def noop(*args, **kwargs):
            pass

        self.sc_table.conditions.insert = noop
        self.sc_table.conditions.t.insert().execute(sc_id=7, when=10000000, data_version=4)

        what = {"foo": "newthing1", "when": 888000, "change_type": "insert"}
        self.assertRaises(MismatchedDataVersionError, self.sc_table.insert, changed_by="bob", **what)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testInsertCreateExistingPK(self):
        what = {"fooid": 3, "foo": "mine is better", "when": 99999999, "change_type": "insert"}
        self.assertRaisesRegex(ValueError, "Cannot schedule change for duplicate PK", self.sc_table.insert, changed_by="bob", **what)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testDeleteScheduledChangeWithoutPKColumns(self):
        class TestTable2(AUSTable):
            def __init__(self, db, metadata):
                self.table = Table(
                    "test_table2", metadata, Column("fooid", Integer, primary_key=True), Column("foo", String(15), primary_key=True), Column("bar", String(15))
                )
                super(TestTable2, self).__init__(db, "sqlite", scheduled_changes=True, versioned=True)

            def getPotentialRequiredSignoffs(self, *args, **kwargs):
                return None

        table = TestTable2("fake", self.metadata)
        self.metadata.create_all()
        what = {"fooid": 2, "when": 4532000, "change_type": "delete"}
        self.assertRaises(ValueError, table.scheduled_changes.insert, changed_by="bob", **what)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testDeleteCompletedScheduledChange(self):
        where = [self.sc_table.sc_id == 5]
        self.assertRaises(ValueError, self.table.scheduled_changes.delete, where=where, changed_by="bob", old_data_version=1)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testRaisesErrorForMultipleDeletion(self):
        what = {"fooid": 4, "foo": "d", "data_version": 2, "when": 929000, "change_type": "delete"}
        self.assertRaises(ChangeScheduledError, self.sc_table.insert, changed_by="bob", **what)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testUpdateCompletedScheduledChange(self):
        where = [self.sc_table.sc_id == 5]
        what = {"foo": "bb"}
        self.assertRaises(ValueError, self.table.scheduled_changes.update, where=where, what=what, changed_by="bob", old_data_version=1)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testUpdateNoChangesSinceCreation(self):
        where = [self.sc_table.sc_id == 1]
        what = {"when": 888000, "foo": "bb"}
        self.sc_table.update(where, what, changed_by="bob", old_data_version=1)
        sc_row = self.sc_table.t.select().where(self.sc_table.sc_id == 1).execute().fetchall()[0]
        sc_history_row = self.sc_table.history.t.select().where(self.sc_table.history.sc_id == 1).execute().fetchall()[0]
        cond_row = self.sc_table.conditions.t.select().where(self.sc_table.conditions.sc_id == 1).execute().fetchall()[0]
        cond_history_row = self.sc_table.conditions.history.t.select().where(self.sc_table.conditions.history.sc_id == 1).execute().fetchall()[0]
        self.assertEqual(sc_row.scheduled_by, "bob")
        self.assertEqual(sc_row.change_type, "update")
        self.assertEqual(sc_row.data_version, 2)
        self.assertEqual(sc_row.base_fooid, 1)
        self.assertEqual(sc_row.base_foo, "bb")
        self.assertEqual(sc_row.base_bar, "barbar")
        self.assertEqual(sc_row.base_data_version, 1)
        self.assertEqual(sc_history_row.changed_by, "bob")
        self.assertEqual(sc_history_row.scheduled_by, "bob")
        self.assertEqual(sc_history_row.change_type, "update")
        self.assertEqual(sc_history_row.data_version, 2)
        self.assertEqual(sc_history_row.base_fooid, 1)
        self.assertEqual(sc_history_row.base_foo, "bb")
        self.assertEqual(sc_history_row.base_bar, "barbar")
        self.assertEqual(sc_history_row.base_data_version, 1)
        self.assertEqual(sc_history_row.change_id, 1)
        self.assertEqual(cond_row.when, 888000)
        self.assertEqual(cond_row.data_version, 2)
        self.assertEqual(cond_history_row.when, 888000)
        self.assertEqual(cond_history_row.data_version, 2)
        self.assertEqual(cond_history_row.change_id, 1)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testUpdateChangeIdAndDataVersionStayInSyncWithoutConditionsChange(self):
        where = [self.sc_table.sc_id == 1]
        what = {"foo": "bb"}
        self.sc_table.update(where, what, changed_by="bob", old_data_version=1)
        sc_row = self.sc_table.t.select().where(self.sc_table.sc_id == 1).execute().fetchall()[0]
        sc_history_row = self.sc_table.history.t.select().where(self.sc_table.history.sc_id == 1).execute().fetchall()[0]
        cond_row = self.sc_table.conditions.t.select().where(self.sc_table.conditions.sc_id == 1).execute().fetchall()[0]
        cond_history_row = self.sc_table.conditions.history.t.select().where(self.sc_table.conditions.history.sc_id == 1).execute().fetchall()[0]
        self.assertEqual(sc_row.scheduled_by, "bob")
        self.assertEqual(sc_row.change_type, "update")
        self.assertEqual(sc_row.data_version, 2)
        self.assertEqual(sc_row.base_fooid, 1)
        self.assertEqual(sc_row.base_foo, "bb")
        self.assertEqual(sc_row.base_bar, "barbar")
        self.assertEqual(sc_row.base_data_version, 1)
        self.assertEqual(sc_history_row.changed_by, "bob")
        self.assertEqual(sc_history_row.scheduled_by, "bob")
        self.assertEqual(sc_history_row.change_type, "update")
        self.assertEqual(sc_history_row.data_version, 2)
        self.assertEqual(sc_history_row.base_fooid, 1)
        self.assertEqual(sc_history_row.base_foo, "bb")
        self.assertEqual(sc_history_row.base_bar, "barbar")
        self.assertEqual(sc_history_row.base_data_version, 1)
        self.assertEqual(sc_history_row.change_id, 1)
        self.assertEqual(cond_row.when, 234000)
        self.assertEqual(cond_row.data_version, 2)
        self.assertEqual(cond_history_row.when, 234000)
        self.assertEqual(cond_history_row.data_version, 2)
        self.assertEqual(cond_history_row.change_id, 1)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testUpdateNoChangesSinceCreationWithDict(self):
        where = {"sc_id": 1}
        what = {"when": 888000, "foo": "bb", "data_version": 1, "fooid": 1}
        self.sc_table.update(where, what, changed_by="bob", old_data_version=1)
        sc_row = self.sc_table.t.select().where(self.sc_table.sc_id == 1).execute().fetchall()[0]
        sc_history_row = self.sc_table.history.t.select().where(self.sc_table.history.sc_id == 1).execute().fetchall()[0]
        cond_row = self.sc_table.conditions.t.select().where(self.sc_table.conditions.sc_id == 1).execute().fetchall()[0]
        cond_history_row = self.sc_table.conditions.history.t.select().where(self.sc_table.conditions.history.sc_id == 1).execute().fetchall()[0]
        self.assertEqual(sc_row.scheduled_by, "bob")
        self.assertEqual(sc_row.change_type, "update")
        self.assertEqual(sc_row.data_version, 2)
        self.assertEqual(sc_row.base_fooid, 1)
        self.assertEqual(sc_row.base_foo, "bb")
        self.assertEqual(sc_row.base_bar, "barbar")
        self.assertEqual(sc_row.base_data_version, 1)
        self.assertEqual(sc_history_row.changed_by, "bob")
        self.assertEqual(sc_history_row.scheduled_by, "bob")
        self.assertEqual(sc_history_row.change_type, "update")
        self.assertEqual(sc_history_row.data_version, 2)
        self.assertEqual(sc_history_row.base_fooid, 1)
        self.assertEqual(sc_history_row.base_foo, "bb")
        self.assertEqual(sc_history_row.base_bar, "barbar")
        self.assertEqual(sc_history_row.base_data_version, 1)
        self.assertEqual(cond_row.when, 888000)
        self.assertEqual(cond_row.data_version, 2)
        self.assertEqual(cond_history_row.when, 888000)
        self.assertEqual(cond_history_row.data_version, 2)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testUpdateWithBadConditions(self):
        where = [self.sc_table.sc_id == 1]
        what = {"telemetry_product": "boop", "telemetry_channel": "boop", "telemetry_uptake": 99}
        self.assertRaisesRegex(ValueError, "Invalid combination of conditions", self.sc_table.update, where, what, changed_by="bob", old_data_version=1)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testUpdateRemoveConditions(self):
        where = [self.sc_table.sc_id == 2]
        what = {"when": None}
        self.assertRaisesRegex(ValueError, "No conditions found", self.sc_table.update, where, what, changed_by="bob", old_data_version=1)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testUpdateRaisesErrorOnDataVersionBetweenCoreAndConditions(self):
        # We need to fake out the conditions table update method to make it possible to have mismatched versions
        def noop(*args, **kwargs):
            pass

        self.sc_table.conditions.update = noop
        self.sc_table.conditions.t.update().where(self.sc_table.conditions.sc_id == 1).execute(data_version=4)
        self.assertRaises(
            MismatchedDataVersionError, self.sc_table.update, [self.sc_table.sc_id == 1], what={"bar": "bar"}, changed_by="bob", old_data_version=1
        )

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testUpdateWithoutPermissionOnBaseTable(self):
        with mock.patch.object(self.sc_table.db, "hasPermission", return_value=False, create=True):
            where = [self.sc_table.sc_id == 2]
            what = {"when": 777000}
            self.assertRaises(PermissionDeniedError, self.sc_table.update, where, what, changed_by="sue", old_data_version=1)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
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
        sc_history_row = self.sc_table.history.t.select().where(self.sc_table.history.sc_id == 4).execute().fetchall()[0]
        cond_row = self.sc_table.conditions.t.select().where(self.sc_table.conditions.sc_id == 4).execute().fetchall()[0]
        cond_history_row = self.sc_table.conditions.history.t.select().where(self.sc_table.conditions.history.sc_id == 4).execute().fetchall()[0]
        self.assertEqual(row.fooid, 2)
        self.assertEqual(row.foo, "b")
        self.assertEqual(row.bar, "bar")
        self.assertEqual(row.data_version, 3)
        # This should end up with the scheduled changed incorporating our new
        # value for "foo" as well as the new "bar" value.
        self.assertEqual(sc_row.scheduled_by, "bob")
        self.assertEqual(sc_row.data_version, 2)
        self.assertEqual(sc_row.base_fooid, 2)
        self.assertEqual(sc_row.base_foo, "dd")
        self.assertEqual(sc_row.base_bar, "bar")
        self.assertEqual(sc_row.base_data_version, 3)
        # ...As well as a new history table entry.
        self.assertEqual(sc_history_row.changed_by, "bob")
        self.assertEqual(sc_history_row.scheduled_by, "bob")
        self.assertEqual(sc_history_row.data_version, 2)
        self.assertEqual(sc_history_row.base_fooid, 2)
        self.assertEqual(sc_history_row.base_foo, "dd")
        self.assertEqual(sc_history_row.base_bar, "bar")
        self.assertEqual(sc_history_row.base_data_version, 3)
        self.assertEqual(cond_row.when, 333000)
        self.assertEqual(cond_row.data_version, 2)
        self.assertEqual(cond_history_row.when, 333000)
        self.assertEqual(cond_history_row.data_version, 2)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testUpdateBaseTableNoConflictChangingToNull(self):
        # fooid 2 has a change scheduled that would update its "foo" column
        # we'll change "bar" underneath it. This doesn't conflict with the
        # scheduled change, so it should simply be updated with the new "bar"
        # value.
        self.table.update([self.table.fooid == 2], what={"bar": None}, changed_by="bob", old_data_version=2)
        row = self.table.t.select().where(self.table.fooid == 2).execute().fetchall()[0]
        sc_row = self.sc_table.t.select().where(self.sc_table.sc_id == 4).execute().fetchall()[0]
        sc_history_row = self.sc_table.history.t.select().where(self.sc_table.history.sc_id == 4).execute().fetchall()[0]
        cond_row = self.sc_table.conditions.t.select().where(self.sc_table.conditions.sc_id == 4).execute().fetchall()[0]
        cond_history_row = self.sc_table.conditions.history.t.select().where(self.sc_table.conditions.history.sc_id == 4).execute().fetchall()[0]
        self.assertEqual(row.fooid, 2)
        self.assertEqual(row.foo, "b")
        self.assertEqual(row.bar, None)
        self.assertEqual(row.data_version, 3)
        # This should end up with the scheduled changed incorporating our new
        # value for "foo" as well as the new "bar" value.
        self.assertEqual(sc_row.scheduled_by, "bob")
        self.assertEqual(sc_row.change_type, "update")
        self.assertEqual(sc_row.data_version, 2)
        self.assertEqual(sc_row.base_fooid, 2)
        self.assertEqual(sc_row.base_foo, "dd")
        self.assertEqual(sc_row.base_bar, None)
        self.assertEqual(sc_row.base_data_version, 3)
        # ...As well as a new history table entry.
        self.assertEqual(sc_history_row.changed_by, "bob")
        self.assertEqual(sc_history_row.scheduled_by, "bob")
        self.assertEqual(sc_history_row.change_type, "update")
        self.assertEqual(sc_history_row.data_version, 2)
        self.assertEqual(sc_history_row.base_fooid, 2)
        self.assertEqual(sc_history_row.base_foo, "dd")
        self.assertEqual(sc_history_row.base_bar, None)
        self.assertEqual(sc_history_row.base_data_version, 3)
        self.assertEqual(cond_row.when, 333000)
        self.assertEqual(cond_row.data_version, 2)
        self.assertEqual(cond_history_row.when, 333000)
        self.assertEqual(cond_history_row.data_version, 2)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testUpdateBaseTableConflictWithRecentChanges(self):
        where = [self.table.fooid == 1]
        what = {"bar": "bar"}
        self.assertRaises(UpdateMergeError, self.table.update, where=where, what=what, changed_by="bob", old_data_version=1)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testUpdateDeleteScheduledChange(self):
        where = {"sc_id": 6}
        what = {"when": 800000, "base_foo": "bb", "data_version": 1, "fooid": 1}
        self.sc_table.update(where, what, changed_by="bob", old_data_version=1)
        sc_row = self.sc_table.t.select().where(self.sc_table.sc_id == 6).execute().fetchall()[0]
        sc_history_row = self.sc_table.history.t.select().where(self.sc_table.history.sc_id == 6).execute().fetchall()[0]
        cond_row = self.sc_table.conditions.t.select().where(self.sc_table.conditions.sc_id == 6).execute().fetchall()[0]
        cond_history_row = self.sc_table.conditions.history.t.select().where(self.sc_table.conditions.history.sc_id == 6).execute().fetchall()[0]
        self.assertEqual(sc_row.scheduled_by, "bob")
        self.assertEqual(sc_row.change_type, "delete")
        self.assertEqual(sc_row.data_version, 2)
        self.assertEqual(sc_row.base_fooid, 1)
        self.assertEqual(sc_row.base_foo, "bb")
        self.assertEqual(sc_row.base_data_version, 1)
        self.assertEqual(sc_history_row.changed_by, "bob")
        self.assertEqual(sc_history_row.scheduled_by, "bob")
        self.assertEqual(sc_history_row.change_type, "delete")
        self.assertEqual(sc_history_row.data_version, 2)
        self.assertEqual(sc_history_row.base_fooid, 1)
        self.assertEqual(sc_history_row.base_foo, "bb")
        self.assertEqual(sc_history_row.base_data_version, 1)
        self.assertEqual(cond_row.when, 800000)
        self.assertEqual(cond_row.data_version, 2)
        self.assertEqual(cond_history_row.when, 800000)
        self.assertEqual(cond_history_row.data_version, 2)

    def testDeleteChangeForDeleteScheduledChange(self):
        self.sc_table.delete(where=[self.sc_table.sc_id == 6], changed_by="bob", old_data_version=1)
        ret = self.sc_table.t.select().where(self.sc_table.sc_id == 6).execute().fetchall()
        self.assertEqual(len(ret), 0)
        ret = self.sc_table.conditions.t.select().where(self.sc_table.conditions.sc_id == 6).execute().fetchall()
        self.assertEqual(len(ret), 0)

    def testDeleteChange(self):
        self.sc_table.delete(where=[self.sc_table.sc_id == 2], changed_by="bob", old_data_version=1)
        ret = self.sc_table.t.select().where(self.sc_table.sc_id == 2).execute().fetchall()
        self.assertEqual(len(ret), 0)
        ret = self.sc_table.conditions.t.select().where(self.sc_table.conditions.sc_id == 2).execute().fetchall()
        self.assertEqual(len(ret), 0)

    def testDeleteChangeWithoutPermission(self):
        self.assertRaises(PermissionDeniedError, self.sc_table.delete, where=[self.sc_table.sc_id == 2], changed_by="nicole", old_data_version=1)

    def testBaseTableDeletesFailsWithScheduledChange(self):
        self.assertRaises(ChangeScheduledError, self.table.delete, where=[self.table.fooid == 2], changed_by="bob", old_data_version=2)

    def testBaseTableDeleteSucceedsWithoutScheduledChange(self):
        self.table.delete(where=[self.table.fooid == 3], changed_by="bob", old_data_version=2)

    def testEnactChangeNewRow(self):
        self.table.scheduled_changes.enactChange(2, "nancy")
        row = self.table.t.select().where(self.table.fooid == 5).execute().fetchall()[0]
        history_rows = self.table.history.t.select().where(self.table.history.fooid == 5).execute().fetchall()
        sc_row = self.sc_table.t.select().where(self.sc_table.sc_id == 2).execute().fetchall()[0]
        self.assertEqual(row.fooid, 5)
        self.assertEqual(row.foo, "cc")
        self.assertEqual(row.bar, "ceecee")
        self.assertEqual(row.data_version, 1)
        self.assertEqual(history_rows[0].fooid, 5)
        self.assertEqual(history_rows[0].foo, None)
        self.assertEqual(history_rows[0].bar, None)
        self.assertEqual(history_rows[0].changed_by, "bob")
        self.assertEqual(history_rows[0].data_version, None)
        self.assertEqual(history_rows[1].fooid, 5)
        self.assertEqual(history_rows[1].foo, "cc")
        self.assertEqual(history_rows[1].bar, "ceecee")
        self.assertEqual(history_rows[1].changed_by, "bob")
        self.assertEqual(history_rows[1].data_version, 1)
        self.assertEqual(sc_row.complete, True)

    def testEnactChangeExistingRow(self):
        self.table.scheduled_changes.enactChange(1, "nancy")
        row = self.table.t.select().where(self.table.fooid == 1).execute().fetchall()[0]
        history_row = self.table.history.t.select().where(self.table.history.fooid == 1).where(self.table.history.data_version == 2).execute().fetchall()[0]
        sc_row = self.sc_table.t.select().where(self.sc_table.sc_id == 1).execute().fetchall()[0]
        self.assertEqual(row.foo, "aa")
        self.assertEqual(row.bar, "barbar")
        self.assertEqual(row.data_version, 2)
        self.assertEqual(history_row.foo, "aa")
        self.assertEqual(history_row.bar, "barbar")
        self.assertEqual(history_row.changed_by, "bob")
        self.assertEqual(history_row.data_version, 2)
        self.assertEqual(sc_row.complete, True)

    def testEnactChangeForDeletingExistingRow(self):
        self.table.scheduled_changes.enactChange(6, "nancy")
        row = self.table.t.select().where(self.table.fooid == 4).execute().fetchall()
        self.assertEqual(row, [])

    def testEnactChangeNoPermissions(self):
        # TODO: May want to add something to permissions api/ui that warns if a user has a scheduled change when changing their permissions
        self.assertRaises(PermissionDeniedError, self.table.scheduled_changes.enactChange, 1, "jeremy")

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testEnactInsertsInConditionsHistory(self):
        where = [self.sc_table.sc_id == 2]
        what = {"foo": "bb"}
        self.sc_table.update(where, what, changed_by="bob", old_data_version=1)
        self.table.scheduled_changes.enactChange(2, "nancy")
        num_history_row = self.sc_table.history.t.select().where(self.sc_table.history.sc_id == 2).execute().fetchall()
        num_cond_history_row = self.sc_table.conditions.history.t.select().where(self.sc_table.conditions.history.sc_id == 2).execute().fetchall()
        self.assertEqual(len(num_cond_history_row), len(num_history_row))

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testMergeUpdateWithConflict(self):
        old_row = self.table.select(where=[self.table.fooid == 1])[0]
        what = {"fooid": 1, "bar": "abc", "data_version": 1}
        self.assertRaises(UpdateMergeError, self.sc_table.mergeUpdate, old_row, what, changed_by="bob")

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testMergeDontChangeScheduledby(self):
        self.table.update([self.table.fooid == 2], what={"bar": "bar1"}, changed_by="mary", old_data_version=2)
        new_row = self.sc_table.select(where=[self.sc_table.sc_id == 4])[0]
        self.assertEqual(new_row["scheduled_by"], "bob")

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testMergeUpdateForDeleteScheduledChange(self):
        old_row = self.table.select(where=[self.table.fooid == 4])[0]
        what = {"fooid": 4, "bar": "abc", "data_version": 2}
        self.sc_table.mergeUpdate(old_row, what, changed_by="bob")
        new_row = self.sc_table.select(where=[self.sc_table.sc_id == 6])[0]
        self.assertEqual(new_row["base_data_version"], 2)
        self.assertEqual(new_row["base_bar"], "abc")

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testMergeUpdateWithConflictWhenSameValAndCol(self):
        # This is from bug #1333874 - if an update and scheduled change update
        # the same column with the same value, mergeUpdate should throw an exception.
        old_row = self.table.select(where=[self.table.fooid == 1])[0]
        what = {"fooid": 1, "bar": "barbar", "data_version": 1}
        self.assertRaises(UpdateMergeError, self.sc_table.mergeUpdate, old_row, what, changed_by="bob")


@pytest.mark.usefixtures("current_db_schema")
class TestScheduledChangesWithConfigurableConditions(unittest.TestCase, MemoryDatabaseMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.metadata.create_all(self.db.engine)
        self.engine = self.db.engine
        self.metadata = self.db.metadata

        class TestTable(AUSTable):
            def __init__(self, db, metadata):
                self.table = Table(
                    "test_table",
                    metadata,
                    Column("fooid", Integer, primary_key=True, autoincrement=True),
                    Column("foo", String(15), nullable=False),
                    Column("bar", String(15)),
                )
                super(TestTable, self).__init__(
                    db, "sqlite", scheduled_changes=True, scheduled_changes_kwargs={"conditions": ["time"]}, versioned=True, historyClass=HistoryTable
                )

            def getPotentialRequiredSignoffs(self, *args, **kwargs):
                return None

        self.table = TestTable(self.db, self.metadata)
        self.sc_table = self.table.scheduled_changes
        self.metadata.create_all()
        self.table.t.insert().execute(fooid=10, foo="h", data_version=1)
        self.table.t.insert().execute(fooid=11, foo="i", bar="j", data_version=1)
        self.sc_table.t.insert().execute(
            sc_id=1, scheduled_by="bob", base_fooid=10, base_foo="h", base_bar="bbb", base_data_version=1, data_version=1, change_type="update"
        )
        self.sc_table.conditions.t.insert().execute(sc_id=1, when=87000, data_version=1)
        self.db.permissions.t.insert().execute(permission="admin", username="bob", data_version=1)

    def testAllTablesCreated(self):
        self.assertTrue(self.table)
        self.assertTrue(self.table.history)
        self.assertTrue(self.table.scheduled_changes)
        self.assertTrue(self.table.scheduled_changes.history)
        self.assertTrue(self.table.scheduled_changes.conditions)
        self.assertTrue(self.table.scheduled_changes.conditions.history)
        self.assertTrue(self.table.scheduled_changes.signoffs)
        self.assertTrue(self.table.scheduled_changes.signoffs.history)

    def testSCTableHasCorrectColumns(self):
        sc_columns = [c.name for c in self.sc_table.t.columns]
        self.assertTrue("sc_id" in sc_columns)
        self.assertTrue("scheduled_by" in sc_columns)
        self.assertTrue("complete" in sc_columns)
        self.assertTrue("data_version" in sc_columns)
        self.assertTrue("base_fooid" in sc_columns)
        self.assertTrue("base_foo" in sc_columns)
        self.assertTrue("base_bar" in sc_columns)
        self.assertTrue("base_data_version" in sc_columns)
        self.assertTrue("telemetry_product" not in sc_columns)
        self.assertTrue("telemetry_channel" not in sc_columns)
        self.assertTrue("telemetry_uptake" not in sc_columns)
        self.assertTrue("when" not in sc_columns)

        cond_columns = [c.name for c in self.sc_table.conditions.t.columns]
        self.assertTrue("sc_id" in cond_columns)
        self.assertTrue("telemetry_product" not in cond_columns)
        self.assertTrue("telemetry_channel" not in cond_columns)
        self.assertTrue("telemetry_uptake" not in cond_columns)
        self.assertTrue("when" in cond_columns)

        signoff_columns = [c.name for c in self.sc_table.signoffs.t.columns]
        self.assertTrue("sc_id" in signoff_columns)
        self.assertTrue("username" in signoff_columns)
        self.assertTrue("role" in signoff_columns)

    def testSCTableWithNoConditions(self):
        class TestTable2(AUSTable):
            def __init__(self, db, metadata):
                self.table = Table(
                    "test_table3",
                    metadata,
                    Column("fooid", Integer, primary_key=True, autoincrement=True),
                    Column("foo", String(15), nullable=False),
                    Column("bar", String(15)),
                )
                super(TestTable2, self).__init__(db, "sqlite", scheduled_changes=True, scheduled_changes_kwargs={"conditions": []}, versioned=True)

            def getPotentialRequiredSignoffs(self, *args, **kwargs):
                return None

        self.assertRaisesRegex(ValueError, "No conditions enabled", TestTable2, self.db, self.metadata)

    def testSCTableWithBadConditions(self):
        class TestTable3(AUSTable):
            def __init__(self, db, metadata):
                self.table = Table(
                    "test_table3",
                    metadata,
                    Column("fooid", Integer, primary_key=True, autoincrement=True),
                    Column("foo", String(15), nullable=False),
                    Column("bar", String(15)),
                )
                super(TestTable3, self).__init__(
                    db, "sqlite", scheduled_changes=True, scheduled_changes_kwargs={"conditions": ["time", "blech"]}, versioned=True
                )

            def getPotentialRequiredSignoffs(self, *args, **kwargs):
                return None

        self.assertRaisesRegex(ValueError, "Unknown conditions", TestTable3, self.db, self.metadata)

    def testValidateConditionsNone(self):
        self.assertRaisesRegex(ValueError, "No conditions found", self.sc_table.conditions.validate, {})

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testValidateConditionsJustWhen(self):
        self.sc_table.conditions.validate({"when": 12345678})

    def testValidateConditionsTelemetryRaisesError(self):
        conditions = {"telemetry_product": "Firefox", "telemetry_channel": "nightly", "telemetry_uptake": "200000"}
        self.assertRaisesRegex(ValueError, "uptake condition is disabled", self.sc_table.conditions.validate, conditions)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testInsertWithEnabledCondition(self):
        what = {"fooid": 11, "foo": "i", "bar": "jjj", "data_version": 1, "when": 909000, "change_type": "update"}
        self.sc_table.insert(changed_by="bob", **what)
        row = self.sc_table.t.select().where(self.sc_table.sc_id == 2).execute().fetchall()[0]
        cond_row = self.sc_table.conditions.t.select().where(self.sc_table.conditions.sc_id == 2).execute().fetchall()[0]
        self.assertEqual(row.scheduled_by, "bob")
        self.assertEqual(row.change_type, "update")
        self.assertEqual(row.data_version, 1)
        self.assertEqual(row.base_fooid, 11)
        self.assertEqual(row.base_foo, "i")
        self.assertEqual(row.base_bar, "jjj")
        self.assertEqual(row.base_data_version, 1)
        self.assertEqual(cond_row.when, 909000)
        self.assertEqual(cond_row.data_version, 1)

    def testInsertWithDisabledCondition(self):
        what = {
            "fooid": 11,
            "foo": "i",
            "bar": "jjj",
            "data_version": 1,
            "telemetry_product": "aa",
            "telemetry_channel": "bb",
            "telemetry_uptake": 34567,
            "change_type": "update",
        }
        self.assertRaisesRegex(ValueError, "uptake condition is disabled", self.sc_table.insert, changed_by="bob", **what)

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testUpdateWithNewValueForEnabledCondition(self):
        where = [self.sc_table.sc_id == 1]
        what = {"when": 1000300, "bar": "ccc"}
        self.sc_table.update(where, what, changed_by="bob", old_data_version=1)
        row = self.sc_table.t.select().where(self.sc_table.sc_id == 1).execute().fetchall()[0]
        cond_row = self.sc_table.conditions.t.select().where(self.sc_table.conditions.sc_id == 1).execute().fetchall()[0]
        history_row = self.sc_table.history.t.select().where(self.sc_table.history.sc_id == 1).execute().fetchall()[0]
        cond_history_row = self.sc_table.conditions.history.t.select().where(self.sc_table.conditions.history.sc_id == 1).execute().fetchall()[0]
        self.assertEqual(row.scheduled_by, "bob")
        self.assertEqual(row.change_type, "update")
        self.assertEqual(row.data_version, 2)
        self.assertEqual(row.base_fooid, 10)
        self.assertEqual(row.base_foo, "h")
        self.assertEqual(row.base_bar, "ccc")
        self.assertEqual(row.base_data_version, 1)
        self.assertEqual(history_row.changed_by, "bob")
        self.assertEqual(history_row.scheduled_by, "bob")
        self.assertEqual(history_row.change_type, "update")
        self.assertEqual(history_row.data_version, 2)
        self.assertEqual(history_row.base_fooid, 10)
        self.assertEqual(history_row.base_foo, "h")
        self.assertEqual(history_row.base_bar, "ccc")
        self.assertEqual(history_row.base_data_version, 1)
        self.assertEqual(cond_row.when, 1000300)
        self.assertEqual(cond_row.data_version, 2)
        self.assertEqual(cond_history_row.changed_by, "bob")
        self.assertEqual(cond_history_row.when, 1000300)
        self.assertEqual(cond_history_row.data_version, 2)

    def testUpdateChangeToDisabledCondition(self):
        where = [self.sc_table.sc_id == 1]
        what = {"telemetry_product": "pro", "telemetry_channel": "cha", "telemetry_uptake": 3456, "bar": "ccc", "when": None}
        self.assertRaisesRegex(ValueError, "uptake condition is disabled", self.sc_table.update, where, what, changed_by="bob", old_data_version=1)


@pytest.mark.usefixtures("current_db_schema")
class TestSignoffsTable(unittest.TestCase, MemoryDatabaseMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.metadata.create_all(self.db.engine)
        self.engine = self.db.engine
        self.metadata = self.db.metadata
        self.signoffs = SignoffsTable(self.db, self.metadata, "sqlite", "test_table")
        self.metadata.create_all()
        self.db.setSystemAccounts(["goodbot"])
        self.db.permissions.user_roles.t.insert().execute(username="bob", role="releng", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="bob", role="dev", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="nancy", role="relman", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="nancy", role="qa", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="janet", role="relman", data_version=1)
        self.db.permissions.t.insert().execute(permission="admin", username="charlie", data_version=1)
        self.signoffs.t.insert().execute(sc_id=1, username="nancy", role="relman")

    def testSignoffsHasCorrectTablesAndColumns(self):
        columns = [c.name for c in self.signoffs.t.columns]
        expected = ["sc_id", "username", "role"]
        self.assertEqual(set(columns), set(expected))
        history_columns = [c.name for c in self.signoffs.history.t.columns]
        expected = ["change_id", "changed_by", "timestamp"] + expected
        self.assertEqual(set(history_columns), set(expected))

    def testSignoffWithPermission(self):
        self.signoffs.insert("bob", sc_id=1, username="bob", role="releng")
        got = self.signoffs.t.select().where(self.signoffs.sc_id == 1).where(self.signoffs.username == "bob").execute().fetchall()
        self.assertEqual(got, [(1, "bob", "releng")])

    def testSignoffWithoutPermission(self):
        self.assertRaisesRegex(
            PermissionDeniedError, "jim cannot signoff with role 'releng'", self.signoffs.insert, "jim", sc_id=1, username="jim", role="releng"
        )

    def testSignoffWithoutPermissionSystemAccount(self):
        self.assertRaisesRegex(
            PermissionDeniedError, "System account cannot signoff", self.signoffs.insert, "goodbot", sc_id=1, username="goodbot", role="releng"
        )

    def testSignoffASecondTimeWithSameRole(self):
        self.signoffs.insert("nancy", sc_id=1, username="nancy", role="relman")
        got = self.signoffs.t.select().where(self.signoffs.sc_id == 1).where(self.signoffs.username == "nancy").execute().fetchall()
        self.assertEqual(got, [(1, "nancy", "relman")])
        history = self.signoffs.history.t.select().where(self.signoffs.sc_id == 1).where(self.signoffs.username == "nancy").execute().fetchall()
        self.assertEqual(len(history), 0)

    def testSignoffWithSecondRole(self):
        self.assertRaisesRegex(PermissionDeniedError, "Cannot signoff with a second role", self.signoffs.insert, "nancy", sc_id=1, username="nancy", role="qa")

    def testCannotUpdateSignoff(self):
        self.assertRaises(AttributeError, self.signoffs.update, {"username": "nancy"}, {"role": "qa"}, "nancy")

    def testRevokeSignoff(self):
        self.signoffs.delete({"sc_id": 1, "username": "nancy"}, changed_by="nancy")
        got = self.signoffs.t.select().where(self.signoffs.sc_id == 1).where(self.signoffs.username == "nancy").execute().fetchall()
        self.assertEqual(len(got), 0)

    def testRevokeOtherUsersSignoffAsAdmin(self):
        self.signoffs.delete({"sc_id": 1, "username": "nancy"}, changed_by="charlie")
        got = self.signoffs.t.select().where(self.signoffs.sc_id == 1).where(self.signoffs.username == "nancy").execute().fetchall()
        self.assertEqual(len(got), 0)

    def testRevokeOtherUsersSignoffWithSameRole(self):
        self.signoffs.delete({"sc_id": 1, "username": "nancy"}, changed_by="janet")
        got = self.signoffs.t.select().where(self.signoffs.sc_id == 1).where(self.signoffs.username == "nancy").execute().fetchall()
        self.assertEqual(len(got), 0)

    def testRevokeOtherUsersSignoffWithoutPermission(self):
        self.assertRaisesRegex(
            PermissionDeniedError,
            "Cannot revoke a signoff made by someone in a group you do not belong to",
            self.signoffs.delete,
            {"sc_id": 1, "username": "nancy"},
            changed_by="bob",
        )

    def testRevokeOtherUsersSignoffWithoutPermissionSystemAccount(self):
        self.assertRaisesRegex(
            PermissionDeniedError, "System accounts cannot revoke a signoff", self.signoffs.delete, {"sc_id": 1, "username": "nancy"}, changed_by="goodbot"
        )


@pytest.mark.usefixtures("current_db_schema")
class TestProductRequiredSignoffsTable(unittest.TestCase, MemoryDatabaseMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.metadata.create_all(self.db.engine)
        self.engine = self.db.engine
        self.metadata = self.db.metadata
        self.rs = self.db.productRequiredSignoffs
        self.metadata.create_all()
        self.db.permissions.t.insert().execute(username="bill", permission="admin", data_version=1)
        self.db.permissions.t.insert().execute(username="bob", permission="required_signoff", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="bob", role="releng", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="bob", role="dev", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="nancy", role="relman", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="nancy", role="qa", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="janet", role="relman", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="janet", role="releng", data_version=1)
        self.rs.t.insert().execute(product="foo", channel="bar", role="releng", signoffs_required=1, data_version=1)
        self.rs.t.insert().execute(product="foo", channel="bar", role="relman", signoffs_required=2, data_version=1)
        self.rs.t.insert().execute(product="apple", channel="orange", role="releng", signoffs_required=2, data_version=1)
        self.rs.scheduled_changes.t.insert().execute(
            sc_id=1,
            scheduled_by="bob",
            complete=False,
            change_type="update",
            data_version=1,
            base_product="apple",
            base_channel="orange",
            base_role="releng",
            base_signoffs_required=1,
            base_data_version=1,
        )
        self.rs.scheduled_changes.conditions.t.insert().execute(sc_id=1, when=300000, data_version=1)
        self.rs.scheduled_changes.signoffs.t.insert().execute(sc_id=1, username="bob", role="releng")
        self.rs.scheduled_changes.signoffs.t.insert().execute(sc_id=1, username="janet", role="releng")
        self.rs.scheduled_changes.t.insert().execute(
            sc_id=2,
            scheduled_by="bob",
            complete=False,
            change_type="delete",
            data_version=1,
            base_product="foo",
            base_channel="bar",
            base_role="releng",
            base_data_version=1,
        )
        self.rs.scheduled_changes.conditions.t.insert().execute(sc_id=2, when=400000, data_version=1)
        self.rs.scheduled_changes.signoffs.t.insert().execute(sc_id=2, username="bob", role="releng")
        self.rs.scheduled_changes.signoffs.t.insert().execute(sc_id=2, username="janet", role="relman")
        self.rs.scheduled_changes.signoffs.t.insert().execute(sc_id=2, username="nancy", role="relman")
        self.rs.scheduled_changes.t.insert().execute(
            sc_id=3,
            scheduled_by="bob",
            complete=False,
            change_type="insert",
            data_version=1,
            base_product="foo",
            base_channel="bar",
            base_role="qa",
            base_signoffs_required=1,
        )
        self.rs.scheduled_changes.conditions.t.insert().execute(sc_id=3, when=300000, data_version=1)
        self.rs.scheduled_changes.signoffs.t.insert().execute(sc_id=3, username="bob", role="releng")
        self.rs.scheduled_changes.signoffs.t.insert().execute(sc_id=3, username="janet", role="relman")
        self.rs.scheduled_changes.signoffs.t.insert().execute(sc_id=3, username="nancy", role="relman")
        self.rs.scheduled_changes.t.insert().execute(
            sc_id=4,
            scheduled_by="bob",
            complete=False,
            change_type="insert",
            data_version=1,
            base_product="foo",
            base_channel="bar",
            base_role="dev",
            base_signoffs_required=1,
        )
        self.rs.scheduled_changes.conditions.t.insert().execute(sc_id=4, when=300000, data_version=1)
        self.rs.scheduled_changes.signoffs.t.insert().execute(sc_id=4, username="bob", role="releng")

    def testInsertNewRequiredSignoff(self):
        self.rs.insert(changed_by="bill", product="carrot", channel="celery", role="releng", signoffs_required=1)
        got = self.rs.t.select().where(self.rs.product == "carrot").execute().fetchall()
        self.assertEqual(got, [("carrot", "celery", "releng", 1, 1)])

    def testInsertNewRequiredSignoffWithSpecificPermission(self):
        self.rs.insert(changed_by="bob", product="carrot", channel="celery", role="releng", signoffs_required=1)
        got = self.rs.t.select().where(self.rs.product == "carrot").execute().fetchall()
        self.assertEqual(got, [("carrot", "celery", "releng", 1, 1)])

    def testInsertNewRequiredSignoffWithoutPermission(self):
        self.assertRaises(PermissionDeniedError, self.rs.insert, changed_by="chuck", product="carrot", channel="celery", role="releng", signoffs_required=1)

    def testCantDirectlyInsertRequiredSignoffForSomethingRequiringSignoff(self):
        self.assertRaises(SignoffRequiredError, self.rs.insert, changed_by="bill", product="apple", channel="orange", role="relman", signoffs_required=2)

    def testCantInsertRequiredSignoffWithoutEnoughUsers(self):
        self.assertRaises(ValueError, self.rs.insert, changed_by="bill", product="carrot", channel="celery", role="dev", signoffs_required=5)

    def testUpdateRequiredSignoffWithoutPermission(self):
        self.assertRaises(
            PermissionDeniedError, self.rs.update, changed_by="chuck", old_data_version=1, where={"product": "apple"}, what={"signoffs_required": 1}
        )

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testCantDirectlyUpdateRequiredSignoff(self):
        self.assertRaises(
            SignoffRequiredError, self.rs.update, changed_by="bill", old_data_version=1, where={"product": "apple"}, what={"signoffs_required": 1}
        )

    def testCantUpdateRequiredSignoffWithoutEnoughUsers(self):
        self.assertRaises(
            ValueError, self.rs.update, {"product": "apple", "channel": "orange"}, {"signoffs_required": 10}, changed_by="bill", old_data_version=1, dryrun=True
        )

    def testDeleteRequiredSignoffWithoutPermission(self):
        self.assertRaises(
            PermissionDeniedError, self.rs.delete, changed_by="chuck", old_data_version=1, where={"product": "foo", "channel": "bar", "role": "relman"}
        )

    def testCantDirectlyDeleteRequiredSignoff(self):
        self.assertRaises(
            SignoffRequiredError, self.rs.delete, changed_by="bill", old_data_version=1, where={"product": "foo", "channel": "bar", "role": "relman"}
        )

    def testInsertRequiredSignoffWithScheduledChange(self):
        self.rs.scheduled_changes.enactChange(sc_id=3, enacted_by="bill")
        got = self.rs.t.select().where(self.rs.product == "foo").where(self.rs.channel == "bar").where(self.rs.role == "qa").execute().fetchall()
        self.assertEqual(got, [("foo", "bar", "qa", 1, 1)])

    def testInsertRequiredSignoffWithoutEnoughSignoffs(self):
        self.assertRaises(SignoffRequiredError, self.rs.scheduled_changes.enactChange, sc_id=4, enacted_by="bill")

    def testUpdateRequiredSignoffWithScheduledChange(self):
        self.rs.scheduled_changes.enactChange(sc_id=1, enacted_by="bill")
        got = self.rs.t.select().where(self.rs.product == "apple").execute().fetchall()
        self.assertEqual(got, [("apple", "orange", "releng", 1, 2)])

    def testDeleteRequiredSignoffWithScheduledChange(self):
        self.rs.scheduled_changes.enactChange(sc_id=2, enacted_by="bill")
        got = self.rs.t.select().where(self.rs.product == "foo").where(self.rs.channel == "bar").where(self.rs.role == "releng").execute().fetchall()
        self.assertEqual(len(got), 0)


@pytest.mark.usefixtures("current_db_schema")
class TestPermissionsRequiredSignoffsTable(unittest.TestCase, MemoryDatabaseMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.metadata.create_all(self.db.engine)
        self.engine = self.db.engine
        self.metadata = self.db.metadata
        self.rs = self.db.permissionsRequiredSignoffs
        self.metadata.create_all()
        self.db.permissions.t.insert().execute(username="bill", permission="admin", data_version=1)
        self.db.permissions.t.insert().execute(username="bob", permission="required_signoff", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="bob", role="releng", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="bob", role="dev", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="nancy", role="relman", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="nancy", role="qa", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="janet", role="relman", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="janet", role="releng", data_version=1)
        self.rs.t.insert().execute(product="foo", role="releng", signoffs_required=1, data_version=1)
        self.rs.t.insert().execute(product="foo", role="relman", signoffs_required=2, data_version=1)
        self.rs.t.insert().execute(product="apple", role="releng", signoffs_required=2, data_version=1)
        self.rs.scheduled_changes.t.insert().execute(
            sc_id=1,
            scheduled_by="bob",
            complete=False,
            change_type="update",
            data_version=1,
            base_product="apple",
            base_role="releng",
            base_signoffs_required=1,
            base_data_version=1,
        )
        self.rs.scheduled_changes.conditions.t.insert().execute(sc_id=1, when=300000, data_version=1)
        self.rs.scheduled_changes.signoffs.t.insert().execute(sc_id=1, username="bob", role="releng")
        self.rs.scheduled_changes.signoffs.t.insert().execute(sc_id=1, username="janet", role="releng")
        self.rs.scheduled_changes.t.insert().execute(
            sc_id=2, scheduled_by="bob", complete=False, change_type="delete", data_version=1, base_product="foo", base_role="releng", base_data_version=1
        )
        self.rs.scheduled_changes.conditions.t.insert().execute(sc_id=2, when=400000, data_version=1)
        self.rs.scheduled_changes.signoffs.t.insert().execute(sc_id=2, username="bob", role="releng")
        self.rs.scheduled_changes.signoffs.t.insert().execute(sc_id=2, username="janet", role="relman")
        self.rs.scheduled_changes.signoffs.t.insert().execute(sc_id=2, username="nancy", role="relman")
        self.rs.scheduled_changes.t.insert().execute(
            sc_id=3, scheduled_by="bob", complete=False, change_type="insert", data_version=1, base_product="foo", base_role="qa", base_signoffs_required=1
        )
        self.rs.scheduled_changes.conditions.t.insert().execute(sc_id=3, when=300000, data_version=1)
        self.rs.scheduled_changes.signoffs.t.insert().execute(sc_id=3, username="bob", role="releng")
        self.rs.scheduled_changes.signoffs.t.insert().execute(sc_id=3, username="janet", role="relman")
        self.rs.scheduled_changes.signoffs.t.insert().execute(sc_id=3, username="nancy", role="relman")

    def testInsertNewRequiredSignoff(self):
        self.rs.insert(changed_by="bill", product="carrot", role="releng", signoffs_required=1)
        got = self.rs.t.select().where(self.rs.product == "carrot").execute().fetchall()
        self.assertEqual(got, [("carrot", "releng", 1, 1)])

    def testInsertNewRequiredSignoffWithSpecificPermission(self):
        self.rs.insert(changed_by="bob", product="carrot", role="releng", signoffs_required=1)
        got = self.rs.t.select().where(self.rs.product == "carrot").execute().fetchall()
        self.assertEqual(got, [("carrot", "releng", 1, 1)])

    def testInsertNewRequiredSignoffWithoutPermission(self):
        self.assertRaises(PermissionDeniedError, self.rs.insert, changed_by="chuck", product="carrot", role="releng", signoffs_required=1)

    def testCantDirectlyInsertRequiredSignoffForSomethingRequiringSignoff(self):
        self.assertRaises(SignoffRequiredError, self.rs.insert, changed_by="bill", product="apple", role="relman", signoffs_required=2)

    def testCantInsertRequiredSignoffWithoutEnoughUsers(self):
        self.assertRaises(ValueError, self.rs.insert, changed_by="bill", product="carrot", role="dev", signoffs_required=5)

    def testUpdateRequiredSignoffWithoutPermission(self):
        self.assertRaises(
            PermissionDeniedError, self.rs.update, changed_by="chuck", old_data_version=1, where={"product": "apple"}, what={"signoffs_required": 1}
        )

    @mock.patch("time.time", mock.MagicMock(return_value=200))
    def testCantDirectlyUpdateRequiredSignoff(self):
        self.assertRaises(
            SignoffRequiredError, self.rs.update, changed_by="bill", old_data_version=1, where={"product": "apple"}, what={"signoffs_required": 1}
        )

    def testCantUpdateRequiredSignoffWithoutEnoughUsers(self):
        self.assertRaises(ValueError, self.rs.update, {"product": "apple"}, {"signoffs_required": 10}, changed_by="bill", old_data_version=1, dryrun=True)

    def testDeleteRequiredSignoffWithoutPermission(self):
        self.assertRaises(PermissionDeniedError, self.rs.delete, changed_by="chuck", old_data_version=1, where={"product": "foo", "role": "relman"})

    def testCantDirectlyDeleteRequiredSignoff(self):
        self.assertRaises(SignoffRequiredError, self.rs.delete, changed_by="bill", old_data_version=1, where={"product": "foo", "role": "relman"})

    def testInsertRequiredSignoffWithScheduledChange(self):
        self.rs.scheduled_changes.enactChange(sc_id=3, enacted_by="bill")
        got = self.rs.t.select().where(self.rs.product == "foo").where(self.rs.role == "qa").execute().fetchall()
        self.assertEqual(got, [("foo", "qa", 1, 1)])

    def testUpdateRequiredSignoffWithScheduledChange(self):
        self.rs.scheduled_changes.enactChange(sc_id=1, enacted_by="bill")
        got = self.rs.t.select().where(self.rs.product == "apple").execute().fetchall()
        self.assertEqual(got, [("apple", "releng", 1, 2)])

    def testDeleteRequiredSignoffWithScheduledChange(self):
        self.rs.scheduled_changes.enactChange(sc_id=2, enacted_by="bill")
        got = self.rs.t.select().where(self.rs.product == "foo").where(self.rs.role == "releng").execute().fetchall()
        self.assertEqual(len(got), 0)


class RulesTestMixin(object):
    def _stripNullColumns(self, rules):
        # We know a bunch of columns are going to be empty...easier to strip them out
        # than to be super verbose (also should let this test continue to work even
        # if the schema changes).
        for rule in rules:
            for key in rule.copy().keys():
                if rule[key] is None:
                    del rule[key]
        return rules


@pytest.mark.usefixtures("current_db_schema")
class TestRulesSimple(unittest.TestCase, RulesTestMixin, MemoryDatabaseMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.metadata.create_all(self.db.engine)
        self.paths = self.db.rules
        self.paths.t.insert().execute(
            rule_id=1, priority=100, version="3.5", buildTarget="d", backgroundRate=100, mapping="c", update_type="z", product="a", channel="a", data_version=1
        )
        self.paths.t.insert().execute(
            rule_id=2, priority=100, version="3.3", buildTarget="d", backgroundRate=100, mapping="b", update_type="z", product="a", channel="a", data_version=1
        )
        self.paths.t.insert().execute(
            rule_id=3, priority=100, version="3.5", buildTarget="a", backgroundRate=100, mapping="a", update_type="z", product="a", data_version=1
        )
        self.paths.t.insert().execute(
            rule_id=4, alias="gandalf", priority=80, buildTarget="d", backgroundRate=100, mapping="a", update_type="z", channel="a", data_version=1
        )
        self.paths.t.insert().execute(rule_id=5, priority=80, buildTarget="d", version="3.3", backgroundRate=0, mapping="c", update_type="z", data_version=1)
        self.paths.t.insert().execute(
            rule_id=6,
            alias="radagast",
            priority=100,
            buildTarget="d",
            mapping="a",
            backgroundRate=100,
            osVersion="foo 1",
            update_type="z",
            product="a",
            channel="a",
            data_version=1,
        )
        self.paths.t.insert().execute(
            rule_id=7,
            priority=100,
            buildTarget="d",
            mapping="a",
            backgroundRate=100,
            osVersion="foo 2,blah 6,bar && baz",
            update_type="z",
            product="a",
            channel="a",
            data_version=1,
        )
        self.paths.t.insert().execute(
            rule_id=8,
            priority=100,
            buildTarget="e",
            mapping="d",
            backgroundRate=100,
            locale="foo,bar-baz",
            update_type="z",
            product="a",
            channel="a",
            data_version=1,
        )
        self.paths.t.insert().execute(
            rule_id=9,
            priority=100,
            buildTarget="f",
            mapping="f",
            backgroundRate=100,
            instructionSet="S",
            update_type="z",
            product="foo",
            channel="foo*",
            data_version=1,
        )
        self.paths.t.insert().execute(
            rule_id=10,
            priority=100,
            buildTarget="g",
            mapping="g",
            fallbackMapping="fallback",
            backgroundRate=100,
            update_type="z",
            product="foo",
            channel="foo",
            data_version=1,
        )

        self.db.permissions.t.insert().execute(permission="admin", username="bill", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="bill", role="bar", data_version=1)
        self.db.permissions.user_roles.t.insert().execute(username="jane", role="bar", data_version=1)
        self.db.productRequiredSignoffs.t.insert().execute(product="foo", channel="foo", role="bar", signoffs_required=2, data_version=1)

    def testAllTablesCreated(self):
        self.assertTrue(self.db.rules)
        self.assertTrue(self.db.rules.history)
        self.assertTrue(self.db.rules.scheduled_changes)
        self.assertTrue(self.db.rules.scheduled_changes.history)
        self.assertTrue(self.db.rules.scheduled_changes.conditions)
        self.assertTrue(self.db.rules.scheduled_changes.conditions.history)

    def testAllColumnsExist(self):
        columns = [c.name for c in self.db.rules.t.columns]
        expected = [
            "rule_id",
            "alias",
            "priority",
            "mapping",
            "fallbackMapping",
            "backgroundRate",
            "update_type",
            "product",
            "version",
            "channel",
            "buildTarget",
            "buildID",
            "locale",
            "osVersion",
            "instructionSet",
            "distribution",
            "distVersion",
            "headerArchitecture",
            "comment",
            "data_version",
            "memory",
            "mig64",
            "jaws",
        ]
        sc_expected = ["base_{}".format(c) for c in expected]
        self.assertEqual(set(columns), set(expected))
        # No need to test the non-base parts of history nor scheduled changes table
        # because tests for those table types verify them.
        history_columns = [c.name for c in self.db.rules.history.t.columns]
        self.assertTrue(set(expected).issubset(set(history_columns)))

        sc_columns = [c.name for c in self.db.rules.scheduled_changes.t.columns]
        self.assertTrue(set(sc_expected).issubset(set(sc_columns)))

        sc_history_columns = [c.name for c in self.db.rules.scheduled_changes.history.t.columns]
        self.assertTrue(set(sc_expected).issubset(set(sc_history_columns)))

    def testGetOrderedRules(self):
        rules = self._stripNullColumns(self.paths.getOrderedRules())
        expected = [
            dict(alias="gandalf", backgroundRate=100, buildTarget="d", channel="a", data_version=1, mapping="a", priority=80, rule_id=4, update_type="z"),
            dict(backgroundRate=0, buildTarget="d", data_version=1, mapping="c", priority=80, rule_id=5, update_type="z", version="3.3"),
            dict(
                alias="radagast",
                backgroundRate=100,
                buildTarget="d",
                channel="a",
                data_version=1,
                mapping="a",
                osVersion="foo 1",
                priority=100,
                product="a",
                rule_id=6,
                update_type="z",
            ),
            dict(
                backgroundRate=100,
                buildTarget="d",
                channel="a",
                data_version=1,
                mapping="a",
                osVersion="foo 2,blah 6,bar && baz",
                priority=100,
                product="a",
                rule_id=7,
                update_type="z",
            ),
            dict(
                backgroundRate=100,
                buildTarget="e",
                channel="a",
                data_version=1,
                locale="foo,bar-baz",
                mapping="d",
                priority=100,
                product="a",
                rule_id=8,
                update_type="z",
            ),
            dict(
                backgroundRate=100,
                buildTarget="f",
                channel="foo*",
                data_version=1,
                mapping="f",
                priority=100,
                product="foo",
                rule_id=9,
                instructionSet="S",
                update_type="z",
            ),
            dict(
                backgroundRate=100,
                buildTarget="g",
                channel="foo",
                data_version=1,
                fallbackMapping="fallback",
                mapping="g",
                priority=100,
                product="foo",
                rule_id=10,
                update_type="z",
            ),
            dict(
                backgroundRate=100,
                buildTarget="d",
                channel="a",
                data_version=1,
                mapping="b",
                priority=100,
                product="a",
                rule_id=2,
                update_type="z",
                version="3.3",
            ),
            dict(backgroundRate=100, buildTarget="a", data_version=1, mapping="a", priority=100, product="a", rule_id=3, update_type="z", version="3.5"),
            dict(
                backgroundRate=100,
                buildTarget="d",
                channel="a",
                data_version=1,
                mapping="c",
                priority=100,
                product="a",
                rule_id=1,
                update_type="z",
                version="3.5",
            ),
        ]

        self.assertEqual(rules, expected)

    def testGetOrderedRulesWithCondition(self):
        rules = self._stripNullColumns(self.paths.getOrderedRules(where=[self.paths.buildTarget == "d"]))
        expected = [
            dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget="d", mapping="a", update_type="z", channel="a", data_version=1),
            dict(rule_id=5, priority=80, backgroundRate=0, version="3.3", buildTarget="d", mapping="c", update_type="z", data_version=1),
            dict(
                rule_id=6,
                alias="radagast",
                priority=100,
                buildTarget="d",
                mapping="a",
                backgroundRate=100,
                osVersion="foo 1",
                update_type="z",
                product="a",
                channel="a",
                data_version=1,
            ),
            dict(
                rule_id=7,
                priority=100,
                buildTarget="d",
                mapping="a",
                backgroundRate=100,
                osVersion="foo 2,blah 6,bar && baz",
                update_type="z",
                product="a",
                channel="a",
                data_version=1,
            ),
            dict(
                rule_id=2,
                priority=100,
                backgroundRate=100,
                version="3.3",
                buildTarget="d",
                mapping="b",
                update_type="z",
                product="a",
                channel="a",
                data_version=1,
            ),
            dict(
                rule_id=1,
                priority=100,
                backgroundRate=100,
                version="3.5",
                buildTarget="d",
                mapping="c",
                update_type="z",
                product="a",
                channel="a",
                data_version=1,
            ),
        ]
        self.assertEqual(rules, expected)

    def testGetRulesMatchingQuery(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(
                product="a",
                version="3.5",
                channel="a",
                buildTarget="a",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(rule_id=3, priority=100, backgroundRate=100, version="3.5", buildTarget="a", mapping="a", update_type="z", product="a", data_version=1)
        ]
        self.assertEqual(rules, expected)

    def testGetRulesMatchingQueryWithNullColumn(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(
                product="a",
                version="3.5",
                channel="a",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(
                rule_id=1,
                priority=100,
                backgroundRate=100,
                version="3.5",
                buildTarget="d",
                mapping="c",
                update_type="z",
                product="a",
                channel="a",
                data_version=1,
            ),
            dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget="d", mapping="a", update_type="z", channel="a", data_version=1),
        ]
        self.assertEqual(rules, expected)

    def testGetRulesMatchingQueryReturnBackgroundThrottledEvenIfNotForced(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(
                product="a",
                version="3.3",
                channel="a",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(
                rule_id=2,
                priority=100,
                backgroundRate=100,
                version="3.3",
                buildTarget="d",
                mapping="b",
                update_type="z",
                product="a",
                channel="a",
                data_version=1,
            ),
            dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget="d", mapping="a", update_type="z", channel="a", data_version=1),
            dict(rule_id=5, priority=80, backgroundRate=0, version="3.3", buildTarget="d", mapping="c", update_type="z", data_version=1),
        ]
        self.assertEqual(rules, expected)

    def testGetRulesMatchingQueryReturnBackgroundThrottled(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(
                product="a",
                version="3.3",
                channel="a",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=True,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(
                rule_id=2,
                priority=100,
                backgroundRate=100,
                version="3.3",
                buildTarget="d",
                mapping="b",
                update_type="z",
                product="a",
                channel="a",
                data_version=1,
            ),
            dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget="d", mapping="a", update_type="z", channel="a", data_version=1),
            dict(rule_id=5, priority=80, backgroundRate=0, version="3.3", buildTarget="d", mapping="c", update_type="z", data_version=1),
        ]
        self.assertEqual(rules, expected)

    def testGetRulesMatchingQueryOsVersionSubstring(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(
                product="a",
                version="5.0",
                channel="a",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="foo 1.2.3",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget="d", mapping="a", update_type="z", channel="a", data_version=1),
            dict(
                rule_id=6,
                alias="radagast",
                priority=100,
                buildTarget="d",
                mapping="a",
                backgroundRate=100,
                osVersion="foo 1",
                update_type="z",
                product="a",
                channel="a",
                data_version=1,
            ),
        ]
        self.assertEqual(rules, expected)

    def testGetRulesMatchingQueryOsVersionSubstringNotAtStart(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(
                product="a",
                version="5.0",
                channel="a",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="bbb,foo 1.2.3",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget="d", mapping="a", update_type="z", channel="a", data_version=1),
            dict(
                rule_id=6,
                alias="radagast",
                priority=100,
                buildTarget="d",
                mapping="a",
                backgroundRate=100,
                osVersion="foo 1",
                update_type="z",
                product="a",
                channel="a",
                data_version=1,
            ),
        ]
        self.assertEqual(rules, expected)

    def testGetRulesMatchingQueryOsVersionMultipleSubstring(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(
                product="a",
                version="5.0",
                channel="a",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="blah 6.3.2",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget="d", mapping="a", update_type="z", channel="a", data_version=1),
            dict(
                rule_id=7,
                priority=100,
                buildTarget="d",
                mapping="a",
                backgroundRate=100,
                osVersion="foo 2,blah 6,bar && baz",
                update_type="z",
                product="a",
                channel="a",
                data_version=1,
            ),
        ]
        self.assertEqual(rules, expected)

    def testGetRulesMatchingQueryOsVersionAndMatching(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(
                product="a",
                version="5.0",
                channel="a",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="bar 1.3 baz 2.3",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget="d", mapping="a", update_type="z", channel="a", data_version=1),
            dict(
                rule_id=7,
                priority=100,
                buildTarget="d",
                mapping="a",
                backgroundRate=100,
                osVersion="foo 2,blah 6,bar && baz",
                update_type="z",
                product="a",
                channel="a",
                data_version=1,
            ),
        ]
        self.assertEqual(rules, expected)

    def testGetRulesMatchingQueryInstructionSet(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(
                product="foo",
                version="5.0",
                channel="foo",
                buildTarget="f",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=6,
                instructionSet="S",
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(
                rule_id=9,
                priority=100,
                buildTarget="f",
                mapping="f",
                backgroundRate=100,
                instructionSet="S",
                update_type="z",
                product="foo",
                channel="foo*",
                data_version=1,
            )
        ]
        self.assertEqual(rules, expected)

    def testGetRulesMatchingQueryInstructionSetNoSubstringMatch(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(
                product="a",
                version="5.0",
                channel="a",
                buildTarget="f",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=6,
                instructionSet="SA",
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        self.assertEqual(rules, [])

    def testGetRulesMatchingQueryFallbackMapping(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(
                product="foo",
                version="5.0",
                channel="foo",
                buildTarget="g",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=6,
                fallbackMapping="fallback",
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(
                rule_id=10,
                priority=100,
                buildTarget="g",
                mapping="g",
                fallbackMapping="fallback",
                backgroundRate=100,
                update_type="z",
                product="foo",
                channel="foo",
                data_version=1,
            )
        ]
        self.assertEqual(rules, expected)

    def testGetRulesMatchingQueryLocale(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(
                product="a",
                version="",
                channel="a",
                buildTarget="e",
                buildID="",
                locale="foo",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [
            dict(
                rule_id=8,
                priority=100,
                buildTarget="e",
                mapping="d",
                backgroundRate=100,
                locale="foo,bar-baz",
                update_type="z",
                product="a",
                channel="a",
                data_version=1,
            )
        ]
        self.assertEqual(rules, expected)

    def testGetRulesMatchingQueryLocaleNoPartialMatch(self):
        rules = self.paths.getRulesMatchingQuery(
            dict(
                product="a",
                version="5",
                channel="a",
                buildTarget="e",
                buildID="",
                locale="bar",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = []
        self.assertEqual(rules, expected)

    def testGetRuleById(self):
        rule = self._stripNullColumns([self.paths.getRule(1)])
        expected = [
            dict(
                rule_id=1,
                priority=100,
                backgroundRate=100,
                version="3.5",
                buildTarget="d",
                mapping="c",
                update_type="z",
                product="a",
                channel="a",
                data_version=1,
            )
        ]
        self.assertEqual(rule, expected)

    def testGetRuleByAlias(self):
        rule = self._stripNullColumns([self.paths.getRule(4)])
        expected = [
            dict(rule_id=4, alias="gandalf", priority=80, backgroundRate=100, buildTarget="d", mapping="a", update_type="z", channel="a", data_version=1)
        ]
        self.assertEqual(rule, expected)

    def testAddRule(self):
        what = dict(backgroundRate=11, mapping="c", update_type="z", priority=60, product="a", channel="a")
        rule_id = self.paths.insert(changed_by="bill", **what)
        rules = self.paths.t.select().where(self.paths.rule_id == rule_id).execute().fetchall()
        copy_rule = dict(rules[0].items())
        rule = self._stripNullColumns([copy_rule])
        what["rule_id"] = rule_id
        what["data_version"] = 1
        what = [what]
        self.assertEqual(rule, what)

    def testAddRuleThatRequiresSignoff(self):
        what = dict(backgroundRate=11, mapping="c", update_type="z", priority=60, product="foo", channel="foo")
        self.assertRaises(SignoffRequiredError, self.paths.insert, changed_by="bill", **what)

    def testAddRuleThatRequiresSignoffWithNull(self):
        what = dict(backgroundRate=11, mapping="c", update_type="z", priority=60)
        self.assertRaises(SignoffRequiredError, self.paths.insert, changed_by="bill", **what)

    def testAddRulesThatRequiresSignoffWithChannelGlob(self):
        what = dict(backgroundRate=11, mapping="c", update_type="z", priority=60, product="foo", channel="foo*")
        self.assertRaises(SignoffRequiredError, self.paths.insert, changed_by="bill", **what)

    def testUpdateRule(self):
        rules = self.paths.t.select().where(self.paths.rule_id == 1).execute().fetchall()
        what = dict(rules[0].items())

        what["mapping"] = "d"
        self.paths.update(where={"rule_id": 1}, what=what, changed_by="bill", old_data_version=1)

        rules = self.paths.t.select().where(self.paths.rule_id == 1).execute().fetchall()
        copy_rule = dict(rules[0].items())
        rule = self._stripNullColumns([copy_rule])

        expected = [
            dict(
                rule_id=1,
                priority=100,
                backgroundRate=100,
                version="3.5",
                buildTarget="d",
                mapping="d",
                update_type="z",
                product="a",
                channel="a",
                data_version=2,
            )
        ]
        self.assertEqual(rule, expected)

    def testUpdateRuleByAlias(self):
        rules = self.paths.t.select().where(self.paths.rule_id == 6).execute().fetchall()
        what = dict(rules[0].items())

        what["mapping"] = "d"
        self.paths.update(where={"rule_id": "radagast"}, what=what, changed_by="bill", old_data_version=1)

        rules = self.paths.t.select().where(self.paths.rule_id == 6).execute().fetchall()
        copy_rule = dict(rules[0].items())
        rule = self._stripNullColumns([copy_rule])

        expected = [
            dict(
                rule_id=6,
                alias="radagast",
                priority=100,
                backgroundRate=100,
                buildTarget="d",
                mapping="d",
                update_type="z",
                osVersion="foo 1",
                product="a",
                channel="a",
                data_version=2,
            )
        ]
        self.assertEqual(rule, expected)

    def testUpdateRuleThatRequiresSignoff(self):
        self.assertRaises(SignoffRequiredError, self.paths.update, where={"rule_id": 10}, what={"mapping": "g"}, changed_by="bill", old_data_version=1)

    def testUpdateRuleThatRequiresSignoffWithChannelGlob(self):
        self.assertRaises(SignoffRequiredError, self.paths.update, where={"rule_id": 9}, what={"mapping": "g"}, changed_by="bill", old_data_version=1)

    def testDeleteRule(self):
        self.paths.delete({"rule_id": 2}, changed_by="bill", old_data_version=1)
        rule = self.paths.t.select().where(self.paths.rule_id == 2).execute().fetchall()
        self.assertEqual(rule, [])

    def testDeleteRuleByAlias(self):
        self.paths.delete({"rule_id": "gandalf"}, changed_by="bill", old_data_version=1)
        rule = self.paths.t.select().where(self.paths.rule_id == 4).execute().fetchall()
        self.assertEqual(rule, [])

    def testDeleteRuleThatRequiresSignoff(self):
        self.assertRaises(SignoffRequiredError, self.paths.delete, {"rule_id": 10}, changed_by="bill", old_data_version=1)

    def testDeleteRuleThatRequiresSignoffWithChannelGlob(self):
        self.assertRaises(SignoffRequiredError, self.paths.delete, {"rule_id": 9}, changed_by="bill", old_data_version=1)

    def testGetNumberOfRules(self):
        self.assertEqual(self.paths.count(), 10)


@pytest.mark.usefixtures("current_db_schema")
class TestJawsRules(unittest.TestCase, RulesTestMixin, MemoryDatabaseMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.metadata.create_all(self.db.engine)
        self.rules = self.db.rules
        self.rules.t.insert().execute(
            rule_id=1, priority=90, mapping="myes", backgroundRate=100, jaws=True, update_type="z", product="mm", channel="mm", data_version=1
        )
        self.rules.t.insert().execute(
            rule_id=2, priority=100, mapping="mno", backgroundRate=100, jaws=False, update_type="z", product="nn", channel="nn", data_version=1
        )

        self.rules.t.insert().execute(
            rule_id=3, priority=110, mapping="anything", backgroundRate=100, update_type="z", product="oo", channel="oo", data_version=1
        )

    def testRuleFalseQueryFalse(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="nn",
                version="53.0",
                channel="nn",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                jaws=False,
                force=False,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [dict(rule_id=2, priority=100, mapping="mno", backgroundRate=100, jaws=False, update_type="z", product="nn", channel="nn", data_version=1)]
        self.assertEqual(rules, expected)

    def testRuleFalseQueryTrue(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="nn",
                version="53.0",
                channel="nn",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                jaws=True,
                force=False,
            ),
            fallbackChannel="",
        )
        self.assertEqual(rules, [])

    def testRuleFalseQueryNull(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="nn",
                version="53.0",
                channel="nn",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                jaws=None,
                force=False,
            ),
            fallbackChannel="",
        )
        self.assertEqual(rules, [])

    def testRuleTrueQueryFalse(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="mm",
                version="53.0",
                channel="mm",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                jaws=False,
                force=False,
            ),
            fallbackChannel="",
        )
        self.assertEqual(rules, [])

    def testRuleTrueQueryTrue(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="mm",
                version="53.0",
                channel="mm",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                jaws=True,
                force=False,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [dict(rule_id=1, priority=90, mapping="myes", backgroundRate=100, jaws=True, update_type="z", product="mm", channel="mm", data_version=1)]
        self.assertEqual(rules, expected)

    def testRuleTrueQueryNull(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="mm",
                version="53.0",
                channel="mm",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                jaws=None,
                force=False,
            ),
            fallbackChannel="",
        )
        self.assertEqual(rules, [])

    def testRuleNullQueryFalse(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="oo",
                version="53.0",
                channel="oo",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                jaws=False,
                force=False,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [dict(rule_id=3, priority=110, mapping="anything", backgroundRate=100, update_type="z", product="oo", channel="oo", data_version=1)]
        self.assertEqual(rules, expected)

    def testRuleNullQueryTrue(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="oo",
                version="53.0",
                channel="oo",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                jaws=True,
                force=False,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [dict(rule_id=3, priority=110, mapping="anything", backgroundRate=100, update_type="z", product="oo", channel="oo", data_version=1)]
        self.assertEqual(rules, expected)

    def testRuleNullQueryNull(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="oo",
                version="53.0",
                channel="oo",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                jaws=None,
                force=False,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [dict(rule_id=3, priority=110, mapping="anything", backgroundRate=100, update_type="z", product="oo", channel="oo", data_version=1)]
        self.assertEqual(rules, expected)


@pytest.mark.usefixtures("current_db_schema")
class TestMig64Rules(unittest.TestCase, RulesTestMixin, MemoryDatabaseMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.metadata.create_all(self.db.engine)
        self.rules = self.db.rules
        self.rules.t.insert().execute(
            rule_id=1, priority=90, mapping="myes", backgroundRate=100, mig64=True, update_type="z", product="mm", channel="mm", data_version=1
        )
        self.rules.t.insert().execute(
            rule_id=2, priority=100, mapping="mno", backgroundRate=100, mig64=False, update_type="z", product="nn", channel="nn", data_version=1
        )

        self.rules.t.insert().execute(
            rule_id=3, priority=110, mapping="anything", backgroundRate=100, update_type="z", product="oo", channel="oo", data_version=1
        )

    def testRuleFalseQueryFalse(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="nn",
                version="53.0",
                channel="nn",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                mig64=False,
                force=False,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [dict(rule_id=2, priority=100, mapping="mno", backgroundRate=100, mig64=False, update_type="z", product="nn", channel="nn", data_version=1)]
        self.assertEqual(rules, expected)

    def testRuleFalseQueryTrue(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="nn",
                version="53.0",
                channel="nn",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                mig64=True,
                force=False,
            ),
            fallbackChannel="",
        )
        self.assertEqual(rules, [])

    def testRuleFalseQueryNull(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="nn",
                version="53.0",
                channel="nn",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                mig64=None,
                force=False,
            ),
            fallbackChannel="",
        )
        self.assertEqual(rules, [])

    def testRuleTrueQueryFalse(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="mm",
                version="53.0",
                channel="mm",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                mig64=False,
                force=False,
            ),
            fallbackChannel="",
        )
        self.assertEqual(rules, [])

    def testRuleTrueQueryTrue(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="mm",
                version="53.0",
                channel="mm",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                mig64=True,
                force=False,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [dict(rule_id=1, priority=90, mapping="myes", backgroundRate=100, mig64=True, update_type="z", product="mm", channel="mm", data_version=1)]
        self.assertEqual(rules, expected)

    def testRuleTrueQueryNull(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="mm",
                version="53.0",
                channel="mm",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                mig64=None,
                force=False,
            ),
            fallbackChannel="",
        )
        self.assertEqual(rules, [])

    def testRuleNullQueryFalse(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="oo",
                version="53.0",
                channel="oo",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                mig64=False,
                force=False,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [dict(rule_id=3, priority=110, mapping="anything", backgroundRate=100, update_type="z", product="oo", channel="oo", data_version=1)]
        self.assertEqual(rules, expected)

    def testRuleNullQueryTrue(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="oo",
                version="53.0",
                channel="oo",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                mig64=True,
                force=False,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [dict(rule_id=3, priority=110, mapping="anything", backgroundRate=100, update_type="z", product="oo", channel="oo", data_version=1)]
        self.assertEqual(rules, expected)

    def testRuleNullQueryNull(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                product="oo",
                version="53.0",
                channel="oo",
                buildTarget="d",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                queryVersion=3,
                mig64=None,
                force=False,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        expected = [dict(rule_id=3, priority=110, mapping="anything", backgroundRate=100, update_type="z", product="oo", channel="oo", data_version=1)]
        self.assertEqual(rules, expected)


@pytest.mark.usefixtures("current_db_schema")
class TestRulesSpecial(unittest.TestCase, RulesTestMixin, MemoryDatabaseMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.metadata.create_all(self.db.engine)
        self.rules = self.db.rules
        self.rules.t.insert().execute(rule_id=1, priority=100, version=">=4.0b1", backgroundRate=100, update_type="z", data_version=1)
        self.rules.t.insert().execute(rule_id=2, priority=100, channel="release*", backgroundRate=100, update_type="z", data_version=1)
        self.rules.t.insert().execute(rule_id=3, priority=100, buildID=">=20010101222222", backgroundRate=100, update_type="z", data_version=1)
        self.rules.t.insert().execute(rule_id=4, priority=90, version="3.0.1,3.0.2,3.0b3", backgroundRate=100, update_type="z", data_version=1)
        self.rules.t.insert().execute(rule_id=5, priority=80, version="2.0.1,2.0.2,2.0.3", backgroundRate=100, update_type="z", data_version=1)
        self.rules.t.insert().execute(rule_id=6, priority=70, channel="abc", memory="<=2000", backgroundRate=100, update_type="z", data_version=1)

    def testGetRulesMatchingQueryVersionComparison(self):
        expected = [dict(rule_id=1, priority=100, backgroundRate=100, version=">=4.0b1", update_type="z", data_version=1)]
        rules = self.rules.getRulesMatchingQuery(
            dict(
                name="",
                product="",
                version="4.0",
                channel="",
                buildTarget="",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        self.assertEqual(rules, expected)

        rules = self.rules.getRulesMatchingQuery(
            dict(
                name="",
                product="",
                version="4.0b2",
                channel="",
                buildTarget="",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        self.assertEqual(rules, expected)

        rules = self.rules.getRulesMatchingQuery(
            dict(
                name="",
                product="",
                version="4.0.1",
                channel="",
                buildTarget="",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        self.assertEqual(rules, expected)

        rules = self.rules.getRulesMatchingQuery(
            dict(
                name="",
                product="",
                version="3.0",
                channel="",
                buildTarget="",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        self.assertEqual(rules, [])

    def testGetRulesMatchingQueryListOfVersionsComparison(self):
        expected = [dict(rule_id=4, priority=90, backgroundRate=100, version="3.0.1,3.0.2,3.0b3", update_type="z", data_version=1)]
        for version_no in ["3.0.1", "3.0.2", "3.0b3"]:
            rules = self.rules.getRulesMatchingQuery(
                dict(
                    name="",
                    product="",
                    version=version_no,
                    channel="",
                    buildTarget="",
                    buildID="",
                    locale="",
                    osVersion="",
                    distribution="",
                    distVersion="",
                    headerArchitecture="",
                    force=False,
                    queryVersion=3,
                ),
                fallbackChannel="",
            )
            rules = self._stripNullColumns(rules)
            self.assertEqual(rules, expected)

    def testGetRulesMatchingQueryIfVersionNotPresentInListOfVersions(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                name="",
                product="",
                version="3.0.3",
                channel="",
                buildTarget="",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        self.assertEqual(rules, [])

    def testGetRulesMatchingQueryPartialVersionDoesNotMatchLongerVersion(self):
        # 2.0 does not match any version in [ 2.0.1, 2.0.2, 2.0.3] for rule_id: 5
        rules = self.rules.getRulesMatchingQuery(
            dict(
                name="",
                product="",
                version="2.0",
                channel="",
                buildTarget="",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        self.assertEqual(rules, [])

    def testGetRulesMatchingQueryChannelGlobbing(self):
        expected = [dict(rule_id=2, priority=100, backgroundRate=100, channel="release*", update_type="z", data_version=1)]
        rules = self.rules.getRulesMatchingQuery(
            dict(
                name="",
                product="",
                version="3.0",
                channel="releasetest",
                buildTarget="",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="releasetest",
        )
        rules = self._stripNullColumns(rules)
        self.assertEqual(rules, expected)

        rules = self.rules.getRulesMatchingQuery(
            dict(
                name="",
                product="",
                version="3.0",
                channel="releasetest-cck-blah",
                buildTarget="",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="releasetest",
        )
        rules = self._stripNullColumns(rules)
        self.assertEqual(rules, expected)

    def testGetRulesMatchingBuildIDComparison(self):
        expected = [dict(rule_id=3, priority=100, backgroundRate=100, buildID=">=20010101222222", update_type="z", data_version=1)]
        rules = self.rules.getRulesMatchingQuery(
            dict(
                name="",
                product="",
                version="3.0",
                channel="",
                buildTarget="",
                buildID="20010101222222",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        self.assertEqual(rules, expected)

        rules = self.rules.getRulesMatchingQuery(
            dict(
                name="",
                product="",
                version="3.0",
                channel="",
                buildTarget="",
                buildID="20010101232323",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        self.assertEqual(rules, expected)

        rules = self.rules.getRulesMatchingQuery(
            dict(
                name="",
                product="",
                version="3.0",
                channel="",
                buildTarget="",
                buildID="20010101212121",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        self.assertEqual(rules, [])

    def testGetRulesMatchingMemoryLessThanEqualTo(self):
        expected = [dict(rule_id=6, priority=70, channel="abc", memory="<=2000", backgroundRate=100, update_type="z", data_version=1)]
        rules = self.rules.getRulesMatchingQuery(
            dict(
                name="",
                product="",
                version="3.0",
                channel="abc",
                memory=1500,
                buildTarget="",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=6,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        self.assertEqual(rules, expected)

    def testGetRulesMatchingMemoryExactMatch(self):
        expected = [dict(rule_id=6, priority=70, channel="abc", memory="<=2000", backgroundRate=100, update_type="z", data_version=1)]
        rules = self.rules.getRulesMatchingQuery(
            dict(
                name="",
                product="",
                version="3.0",
                channel="abc",
                memory=2000,
                buildTarget="",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=6,
            ),
            fallbackChannel="",
        )
        rules = self._stripNullColumns(rules)
        self.assertEqual(rules, expected)

    def testGetRulesMatchingMemoryNoMatch(self):
        rules = self.rules.getRulesMatchingQuery(
            dict(
                name="",
                product="",
                version="3.0",
                channel="abc",
                memory=2500,
                buildTarget="",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=6,
            ),
            fallbackChannel="",
        )
        self.assertEqual(rules, [])


@pytest.mark.usefixtures("current_db_schema")
class TestReleases(unittest.TestCase, MemoryDatabaseMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        dbo.setDb(self.dburi, releases_history_buckets={"*": "fake"}, releases_history_class=FakeGCSHistory)
        self.metadata.create_all(dbo.engine)
        self.rules = dbo.rules
        self.releases = dbo.releases
        self.permissions = dbo.permissions
        self.rules.t.insert().execute(rule_id=1, product="b", channel="h", mapping="h", backgroundRate=100, priority=100, update_type="minor", data_version=1)
        self.rules.t.insert().execute(
            rule_id=2, product="b", channel="h", mapping="c", fallbackMapping="h", backgroundRate=100, priority=100, update_type="minor", data_version=1
        )
        self.rules.t.insert().execute(rule_id=5, priority=100, channel="r*", backgroundRate=100, update_type="z", data_version=1)
        self.rules.t.insert().execute(rule_id=6, priority=100, channel="r*test*", backgroundRate=100, update_type="z", data_version=1)
        self.releases.t.insert().execute(name="a", product="a", data=createBlob(dict(name="a", schema_version=1, hashFunction="sha512")), data_version=1)
        self.releases.t.insert().execute(name="ab", product="a", data=createBlob(dict(name="ab", schema_version=1, hashFunction="sha512")), data_version=1)
        self.releases.t.insert().execute(name="b", product="b", data=createBlob(dict(name="b", schema_version=1, hashFunction="sha512")), data_version=1)
        self.releases.t.insert().execute(name="c", product="c", data=createBlob(dict(name="c", schema_version=1, hashFunction="sha512")), data_version=1)
        self.releases.t.insert().execute(name="h", product="b", data=createBlob(dict(name="h", schema_version=1, hashFunction="sha512")), data_version=1)
        self.permissions.t.insert().execute(permission="admin", username="bill", data_version=1)
        self.permissions.t.insert().execute(permission="admin", username="me", data_version=1)
        self.permissions.t.insert().execute(permission="release", username="bob", options=dict(products=["c"]), data_version=1)
        self.permissions.user_roles.t.insert().execute(username="bill", role="bar", data_version=1)
        self.permissions.user_roles.t.insert().execute(username="me", role="bar", data_version=1)
        dbo.productRequiredSignoffs.t.insert().execute(product="b", channel="h", role="bar", signoffs_required=2, data_version=1)
        dbo.productRequiredSignoffs.t.insert().execute(product="Z", channel="a", role="foo", signoffs_required=1, data_version=1)
        dbo.productRequiredSignoffs.t.insert().execute(product="Z", channel="b", role="bar", signoffs_required=2, data_version=1)
        dbo.productRequiredSignoffs.t.insert().execute(product="Z", channel="b", role="foo", signoffs_required=2, data_version=1)
        dbo.productRequiredSignoffs.t.insert().execute(product="Z", channel="c", role="baz", signoffs_required=1, data_version=1)
        dbo.productRequiredSignoffs.t.insert().execute(product="Z", channel="d", role="bar", signoffs_required=4, data_version=1)

    def tearDown(self):
        dbo.reset()

    def _stripNullColumns(self, rules):
        # We know a bunch of columns are going to be empty...easier to strip them out
        # than to be super verbose (also should let this test continue to work even
        # if the schema changes).
        for rule in rules:
            for key in rule.copy().keys():
                if rule[key] is None:
                    del rule[key]
        return rules

    def testAllTablesCreated(self):
        self.assertTrue(dbo.releases)
        self.assertTrue(dbo.releases.scheduled_changes)
        self.assertTrue(dbo.releases.scheduled_changes.history)
        self.assertTrue(dbo.releases.scheduled_changes.conditions)
        self.assertTrue(dbo.releases.scheduled_changes.conditions.history)

    def testGetReleases(self):
        self.assertEqual(len(self.releases.getReleases()), 5)

    def testGetReleasesWithLimit(self):
        self.assertEqual(len(self.releases.getReleases(limit=1)), 1)

    def testGetReleasesWithWhere(self):
        expected = [dict(product="b", name="b", data=createBlob(dict(name="b", schema_version=1, hashFunction="sha512")), data_version=1)]
        self.assertEqual(self.releases.getReleases(name="b"), expected)

    def testGetReleaseBlob(self):
        expected = createBlob(dict(name="c", schema_version=1, hashFunction="sha512"))
        self.assertEqual(self.releases.getReleaseBlob(name="c"), expected)

    def testGetReleaseBlobNonExistentRelease(self):
        self.assertRaises(KeyError, self.releases.getReleaseBlob, name="z")

    def testGetReleaseInfoAll(self):
        releases = self.releases.getReleaseInfo()
        expected = [
            dict(name="a", product="a", data_version=1, read_only=False, rule_ids=[], rule_info={}),
            dict(name="ab", product="a", data_version=1, read_only=False, rule_ids=[], rule_info={}),
            dict(name="b", product="b", data_version=1, read_only=False, rule_ids=[], rule_info={}),
            dict(name="c", product="c", data_version=1, read_only=False, rule_ids=[2], rule_info={"2": {"product": "b", "channel": "h"}}),
            dict(
                name="h",
                product="b",
                data_version=1,
                read_only=False,
                rule_ids=[1, 2],
                rule_info={"1": {"product": "b", "channel": "h"}, "2": {"product": "b", "channel": "h"}},
            ),
        ]
        self.assertEqual(releases, expected)

    def testGetReleaseInfoProduct(self):
        releases = self.releases.getReleaseInfo(product="a")
        expected = [
            dict(name="a", product="a", data_version=1, read_only=False, rule_ids=[], rule_info={}),
            dict(name="ab", product="a", data_version=1, read_only=False, rule_ids=[], rule_info={}),
        ]
        self.assertEqual(releases, expected)

    def testGetReleaseInfoWithFallbackMapping(self):
        self.releases.t.insert().execute(name="fallback", product="e", data=createBlob(dict(name="e", schema_version=1, hashFunction="sha512")), data_version=1)
        self.rules.t.insert().execute(rule_id=4, priority=100, fallbackMapping="fallback", version="3.5", update_type="z", data_version=1)
        releases = self.releases.getReleaseInfo(product="e")
        expected = [dict(name="fallback", product="e", data_version=1, read_only=False, rule_ids=[4], rule_info={"4": {"product": None, "channel": None}})]
        self.assertEqual(releases, expected)

    def testGetReleaseInfoNoMatch(self):
        releases = self.releases.getReleaseInfo(product="ue")
        expected = []
        self.assertEqual(releases, expected)

    def testGetReleaseInfoNamePrefix(self):
        releases = self.releases.getReleaseInfo(name_prefix="a")
        expected = [
            dict(name="a", product="a", data_version=1, read_only=False, rule_ids=[], rule_info={}),
            dict(name="ab", product="a", data_version=1, read_only=False, rule_ids=[], rule_info={}),
        ]
        self.assertEqual(releases, expected)

    def testGetReleaseInfoNamePrefixNameOnly(self):
        releases = self.releases.getReleaseInfo(name_prefix="a", nameOnly=True)
        expected = [{"name": "a"}, {"name": "ab"}]
        self.assertEqual(releases, expected)

    def testPresentRuleIdField(self):
        releases = self.releases.getReleaseInfo()
        self.assertTrue("rule_ids" in releases[0])
        self.assertTrue("rule_info" in releases[0])

    def testGetReleaseNames(self):
        releases = self.releases.getReleaseNames()
        expected = [dict(name="a"), dict(name="ab"), dict(name="b"), dict(name="c"), dict(name="h")]
        self.assertEqual(releases, expected)

    def testGetReleaseNamesProduct(self):
        releases = self.releases.getReleaseNames(product="a")
        expected = [dict(name="a"), dict(name="ab")]
        self.assertEqual(releases, expected)

    def testGetReleaseNamesNoMatch(self):
        releases = self.releases.getReleaseNames(product="oo")
        expected = []
        self.assertEqual(releases, expected)

    def testGetNumberOfReleases(self):
        # because 4 releases were set up in the setUp()
        self.assertEqual(self.releases.count(), 5)

    def testDeleteRelease(self):
        self.releases.delete({"name": "a"}, changed_by="bill", old_data_version=1)
        release = self.releases.t.select().where(self.releases.name == "a").execute().fetchall()
        self.assertEqual(release, [])

    def testDeleteReleaseDontAllowMultiple(self):
        self.assertRaises(ValueError, self.releases.delete, {"product": "a"}, changed_by="bill", old_data_version=1)

    def testDeleteWithRuleMapping(self):
        self.releases.t.insert().execute(name="d", product="d", data=createBlob(dict(name="d", schema_version=1, hashFunction="sha512")), data_version=1)
        self.rules.t.insert().execute(rule_id=4, priority=100, version="3.5", buildTarget="d", backgroundRate=100, mapping="d", update_type="z", data_version=1)
        self.assertRaises(ValueError, self.releases.delete, {"name": "d"}, changed_by="me", old_data_version=1)

    def testDeleteWithRuleFallbackMapping(self):
        self.releases.t.insert().execute(name="fallback", product="e", data=createBlob(dict(name="e", schema_version=1, hashFunction="sha512")), data_version=1)
        self.rules.t.insert().execute(
            rule_id=4, priority=100, fallbackMapping="fallback", version="3.5", buildTarget="e", backgroundRate=100, update_type="z", data_version=1
        )

        self.assertRaises(ValueError, self.releases.delete, {"name": "fallback"}, changed_by="me", old_data_version=1)

    def testDeleteReleaseWhenReadOnly(self):
        self.releases.t.update(values=dict(read_only=True, data_version=2)).where(self.releases.name == "a").execute()
        self.assertRaises(ReadOnlyError, self.releases.delete, {"name": "a"}, changed_by="me", old_data_version=2)

    # Ideally we'd run these, but they end up raising a ValueError because they are mapped to,
    # so we never see a SignoffRequiredError
    #    def testDeleteReleaseWithRuleMappingThatRequiresSignoff(self):
    #        self.assertRaises(SignoffRequiredError, self.releases.delete, {"name": "h"}, changed_by="me", old_data_version=1)
    #
    #    def testDeleteReleaseWithRuleFallbackMappingAtItThatRequiresSignoff(self):
    #        self.assertRaises(SignoffRequiredError, self.releases.delete, {"name": "h"}, changed_by="me", old_data_version=1)
    #
    #    def testDeleteReleaseWithRuleWhitelistThatRequiresSignoff(self):
    #        self.assertRaises(SignoffRequiredError, self.releases.delete, {"name": "h"}, changed_by="me", old_data_version=1)

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
        self.assertEqual(select([self.releases.read_only]).where(self.releases.name == "a").execute().fetchone()[0], True)

    def testUpdateReleaseNoPermissionToSetReadOnly(self):
        self.assertRaises(PermissionDeniedError, self.releases.update, {"name": "c"}, {"read_only": True}, "bob", 1)

    def testUpdateReleaseWithRuleMappingThatRequiresSignoff(self):
        newBlob = ReleaseBlobV1(name="h", schema_version=1, hashFunction="sha256")
        self.assertRaises(SignoffRequiredError, self.releases.update, {"name": "h"}, {"data": newBlob}, "bill", 1)

    def testUpdateReleaseWithRuleFallbackMappingAtItThatRequiresSignoff(self):
        newBlob = ReleaseBlobV1(name="h", schema_version=1, hashFunction="sha256")
        self.assertRaises(SignoffRequiredError, self.releases.update, {"name": "h"}, {"data": newBlob}, "bill", 1)

    def testIsReadOnly(self):
        self.releases.t.update(values=dict(read_only=True, data_version=2)).where(self.releases.name == "a").execute()
        self.assertEqual(self.releases.isReadOnly("a"), True)

    def testProceedIfNotReadOnly(self):
        self.releases.t.update(values=dict(read_only=True, data_version=2)).where(self.releases.name == "a").execute()
        self.assertRaises(ReadOnlyError, self.releases._proceedIfNotReadOnly, "a")

    def testGetRulesMatchingQueryChannelCheckMinLengthGlobbing(self):
        # To ensure length of ruleChannel is >=3
        expected = []
        rules = self.rules.getRulesMatchingQuery(
            dict(
                name="",
                product="",
                version="3.0",
                channel="releasetest",
                buildTarget="",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="releasetest",
        )
        rules = self._stripNullColumns(rules)
        self.assertEqual(rules, expected)

    def testGetRulesMatchingQueryChannelGlobbingAtEndPass(self):
        # To ensure globbing at end only -- Pass case
        expected = [dict(rule_id=6, priority=100, backgroundRate=100, channel="r*test*", update_type="z", data_version=1)]
        rules = self.rules.getRulesMatchingQuery(
            dict(
                name="",
                product="",
                version="3.0",
                channel="r*test-cck-blah",
                buildTarget="",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="releasetest",
        )
        rules = self._stripNullColumns(rules)
        self.assertEqual(rules, expected)

    def testGetRulesMatchingQueryChannelGlobbingAtEndFail(self):
        # To ensure globbing at end only -- Fail case
        expected = []
        rules = self.rules.getRulesMatchingQuery(
            dict(
                name="",
                product="",
                version="3.0",
                channel="raaatest",
                buildTarget="",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="releasetest",
        )
        rules = self._stripNullColumns(rules)
        self.assertEqual(rules, expected)

    def testGetPotentialRequiredSignoffsForProduct(self):
        release = {"name": "Z", "product": "Z"}
        signoffs_required = self.releases.getPotentialRequiredSignoffsForProduct(release["product"])
        self.assertIn("rs", signoffs_required)
        self.assertEqual(len(signoffs_required["rs"]), 3)
        signoffs_by_role = {rs["role"]: rs["signoffs_required"] for signoffs in signoffs_required.values() for rs in signoffs}
        self.assertEqual(signoffs_by_role["foo"], 2)
        self.assertEqual(signoffs_by_role["bar"], 4)
        self.assertEqual(signoffs_by_role["baz"], 1)

    def testGetPotentialRequiredSignoffsForProductNoSignoffsRequired(self):
        release = {"name": "ZA", "product": "ZA"}
        signoffs_required = self.releases.getPotentialRequiredSignoffsForProduct(release["product"])
        self.assertIn("rs", signoffs_required)
        self.assertEqual(len(signoffs_required["rs"]), 0)


@pytest.mark.usefixtures("current_db_schema")
class TestReleasesJSON(unittest.TestCase, MemoryDatabaseMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        dbo.setDb(self.dburi, releases_history_buckets={"*": "fake"}, async_releases_history_class=FakeGCSHistoryAsync)
        self.metadata.create_all(dbo.engine)
        self.rules = dbo.rules
        self.releases = dbo.releases_json
        self.release_assets = dbo.release_assets
        dbo.permissions.t.insert().execute(permission="admin", username="bob", data_version=1)
        dbo.permissions.user_roles.t.insert().execute(username="bob", role="releng", data_version=1)
        dbo.productRequiredSignoffs.t.insert().execute(product="Firefox", channel="release", role="releng", signoffs_required=1, data_version=1)
        self.rules.t.insert().execute(
            rule_id=1,
            product="Firefox",
            channel="beta",
            mapping="Firefox-60.0-build1",
            backgroundRate=100,
            priority=100,
            update_type="minor",
            data_version=1,
        )
        self.releases.t.insert().execute(
            name="Firefox-60.0-build1",
            product="Firefox",
            data_version=1,
            data="""{
    "name": "Firefox-60.0-build1",
    "schema_version": 9,
    "hashFunction": "sha512"
}""",
        )
        self.release_assets.t.insert().execute(
            name="Firefox-60.0-build1",
            path=".platforms.Linux_x86_64-gcc3.locales.en-US",
            data_version=1,
            data="""{
    "appVersion": "60.0",
    "buildID": "20180827144429",
    "completes": [
        {
            "filesize": 42510045,
            "from": "*",
            "hashValue": "73c05d2e15a3d33cbbee3b874dbd9a3e3560ddf74b343bad5ff2d55dccd3a7cf9a5a9da5e05eefea8cabdfd186d98ada94804e83c61011f385c4f335a9a50996"
        }
    ],
    "displayVersion": "60.0",
    "partials": [
        {
            "filesize": 18695829,
            "from": "Firefox-59.0-build3",
            "hashValue": "311324ceacfb8450a948da6b2176a1103d8a4eb716381951fb197b4414097efee9a91c9fd4fbcb797dd1e80fe69b8e2410a945602d5dfd0a5c485a004c52fbda"
        }
    ]
}""",
        )

    def tearDown(self):
        dbo.reset()

    @pytest.mark.asyncio
    @mock.patch("time.time", mock.MagicMock(return_value=1.0))
    async def testInsertCreatesCorrectHistory(self):
        await self.release_assets.async_insert(
            changed_by="bob",
            name="Firefox-60.0-build1",
            path=".platforms.WINNT_x86_64-msvc.locales.en-US",
            data="""{
    "appVersion": "60.0",
    "buildID": "20180827144429",
    "completes": [
        {
            "filesize": 43038283,
            "from": "*",
            "hashValue": "264119c2e5ab41ba9dd7a527d741a132934765168aa7b5d37c2f136a6a6514af36ae3521ac792049edfe6c100c139c69d3bb907566e786f815a0d67664953151"
        }
    ],
    "displayVersion": "60.0",
    "partials": [
        {
            "filesize": 22394857,
            "from": "Firefox-59.0-build3",
            "hashValue": "92bc9de7e3db051a2bd0b789cf7bbb1790bf0c517d62131fce13b661243503f8c0dc1a92268a3e38bfb4e9a8622451f76996abb504662660852cccb0d71ef4b1"
        }
    ]
}""",
        )
        history_entries = []
        for k in self.release_assets.history.bucket.blobs:
            if k.startswith("Firefox-60.0-build1"):
                history_entries.append(k)
        expected = [
            "Firefox-60.0-build1-.platforms.WINNT_x86_64-msvc.locales.en-US/None-999-bob.json",
            "Firefox-60.0-build1-.platforms.WINNT_x86_64-msvc.locales.en-US/1-1000-bob.json",
        ]
        assert history_entries == expected

    @pytest.mark.asyncio
    @mock.patch("time.time", mock.MagicMock(return_value=1.0))
    async def testUpdateCreatesCorrectHistory(self):
        await self.release_assets.async_update(
            where={"name": "Firefox-60.0-build1", "path": ".platforms.Linux_x86_64-gcc3.locales.en-US"},
            what={
                "data": """{
    "appVersion": "60.0",
    "buildID": "20200827144429",
    "completes": [
        {
            "filesize": 99999999,
            "from": "*",
            "hashValue": "73c05d2e15a3d33cbbee3b874dbd9a3e3560ddf74b343bad5ff2d55dccd3a7cf9a5a9da5e05eefea8cabdfd186d98ada94804e83c61011999999999999999999"
        }
    ],
    "displayVersion": "60.0",
    "partials": [
        {
            "filesize": 18695829,
            "from": "Firefox-59.0-build3",
            "hashValue": "311324ceacfb8450a948da6b2176a1103d8a4eb716381951fb197b4414097efee9a91c9fd4fbcb797dd1e80fe69b8e2410a945602d5dfd0a5c485a004c52fbda"
        }
    ]
}"""
            },
            changed_by="bob",
            old_data_version=1,
        )
        history_entries = []
        for k in self.release_assets.history.bucket.blobs:
            if k.startswith("Firefox-60.0-build1"):
                history_entries.append(k)
        expected = [
            "Firefox-60.0-build1-.platforms.Linux_x86_64-gcc3.locales.en-US/2-1000-bob.json",
        ]
        assert history_entries == expected

    @pytest.mark.asyncio
    @mock.patch("time.time", mock.MagicMock(return_value=1.0))
    async def testDeleteCreatesCorrectHistory(self):
        await self.release_assets.async_delete(
            where={"name": "Firefox-60.0-build1", "path": ".platforms.Linux_x86_64-gcc3.locales.en-US"},
            changed_by="bob",
            old_data_version=1,
        )
        history_entries = []
        for k in self.release_assets.history.bucket.blobs:
            if k.startswith("Firefox-60.0-build1"):
                history_entries.append(k)
        expected = [
            "Firefox-60.0-build1-.platforms.Linux_x86_64-gcc3.locales.en-US/None-1000-bob.json",
        ]
        assert history_entries == expected


@pytest.mark.usefixtures("current_db_schema")
class TestRulesCaching(unittest.TestCase, MemoryDatabaseMixin, RulesTestMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        cache.reset()
        cache.make_copies = True
        cache.make_cache("rules", 20, 4)
        self.db = AUSDatabase(self.dburi)
        self.metadata.create_all(self.db.engine)
        self.rules = self.db.rules
        self.rules.t.insert().execute(rule_id=1, priority=100, version="3.5", buildTarget="d", backgroundRate=100, mapping="c", update_type="z", data_version=1)
        self.rules.t.insert().execute(rule_id=2, priority=100, version="3.3", buildTarget="d", backgroundRate=100, mapping="b", update_type="z", data_version=1)
        self.rules.t.insert().execute(rule_id=3, priority=100, version="3.5", buildTarget="a", backgroundRate=100, mapping="a", update_type="z", data_version=1)

    def tearDown(self):
        cache.reset()

    def _checkCacheStats(self, cache, lookups, hits, misses):
        self.assertEqual(cache.lookups, lookups)
        self.assertEqual(cache.hits, hits)
        self.assertEqual(cache.misses, misses)

    def testGetRulesMatchingQueryCacheKeysAreCorrect(self):
        """Try a few different queries to make sure cache keys are constructed correctly."""
        self.rules.getRulesMatchingQuery(
            dict(
                product="",
                version="3.5",
                channel="",
                buildTarget="a",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        self.rules.getRulesMatchingQuery(
            dict(
                product="c",
                version="3.5",
                channel="",
                buildTarget="a",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=False,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        self.rules.getRulesMatchingQuery(
            dict(
                product="b",
                version="3.5",
                channel="",
                buildTarget="e",
                buildID="",
                locale="",
                osVersion="",
                distribution="",
                distVersion="",
                headerArchitecture="",
                force=True,
                queryVersion=3,
            ),
            fallbackChannel="",
        )
        expected = set([":a:::False", "c:a:::False", "b:e:::True"])
        self.assertEqual(set(cache.caches["rules"].data.keys()), expected)

    def testGetRulesMatchingQueryUsesCachedRules(self):
        """Ensure that getRulesMatchingQuery properly uses the rules cache"""
        with mock.patch("time.time") as t:
            t.return_value = 0
            for i in range(5):
                rules = self.rules.getRulesMatchingQuery(
                    dict(
                        product="",
                        version="3.5",
                        channel="",
                        buildTarget="a",
                        buildID="",
                        locale="",
                        osVersion="",
                        distribution="",
                        distVersion="",
                        headerArchitecture="",
                        force=False,
                        queryVersion=3,
                    ),
                    fallbackChannel="",
                )
                rules = self._stripNullColumns(rules)
                expected = [dict(rule_id=3, priority=100, backgroundRate=100, version="3.5", buildTarget="a", mapping="a", update_type="z", data_version=1)]
                self.assertEqual(rules, expected)

                t.return_value += 1

            self._checkCacheStats(cache.caches["rules"], 5, 3, 2)

    def testGetRulesMatchingQueryRefreshesAfterExpiry(self):
        """Ensure that getRulesMatchingQuery picks up changes to the rules table after expiry"""
        with mock.patch("time.time") as t:
            t.return_value = 0
            for i in range(3):
                rules = self.rules.getRulesMatchingQuery(
                    dict(
                        product="",
                        version="3.5",
                        channel="",
                        buildTarget="a",
                        buildID="",
                        locale="",
                        osVersion="",
                        distribution="",
                        distVersion="",
                        headerArchitecture="",
                        force=False,
                        queryVersion=3,
                    ),
                    fallbackChannel="",
                )
                rules = self._stripNullColumns(rules)
                expected = [dict(rule_id=3, priority=100, backgroundRate=100, version="3.5", buildTarget="a", mapping="a", update_type="z", data_version=1)]
                self.assertEqual(rules, expected)

                t.return_value += 1

            self.rules.t.update(values=dict(mapping="b")).where(self.rules.rule_id == 3).execute()

            rules = self.rules.getRulesMatchingQuery(
                dict(
                    product="",
                    version="3.5",
                    channel="",
                    buildTarget="a",
                    buildID="",
                    locale="",
                    osVersion="",
                    distribution="",
                    distVersion="",
                    headerArchitecture="",
                    force=False,
                    queryVersion=3,
                ),
                fallbackChannel="",
            )
            rules = self._stripNullColumns(rules)
            expected = [dict(rule_id=3, priority=100, backgroundRate=100, version="3.5", buildTarget="a", mapping="a", update_type="z", data_version=1)]
            self.assertEqual(rules, expected)

            t.return_value += 1

            for i in range(2):
                rules = self.rules.getRulesMatchingQuery(
                    dict(
                        product="",
                        version="3.5",
                        channel="",
                        buildTarget="a",
                        buildID="",
                        locale="",
                        osVersion="",
                        distribution="",
                        distVersion="",
                        headerArchitecture="",
                        force=False,
                        queryVersion=3,
                    ),
                    fallbackChannel="",
                )
                rules = self._stripNullColumns(rules)
                expected = [dict(rule_id=3, priority=100, backgroundRate=100, version="3.5", buildTarget="a", mapping="b", update_type="z", data_version=1)]
                self.assertEqual(rules, expected)

                t.return_value += 1

            self._checkCacheStats(cache.caches["rules"], 6, 4, 2)

    def testGetRulesMatchingQueryWithFunkyQuery(self):
        """Ensure that an unsubstituted query caches properly."""
        with mock.patch("time.time") as t:
            t.return_value = 0
            for i in range(5):
                rules = self.rules.getRulesMatchingQuery(
                    dict(
                        product="%PRODUCT%",
                        version="%VERSION%",
                        channel="%CHANNEL%",
                        buildTarget="%BUILD_TARGET%",
                        buildID="%BUILDID%",
                        locale="%LOCALE%",
                        osVersion="%OS_VERSION%",
                        distribution="%DISTRIBUTION%",
                        distVersion="%DIST_VERSION%",
                        headerArchitecture="",
                        force=False,
                        queryVersion=3,
                    ),
                    fallbackChannel="",
                )
                rules = self._stripNullColumns(rules)
                self.assertEqual(rules, [])

                t.return_value += 1

            self._checkCacheStats(cache.caches["rules"], 5, 3, 2)


@pytest.mark.usefixtures("current_db_schema")
class TestBlobCaching(unittest.TestCase, MemoryDatabaseMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        dbo.setDb(self.dburi, releases_history_buckets={"*": "fake"}, releases_history_class=FakeGCSHistory)
        self.metadata.create_all(dbo.engine)
        cache.reset()
        cache.make_copies = True
        cache.make_cache("blob", 10, 10)
        cache.make_cache("blob_version", 10, 4)
        self.rules = dbo.rules
        self.releases = dbo.releases
        self.permissions = dbo.permissions
        self.releases.t.insert().execute(name="a", product="a", data=createBlob(dict(name="a", schema_version=1, hashFunction="sha512")), data_version=1)
        self.releases.t.insert().execute(name="b", product="b", data=createBlob(dict(name="b", schema_version=1, hashFunction="sha512")), data_version=1)
        self.permissions.t.insert().execute(permission="admin", username="bill", data_version=1)
        self.permissions.t.insert().execute(permission="admin", username="bob", data_version=1)
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
        self.assertEqual(cache.lookups, lookups)
        self.assertEqual(cache.hits, hits)
        self.assertEqual(cache.misses, misses)

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
            self.assertEqual(blob["appv"], "2")
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
            self.releases.insert(changed_by="bill", name="abc", product="bbb", data=ReleaseBlobV1(name="abc", schema_version=1, hashFunction="sha512"))
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

            newBlob = {"schema_version": 1, "name": "b", "hashFunction": "sha512", "platforms": {"win": {"locales": {"zu": {"buildID": 123}}}}}

            self.assertEqual(blob, newBlob)
            # The first getReleaseBlob call is a miss
            # addLocaleToRelease retrieve the blob (a hit) before updating it,
            # and updates the cache.
            # The second getReleaseBlob call will be a cache hit of the newly
            # updated contents.
            self._checkCacheStats(cache.caches["blob"], 3, 2, 1)
            self._checkCacheStats(cache.caches["blob_version"], 3, 2, 1)


@pytest.mark.usefixtures("current_db_schema")
class TestReleasesAppReleaseBlobs(unittest.TestCase, MemoryDatabaseMixin):
    """Tests for the Releases class that are interwoven with AppRelease blob schemas"""

    maxDiff = 2000

    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi, releases_history_buckets={"*": "fake"}, releases_history_class=FakeGCSHistory)
        self.metadata.create_all(self.db.engine)
        self.releases = self.db.releases
        self.releases.t.insert().execute(
            name="a",
            product="a",
            data_version=1,
            data=createBlob(
                """
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
"""
            ),
        )
        self.releases.t.insert().execute(
            name="b",
            product="b",
            data_version=1,
            data=createBlob(
                """
{
    "name": "b",
    "hashFunction": "sha512",
    "schema_version": 1
}
"""
            ),
        )
        self.db.permissions.t.insert().execute(permission="admin", username="bill", data_version=1)
        self.db.permissions.t.insert().execute(permission="admin", username="me", data_version=1)

    def testAddRelease(self):
        blob = ReleaseBlobV1(name="d", hashFunction="sha512")
        self.releases.insert(changed_by="bill", name="d", product="d", data=blob)
        expected = [("d", "d", False, createBlob(dict(name="d", schema_version=1, hashFunction="sha512")), 1)]
        self.assertEqual(self.releases.t.select().where(self.releases.name == "d").execute().fetchall(), expected)

    @emits_warning()
    def testAddReleaseAlreadyExists(self):
        blob = ReleaseBlobV1(name="a", hashFunction="sha512")
        self.assertRaises(TransactionError, self.releases.insert, changed_by="bill", name="a", product="a", data=blob)

    def testUpdateRelease(self):
        blob = ReleaseBlobV1(name="a", hashFunction="sha512")
        self.releases.update({"name": "a"}, {"product": "z", "data": blob}, "bill", 1)
        expected = [("a", "z", False, createBlob(dict(name="a", schema_version=1, hashFunction="sha512")), 2)]
        self.assertEqual(self.releases.t.select().where(self.releases.name == "a").execute().fetchall(), expected)

    def testUpdateReleaseWhenReadOnly(self):
        blob = ReleaseBlobV1(name="a", hashFunction="sha512")
        # set release 'a' to read-only
        self.releases.t.update(values=dict(read_only=True, data_version=2)).where(self.releases.name == "a").execute()
        self.assertRaises(ReadOnlyError, self.releases.update, {"name": "a"}, {"product": "z", "data": blob}, "me", 2)

    def testUpdateReleaseWithBlob(self):
        blob = ReleaseBlobV1(name="b", schema_version=1, hashFunction="sha512")
        self.releases.update({"name": "b"}, {"product": "z", "data": blob}, "bill", 1)
        expected = [("b", "z", False, createBlob(dict(name="b", schema_version=1, hashFunction="sha512")), 2)]
        self.assertEqual(self.releases.t.select().where(self.releases.name == "b").execute().fetchall(), expected)

    def testUpdateReleaseInvalidBlob(self):
        blob = ReleaseBlobV1(name="2", hashFunction="sha512")
        blob["foo"] = "bar"
        self.assertRaises(BlobValidationError, self.releases.update, where={"name": "b"}, what={"data": blob}, changed_by="bill", old_data_version=1)

    def testAddLocaleToRelease(self):
        data = {"complete": {"filesize": 1, "from": "*", "hashValue": "abc"}}
        self.releases.addLocaleToRelease(name="a", product="a", platform="p", locale="c", data=data, old_data_version=1, changed_by="bill")
        ret = select([self.releases.data]).where(self.releases.name == "a").execute().fetchone()[0]
        expected = createBlob(
            """
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
"""
        )
        self.assertEqual(ret, expected)

    def testAddLocaleToReleaseWithAlias(self):
        data = {"complete": {"filesize": 123, "from": "*", "hashValue": "abc"}}
        self.releases.addLocaleToRelease(name="a", product="a", platform="p", locale="c", data=data, old_data_version=1, changed_by="bill", alias=["p4"])
        ret = select([self.releases.data]).where(self.releases.name == "a").execute().fetchone()[0]
        expected = createBlob(
            """
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
"""
        )
        self.assertEqual(ret, expected)

    def testAddLocaleToReleaseOverride(self):
        data = {"complete": {"filesize": 123, "from": "*", "hashValue": "789"}}
        self.releases.addLocaleToRelease(name="a", product="a", platform="p", locale="l", data=data, old_data_version=1, changed_by="bill")
        ret = select([self.releases.data]).where(self.releases.name == "a").execute().fetchone()[0]
        expected = createBlob(
            """
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
"""
        )
        self.assertEqual(ret, expected)

    def testAddLocaleToReleasePlatformsDoesntExist(self):
        data = {"complete": {"filesize": 432, "from": "*", "hashValue": "abc"}}
        self.releases.addLocaleToRelease(name="b", product="b", platform="q", locale="l", data=data, old_data_version=1, changed_by="bill")
        ret = select([self.releases.data]).where(self.releases.name == "b").execute().fetchone()[0]
        expected = createBlob(
            """
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
"""
        )
        self.assertEqual(ret, expected)

    def testAddLocaleToReleaseNoLocales(self):
        data = {"complete": {"filesize": 432, "from": "*", "hashValue": "abc"}}
        self.releases.addLocaleToRelease(name="a", product="a", platform="p3", locale="l", data=data, old_data_version=1, changed_by="bill")
        ret = select([self.releases.data]).where(self.releases.name == "a").execute().fetchone()[0]
        expected = createBlob(
            """
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
"""
        )
        self.assertEqual(ret, expected)

    def testAddLocaleToReleaseSecondPlatform(self):
        data = {"complete": {"filesize": 324, "from": "*", "hashValue": "abc"}}
        self.releases.addLocaleToRelease(name="a", product="a", platform="q", locale="l", data=data, old_data_version=1, changed_by="bill")
        ret = select([self.releases.data]).where(self.releases.name == "a").execute().fetchone()[0]
        expected = createBlob(
            """
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
"""
        )
        self.assertEqual(ret, expected)

    def testAddLocaleToReleaseResolveAlias(self):
        data = {"complete": {"filesize": 444, "from": "*", "hashValue": "abc"}}
        self.releases.addLocaleToRelease(name="a", product="a", platform="p2", locale="j", data=data, old_data_version=1, changed_by="bill")
        ret = select([self.releases.data]).where(self.releases.name == "a").execute().fetchone()[0]
        expected = createBlob(
            """
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
"""
        )
        self.assertEqual(ret, expected)

    def testAddLocaleWhenReadOnly(self):
        data = {"complete": {"filesize": 1, "from": "*", "hashValue": "abc"}}
        self.releases.t.update(values=dict(read_only=True, data_version=2)).where(self.releases.name == "a").execute()
        self.assertRaises(
            ReadOnlyError, self.releases.addLocaleToRelease, name="a", product="a", platform="p", locale="c", data=data, old_data_version=1, changed_by="bill"
        )

    def testAddMergeableOutdatedData(self):
        ancestor_blob = createBlob(
            """
{
    "name": "p",
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
"""
        )
        blob1 = createBlob(
            """
{
    "name": "p",
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
"""
        )
        blob2 = createBlob(
            """
{
    "name": "p",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "c1": {
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
"""
        )
        result_blob = createBlob(
            """
{
    "name": "p",
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
                },
                "c1": {
                    "complete": {
                        "filesize": 1,
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
"""
        )
        with self.db.begin() as trans:
            self.releases.insert(changed_by="bill", name="p", product="z", data=ancestor_blob, transaction=trans)
            self.releases.update({"name": "p"}, {"product": "z", "data": blob1}, changed_by="bill", old_data_version=1, transaction=trans)
            self.releases.update({"name": "p"}, {"product": "z", "data": blob2}, changed_by="bill", old_data_version=1, transaction=trans)
        ret = select([self.releases.data]).where(self.releases.name == "p").execute().fetchone()[0]
        self.assertEqual(result_blob, ret)
        history_entries = [blob.data for name, blob in self.releases.history.bucket.blobs.items() if name.startswith("p")]
        self.assertEqual(len(history_entries), 4)
        self.assertEqual(history_entries[0], "")
        self.assertEqual(json.loads(history_entries[1]), ancestor_blob)
        self.assertEqual(json.loads(history_entries[2]), blob1)
        self.assertEqual(json.loads(history_entries[3]), result_blob)

    def testAddMergeableWithChangesToList(self):
        ancestor_blob = createBlob(
            """
{
    "name": "release4",
    "schema_version": 4,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "completes": [
                        {
                            "filesize": 1234,
                            "from": "*",
                            "hashValue": "def"
                        }
                    ],
                    "partials": [
                        {
                            "filesize": 1234,
                            "from": "release1",
                            "hashValue": "def"
                        }
                    ]
                }
            }
        }
    }
}
"""
        )
        blob1 = createBlob(
            """
{
    "name": "release4",
    "schema_version": 4,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "completes": [
                        {
                            "filesize": 1234,
                            "from": "*",
                            "hashValue": "def"
                        }
                    ],
                    "partials": [
                        {
                            "filesize": 1234,
                            "from": "release1",
                            "hashValue": "def"
                        },
                        {
                            "filesize": 5678,
                            "from": "release2",
                            "hashValue": "aaa"
                        }
                    ]
                }
            }
        }
    }
}
"""
        )
        blob2 = createBlob(
            """
{
    "name": "release4",
    "schema_version": 4,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "completes": [
                        {
                            "filesize": 1234,
                            "from": "*",
                            "hashValue": "def"
                        }
                    ],
                    "partials": [
                        {
                            "filesize": 1234,
                            "from": "release1",
                            "hashValue": "def"
                        },
                        {
                            "filesize": 9012,
                            "from": "release3",
                            "hashValue": "bbb"
                        }
                    ]
                }
            }
        }
    }
}
"""
        )
        result_blob = createBlob(
            """
{
    "name": "release4",
    "schema_version": 4,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "completes": [
                        {
                            "filesize": 1234,
                            "from": "*",
                            "hashValue": "def"
                        }
                    ],
                    "partials": [
                        {
                            "filesize": 1234,
                            "from": "release1",
                            "hashValue": "def"
                        },
                        {
                            "filesize": 5678,
                            "from": "release2",
                            "hashValue": "aaa"
                        },
                        {
                            "filesize": 9012,
                            "from": "release3",
                            "hashValue": "bbb"
                        }
                    ]
                }
            }
        }
    }
}
"""
        )
        with self.db.begin() as trans:
            self.releases.insert(changed_by="bill", name="release4", product="z", data=ancestor_blob, transaction=trans)
            self.releases.update({"name": "release4"}, {"product": "z", "data": blob1}, changed_by="bill", old_data_version=1, transaction=trans)
            self.releases.update({"name": "release4"}, {"product": "z", "data": blob2}, changed_by="bill", old_data_version=1, transaction=trans)
        ret = select([self.releases.data]).where(self.releases.name == "release4").execute().fetchone()[0]
        self.assertEqual(result_blob, ret)
        history_entries = [blob.data for name, blob in self.releases.history.bucket.blobs.items() if name.startswith("release4")]
        self.assertEqual(len(history_entries), 4)
        self.assertEqual(history_entries[0], "")
        self.assertEqual(json.loads(history_entries[1]), ancestor_blob)
        self.assertEqual(json.loads(history_entries[2]), blob1)
        self.assertEqual(json.loads(history_entries[3]), result_blob)

    def testAddConflictingOutdatedData(self):
        ancestor_blob = createBlob(
            """
{
    "name": "p",
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
"""
        )
        blob1 = createBlob(
            """
{
    "name": "p",
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
"""
        )
        blob2 = createBlob(
            """
{
    "name": "p",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "c": {
                    "complete": {
                        "filesize": 12,
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
"""
        )
        with self.db.begin() as trans:
            self.releases.insert(changed_by="bill", name="p", product="z", data=ancestor_blob, transaction=trans)
            self.releases.update({"name": "p"}, {"product": "z", "data": blob1}, changed_by="bill", old_data_version=1, transaction=trans)
            self.assertRaises(
                OutdatedDataError,
                self.releases.update,
                {"name": "p"},
                {"product": "z", "data": blob2},
                changed_by="bill",
                old_data_version=1,
                transaction=trans,
            )
        history_entries = [blob.data for name, blob in self.releases.history.bucket.blobs.items() if name.startswith("p")]
        self.assertEqual(len(history_entries), 3)
        self.assertEqual(history_entries[0], "")
        self.assertEqual(json.loads(history_entries[1]), ancestor_blob)
        self.assertEqual(json.loads(history_entries[2]), blob1)

    def testAddLocaleToReleaseDoesMerging(self):
        ancestor_blob = createBlob(
            """
{
    "name": "release4",
    "schema_version": 4,
    "hashFunction": "sha512",
    "product": "p",
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "completes": [
                        {
                            "filesize": 1234,
                            "from": "*",
                            "hashValue": "def"
                        }
                    ],
                    "partials": [
                        {
                            "filesize": 1234,
                            "from": "release1",
                            "hashValue": "def"
                        }
                    ]
                }
            }
        }
    }
}
"""
        )
        result_blob = createBlob(
            """
{
    "name": "release4",
    "schema_version": 4,
    "hashFunction": "sha512",
    "product": "p",
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "completes": [
                        {
                            "filesize": 1234,
                            "from": "*",
                            "hashValue": "def"
                        }
                    ],
                    "partials": [
                        {
                            "filesize": 1234,
                            "from": "release1",
                            "hashValue": "def"
                        },
                        {
                            "filesize": 567,
                            "from": "release2",
                            "hashValue": "ghi"
                        },
                        {
                            "filesize": 890,
                            "from": "release3",
                            "hashValue": "jkl"
                        }
                    ]
                }
            }
        }
    }
}
"""
        )
        with self.db.begin() as trans:
            self.releases.insert(changed_by="bill", name="release4", product="z", data=ancestor_blob, transaction=trans)
            self.releases.addLocaleToRelease(
                "release4",
                "p",
                "p",
                "l",
                {"partials": [{"filesize": 567, "from": "release2", "hashValue": "ghi"}]},
                old_data_version=1,
                changed_by="bill",
                transaction=trans,
            )
            self.releases.addLocaleToRelease(
                "release4",
                "p",
                "p",
                "l",
                {"partials": [{"filesize": 890, "from": "release3", "hashValue": "jkl"}]},
                old_data_version=1,
                changed_by="bill",
                transaction=trans,
            )
        ret = select([self.releases.data]).where(self.releases.name == "release4").execute().fetchone()[0]
        self.assertEqual(result_blob, ret)
        history_entries = [blob.data for name, blob in self.releases.history.bucket.blobs.items() if name.startswith("release4")]
        self.assertEqual(len(history_entries), 4)
        interim_blob = deepcopy(ancestor_blob)
        interim_blob["platforms"]["p"]["locales"]["l"] = {"partials": [{"filesize": 567, "from": "release2", "hashValue": "ghi"}]}
        self.assertEqual(history_entries[0], "")
        self.assertEqual(json.loads(history_entries[1]), ancestor_blob)
        self.assertEqual(json.loads(history_entries[2]), interim_blob)
        self.assertEqual(json.loads(history_entries[3]), result_blob)


@pytest.mark.usefixtures("current_db_schema")
class TestPinnableReleases(unittest.TestCase, MemoryDatabaseMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        dbo.setDb(self.dburi, releases_history_buckets={"*": "fake"}, releases_history_class=FakeGCSHistory)
        self.metadata.create_all(dbo.engine)
        dbo.releases_json.t.insert().execute(
            name="Firefox-60.0-build1",
            product="Firefox",
            data_version=1,
            data="""{
    "name": "Firefox-60.0-build1",
    "schema_version": 9,
    "hashFunction": "sha512"
}""",
        )
        dbo.releases_json.t.insert().execute(
            name="Firefox-60.0-build2",
            product="Firefox",
            data_version=1,
            data="""{
    "name": "Firefox-60.0-build2",
    "schema_version": 9,
    "hashFunction": "sha512"
}""",
        )
        self.pinnable_releases = dbo.pinnable_releases
        dbo.permissions.t.insert().execute(permission="admin", username="bob", data_version=1)
        dbo.permissions.user_roles.t.insert().execute(username="bob", role="releng", data_version=1)

    def testInsertUpdateAndDeletePinnableRelease(self):
        product = "Firefox"
        version = "60."
        channel = "beta"
        row = self.pinnable_releases.insert(changed_by="bob", product=product, version=version, channel=channel, mapping="Firefox-60.0-build1")
        self.assertEqual(self.pinnable_releases.getPinMapping(product=product, version=version, channel=channel), "Firefox-60.0-build1")
        row = self.pinnable_releases.update(
            where=[self.pinnable_releases.product == product, self.pinnable_releases.version == version, self.pinnable_releases.channel == channel],
            what={"mapping": "Firefox-60.0-build2"},
            changed_by="bob",
            old_data_version=row["data_version"],
        )
        self.assertEqual(self.pinnable_releases.getPinMapping(product=product, version=version, channel=channel), "Firefox-60.0-build2")
        row = self.pinnable_releases.delete(
            changed_by="bob",
            where=[self.pinnable_releases.product == product, self.pinnable_releases.version == version, self.pinnable_releases.channel == channel],
            old_data_version=row["data_version"],
        )
        self.assertEqual(self.pinnable_releases.getPinMapping(product=product, version=version, channel=channel), None)

    def testCannotInsertNonexistentRelease(self):
        with dbo.begin() as trans:
            with self.assertRaises(ValueError):
                releases.set_pinnable("fakemapping", product="Firefox", channel="beta", version="60.", when=None, username="bob", trans=trans)

    def testMustRemovePinToRemoveRelease(self):
        self.assertEqual(dbo.releases_json.count(where=[dbo.releases_json.name == "Firefox-60.0-build1"]), 1)
        row = self.pinnable_releases.insert(changed_by="bob", product="Firefox", version="60.", channel="beta", mapping="Firefox-60.0-build1")
        with dbo.begin() as trans:
            self.assertRaises(ValueError, releases.delete_release, name="Firefox-60.0-build1", changed_by="bob", trans=trans)
        self.assertEqual(dbo.releases_json.count(where=[dbo.releases_json.name == "Firefox-60.0-build1"]), 1)
        self.pinnable_releases.delete(changed_by="bob", where=[self.pinnable_releases.mapping == "Firefox-60.0-build1"], old_data_version=row["data_version"])
        dbo.releases_json.t.delete().where(dbo.releases_json.name == "Firefox-60.0-build1").execute()
        self.assertEqual(dbo.releases_json.count(where=[dbo.releases_json.name == "Firefox-60.0-build1"]), 0)


@pytest.mark.usefixtures("current_db_schema")
class TestPermissions(unittest.TestCase, MemoryDatabaseMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.metadata.create_all(self.db.engine)
        self.permissions = self.db.permissions
        self.user_roles = self.db.permissions.user_roles
        self.permissions.t.insert().execute(permission="admin", username="bill", data_version=1)
        self.permissions.t.insert().execute(permission="permission", username="bob", data_version=1)
        self.permissions.t.insert().execute(permission="permission", username="sean", data_version=1)
        self.permissions.t.insert().execute(permission="release", username="bob", options=dict(products=["fake"]), data_version=1)
        self.permissions.t.insert().execute(permission="release", username="janet", options=dict(products=["fake"]), data_version=1)
        self.permissions.t.insert().execute(permission="rule", username="cathy", data_version=1)
        self.permissions.t.insert().execute(permission="rule", username="bob", options=dict(actions=["modify"]), data_version=1)
        self.permissions.t.insert().execute(permission="rule", username="fred", options=dict(products=["foo", "bar"], actions=["modify"]), data_version=1)
        self.permissions.t.insert().execute(permission="admin", username="george", options=dict(products=["foo"]), data_version=1)
        self.user_roles.t.insert().execute(username="bob", role="releng", data_version=1)
        self.user_roles.t.insert().execute(username="bob", role="dev", data_version=1)
        self.user_roles.t.insert().execute(username="cathy", role="releng", data_version=1)
        self.user_roles.t.insert().execute(username="janet", role="releng", data_version=1)
        self.db.productRequiredSignoffs.t.insert().execute(product="foo", channel="bar", role="dev", signoffs_required=1, data_version=1)
        self.db.permissionsRequiredSignoffs.t.insert().execute(product="foo", role="dev", signoffs_required=1, data_version=2)

    def testAllTablesCreated(self):
        self.assertTrue(self.db.permissions)
        self.assertTrue(self.db.permissions.history)
        self.assertTrue(self.db.permissions.scheduled_changes)
        self.assertTrue(self.db.permissions.scheduled_changes.history)
        self.assertTrue(self.db.permissions.scheduled_changes.conditions)
        self.assertTrue(self.db.permissions.scheduled_changes.conditions.history)

    def testPermissionsHasCorrectTablesAndColumns(self):
        columns = [c.name for c in self.permissions.t.columns]
        expected = ["username", "permission", "options", "data_version"]
        self.assertEqual(set(columns), set(expected))
        history_columns = [c.name for c in self.permissions.history.t.columns]
        expected = ["change_id", "changed_by", "timestamp"] + expected
        self.assertEqual(set(history_columns), set(expected))

    def testUserRolesHasCorrectTablesAndColumns(self):
        columns = [c.name for c in self.user_roles.t.columns]
        expected = ["username", "role", "data_version"]
        self.assertEqual(set(columns), set(expected))
        history_columns = [c.name for c in self.user_roles.history.t.columns]
        expected = ["change_id", "changed_by", "timestamp"] + expected
        self.assertEqual(set(history_columns), set(expected))

    def testGrantPermissions(self):
        self.permissions.insert(
            "bob",
            signoffs=[{"sc_id": 1, "username": "bill", "role": "admin"}, {"sc_id": 1, "username": "zawadi", "role": "admin"}],
            username="cathy",
            permission="release",
            options=dict(products=["SeaMonkey"]),
        )
        query = self.permissions.t.select().where(self.permissions.username == "cathy")
        query = query.where(self.permissions.permission == "release")
        self.assertEqual(query.execute().fetchall(), [("release", "cathy", dict(products=["SeaMonkey"]), 1)])

    def testGrantPermissionsUnknownPermission(self):
        self.assertRaises(ValueError, self.permissions.insert, changed_by="bob", username="bud", permission="bad")

    def testGrantPermissionsUnknownOption(self):
        self.assertRaises(ValueError, self.permissions.insert, changed_by="bob", username="bud", permission="rule", options=dict(foo=1))

    def testGrantPermissionWithProductThatRequiresSignoff(self):
        self.assertRaises(SignoffRequiredError, self.permissions.insert, changed_by="bill", username="janet", permission="admin", options={"products": ["foo"]})

    def testGrantPermissionWithoutProductThatRequiresSignoff(self):
        self.assertRaises(SignoffRequiredError, self.permissions.insert, changed_by="bill", username="janet", permission="admin")

    def testGrantRoleWithPermission(self):
        self.permissions.grantRole("fred", "relman", "bill")
        got = self.user_roles.t.select().where(self.user_roles.username == "fred").execute().fetchall()
        self.assertEqual(got, [("fred", "relman", 1)])

    def testGrantRoleWithoutPermission(self):
        self.assertRaises(PermissionDeniedError, self.permissions.grantRole, username="rory", role="releng", changed_by="cathy")

    @emits_warning()
    def testGrantRoleExistingRole(self):
        self.assertRaises(TransactionError, self.permissions.grantRole, username="bob", role="releng", changed_by="bill")

    def testGrantRoleForExistingUser(self):
        self.permissions.grantRole("bob", "relman", "bill")
        got = self.user_roles.t.select().where(self.user_roles.username == "bob").execute().fetchall()
        self.assertEqual(len(got), 3)
        self.assertIn(("bob", "releng", 1), got)
        self.assertIn(("bob", "dev", 1), got)
        self.assertIn(("bob", "relman", 1), got)

    def testGrantRoleToUserWhoDoesntHaveAPermission(self):
        self.assertRaisesRegex(
            ValueError, "Cannot grant a role to a user without any permissions", self.permissions.grantRole, changed_by="bill", username="kirk", role="dev"
        )

    def testRevokePermission(self):
        self.permissions.delete(
            {"username": "bob", "permission": "release"},
            changed_by="bill",
            old_data_version=1,
            signoffs=[{"sc_id": 5, "username": "bill", "role": "admin"}, {"sc_id": 5, "username": "zawadi", "role": "admin"}],
        )
        query = self.permissions.t.select().where(self.permissions.username == "bob")
        query = query.where(self.permissions.permission == "release")
        self.assertEqual(len(query.execute().fetchall()), 0)

    def testRevokePermissionThatDoesntSupportProductOption(self):
        self.assertRaises(
            SignoffRequiredError, self.permissions.delete, {"username": "sean", "permission": "permission"}, changed_by="bill", old_data_version=1
        )

    def testRevokeRoleWithPermission(self):
        self.permissions.revokeRole("bob", "releng", "bill", old_data_version=1)
        got = self.user_roles.t.select().where(self.user_roles.username == "bob").execute().fetchall()
        self.assertEqual(len(got), 1)
        self.assertEqual(got[0], ("bob", "dev", 1))

    def testRevokeRoleWithoutPermission(self):
        self.assertRaises(PermissionDeniedError, self.permissions.revokeRole, username="bob", role="releng", changed_by="kirk", old_data_version=1)

    def testRevokingPermissionAlsoRevokeRoles(self):
        self.permissions.delete(
            {"username": "janet", "permission": "release"},
            changed_by="bill",
            old_data_version=1,
            signoffs=[{"sc_id": 3, "username": "bill", "role": "admin"}, {"sc_id": 3, "username": "zawadi", "role": "admin"}],
        )
        got = self.db.permissions.t.select().where(self.db.permissions.username == "janet").execute().fetchall()
        self.assertEqual(len(got), 0)
        got = self.user_roles.t.select().where(self.user_roles.username == "janet").execute().fetchall()
        self.assertEqual(len(got), 0)

    def testRevokePermissionWithProductThatRequiresSignoff(self):
        self.assertRaises(SignoffRequiredError, self.permissions.delete, {"username": "george", "permission": "admin"}, changed_by="bill", old_data_version=1)

    def testRevokePermissionWithoutProductThatRequiresSignoff(self):
        self.assertRaises(SignoffRequiredError, self.permissions.delete, {"username": "cathy", "permission": "rule"}, changed_by="bill", old_data_version=1)

    def testCannotRevokeRoleThatMakesRequiredSignoffImpossible(self):
        self.assertRaisesRegex(
            ValueError,
            "Revoking dev role would make it impossible for Required Signoffs to be fulfilled",
            self.permissions.revokeRole,
            "bob",
            "dev",
            "bill",
            old_data_version=1,
        )

    def testGetAllUsers(self):
        self.assertEqual(
            self.permissions.getAllUsers(),
            (
                {
                    "bill": {"roles": []},
                    "bob": {"roles": [{"data_version": 1, "role": "dev"}, {"data_version": 1, "role": "releng"}]},
                    "cathy": {"roles": [{"data_version": 1, "role": "releng"}]},
                    "fred": {"roles": []},
                    "george": {"roles": []},
                    "janet": {"roles": [{"data_version": 1, "role": "releng"}]},
                    "sean": {"roles": []},
                }
            ),
        )

    def testCountAllUsers(self):
        self.assertEqual(self.permissions.countAllUsers(), 7)

    def testGetPermission(self):
        expected = {"permission": "release", "username": "bob", "options": dict(products=["fake"]), "data_version": 1}
        self.assertEqual(self.permissions.getPermission("bob", "release"), expected)

    def testGetPermissionNonExistant(self):
        self.assertEqual(self.permissions.getPermission("cathy", "release"), {})

    def testGetUserPermissions(self):
        expected = {
            "permission": dict(options=None, data_version=1),
            "release": dict(options=dict(products=["fake"]), data_version=1),
            "rule": dict(options=dict(actions=["modify"]), data_version=1),
        }
        self.assertEqual(self.permissions.getUserPermissions("bob", "bob"), expected)

    def testGetOptions(self):
        expected = dict(products=["fake"])
        self.assertEqual(self.permissions.getOptions("bob", "release"), expected)

    def testGetOptionsPermissionDoesntExist(self):
        self.assertRaises(ValueError, self.permissions.getOptions, "fake", "fake")

    def testGetOptionsNoOptions(self):
        self.assertEqual(self.permissions.getOptions("cathy", "rule"), None)

    def testHasPermissionAdmin(self):
        self.assertTrue(self.permissions.hasPermission("bill", "rule", "delete"))

    def testHasPermissionProductAdmin(self):
        self.assertFalse(self.permissions.hasPermission("george", "rule", "delete"))
        self.assertTrue(self.permissions.hasPermission("george", "rule", "delete", "foo"))
        self.assertFalse(self.permissions.hasPermission("george", "rule", "delete", "bar"))

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

    def testGetUserRoles(self):
        got = self.permissions.getUserRoles("bob")
        got = sorted(got, key=lambda k: k["role"])
        expected = sorted([{"data_version": 1, "role": "releng"}, {"data_version": 1, "role": "dev"}], key=lambda k: k["role"])
        self.assertEqual(got, expected)

    def testGetUserRolesNonExistantUser(self):
        got = self.permissions.getUserRoles("kirk")
        self.assertEqual(got, [])

    def testUpdateUserRole(self):
        self.assertRaises(AttributeError, self.user_roles.update, {"username": "bob"}, {"role": "relman"}, "bill", 1)

    def testHasRole(self):
        self.assertTrue(self.permissions.hasRole("bob", "releng"))

    def testHasRoleNegative(self):
        self.assertFalse(self.permissions.hasRole("cathy", "dev"))

    def testIsAdmin(self):
        self.assertTrue(self.permissions.isAdmin("bill"))

    def testIsAdminNegative(self):
        self.assertFalse(self.permissions.isAdmin("bob"))

    def testKnownUser(self):
        self.assertTrue(self.permissions.isKnownUser("bob"))

    def testUnknownUser(self):
        self.assertFalse(self.permissions.isKnownUser(None))
        self.assertFalse(self.permissions.isKnownUser("adams"))


@pytest.mark.usefixtures("current_db_schema")
class TestDockerflow(unittest.TestCase, MemoryDatabaseMixin):
    def setUp(self):
        MemoryDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.metadata.create_all(self.db.engine)
        self.dockerflow = self.db.dockerflow

    def testInitAndIncrementValue(self):
        user = "dockerflow_test"

        with self.assertRaises(IndexError):
            self.dockerflow.getDockerflowEntry()
        self.dockerflow.incrementWatchdogValue(changed_by=user)
        entry = self.dockerflow.getDockerflowEntry()
        self.assertEqual(entry["watchdog"], 1)

        self.dockerflow.incrementWatchdogValue(changed_by=user)
        entry = self.dockerflow.getDockerflowEntry()
        self.assertEqual(entry["watchdog"], 2)


class TestDB(unittest.TestCase):
    def testSetDburiAlreadySetup(self):
        db = AUSDatabase("sqlite:///:memory:")
        self.assertRaises(AlreadySetupError, db.setDburi, "sqlite:///:memory:")

    def testReset(self):
        db = AUSDatabase("sqlite:///:memory:")
        db.reset()
        # If we can set the dburi again, reset worked!
        db.setDburi("sqlite:///:memory:")
        db.create()
        insp = Inspector.from_engine(db.engine)
        self.assertNotEqual(insp.get_table_names(), [])


class TestDBModel(unittest.TestCase, NamedFileDatabaseMixin):
    @classmethod
    def setUpClass(cls):
        cls.db_tables = set(
            [
                "dockerflow",
                # TODO: dive into this more
                # Migrate version only exists in production-like databases.
                # "migrate_version", # noqa
                "permissions",
                "permissions_history",
                "permissions_scheduled_changes",
                "permissions_scheduled_changes_conditions",
                "permissions_scheduled_changes_conditions_history",
                "permissions_scheduled_changes_history",
                "permissions_scheduled_changes_signoffs",
                "permissions_scheduled_changes_signoffs_history",
                "permissions_req_signoffs",
                "permissions_req_signoffs_history",
                "permissions_req_signoffs_scheduled_changes",
                "permissions_req_signoffs_scheduled_changes_conditions",
                "permissions_req_signoffs_scheduled_changes_conditions_history",
                "permissions_req_signoffs_scheduled_changes_history",
                "permissions_req_signoffs_scheduled_changes_signoffs",
                "permissions_req_signoffs_scheduled_changes_signoffs_history",
                "pinnable_releases",
                "pinnable_releases_history",
                "pinnable_releases_scheduled_changes",
                "pinnable_releases_scheduled_changes_conditions",
                "pinnable_releases_scheduled_changes_conditions_history",
                "pinnable_releases_scheduled_changes_history",
                "pinnable_releases_scheduled_changes_signoffs",
                "pinnable_releases_scheduled_changes_signoffs_history",
                "product_req_signoffs",
                "product_req_signoffs_history",
                "product_req_signoffs_scheduled_changes",
                "product_req_signoffs_scheduled_changes_conditions",
                "product_req_signoffs_scheduled_changes_conditions_history",
                "product_req_signoffs_scheduled_changes_history",
                "product_req_signoffs_scheduled_changes_signoffs",
                "product_req_signoffs_scheduled_changes_signoffs_history",
                "releases",
                "releases_scheduled_changes",
                "releases_scheduled_changes_conditions",
                "releases_scheduled_changes_conditions_history",
                "releases_scheduled_changes_history",
                "releases_scheduled_changes_signoffs",
                "releases_scheduled_changes_signoffs_history",
                "releases_json",
                "releases_json_scheduled_changes",
                "releases_json_scheduled_changes_conditions",
                "releases_json_scheduled_changes_conditions_history",
                "releases_json_scheduled_changes_history",
                "releases_json_scheduled_changes_signoffs",
                "releases_json_scheduled_changes_signoffs_history",
                "release_assets",
                "release_assets_scheduled_changes",
                "release_assets_scheduled_changes_conditions",
                "release_assets_scheduled_changes_conditions_history",
                "release_assets_scheduled_changes_history",
                "release_assets_scheduled_changes_signoffs",
                "release_assets_scheduled_changes_signoffs_history",
                "rules",
                "rules_history",
                "rules_scheduled_changes",
                "rules_scheduled_changes_conditions",
                "rules_scheduled_changes_conditions_history",
                "rules_scheduled_changes_history",
                "rules_scheduled_changes_signoffs",
                "rules_scheduled_changes_signoffs_history",
                "user_roles",
                "user_roles_history",
                "emergency_shutoffs",
                "emergency_shutoffs_history",
                "emergency_shutoffs_scheduled_changes",
                "emergency_shutoffs_scheduled_changes_history",
                "emergency_shutoffs_scheduled_changes_conditions",
                "emergency_shutoffs_scheduled_changes_conditions_history",
                "emergency_shutoffs_scheduled_changes_signoffs",
                "emergency_shutoffs_scheduled_changes_signoffs_history",
            ]
        )

        # autoincrement isn't tested as Sqlite does not support this outside of INTEGER PRIMARY KEYS.
        # If the testing db is ever switched to mysql, this should be revisited.
        cls.properties = (
            "nullable",
            "primary_key",
            # 'autoincrement',
            "constraints",
            "foreign_keys",
            "index",
            "timetuple",
        )
        cls.property_err_msg = (
            "Property '{property}' on '{table_name}.{column}' differs between model " "and migration: (model) {model_prop} != (migration) {reflected_prop}"
        )

    def setUp(self):
        NamedFileDatabaseMixin.setUp(self)
        self.db = AUSDatabase(self.dburi)
        self.db.metadata.create_all()

    def tearDown(self):
        NamedFileDatabaseMixin.tearDown(self)

    def _is_column_unique(self, col_obj):
        """
        Check to see if a column is unique using a Sqlite-specific query.
        """
        col_engine = col_obj.table.metadata.bind
        table_name = col_obj.table.name
        res = col_engine.execute("SELECT sql FROM sqlite_master WHERE name = :table_name", table_name=table_name)
        res = res.fetchone()[0]

        # Return None instead of False in order to adhere to SQLAlchemy's style: Column.unique returns None
        # if it hasn't been explicitly set.
        if re.search(r"(?:CONSTRAINT (\w+) +)?UNIQUE *\({0}\)".format(col_obj.name), res) is None:
            return None
        return True

    def _get_migrated_db(self):
        db = AUSDatabase("sqlite:///" + self.getTempfile())
        db.create()
        return db

    def _get_reflected_metadata(self, db):
        """
        @type db: AUSDatabase
        """
        mt = MetaData()
        engine = create_engine(db.dburi)
        mt.bind = engine
        mt.reflect()
        return mt

    def assert_attributes_for_tables(self, tables):
        """
        Expects an iterable of sqlalchemy (Table, Table) pairs. The first table
        should be the result of migrations, the second should be the model
        taken directly from db.py.
        """
        failures = []
        for reflected_table, table_model_instance in tables:
            for col_name in table_model_instance.c.keys():
                db_py_col = table_model_instance.c[col_name]
                reflected_db_col = reflected_table.c[col_name]

                for col_property in self.properties:
                    db_py_col_property = getattr(db_py_col, col_property)
                    reflected_db_col_property = getattr(reflected_db_col, col_property)

                    if db_py_col_property != reflected_db_col_property:
                        failures.append(
                            self.property_err_msg.format(
                                property=col_property,
                                table_name=table_model_instance.name,
                                column=col_name,
                                model_prop=db_py_col_property,
                                reflected_prop=reflected_db_col_property,
                            )
                        )

                # Testing 'unique' separately since Sqlalchemy < 1.0.0 can't reflect this attribute for this version of sqlite
                # ref_uniq = self._is_column_unique(reflected_db_col)
                # if db_py_col.unique != ref_uniq:
                #    failures.append(
                #        self.property_err_msg.format(
                #            property="unique",
                #            table_name=table_model_instance.name,
                #            column=col_name,
                #            model_prop=db_py_col.unique,
                #            reflected_prop=ref_uniq))

        self.assertEqual(failures, [], "Column properties different between models and migrations:\n" + "\n".join(failures))

    def testAllTablesExist(self):
        self.assertEqual(set(self.db.metadata.tables.keys()), self.db_tables)

    def testModelIsSameAsRepository(self):
        db2 = self._get_migrated_db()
        diff = migrate.versioning.api.compare_model_to_db(db2.engine, self.db.migrate_repo, self.db.metadata)
        if diff:
            self.fail(str(diff))

    def testColumnAttributesAreSameAsDb(self):
        table_instances = []

        db = self._get_migrated_db()
        meta_data = self._get_reflected_metadata(db)

        for table_name in self.db_tables:
            table_instances.append((meta_data.tables[table_name], self.db.metadata.tables[table_name]))

        self.assert_attributes_for_tables(table_instances)

    def _rules_version_length_migration_test(self, db, upgrade=True):
        """
        Tests the upgrades and downgrades for version 23 work properly.
        :param db: migrated DB object.
        :param upgrade: boolean parameter. If true run for upgrade script tests else
          run downgrade script tests.
        """
        upgraded_length = 75
        downgrade_length = 10
        meta_data = self._get_reflected_metadata(db)
        tables_list = ["rules", "rules_history"]
        scheduled_changes_tables = ["rules_scheduled_changes", "rules_scheduled_changes_history"]
        if upgrade:
            for table_name in tables_list:
                self.assertEqual(upgraded_length, meta_data.tables[table_name].c.version.type.length)
            for table_name in scheduled_changes_tables:
                self.assertEqual(upgraded_length, meta_data.tables[table_name].c.base_version.type.length)
        else:
            for table_name in tables_list:
                self.assertEqual(downgrade_length, meta_data.tables[table_name].c.version.type.length)
            for table_name in scheduled_changes_tables:
                self.assertEqual(downgrade_length, meta_data.tables[table_name].c.base_version.type.length)

    def _delete_whitelist_migration_test(self, db, upgrade=True):
        """
        Tests the upgrades and downgrades for version 24 work properly.
        :param db: migrated DB object
        :param upgrade: boolean parameter. If true run for upgrade script tests else
          run downgrade script tests.
        """

        meta_data = self._get_reflected_metadata(db)

        whitelist_tables = ["rules", "rules_history"]
        base_whitelist_tables = ["rules_scheduled_changes", "rules_scheduled_changes_history"]

        if upgrade:
            for table_name in whitelist_tables:
                self.assertNotIn("whitelist", meta_data.tables[table_name].c)

            for table_name in base_whitelist_tables:
                self.assertNotIn("base_whitelist", meta_data.tables[table_name].c)
        else:
            for table_name in whitelist_tables:
                self.assertIn("whitelist", meta_data.tables[table_name].c)

            for table_name in base_whitelist_tables:
                self.assertIn("base_whitelist", meta_data.tables[table_name].c)

    def _add_memory_migration_test(self, db, upgrade=True):
        metadata = self._get_reflected_metadata(db)
        memory_tables = ["rules", "rules_history"]
        base_memory_tables = ["rules_scheduled_changes", "rules_scheduled_changes_history"]

        if upgrade:
            for table_name in memory_tables:
                self.assertIn("memory", metadata.tables[table_name].c)
            for table_name in base_memory_tables:
                self.assertIn("base_memory", metadata.tables[table_name].c)
        else:
            for table_name in memory_tables:
                self.assertNotIn("memory", metadata.tables[table_name].c)
            for table_name in base_memory_tables:
                self.assertNotIn("base_memory", metadata.tables[table_name].c)

    def _add_instructionSet_test(self, db, upgrade=True):
        metadata = self._get_reflected_metadata(db)
        capabilities_tables = ["rules", "rules_history"]
        base_capabilities_tables = ["rules_scheduled_changes", "rules_scheduled_changes_history"]

        if upgrade:
            for table_name in capabilities_tables:
                self.assertIn("instructionSet", metadata.tables[table_name].c)
            for table_name in base_capabilities_tables:
                self.assertIn("base_instructionSet", metadata.tables[table_name].c)
        else:
            for table_name in capabilities_tables:
                self.assertNotIn("instructionSet", metadata.tables[table_name].c)
            for table_name in base_capabilities_tables:
                self.assertNotIn("base_instructionSet", metadata.tables[table_name].c)

    def _remove_systemCapabilities_test(self, db, upgrade=True):
        metadata = self._get_reflected_metadata(db)
        capabilities_tables = ["rules", "rules_history"]
        base_capabilities_tables = ["rules_scheduled_changes", "rules_scheduled_changes_history"]

        if upgrade:
            for table_name in capabilities_tables:
                self.assertNotIn("systemCapabilities", metadata.tables[table_name].c)
            for table_name in base_capabilities_tables:
                self.assertNotIn("base_systemCapabilities", metadata.tables[table_name].c)
        else:
            for table_name in capabilities_tables:
                self.assertIn("systemCapabilities", metadata.tables[table_name].c)
            for table_name in base_capabilities_tables:
                self.assertIn("base_systemCapabilities", metadata.tables[table_name].c)

    def _add_mig64_test(self, db, upgrade=True):
        metadata = self._get_reflected_metadata(db)
        mig64_tables = ["rules", "rules_history"]
        base_mig64_tables = ["rules_scheduled_changes", "rules_scheduled_changes_history"]

        if upgrade:
            for table_name in mig64_tables:
                self.assertIn("mig64", metadata.tables[table_name].c)
            for table_name in base_mig64_tables:
                self.assertIn("base_mig64", metadata.tables[table_name].c)
        else:
            for table_name in mig64_tables:
                self.assertNotIn("mig64", metadata.tables[table_name].c)
            for table_name in base_mig64_tables:
                self.assertNotIn("base_mig64", metadata.tables[table_name].c)

    def _add_jaws_test(self, db, upgrade=True):
        metadata = self._get_reflected_metadata(db)
        jaws_tables = ["rules", "rules_history"]
        base_jaws_tables = ["rules_scheduled_changes", "rules_scheduled_changes_history"]

        if upgrade:
            for table_name in jaws_tables:
                self.assertIn("jaws", metadata.tables[table_name].c)
            for table_name in base_jaws_tables:
                self.assertIn("base_jaws", metadata.tables[table_name].c)
        else:
            for table_name in jaws_tables:
                self.assertNotIn("jaws", metadata.tables[table_name].c)
            for table_name in base_jaws_tables:
                self.assertNotIn("base_jaws", metadata.tables[table_name].c)

    def _add_emergency_shutoff_tables(self, db, upgrade=True):
        metadata = self._get_reflected_metadata(db)
        shutoff_tables = [
            "emergency_shutoffs",
            "emergency_shutoffs_history",
            "emergency_shutoffs_scheduled_changes",
            "emergency_shutoffs_scheduled_changes_history",
            "emergency_shutoffs_scheduled_changes_conditions",
            "emergency_shutoffs_scheduled_changes_conditions_history",
            "emergency_shutoffs_scheduled_changes_signoffs",
            "emergency_shutoffs_scheduled_changes_signoffs_history",
        ]
        if upgrade:
            for table in shutoff_tables:
                self.assertIn(table, metadata.tables)
        else:
            for table in shutoff_tables:
                self.assertNotIn(table, metadata.tables)

    def _add_emergency_shutoff_comments(self, db, upgrade=True):
        metadata = self._get_reflected_metadata(db)
        emergency_shutoff_tables = [
            "emergency_shutoffs",
            "emergency_shutoffs_history",
        ]

        emergency_shutoff_sc_tables = [
            "emergency_shutoffs_scheduled_changes",
            "emergency_shutoffs_scheduled_changes_history",
        ]

        if upgrade:
            for table_name in emergency_shutoff_tables:
                self.assertIn("comment", metadata.tables[table_name].c)
            for table_name in emergency_shutoff_sc_tables:
                self.assertIn("base_comment", metadata.tables[table_name].c)
        else:
            for table_name in emergency_shutoff_tables:
                self.assertNotIn("comment", metadata.tables[table_name].c)
            for table_name in emergency_shutoff_sc_tables:
                self.assertNotIn("base_comment", metadata.tables[table_name].c)

    def _add_release_json_tables(self, db, upgrade=True):
        metadata = self._get_reflected_metadata(db)
        releases_tables = [
            "releases_json",
            "releases_json_scheduled_changes",
            "releases_json_scheduled_changes_history",
            "releases_json_scheduled_changes_conditions",
            "releases_json_scheduled_changes_conditions_history",
            "releases_json_scheduled_changes_signoffs",
            "releases_json_scheduled_changes_signoffs_history",
            "release_assets",
            "release_assets_scheduled_changes",
            "release_assets_scheduled_changes_history",
            "release_assets_scheduled_changes_conditions",
            "release_assets_scheduled_changes_conditions_history",
            "release_assets_scheduled_changes_signoffs",
            "release_assets_scheduled_changes_signoffs_history",
        ]
        if upgrade:
            for table in releases_tables:
                self.assertIn(table, metadata.tables)
        else:
            for table in releases_tables:
                self.assertNotIn(table, metadata.tables)

    def _add_pinnable_releases_tables(self, db, upgrade=True):
        metadata = self._get_reflected_metadata(db)
        pin_tables = [
            "pinnable_releases",
            "pinnable_releases_scheduled_changes",
            "pinnable_releases_scheduled_changes_history",
            "pinnable_releases_scheduled_changes_conditions",
            "pinnable_releases_scheduled_changes_conditions_history",
            "pinnable_releases_scheduled_changes_signoffs",
            "pinnable_releases_scheduled_changes_signoffs_history",
        ]
        if upgrade:
            for table in pin_tables:
                self.assertIn(table, metadata.tables)
        else:
            for table in pin_tables:
                self.assertNotIn(table, metadata.tables)

    def _fix_column_attributes_migration_test(self, db, upgrade=True):
        """
        Tests the upgrades and downgrades for version 22 work properly.
        :param db: migrated DB object
        :param upgrade: boolean parameter. If true run for upgrade script tests else
          run downgrade script tests.
        """
        data_version_nullable_tables = [
            "permissions_req_signoffs_scheduled_changes_conditions",
            "permissions_scheduled_changes",
            "permissions_scheduled_changes_conditions",
            "product_req_signoffs_scheduled_changes_conditions",
            "releases_scheduled_changes",
            "releases_scheduled_changes_conditions",
            "rules_scheduled_changes",
            "rules_scheduled_changes_conditions",
            "user_roles",
        ]

        when_nullable_tables = ["permissions_scheduled_changes_conditions", "releases_scheduled_changes_conditions"]

        meta_data = self._get_reflected_metadata(db)

        if upgrade:
            for table_name in data_version_nullable_tables:
                self.assertFalse(meta_data.tables[table_name].c.data_version.nullable)
            for table_name in when_nullable_tables:
                self.assertTrue(meta_data.tables[table_name].c.when.nullable)
        else:
            for table_name in data_version_nullable_tables:
                self.assertTrue(meta_data.tables[table_name].c.data_version.nullable)
            for table_name in when_nullable_tables:
                self.assertFalse(meta_data.tables[table_name].c.when.nullable)

    def _test_rules_longer_distribution(self, db, upgrade=True):
        upgraded_length = 2000
        downgrade_length = 100
        meta_data = self._get_reflected_metadata(db)
        tables_list = ["rules", "rules_history"]
        scheduled_changes_tables = ["rules_scheduled_changes", "rules_scheduled_changes_history"]
        if upgrade:
            for table_name in tables_list:
                self.assertEqual(upgraded_length, meta_data.tables[table_name].c.distribution.type.length)
            for table_name in scheduled_changes_tables:
                self.assertEqual(upgraded_length, meta_data.tables[table_name].c.base_distribution.type.length)
        else:
            for table_name in tables_list:
                self.assertEqual(downgrade_length, meta_data.tables[table_name].c.distribution.type.length)
            for table_name in scheduled_changes_tables:
                self.assertEqual(downgrade_length, meta_data.tables[table_name].c.base_distribution.type.length)

    def testVersionChangesWorkAsExpected(self):
        """
        Tests that downgrades and upgrades work as expected. Since the DB will never
        be rolled back beyond version 21 we treat it as the base version for all future versions from now.
        Note: These tests run and verify migrations on a sqlite DB
        whereas the actual migration happens on a mySQL DB.
        """
        # TODO Remove these tests when we upgrade sqlalchemy so that these per-version tests are no longer required.
        latest_version = version(path.abspath(path.join(path.dirname(auslib.__file__), "migrate")))
        db = self._get_migrated_db()

        def _noop(*args, **kwargs):
            pass

        versions_migrate_tests_dict = {
            35: self._add_emergency_shutoff_comments,
            34: self._add_pinnable_releases_tables,
            33: self._add_release_json_tables,
            # This version removes the releases_history table, which is verified by other tests
            32: _noop,
            31: self._test_rules_longer_distribution,
            30: self._add_emergency_shutoff_tables,
            29: self._add_jaws_test,
            28: self._add_mig64_test,
            27: self._remove_systemCapabilities_test,
            26: self._add_instructionSet_test,
            # No-op migration
            25: _noop,
            24: self._add_memory_migration_test,
            23: self._delete_whitelist_migration_test,
            22: self._rules_version_length_migration_test,
            21: self._fix_column_attributes_migration_test,
        }

        for v in range(latest_version - 1, 20, -1):
            db.downgrade(version=v)
            versions_migrate_tests_dict[v](db=db, upgrade=False)

        for v in range(22, latest_version + 1):
            db.upgrade(version=v)
            versions_migrate_tests_dict[v - 1](db=db)
