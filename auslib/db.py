from collections import defaultdict
from copy import copy
import itertools
from os import path
import pprint
import re
import simplejson as json
import sys
import time

from sqlalchemy import Table, Column, Integer, Text, String, MetaData, \
    create_engine, select, BigInteger, Boolean, join
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import null
import sqlalchemy.types

import migrate.versioning.schema
import migrate.versioning.api

import dictdiffer
import dictdiffer.merge

from auslib.global_state import cache, dbo
from auslib.blobs.base import createBlob
from auslib.util.comparison import string_compare, version_compare
from auslib.util.timestamp import getMillisecondTimestamp

import logging


def rowsToDicts(fn):
    """Decorator that converts the result of any function returning a dict-like
       object to an actual dict. Eg, converts read-only row objects to writable
       dicts."""
    def convertRows(*args, **kwargs):
        ret = []
        for row in fn(*args, **kwargs):
            d = {}
            for key in row.keys():
                d[key] = row[key]
            ret.append(d)
        return ret
    return convertRows


class AlreadySetupError(Exception):

    def __str__(self):
        return "Can't connect to new database, still connected to previous one"


class PermissionDeniedError(Exception):
    pass


class TransactionError(SQLAlchemyError):
    """Raised when a transaction fails for any reason."""


class OutdatedDataError(SQLAlchemyError):
    """Raised when an update or delete fails because of outdated data."""


class WrongNumberOfRowsError(SQLAlchemyError):
    """Raised when an update or delete fails because the clause matches more than one row."""


class UpdateMergeError(SQLAlchemyError):
    pass


class ReadOnlyError(SQLAlchemyError):
    """Raised when a release marked as read-only is attempted to be changed."""


class ChangeScheduledError(SQLAlchemyError):
    """Raised when a Scheduled Change cannot be created, modified, or deleted
    for data consistency reasons."""


class AUSTransaction(object):
    """Manages a single transaction. Requires a connection object.

       @param conn: connection object to perform the transaction on
       @type conn: sqlalchemy.engine.base.Connection
    """

    def __init__(self, engine):
        self.engine = engine
        self.conn = self.engine.connect()
        self.trans = self.conn.begin()
        self.log = logging.getLogger(self.__class__.__name__)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        try:
            # If something that executed in the context raised an Exception,
            # rollback and re-raise it.
            if exc[0]:
                self.log.debug("exc is:", exc_info=True)
                self.rollback()
                raise exc[0], exc[1], exc[2]
            # Also need to check for exceptions during commit!
            try:
                self.commit()
            except:
                self.rollback()
                raise
        finally:
            # Always make sure the connection is closed, bug 740360
            self.close()

    def close(self):
        # For some reason, sometimes the connection appears to close itself...
        if not self.conn.closed:
            self.conn.close()

    def execute(self, statement):
        try:
            self.log.debug("Attempting to execute %s" % statement)
            return self.conn.execute(statement)
        except:
            self.log.debug("Caught exception")
            # We want to raise our own Exception, so that errors are easily
            # caught by consumers. The dance below lets us do that without
            # losing the original Traceback, which will be much more
            # informative than one starting from this point.
            klass, e, tb = sys.exc_info()
            self.rollback()
            e = TransactionError(e.args)
            raise TransactionError, e, tb

    def commit(self):
        try:
            self.trans.commit()
        except:
            klass, e, tb = sys.exc_info()
            self.rollback()
            e = TransactionError(e.args)
            raise TransactionError, e, tb

    def rollback(self):
        self.trans.rollback()


class AUSTable(object):
    """Base class for all AUS Tables. By default, all tables have a history
       table created for them, too, which mirrors their own structure and adds
       a record of who made a change, and when the change happened.

       @param history: Whether or not to create a history table for this table.
                       When True, a History object will be created for this
                       table, and all changes will be logged to it. Defaults
                       to True.
       @type history: bool
       @param versioned: Whether or not this table is versioned. When True,
                         an additional 'data_version' column will be added
                         to the Table, and its version increased with every
                         update. This is useful for detecting colliding
                         updates.
       @type versioned: bool
       @param scheduled_changes: Whether or not this table should allow changes
                                 to be scheduled. When True, two additional tables
                                 will be created: a $name_scheduled_changes, which
                                 will contain data needed to schedule changes to
                                 $name, and $name_scheduled_changes_history, which
                                 tracks the history of a scheduled change.
       @type scheduled_changes: bool
       @param onInsert: A callback that will be called whenever an insert is
                        made to the table. It must accept the following 4
                        parameters:
                         * The table object the query is being performed on
                         * The type of query being performed (eg: INSERT)
                         * The name of the user making the change
                         * The query object that will be execeuted
                        If the callback raises an exception the change will
                        be aborted.
       @type onInsert: callable
       @param onDelete: See onInsert
       @type onDelete: callable
       @param onUpdate: See onInsert
       @type onUpdate: callable
    """

    def __init__(self, db, dialect, history=True, versioned=True, scheduled_changes=False,
                 onInsert=None, onUpdate=None, onDelete=None):
        self.db = db
        self.t = self.table
        # Enable versioning, if required
        if versioned:
            self.t.append_column(Column('data_version', Integer, nullable=False))
        self.versioned = versioned
        self.onInsert = onInsert
        self.onUpdate = onUpdate
        self.onDelete = onDelete
        # Mirror the columns as attributes for easy access
        self.primary_key = []
        for col in self.table.get_children():
            setattr(self, col.name, col)
            if col.primary_key:
                self.primary_key.append(col)
        # Set-up a history table to do logging in, if required
        if history:
            self.history = History(db, dialect, self.t.metadata, self)
        else:
            self.history = None
        # Set-up a scheduled changes table if required
        if scheduled_changes:
            self.scheduled_changes = ScheduledChangeTable(db, dialect, self.t.metadata, self)
        else:
            self.scheduled_changes = None
        self.log = logging.getLogger(self.__class__.__name__)

    # Can't do this in the constructor, because the engine is always
    # unset when we're instantiated
    def getEngine(self):
        return self.t.metadata.bind

    def _returnRowOrRaise(self, where, columns=None, transaction=None):
        """Return the row matching the where clause supplied. If no rows match or multiple rows match,
           a WrongNumberOfRowsError will be raised."""
        rows = self.select(where=where, columns=columns, transaction=transaction)
        if len(rows) == 0:
            raise WrongNumberOfRowsError("where clause matched no rows")
        if len(rows) > 1:
            raise WrongNumberOfRowsError("where clause matches multiple rows (primary keys: %s)" % rows)
        return rows[0]

    def _selectStatement(self, columns=None, where=None, order_by=None, limit=None, offset=None, distinct=False):
        """Create a SELECT statement on this table.

           @param columns: Column objects to select. Defaults to None, meaning select all columns
           @type columns: A sequence of sqlalchemy.schema.Column objects or column names as strings
           @param order_by: Columns to sort the rows by. Defaults to None, meaning no ORDER BY clause
           @type order_by: A sequence of sqlalchemy.schema.Column objects
           @param limit: Limit results to this many. Defaults to None, meaning no limit
           @type limit: int
           @param distinct: Whether or not to return only distinct rows. Default: False.
           @type distinct: bool

           @rtype: sqlalchemy.sql.expression.Select
        """
        if columns:
            query = select(columns, order_by=order_by, limit=limit, offset=offset, distinct=distinct)
        else:
            query = self.t.select(order_by=order_by, limit=limit, offset=offset, distinct=distinct)
        if where:
            for cond in where:
                query = query.where(cond)
        return query

    @rowsToDicts
    def select(self, where=None, transaction=None, **kwargs):
        """Perform a SELECT statement on this table.
           See AUSTable._selectStatement for possible arguments.

           @param where: A list of SQLAlchemy clauses, or a key/value pair of columns and values.
           @type where: list of clauses or key/value pairs.

           @rtype: sqlalchemy.engine.base.ResultProxy
        """

        # If "where" is key/value pairs, we need to convert it to SQLAlchemy
        # clauses before porceeding.
        if hasattr(where, "keys"):
            where = [getattr(self, k) == v for k, v in where.iteritems()]

        query = self._selectStatement(where=where, **kwargs)
        if transaction:
            return transaction.execute(query).fetchall()
        else:
            return query.execute().fetchall()

    def _insertStatement(self, **columns):
        """Create an INSERT statement for this table

           @param columns: Data to insert
           @type colmuns: dict

           @rtype: sqlalchemy.sql.express.Insert
        """
        return self.t.insert(values=columns)

    def _prepareInsert(self, trans, changed_by, **columns):
        """Prepare an INSERT statement for commit. If this table has versioning enabled,
           data_version will be set to 1. If this table has history enabled, two rows
           will be created in that table: one representing the current state (NULL),
           and one representing the new state.

           @rtype: sqlalchemy.engine.base.ResultProxy
        """
        data = columns.copy()
        if self.versioned:
            data['data_version'] = 1
        query = self._insertStatement(**data)

        if self.onInsert:
            self.onInsert(self, "INSERT", changed_by, query)

        ret = trans.execute(query)
        if self.history:
            for q in self.history.forInsert(ret.inserted_primary_key, data, changed_by):
                trans.execute(q)
        return ret

    def insert(self, changed_by=None, transaction=None, **columns):
        """Perform an INSERT statement on this table. See AUSTable._insertStatement for
           a description of columns.

           @param changed_by: The username of the person inserting the row. Required when
                              history is enabled. Unused otherwise. No authorization checks are done
                              at this level.
           @type changed_by: str
           @param transaction: A transaction object to add the insert statement (and history changes) to.
                               If provided, you must commit the transaction yourself. If None, they will
                               be added to a locally-scoped transaction and committed.

           @rtype: sqlalchemy.engine.base.ResultProxy
        """
        if self.history and not changed_by:
            raise ValueError("changed_by must be passed for Tables that have history")

        if transaction:
            return self._prepareInsert(transaction, changed_by, **columns)
        else:
            with AUSTransaction(self.getEngine()) as trans:
                return self._prepareInsert(trans, changed_by, **columns)

    def _deleteStatement(self, where):
        """Create a DELETE statement for this table.

           @param where: Conditions to apply on this select.
           @type where: A sequence of sqlalchemy.sql.expression.ClauseElement objects

           @rtype: sqlalchemy.sql.expression.Delete
        """
        query = self.t.delete()
        if where:
            for cond in where:
                query = query.where(cond)
        return query

    def _prepareDelete(self, trans, where, changed_by, old_data_version):
        """Prepare a DELETE statament for commit. If this table has history enabled,
           a row will be created in that table representing the new state of the
           row being deleted (NULL). If versioning is enabled and old_data_version
           doesn't match the current version of the row to be deleted, an OutdatedDataError
           will be raised.

           @rtype: sqlalchemy.engine.base.ResultProxy
        """
        row = self._returnRowOrRaise(where=where, columns=self.primary_key, transaction=trans)

        if self.versioned:
            where = copy(where)
            where.append(self.data_version == old_data_version)

        query = self._deleteStatement(where)

        if self.onDelete:
            self.onDelete(self, "DELETE", changed_by, query)

        ret = trans.execute(query)
        if ret.rowcount != 1:
            raise OutdatedDataError("Failed to delete row, old_data_version doesn't match current data_version")
        if self.history:
            trans.execute(self.history.forDelete(row, changed_by))
        if self.scheduled_changes:
            # If this table has active scheduled changes we cannot allow it to be deleted
            sc_where = [self.scheduled_changes.complete == False]  # noqa
            for pk in self.primary_key:
                sc_where.append(getattr(self.scheduled_changes, "base_%s" % pk.name) == row[pk.name])
            if self.scheduled_changes.select(where=sc_where, transaction=trans):
                raise ChangeScheduledError("Cannot delete rows that have changes scheduled.")

        return ret

    def delete(self, where, changed_by=None, old_data_version=None, transaction=None):
        """Perform a DELETE statement on this table. See AUSTable._deleteStatement for
           a description of `where'. To simplify versioning, this method can only
           delete a single row per invocation. If the where clause given would delete
           zero or multiple rows, a WrongNumberOfRowsError is raised.

           @param where: A list of SQLAlchemy clauses, or a key/value pair of columns and values.
           @type where: list of clauses or key/value pairs.
           @param changed_by: The username of the person deleting the row(s). Required when
                              history is enabled. Unused otherwise. No authorization checks are done
                              at this level.
           @type changed_by: str
           @param old_data_version: Previous version of the row to be deleted. If this version doesn't
                                    match the current version of the row, an OutdatedDataError will be
                                    raised and the delete will fail. Required when versioning is enabled.
           @type old_data_version: int

           @rtype: sqlalchemy.engine.base.ResultProxy
        """
        # If "where" is key/value pairs, we need to convert it to SQLAlchemy
        # clauses before porceeding.
        if hasattr(where, "keys"):
            where = [getattr(self, k) == v for k, v in where.iteritems()]

        if self.history and not changed_by:
            raise ValueError("changed_by must be passed for Tables that have history")
        if self.versioned and not old_data_version:
            raise ValueError("old_data_version must be passed for Tables that are versioned")

        if transaction:
            return self._prepareDelete(transaction, where, changed_by, old_data_version)
        else:
            with AUSTransaction(self.getEngine()) as trans:
                return self._prepareDelete(trans, where, changed_by, old_data_version)

    def _updateStatement(self, where, what):
        """Create an UPDATE statement for this table

           @param where: Conditions to apply to this UPDATE.
           @type where: A sequence of sqlalchemy.sql.expression.ClauseElement objects.
           @param what: Data to update
           @type what: dict

           @rtype: sqlalchemy.sql.expression.Update
        """
        query = self.t.update(values=what)
        if where:
            for cond in where:
                query = query.where(cond)
        return query

    def _prepareUpdate(self, trans, where, what, changed_by, old_data_version):
        """Prepare an UPDATE statement for commit. If this table has versioning enabled,
           data_version will be increased by 1. If this table has history enabled, a
           row will be added to that table represent the new state of the data.

           @rtype: sqlalchemy.engine.base.ResultProxy
        """
        # To do merge detection for tables with scheduled changes we need a
        # copy of the original row, and what will be changed. To record
        # history, we need a copy of the entire new row.
        orig_row = self._returnRowOrRaise(where=where, transaction=trans)
        new_row = orig_row.copy()
        if self.versioned:
            where = copy(where)
            where.append(self.data_version == old_data_version)
            new_row['data_version'] += 1
            what["data_version"] = new_row["data_version"]

        # Copy the new data into the row
        for col in what:
            new_row[col] = what[col]

        query = self._updateStatement(where, new_row)

        if self.onUpdate:
            self.onUpdate(self, "UPDATE", changed_by, query)

        ret = trans.execute(query)
        if self.history:
            trans.execute(self.history.forUpdate(new_row, changed_by))
        if self.scheduled_changes:
            self.scheduled_changes.mergeUpdate(orig_row, what, changed_by, trans)
        if ret.rowcount != 1:
            raise OutdatedDataError("Failed to update row, old_data_version doesn't match current data_version")
        return ret

    def update(self, where, what, changed_by=None, old_data_version=None, transaction=None):
        """Perform an UPDATE statement on this stable. See AUSTable._updateStatement for
           a description of `where' and `what'. This method can only update a single row
           per invocation. If the where clause given would update zero or multiple rows, a
           WrongNumberOfRowsError is raised.

           @param where: A list of SQLAlchemy clauses, or a key/value pair of columns and values.
           @type where: list of clauses or key/value pairs.
           @param changed_by: The username of the person inserting the row. Required when
                              history is enabled. Unused otherwise. No authorization checks are done
                              at this level.
           @type changed_by: str
           @param old_data_version: Previous version of the row to be deleted. If this version doesn't
                                    match the current version of the row, an OutdatedDataError will be
                                    raised and the delete will fail. Required when versioning is enabled.
           @type old_data_version: int

           @rtype: sqlalchemy.engine.base.ResultProxy
        """

        # If "where" is key/value pairs, we need to convert it to SQLAlchemy
        # clauses before porceeding.
        if hasattr(where, "keys"):
            where = [getattr(self, k) == v for k, v in where.iteritems()]

        if self.history and not changed_by:
            raise ValueError("changed_by must be passed for Tables that have history")
        if self.versioned and not old_data_version:
            raise ValueError("update: old_data_version must be passed for Tables that are versioned")

        if transaction:
            return self._prepareUpdate(transaction, where, what, changed_by, old_data_version)
        else:
            with AUSTransaction(self.getEngine()) as trans:
                return self._prepareUpdate(trans, where, what, changed_by, old_data_version)

    def getRecentChanges(self, limit=10, transaction=None):
        return self.history.select(transaction=transaction,
                                   limit=limit,
                                   order_by=self.history.timestamp.desc())


class History(AUSTable):
    """Represents a history table that may be attached to another AUSTable.
       History tables mirror the structure of their `baseTable', with the exception
       that nullable and primary_key attributes are always overwritten to be
       True and False respectively. Additionally, History tables have a unique
       change_id for each row, and record the username making a change, and the
       timestamp of each change. The methods forInsert, forDelete, and forUpdate
       will generate appropriate INSERTs to the History table given appropriate
       inputs, and are documented below. History tables are never versioned,
       and cannot have history of their own."""

    def __init__(self, db, dialect, metadata, baseTable):
        self.baseTable = baseTable
        self.table = Table('%s_history' % baseTable.t.name, metadata,
                           Column('change_id', Integer, primary_key=True, autoincrement=True),
                           Column('changed_by', String(100), nullable=False),
                           )
        # Timestamps are stored as an integer, but actually contain
        # precision down to the millisecond, achieved through
        # multiplication.
        # SQLAlchemy's SQLite dialect doesn't support fully support BigInteger.
        # The Column will work, but it ends up being a NullType Column which
        # breaks our upgrade unit tests. Because of this, we make sure to use
        # a plain Integer column for SQLite. In MySQL, an Integer is
        # Integer(11), which is too small for our needs.
        if dialect == 'sqlite':
            self.table.append_column(Column('timestamp', Integer, nullable=False))
        else:
            self.table.append_column(Column('timestamp', BigInteger, nullable=False))
        self.base_primary_key = [pk.name for pk in baseTable.primary_key]
        for col in baseTable.t.get_children():
            newcol = col.copy()
            if col.primary_key:
                newcol.primary_key = False
            else:
                newcol.nullable = True
            self.table.append_column(newcol)
        AUSTable.__init__(self, db, dialect, history=False, versioned=False)

    def forInsert(self, insertedKeys, columns, changed_by):
        """Inserts cause two rows in the History table to be created. The first
           one records the primary key data and NULLs for other row data. This
           represents that the row did not exist prior to the insert. The
           timestamp for this row is 1 millisecond behind the real timestamp to
           reflect this. The second row records the full data of the row at the
           time of insert."""
        primary_key_data = {}
        queries = []
        for i in range(0, len(self.base_primary_key)):
            name = self.base_primary_key[i]
            primary_key_data[name] = insertedKeys[i]
            # Make sure the primary keys are included in the second row as well
            columns[name] = insertedKeys[i]

        ts = getMillisecondTimestamp()
        queries.append(self._insertStatement(changed_by=changed_by, timestamp=ts - 1, **primary_key_data))
        queries.append(self._insertStatement(changed_by=changed_by, timestamp=ts, **columns))
        return queries

    def forDelete(self, rowData, changed_by):
        """Deletes cause a single row to be created, which only contains the
           primary key data. This represents that the row no longer exists."""
        row = {}
        for k in rowData:
            row[str(k)] = rowData[k]
        # Tack on history table information to the row
        row['changed_by'] = changed_by
        row['timestamp'] = getMillisecondTimestamp()
        return self._insertStatement(**row)

    def forUpdate(self, rowData, changed_by):
        """Updates cause a single row to be created, which contains the full,
           new data of the row at the time of the update."""
        row = {}
        for k in rowData:
            row[str(k)] = rowData[k]
        row['changed_by'] = changed_by
        row['timestamp'] = getMillisecondTimestamp()
        return self._insertStatement(**row)

    def getChange(self, change_id=None, column_values=None, data_version=None, transaction=None):
        """ Returns the unique change that matches the give change_id or
            combination of data_version and values for the specified columns.
            column_values is a dict that contains the column names that are
            versioned and their values.
            Ignores non primary key attributes specified in column_values."""
        # if change_id is not None, we use it to get the change, ignoring
        # data_version and column_values
        by_change_id = False if change_id is None else True
        # column_names lists all primary keys as string keys with the column
        # objects as values
        column_names = {col.name: col for col in self.table.columns if col.name in self.base_primary_key}

        if not by_change_id:
            # we check if the entire primary key is present in column_values,
            # since there might be multiple rows that match an incomplete
            # primary key
            for col in column_names.keys():
                if col not in column_values.keys():
                    raise ValueError("Entire primary key not present")
            # data_version can only be queried for versioned tables
            if not self.baseTable.versioned:
                raise ValueError("data_version queried for non-versioned table")

            where = [self.data_version == data_version]
            for col in column_names.keys():
                where.append(column_names[col] == column_values[col])
            changes = self.select(where=where,
                                  transaction=transaction)
        else:
            changes = self.select(where=[self.change_id == change_id], transaction=transaction)
        found = len(changes)
        if found > 1 or found == 0:
            self.log.debug("Found %s changes, should have been 1", found)
            return None
        return changes[0]

    def getPrevChange(self, change_id, row_primary_keys, transaction=None):
        """ Returns the most recent change to a given row in the base table """
        where = [self.change_id < change_id]
        for i in range(0, len(self.base_primary_key)):
            self_prim = getattr(self, self.base_primary_key[i])
            where.append((self_prim == row_primary_keys[i]))

        changes = self.select(where=where, transaction=transaction, limit=1, order_by=self.change_id.desc())
        length = len(changes)
        if(length == 0):
            self.log.debug("No previous changes found")
            return None
        return changes[0]

    def _stripNullColumns(self, change):
        # We know a bunch of columns are going to be empty...easier to strip them out
        # than to be super verbose (also should let this test continue to work even
        # if the schema changes).
        for key in change.keys():
            if change[key] is None:
                del change[key]
        return change

    def _stripHistoryColumns(self, change):
        """ Will strip history specific columns as well as data_version from the given change """
        del change['change_id']
        del change['changed_by']
        del change['timestamp']
        del change['data_version']
        return change

    def _isNull(self, change, row_primary_keys):
        # Define a row that's empty except for the primary keys
        # This is what the NULL rows for inserts and deletes will look like.
        null_row = dict()
        for i in range(0, len(self.base_primary_key)):
            null_row[self.base_primary_key[i]] = row_primary_keys[i]
        return self._stripNullColumns(change) == null_row

    def _isDelete(self, cur_base_state, row_primary_keys):
        return self._isNull(cur_base_state.copy(), row_primary_keys)

    def _isInsert(self, prev_base_state, row_primary_keys):
        return self._isNull(prev_base_state.copy(), row_primary_keys)

    def _isUpdate(self, cur_base_state, prev_base_state, row_primary_keys):
        return (not self._isNull(cur_base_state.copy(), row_primary_keys)) and (not self._isNull(prev_base_state.copy(), row_primary_keys))

    def rollbackChange(self, change_id, changed_by, transaction=None):
        """ Rollback the change given by the change_id,
        Will handle all cases: insert, delete, update """

        change = self.getChange(change_id=change_id, transaction=transaction)

        # Get the values of the primary keys for the given row
        row_primary_keys = [0] * len(self.base_primary_key)
        for i in range(0, len(self.base_primary_key)):
            row_primary_keys[i] = change[self.base_primary_key[i]]

        # Strip the History Specific Columns from the cahgnes
        prev_base_state = self._stripHistoryColumns(self.getPrevChange(change_id, row_primary_keys, transaction))
        cur_base_state = self._stripHistoryColumns(change.copy())

        # Define a row that's empty except for the primary keys
        # This is what the NULL rows for inserts and deletes will look like.
        null_row = dict()
        for i in range(0, len(self.base_primary_key)):
            null_row[self.base_primary_key[i]] = row_primary_keys[i]

        # If the row has all NULLS, then the operation we're rolling back is a DELETE
        # We need to do an insert, with the data from the previous change
        if self._isDelete(cur_base_state, row_primary_keys):
            self.log.debug("reverting a DELETE")
            self.baseTable.insert(changed_by=changed_by, transaction=transaction, **prev_base_state)

        # If the previous change is NULL, then the operation is an INSERT
        # We will need to do a delete.
        elif self._isInsert(prev_base_state, row_primary_keys):
            self.log.debug("reverting an INSERT")
            where = []
            for i in range(0, len(self.base_primary_key)):
                self_prim = getattr(self.baseTable, self.base_primary_key[i])
                where.append((self_prim == row_primary_keys[i]))

            self.baseTable.delete(changed_by=changed_by, transaction=transaction, where=where, old_data_version=change['data_version'])

        elif self._isUpdate(cur_base_state, prev_base_state, row_primary_keys):
            # If this operation is an UPDATE
            # We will need to do an update to the previous change's state
            self.log.debug("reverting an UPDATE")
            where = []
            for i in range(0, len(self.base_primary_key)):
                self_prim = getattr(self.baseTable, self.base_primary_key[i])
                where.append((self_prim == row_primary_keys[i]))

            what = prev_base_state
            old_data_version = change['data_version']
            self.baseTable.update(changed_by=changed_by, where=where, what=what, old_data_version=old_data_version, transaction=transaction)
        else:
            self.log.debug("ERROR, change doesn't correspond to any known operation")


class ScheduledChangeTable(AUSTable):
    """A Table that stores the necessary information to schedule changes
    to the baseTable provided. A ScheduledChangeTable ends up mirroring the
    columns of its base, and adding the necessary ones to provide the schedule.
    By default, ScheduledChangeTables enable History on themselves."""

    # Scheduled changes may only have a single type of condition, but some
    # conditions require mulitple arguments. This data structure defines
    # each type of condition, and groups their args together for easier
    # processing.
    condition_groups = (
        ("when",),
        ("telemetry_product", "telemetry_channel", "telemetry_uptake"),
    )

    def __init__(self, db, dialect, metadata, baseTable, history=True):
        self.baseTable = baseTable
        self.table = Table("%s_scheduled_changes" % baseTable.t.name, metadata,
                           Column("sc_id", Integer, primary_key=True, autoincrement=True),
                           Column("scheduled_by", String(100), nullable=False),
                           Column("complete", Boolean, default=False),
                           Column("telemetry_product", String(15)),
                           Column("telemetry_channel", String(75)),
                           Column("telemetry_uptake", Integer),
                           )
        if dialect == "sqlite":
            self.table.append_column(Column("when", Integer))
        else:
            self.table.append_column(Column("when", BigInteger))

        # The primary key column(s) are used in construct "where" clauses for
        # existing rows.
        self.base_primary_key = []
        # A ScheduledChangesTable requires all of the columns from its base
        # table, with a few tweaks:
        for col in baseTable.t.get_children():
            if col.primary_key:
                self.base_primary_key.append(col.name)
            newcol = col.copy()
            # 1) Columns are prefixed with "base_", to make them easy to
            # identify and avoid conflicts.
            # Renaming a column requires to change both the key and the name
            # See https://github.com/zzzeek/sqlalchemy/blob/rel_0_7/lib/sqlalchemy/schema.py#L781
            # for background.
            newcol.key = newcol.name = "base_%s" % col.name
            # 2) Primary keys on the base table are normal columns here,
            # and are allowed to be null (because we support adding new rows
            # to tables with autoincrementing keys via scheduled changes).
            # The base table's data version may also be null for the same reason.
            if col.primary_key or newcol.name == "base_data_version":
                newcol.primary_key = False
                newcol.nullable = True
            # Notable because of its abscence, other columns retain their
            # nullability because whether or not we're adding a new row or
            # modifying an existing one, those NOT NULL columns are required.
            self.table.append_column(newcol)

        super(ScheduledChangeTable, self).__init__(db, dialect, history=history, versioned=True)

    def _prefixColumns(self, columns):
        """Helper function which takes key/value pairs of columns for this
        scheduled changes table - which could contain some unprefixed base
        table columns - and returns key/values pairs of the same columns
        with the base table ones prefixed."""
        ret = {}
        base_columns = [c.name for c in self.baseTable.t.get_children()]
        for k, v in columns.iteritems():
            if k in base_columns:
                ret["base_%s" % k] = v
            else:
                ret[k] = v
        return ret

    def _validateConditions(self, conditions):
        # Filter out conditions whose values are none before processing.
        conditions = {k: v for k, v in conditions.iteritems() if conditions[k]}
        if not conditions:
            raise ValueError("No conditions found")

        for c in conditions:
            if c not in itertools.chain(*self.condition_groups):
                raise ValueError("Invalid condition: %s", c)

        for group in self.condition_groups:
            if set(group) == set(conditions.keys()):
                break
        else:
            raise ValueError("Invalid combination of conditions: %s", conditions.keys())

        if "when" in conditions:
            try:
                time.gmtime(conditions["when"] / 1000)
            except:
                raise ValueError("Cannot parse 'when' as a unix timestamp.")

            if conditions["when"] < getMillisecondTimestamp():
                raise ValueError("Cannot schedule changes in the past")

    def insert(self, changed_by, transaction=None, dryrun=False, **columns):
        # We need to do additional checks for any changes that are modifying an
        # existing row. These lists will have PK clauses in them at the end of
        # the following loop, but only if the change contains a PK. This makes
        # it easy to do the extra checks conditionally afterwards.
        base_table_where = []
        sc_table_where = []
        for pk in self.base_primary_key:
            base_column = getattr(self.baseTable, pk)
            if pk in columns:
                sc_table_where.append(getattr(self, "base_%s" % pk) == columns[pk])
                # If a non-null data_version was provided it implies that the
                # base table row should already exist. This will be checked for
                # after we finish basic checks on the individual parts of the
                # PK.
                if "data_version" in columns and columns["data_version"]:
                    base_table_where.append(getattr(self.baseTable, pk) == columns[pk])
            # Non-Integer columns can have autoincrement set to True for some reason.
            # Any non-integer columns in the primary key are always required (because
            # autoincrement actually isn't a thing for them), and any Integer columns
            # that _aren't_ autoincrement are required as well.
            elif not isinstance(base_column.type, (sqlalchemy.types.Integer,)) or not base_column.autoincrement:
                raise ValueError("Missing primary key column '%s' which is not autoincrement", pk)

        # If anything ended up in base_table_where, it means that the baseTable
        # row should already exist. In these cases, we need to check to make sure
        # that the scheduled change has the same data version as the base table,
        # to ensure that a change is not being scheduled from an out of date version
        # of the base table row.
        if base_table_where:
            current_data_version = self.baseTable.select(columns=(self.baseTable.data_version,), where=base_table_where, transaction=transaction)

            if not current_data_version:
                raise ValueError("Cannot create scheduled change with data_version for non-existent row")

            if current_data_version and current_data_version[0]["data_version"] != columns.get("data_version"):
                raise OutdatedDataError("Wrong data_version given for base table, cannot create scheduled change.")

        # If the change has a PK in it, we must ensure that no existing change
        # with that PK is active before allowing it.
        if sc_table_where:
            sc_table_where.append(self.complete == False) # noqa because we need to use == for sqlalchemy operator overloading to work
            if len(self.select(columns=[self.sc_id], where=sc_table_where)) > 0:
                raise ChangeScheduledError("Cannot scheduled a change for a row with one already scheduled")

        what = self._prefixColumns(columns)
        conditions = {}
        for col in what:
            if not col.startswith("base_"):
                conditions[col] = what[col]

        self._validateConditions(conditions)

        # Use the appropriate base table methods in dry run mode to ensure the
        # user has permission for the change they want to schedule
        if columns.get("data_version"):
            self.baseTable.update(base_table_where, columns, changed_by, columns["data_version"], transaction=transaction, dryrun=True)
        else:
            self.baseTable.insert(changed_by, transaction=transaction, dryrun=True, **columns)

        if not dryrun:
            what["scheduled_by"] = changed_by
            ret = super(ScheduledChangeTable, self).insert(changed_by=changed_by, transaction=transaction, **what)
            return ret.inserted_primary_key[0]

    def update(self, where, what, changed_by, old_data_version, transaction=None, dryrun=False):
        # We need to check each Scheduled Change that would be affected by this
        # to ensure the new row will be valid.
        for row in self.select(where=where, transaction=transaction):
            new_row = row.copy()
            new_row.update(self._prefixColumns(what))
            base_table_where = {pk: new_row["base_%s" % pk] for pk in self.base_primary_key}
            if new_row.get("base_data_version"):
                self.baseTable.update(base_table_where, new_row, changed_by, new_row["base_data_version"], transaction=transaction, dryrun=True)
            else:
                self.baseTable.insert(changed_by, transaction=transaction, dryrun=True, **new_row)

            conditions = {}
            for cond in itertools.chain(*self.condition_groups):
                if cond in new_row:
                    conditions[cond] = new_row[cond]
                elif row.get(cond):
                    conditions[cond] = row[cond]

            self._validateConditions(conditions)

        if not dryrun:
            renamed_what = self._prefixColumns(what)
            renamed_what["scheduled_by"] = changed_by
            return super(ScheduledChangeTable, self).update(where, renamed_what, changed_by, old_data_version, transaction)

    def delete(self, where, changed_by=None, old_data_version=None, transaction=None, dryrun=False):
        for row in self.select(where=where, transaction=transaction):
            base_row = {col[5:]: row[col] for col in row if col.startswith("base_")}
            base_table_where = {pk: row["base_%s" % pk] for pk in self.base_primary_key}
            # TODO: What permissions *should* be required to delete a scheduled change?
            # It seems a bit odd to be checking base table update/insert here. Maybe
            # something broader should be required?
            if base_row.get("base_data_version"):
                self.baseTable.update(base_table_where, base_row, changed_by, base_row["base_data_version"], transaction=transaction, dryrun=True)
            else:
                self.baseTable.insert(changed_by, transaction=transaction, dryrun=True, **base_row)

        if not dryrun:
            return super(ScheduledChangeTable, self).delete(where, changed_by, old_data_version, transaction)

    def enactChange(self, sc_id, enacted_by, transaction=None):
        """Enacts a previously scheduled change by running update or insert on
        the base table."""
        if not self.db.hasPermission(enacted_by, "scheduled_change", "enact", transaction=transaction):
            raise PermissionDeniedError("%s is not allowed to enact scheduled changes", enacted_by)

        sc = self.select(where=[self.sc_id == sc_id], transaction=transaction)[0]
        what = {}
        for col in sc:
            if col.startswith("base_"):
                what[col[5:]] = sc[col]

        # The scheduled change is marked as complete first to avoid it being
        # updated unnecessarily when the base table's update method calls
        # mergeUpdate. If the base table update fails, this will get reverted
        # when the transaction is rolled back.
        # We explicitly avoid using ScheduledChangeTable's update() method here
        # because we don't want to trigger its validation of conditions. Doing so
        # would raise any exception for any timestamp based changes, because
        # they are already in the past when we're ready to enact them.
        super(ScheduledChangeTable, self).update(
            where=[self.sc_id == sc_id], what={"complete": True}, changed_by=sc["scheduled_by"], old_data_version=sc["data_version"],
            transaction=transaction
        )

        # If the scheduled change had a data version, it means the row already
        # exists, and we need to use update() to enact it.
        if what["data_version"]:
            where = []
            for col in self.base_primary_key:
                where.append((getattr(self.baseTable, col) == sc["base_%s" % col]))
            self.baseTable.update(where, what, sc["scheduled_by"], sc["base_data_version"], transaction=transaction)
        else:
            self.baseTable.insert(sc["scheduled_by"], transaction=transaction, **what)

    def mergeUpdate(self, old_row, what, changed_by, transaction=None):
        """Merges an update to the base table into any changes that may be
        scheduled for the affected row. If the changes are unmergable
        (meaning: the scheduled change and the new version of the row modify
        the same columns), an UpdateMergeError is raised."""

        # pyflakes thinks this should be "is False", but that's not how SQLAlchemy
        # works, so we need to shut it up.
        # http://stackoverflow.com/questions/18998010/flake8-complains-on-boolean-comparison-in-filter-clause
        where = [self.complete == False]  # noqa
        for col in self.base_primary_key:
            where.append((getattr(self, "base_%s" % col) == old_row[col]))

        scheduled_changes = self.select(where=where, transaction=transaction)
        if not scheduled_changes:
            self.log.debug("No scheduled changes found for update; nothing to do")
            return
        for sc in scheduled_changes:
            self.log.debug("Trying to merge update with scheduled change '%s'", sc["sc_id"])

            for col in what:
                # If the scheduled change is different than the old row it will
                # be modifying the row when enacted. If the update to the row
                # ("what") is also modifying the same column, this is a conflict
                # that the server cannot resolve.
                if sc["base_%s" % col] != old_row.get(col) and sc["base_%s" % col] != what.get(col):
                    raise UpdateMergeError("Cannot safely merge change to '%s' with scheduled change '%s'", col, sc["sc_id"])

            # If we get here, the change is safely mergeable
            self.update(where=[self.sc_id == sc["sc_id"]], what=what, changed_by=changed_by, old_data_version=sc["data_version"], transaction=transaction)
            self.log.debug("Merged %s into scheduled change '%s'", what, sc["sc_id"])


class Rules(AUSTable):

    def __init__(self, db, metadata, dialect):
        self.table = Table('rules', metadata,
                           Column('rule_id', Integer, primary_key=True, autoincrement=True),
                           Column('alias', String(50), unique=True),
                           Column('priority', Integer),
                           Column('mapping', String(100)),
                           Column('backgroundRate', Integer),
                           Column('update_type', String(15), nullable=False),
                           Column('product', String(15)),
                           Column('version', String(10)),
                           Column('channel', String(75)),
                           Column('buildTarget', String(75)),
                           Column('buildID', String(20)),
                           Column('locale', String(200)),
                           Column('osVersion', String(1000)),
                           Column('systemCapabilities', String(1000)),
                           Column('distribution', String(100)),
                           Column('distVersion', String(100)),
                           Column('headerArchitecture', String(10)),
                           Column('comment', String(500)),
                           Column('whitelist', String(100)),
                           )
        AUSTable.__init__(self, db, dialect, scheduled_changes=True)

    def _matchesRegex(self, foo, bar):
        # Expand wildcards and use ^/$ to make sure we don't succeed on partial
        # matches. Eg, 3.6* matches 3.6, 3.6.1, 3.6b3, etc.
        test = foo.replace('.', '\.').replace('*', '.*')
        test = '^%s$' % test
        if re.match(test, bar):
            return True
        return False

    def _channelMatchesRule(self, ruleChannel, queryChannel, fallbackChannel):
        """Decides whether a channel from the rules matches an incoming one.
           If the ruleChannel is null, we match any queryChannel. We also match
           if the channels match exactly, or match after wildcards in ruleChannel
           are resolved. Channels may have a fallback specified, too, so we must
           check if the fallback version of the queryChannel matches the ruleChannel."""
        if ruleChannel is None:
            return True
        if self._matchesRegex(ruleChannel, queryChannel):
            return True
        if self._matchesRegex(ruleChannel, fallbackChannel):
            return True

    def _matchesList(self, ruleString, queryString):
        """Decides whether a ruleString from a rule matches an incoming string.
           The rule may specify multiple matches, delimited by a comma. Once
           split we look for an exact match against the string from the queries.
           We want an exact match so (eg) we only get the locales we specify"""
        if ruleString is None:
            return True
        for subString in ruleString.split(','):
            if subString == queryString:
                return True

    def _versionMatchesRule(self, ruleVersion, queryVersion):
        """Decides whether a version from the rules matches an incoming version.
           If the ruleVersion is null, we match any queryVersion. If it's not
           null, we must either match exactly, or match a comparison operator."""
        self.log.debug('ruleVersion: %s, queryVersion: %s', ruleVersion, queryVersion)
        if ruleVersion is None:
            return True
        return version_compare(queryVersion, ruleVersion)

    def _buildIDMatchesRule(self, ruleBuildID, queryBuildID):
        """Decides whether a buildID from the rules matches an incoming one.
           If the ruleBuildID is null, we match any queryBuildID. If it's not
           null, we must either match exactly, or match with a camparison
           operator."""
        if ruleBuildID is None:
            return True
        return string_compare(queryBuildID, ruleBuildID)

    def _csvMatchesRule(self, ruleString, queryString, substring=True):
        """Decides whether a column from a rule matches an incoming one.
           Some columns in a rule may specify multiple values delimited by a
           comma. Once split we do a full or substring match against the query
           string. Because we support substring matches, there's no need
           to support globbing as well."""
        if ruleString is None:
            return True
        for part in ruleString.split(','):
            if substring and part in queryString:
                return True
            elif part == queryString:
                return True
        return False

    def _localeMatchesRule(self, ruleLocales, queryLocale):
        """Decides if a comma seperated list of locales in a rule matches an
        update request"""
        return self._matchesList(ruleLocales, queryLocale)

    def _isAlias(self, id_or_alias):
        if re.match("^[a-zA-Z][a-zA-Z0-9-]*$", str(id_or_alias)):
            return True
        return False

    def insert(self, changed_by, transaction=None, dryrun=False, **columns):
        if not self.db.hasPermission(changed_by, "rule", "create", columns.get("product"), transaction):
            raise PermissionDeniedError("%s is not allowed to create new rules for product %s" % (changed_by, columns.get("product")))
        if not dryrun:
            ret = super(Rules, self).insert(changed_by=changed_by, transaction=transaction, **columns)
            return ret.inserted_primary_key[0]

    def getOrderedRules(self, transaction=None):
        """Returns all of the rules, sorted in ascending order"""
        return self.select(order_by=(self.priority, self.version, self.mapping), transaction=transaction)

    def countRules(self, transaction=None):
        """Returns a number of the count of rules"""
        count, = self.t.count().execute().fetchone()
        return count

    def getRulesMatchingQuery(self, updateQuery, fallbackChannel, transaction=None):
        """Returns all of the rules that match the given update query.
           For cases where a particular updateQuery channel has no
           fallback, fallbackChannel should match the channel from the query."""

        def getRawMatches():
            where = [
                ((self.product == updateQuery['product']) | (self.product == null())) &
                ((self.buildTarget == updateQuery['buildTarget']) | (self.buildTarget == null())) &
                ((self.headerArchitecture == updateQuery['headerArchitecture']) | (self.headerArchitecture == null()))
            ]
            # Query version 2 doesn't have distribution information, and to keep
            # us maximally flexible, we won't match any rules that have
            # distribution update set.
            if updateQuery['queryVersion'] == 2:
                where.extend([(self.distribution == null()) & (self.distVersion == null())])
            # Only query versions 3 and 4 have distribution information, so we
            # need to consider it.
            if updateQuery['queryVersion'] in (3, 4):
                where.extend([
                    ((self.distribution == updateQuery['distribution']) | (self.distribution == null())) &
                    ((self.distVersion == updateQuery['distVersion']) | (self.distVersion == null()))
                ])

            self.log.debug("where: %s" % where)
            return self.select(where=where, transaction=transaction)

        # This cache key is constructed from all parts of the updateQuery that
        # are used in the select() to get the "raw" rule matches. For the most
        # part, product and buildTarget will be the only applicable ones which
        # means we should get very high cache hit rates, as there's not a ton
        # of variability of possible combinations for those.
        cache_key = "%s:%s:%s:%s:%s:%s" % \
            (updateQuery["product"], updateQuery["buildTarget"], updateQuery["headerArchitecture"],
             updateQuery.get("distribution"), updateQuery.get("distVersion"), updateQuery["force"])
        rules = cache.get("rules", cache_key, getRawMatches)

        self.log.debug("Raw matches:")

        matchingRules = []
        for rule in rules:
            self.log.debug(rule)

            # Resolve special means for channel, version, and buildID - dropping
            # rules that don't match after resolution.
            if not self._channelMatchesRule(rule['channel'], updateQuery['channel'], fallbackChannel):
                self.log.debug("%s doesn't match %s", rule['channel'], updateQuery['channel'])
                continue
            if not self._versionMatchesRule(rule['version'], updateQuery['version']):
                self.log.debug("%s doesn't match %s", rule['version'], updateQuery['version'])
                continue
            if not self._buildIDMatchesRule(rule['buildID'], updateQuery['buildID']):
                self.log.debug("%s doesn't match %s", rule['buildID'], updateQuery['buildID'])
                continue
            # To help keep the rules table compact, multiple OS versions may be
            # specified in a single rule. They are comma delimited, so we need to
            # break them out and create clauses for each one.
            if not self._csvMatchesRule(rule['osVersion'], updateQuery['osVersion']):
                self.log.debug("%s doesn't match %s", rule['osVersion'], updateQuery['osVersion'])
                continue
            # Same deal for system capabilities
            if not self._csvMatchesRule(rule['systemCapabilities'], updateQuery.get('systemCapabilities', ""), substring=False):
                self.log.debug("%s doesn't match %s", rule['systemCapabilities'], updateQuery.get('systemCapabilities'))
                continue
            # Locales may be a comma delimited rule too, exact matches only
            if not self._localeMatchesRule(rule['locale'], updateQuery['locale']):
                self.log.debug("%s doesn't match %s", rule['locale'], updateQuery['locale'])
                continue
            # If a rule has a whitelist attached to it, the rule is only
            # considered "matching" if it passes the whitelist check.
            # The decision about matching or not is delegated to the whitelist blob.
            if rule.get("whitelist"):
                self.log.debug("Matching rule requires a whitelist")
                try:
                    whitelist = dbo.releases.getReleaseBlob(name=rule["whitelist"], transaction=transaction)
                    if whitelist and not whitelist.shouldServeUpdate(updateQuery):
                        continue
                # It shouldn't be possible for the whitelist blob not to exist,
                # but just in case...
                except KeyError:
                    self.log.warning("Got exeception when looking for whitelist blob %s", rule["whitelist"], exc_info=True)

            matchingRules.append(rule)

        self.log.debug("Reduced matches:")
        if self.log.isEnabledFor(logging.DEBUG):
            for r in matchingRules:
                self.log.debug(r)
        return matchingRules

    def getRule(self, id_or_alias, transaction=None):
        """ Returns the unique rule that matches the give rule_id or alias."""
        where = []
        # Figuring out which column to use ahead of times means there's only
        # one potential index for the database to use, which should make
        # queries faster (it will always use the most efficient one).
        if self._isAlias(id_or_alias):
            where.append(self.alias == id_or_alias)
        else:
            where.append(self.rule_id == id_or_alias)

        rules = self.select(where=where, transaction=transaction)
        found = len(rules)
        if found > 1 or found == 0:
            self.log.debug("Found %s rules, should have been 1", found)
            return None
        return rules[0]

    def update(self, where, what, changed_by, old_data_version, transaction=None, dryrun=False):
        # Rather than forcing callers to figure out whether the identifier
        # they have is an id or an alias, we handle it here.
        if "rule_id" in where and self._isAlias(where["rule_id"]):
            where["alias"] = where["rule_id"]
            del where["rule_id"]

        # If the product is being changed, we also need to make sure the user
        # permission to modify _that_ product.
        if "product" in what:
            if not self.db.hasPermission(changed_by, "rule", "modify", what["product"], transaction):
                raise PermissionDeniedError("%s is not allowed to modify rules for product %s" % (changed_by, what["product"]))

        for current_rule in self.select(where=where, columns=[self.product], transaction=transaction):
            if not self.db.hasPermission(changed_by, "rule", "modify", current_rule["product"], transaction):
                raise PermissionDeniedError("%s is not allowed to modify rules for product %s" % (changed_by, current_rule["product"]))

        if not dryrun:
            return super(Rules, self).update(changed_by=changed_by, where=where, what=what, old_data_version=old_data_version, transaction=transaction)

    def delete(self, where, changed_by=None, old_data_version=None, transaction=None, dryrun=False):
        if "rule_id" in where and self._isAlias(where["rule_id"]):
            where["alias"] = where["rule_id"]
            del where["rule_id"]

        product = self.select(where=where, columns=[self.product], transaction=transaction)[0]["product"]
        if not self.db.hasPermission(changed_by, "rule", "delete", product, transaction):
            raise PermissionDeniedError("%s is not allowed to delete rules for product %s" % (changed_by, product))

        if not dryrun:
            super(Rules, self).delete(changed_by=changed_by, where=where, old_data_version=old_data_version, transaction=transaction)


class Releases(AUSTable):

    def __init__(self, db, metadata, dialect):
        self.domainWhitelist = []

        self.table = Table('releases', metadata,
                           Column('name', String(100), primary_key=True),
                           Column('product', String(15), nullable=False),
                           Column('read_only', Boolean, default=False),
                           )
        if dialect == 'mysql':
            from sqlalchemy.dialects.mysql import LONGTEXT
            dataType = LONGTEXT
        else:
            dataType = Text
        self.table.append_column(Column('data', dataType, nullable=False))
        AUSTable.__init__(self, db, dialect)

    def setDomainWhitelist(self, domainWhitelist):
        self.domainWhitelist = domainWhitelist

    def getReleases(self, name=None, product=None, limit=None, transaction=None):
        self.log.debug("Looking for releases with:")
        self.log.debug("name: %s", name)
        self.log.debug("product: %s", product)
        where = []
        if name:
            where.append(self.name == name)
        if product:
            where.append(self.product == product)
        # We could get the "data" column here too, but getReleaseBlob knows how
        # to grab cached versions of that, so it's better to let it take care
        # of it.
        rows = self.select(columns=[self.name, self.product, self.data_version],
                           where=where, limit=limit, transaction=transaction)
        for row in rows:
            row["data"] = self.getReleaseBlob(row["name"], transaction)
        return rows

    def countReleases(self, transaction=None):
        """Returns a number of the count of releases"""
        count, = self.t.count().execute().fetchone()
        return count

    def getReleaseInfo(self, product=None, limit=None,
                       transaction=None, nameOnly=False, name_prefix=None):
        where = []
        if product:
            where.append(self.product == product)
        if name_prefix:
            where.append(self.name.startswith(name_prefix))
        if nameOnly:
            column = [self.name]
        else:
            column = [self.name, self.product, self.data_version, self.read_only]

        rows = self.select(where=where, columns=column, limit=limit, transaction=transaction)

        if not nameOnly:
            j = join(dbo.releases.t, dbo.rules.t, ((dbo.releases.name == dbo.rules.mapping) | (dbo.releases.name == dbo.rules.whitelist)))
            ref_list = select([dbo.releases.name, dbo.rules.rule_id]).select_from(j).execute().fetchall()

            for row in rows:
                refs = [ref for ref in ref_list if ref[0] == row['name']]
                ref_list = [ref for ref in ref_list if ref[0] != row['name']]
                if len(refs) > 0:
                    row['rule_ids'] = [ref[1] for ref in refs]
                else:
                    row['rule_ids'] = []

        return rows

    def getReleaseNames(self, **kwargs):
        return self.getReleaseInfo(nameOnly=True, **kwargs)

    def getReleaseBlob(self, name, transaction=None):
        # Putting the data_version and blob getters into these methods lets us
        # delegate the decision about whether or not to use the cached values
        # to the cache class. It will either return as a cached value, or use
        # the getter to return a fresh value (and cache it).
        def getDataVersion():
            try:
                return self.select(where=[self.name == name], columns=[self.data_version], limit=1, transaction=transaction)[0]
            except IndexError:
                raise KeyError("Couldn't find release with name '%s'" % name)

        data_version = cache.get("blob_version", name, getDataVersion)

        def getBlob():
            try:
                row = self.select(where=[self.name == name], columns=[self.data], limit=1, transaction=transaction)[0]
                blob = createBlob(row['data'])
                return {"data_version": data_version, "blob": blob}
            except IndexError:
                raise KeyError("Couldn't find release with name '%s'" % name)

        cached_blob = cache.get("blob", name, getBlob)

        # Even though we may have retrieved a cached blob, we need to make sure
        # that it's not older than the one in the database. If the data version
        # of the cached blob and the latest data version don't match, we need
        # to update the cache with the latest blob.
        if data_version > cached_blob["data_version"]:
            blob_info = getBlob()
            cache.put("blob", name, blob_info)
            blob = blob_info["blob"]
        else:
            # And while it's extremely unlikely, there is a remote possibility
            # that the cached blob actually has a newer data version than the
            # blob version cache. This can occur if the blob cache expired
            # between retrieving the cached data version and cached blob.
            # (Because the blob version cache ttl should be shorter than the
            # blob cache ttl, if the blob cache expired prior to retrieving the
            # data version, the blob version cache would've expired as well.
            # If we hit one of these cases, we should bring the blob version
            # cache up to date since we have it.
            if cached_blob["data_version"] > data_version:
                cache.put("blob_version", name, data_version)
            blob = cached_blob["blob"]

        return blob

    def insert(self, changed_by, transaction=None, dryrun=False, **columns):
        if "name" not in columns or "product" not in columns or "data" not in columns:
            raise ValueError("name, product, and data are all required")

        blob = columns["data"]

        if not self.db.hasPermission(changed_by, "release", "create", columns["product"], transaction):
            raise PermissionDeniedError("%s is not allowed to create releases for product %s" % (changed_by, columns["product"]))

        blob.validate(columns["product"], self.domainWhitelist)
        if columns["name"] != blob["name"]:
            raise ValueError("name in database (%s) does not match name in blob (%s)" % (columns["name"], blob["name"]))
        columns["data"] = blob.getJSON()

        if not dryrun:
            ret = super(Releases, self).insert(changed_by=changed_by, transaction=transaction, **columns)
            cache.put("blob", columns["name"], {"data_version": 1, "blob": blob})
            cache.put("blob_version", columns["name"], 1)
            return ret.inserted_primary_key[0]

    def update(self, where, what, changed_by, old_data_version, transaction=None, dryrun=False):
        blob = what.get("data")

        current_releases = self.select(where=where, columns=[self.name, self.product, self.read_only], transaction=transaction)
        for current_release in current_releases:
            name = current_release["name"]
            if "product" in what or "data" in what:
                self._proceedIfNotReadOnly(current_release["name"], transaction=transaction)

            if not self.db.hasPermission(changed_by, "release", "modify", current_release["product"], transaction):
                raise PermissionDeniedError("%s is not allowed to modify releases for product %s" % (changed_by, current_release["product"]))

            if "product" in what:
                # If the product is being changed, we need to make sure the user
                # has permission to modify releases of that product, too.
                if not self.db.hasPermission(changed_by, "release", "modify", what["product"], transaction):
                    raise PermissionDeniedError("%s is not allowed to modify releases for product %s" % (changed_by, what["product"]))

            # The way things stand right now we cannot grant access to _only_ modify
            # the read only flag. When the permissions were still enforced at the
            # web level we had this because that flag had its own endpoint.
            # If we want this again we'll need to adjust this code, and perhaps
            # make a special method on this class that only modifies read_only
            # (similar to addLocaleToRelease).
            if "read_only" in what:
                # In addition to being able to modify the release overall, users
                # need to be granted explicit access to manipulate the read_only
                # flag. This lets us give out very granular access, which can be
                # very helpful particularly in automation.
                if what["read_only"] is False:
                    if not self.db.hasPermission(changed_by, "release_read_only", "unset", what.get("product"), transaction):
                        raise PermissionDeniedError("%s is not allowed to mark %s products read write" % (changed_by, what.get("product")))
                elif what["read_only"] is True:
                    if not self.db.hasPermission(changed_by, "release_read_only", "set", what.get("product"), transaction):
                        raise PermissionDeniedError("%s is not allowed to mark %s products read only" % (changed_by, what.get("product")))

            if blob:
                blob.validate(what.get("product", current_release["product"]),
                              self.domainWhitelist)
                name = what.get("name", name)
                if name != blob["name"]:
                    raise ValueError("name in database (%s) does not match name in blob (%s)" % (name, blob.get("name")))
                what['data'] = blob.getJSON()
        if not dryrun:
            for release in current_releases:
                name = current_release["name"]
                new_data_version = old_data_version + 1
                try:
                    super(Releases, self).update(where={"name": name}, what=what, changed_by=changed_by, old_data_version=old_data_version,
                                                 transaction=transaction)
                except OutdatedDataError as e:
                    self.log.debug("trying to update older data_version %s for release %s" % (old_data_version, name))
                    if blob is not None:
                        ancestor_change = self.history.getChange(data_version=old_data_version,
                                                                 column_values={'name': name},
                                                                 transaction=transaction)
                        # if we have no historical information about the ancestor blob
                        if ancestor_change is None:
                            self.log.debug("history for data_version %s for release %s absent" % (old_data_version, name))
                            raise
                        ancestor_blob = createBlob(ancestor_change.get('data'))
                        tip_release = self.getReleases(name=name, transaction=transaction)[0]
                        tip_blob = tip_release.get('data')
                        m = dictdiffer.merge.Merger(ancestor_blob, tip_blob, blob, {})
                        try:
                            m.run()
                            # Merger merges the patches into a single unified patch,
                            # but we need dictdiffer.patch to actually apply the patch
                            # to the original blob
                            unified_blob = dictdiffer.patch(m.unified_patches, ancestor_blob)
                            # converting the resultant dict into a blob and then
                            # converting it to JSON
                            what['data'] = createBlob(unified_blob).getJSON()
                            # we want the data_version for the dictdiffer.merged blob to be one
                            # more than that of the latest blob
                            tip_data_version = tip_release['data_version']
                            super(Releases, self).update(where={"name": name}, what=what, changed_by=changed_by, old_data_version=tip_data_version,
                                                         transaction=transaction)
                            # cache will have a data_version of one plus the tip
                            # data_version
                            new_data_version = tip_data_version + 1
                        except dictdiffer.merge.UnresolvedConflictsException:
                            self.log.debug("latest version of release %s cannot be merged with new blob" % name)
                            raise e
                cache.put("blob", name, {"data_version": new_data_version, "blob": blob})
                cache.put("blob_version", name, new_data_version)

    def addLocaleToRelease(self, name, product, platform, locale, data, old_data_version, changed_by, transaction=None, alias=None):
        """Adds or update's the existing data for a specific platform + locale
           combination, in the release identified by 'name'. The data is
           validated before commiting it, and a ValueError is raised if it is
           invalid.
        """
        self._proceedIfNotReadOnly(name, transaction=transaction)

        where = [self.name == name]
        product = self.select(where=where, columns=[self.product], transaction=transaction)[0]["product"]
        if not self.db.hasPermission(changed_by, "release_locale", "modify", product, transaction):
            raise PermissionDeniedError("%s is not allowed to add builds for product %s" % (changed_by, product))

        releaseBlob = self.getReleaseBlob(name, transaction=transaction)
        if 'platforms' not in releaseBlob:
            releaseBlob['platforms'] = {}

        if platform in releaseBlob['platforms']:
            # If the platform we're given is aliased to another one, we need
            # to resolve that before doing any updating. If we don't, the data
            # will go into an aliased platform and be ignored!
            platform = releaseBlob.getResolvedPlatform(platform)

        if platform not in releaseBlob['platforms']:
            releaseBlob['platforms'][platform] = {}

        if 'locales' not in releaseBlob['platforms'][platform]:
            releaseBlob['platforms'][platform]['locales'] = {}

        releaseBlob['platforms'][platform]['locales'][locale] = data

        # we don't allow modification of existing platforms (aliased or not)
        if alias:
            for a in alias:
                if a not in releaseBlob['platforms']:
                    releaseBlob['platforms'][a] = {'alias': platform}

        releaseBlob.validate(product, self.domainWhitelist)
        what = dict(data=releaseBlob.getJSON())

        super(Releases, self).update(where=where, what=what, changed_by=changed_by, old_data_version=old_data_version,
                                     transaction=transaction)
        new_data_version = old_data_version + 1
        cache.put("blob", name, {"data_version": new_data_version, "blob": releaseBlob})
        cache.put("blob_version", name, new_data_version)

    def getLocale(self, name, platform, locale, transaction=None):
        try:
            blob = self.getReleaseBlob(name, transaction=transaction)
            return blob['platforms'][platform]['locales'][locale]
        except KeyError:
            raise KeyError("Couldn't find locale identified by: %s, %s, %s" % (name, platform, locale))

    def localeExists(self, name, platform, locale, transaction=None):
        try:
            self.getLocale(name, platform, locale, transaction)
            return True
        except KeyError:
            return False

    def delete(self, where, changed_by, old_data_version, transaction=None, dryrun=False):
        names = []
        for toDelete in self.select(where=where, columns=[self.name, self.product], transaction=transaction):
            names.append(toDelete["name"])
            self._proceedIfNotReadOnly(toDelete["name"], transaction=transaction)
            if not self.db.hasPermission(changed_by, "release", "delete", toDelete["product"], transaction):
                raise PermissionDeniedError("%s is not allowed to delete releases for product %s" % (changed_by, toDelete["product"]))

        if not dryrun:
            super(Releases, self).delete(where=where, changed_by=changed_by, old_data_version=old_data_version, transaction=transaction)
            for name in names:
                cache.invalidate("blob", name)
                cache.invalidate("blob_version", name)

    def isReadOnly(self, name, limit=None, transaction=None):
        where = [self.name == name]
        column = [self.read_only]
        row = self.select(where=where, columns=column, limit=limit, transaction=transaction)[0]
        return row['read_only']

    def _proceedIfNotReadOnly(self, name, limit=None, transaction=None):
        if self.isReadOnly(name, limit, transaction):
            raise ReadOnlyError("Release '%s' is read only" % name)


class Permissions(AUSTable):
    """allPermissions defines the structure and possible options for all
       available permissions. Permissions can be limited to specific types
       of actions. Eg: granting the "rule" permission with "actions" set to
       ["create"] allows rules to be created but not modified or deleted.
       Permissions that relate to rules or releases can be further limited
       by product. Eg: granting the "release" permission with "products" set
       to ["GMP"] allows the user to modify GMP releases, but not Firefox."""
    allPermissions = {
        "admin": ["products"],
        "release": ["actions", "products"],
        "release_locale": ["actions", "products"],
        "release_read_only": ["actions", "products"],
        "rule": ["actions", "products"],
        "permission": ["actions"],
        "scheduled_change": ["actions"],
    }

    def __init__(self, db, metadata, dialect):
        self.table = Table('permissions', metadata,
                           Column('permission', String(50), primary_key=True),
                           Column('username', String(100), primary_key=True),
                           Column('options', Text)
                           )
        AUSTable.__init__(self, db, dialect)

    def assertPermissionExists(self, permission):
        if permission not in self.allPermissions.keys():
            raise ValueError('Unknown permission "%s"' % permission)

    def assertOptionsExist(self, permission, options):
        for opt in options:
            if opt not in self.allPermissions[permission]:
                raise ValueError('Unknown option "%s" for permission "%s"' % (opt, permission))

    def getAllUsers(self, transaction=None):
        res = self.select(columns=[self.username], distinct=True, transaction=transaction)
        return [r['username'] for r in res]

    def getAllPermissions(self, transaction=None):
        ret = defaultdict(dict)
        for r in self.select(transaction=transaction):
            ret[r["username"]][r["permission"]] = r["options"]
        return ret

    def countAllUsers(self, transaction=None):
        res = self.select(columns=[self.username], distinct=True, transaction=transaction)
        return len(res)

    def insert(self, changed_by, transaction=None, dryrun=False, **columns):
        if "permission" not in columns or "username" not in columns:
            raise ValueError("permission and username are required")

        self.assertPermissionExists(columns["permission"])
        if columns.get("options"):
            self.assertOptionsExist(columns["permission"], columns["options"])
            columns["options"] = json.dumps(columns["options"])

        if not self.db.hasPermission(changed_by, "permission", "create", transaction=transaction):
            raise PermissionDeniedError("%s is not allowed to grant permissions" % changed_by)

        if not dryrun:
            self.log.debug("granting %s to %s with options %s", columns["permission"], columns["username"],
                           columns.get("options"))
            super(Permissions, self).insert(changed_by=changed_by, transaction=transaction, **columns)
            self.log.debug("successfully granted %s to %s with options %s", columns["permission"],
                           columns["username"], columns.get("options"))

    def update(self, where, what, changed_by, old_data_version, transaction=None, dryrun=False):
        if not self.db.hasPermission(changed_by, "permission", "modify", transaction=transaction):
            raise PermissionDeniedError("%s is not allowed to modify permissions" % changed_by)

        if "permission" in what:
            self.assertPermissionExists(what["permission"])

        for current_permission in self.select(where=where, transaction=transaction):
            if what.get("options"):
                self.assertOptionsExist(what.get("permission", current_permission["permission"]), what["options"])

        if what.get("options"):
            what["options"] = json.dumps(what["options"])
        else:
            what["options"] = None

        if not dryrun:
            super(Permissions, self).update(where=where, what=what, changed_by=changed_by, old_data_version=old_data_version, transaction=transaction)

    def delete(self, where, changed_by=None, old_data_version=None, transaction=None, dryrun=False):
        if not self.db.hasPermission(changed_by, "permission", "delete", transaction=transaction):
            raise PermissionDeniedError("%s is not allowed to revoke permissions", changed_by)

        if not dryrun:
            super(Permissions, self).delete(changed_by=changed_by, where=where, old_data_version=old_data_version, transaction=transaction)

    def getPermission(self, username, permission, transaction=None):
        try:
            row = self.select(where=[self.username == username, self.permission == permission], transaction=transaction)[0]
            if row['options']:
                row['options'] = json.loads(row['options'])
            return row
        except IndexError:
            return {}

    def getUserPermissions(self, username, transaction=None):
        rows = self.select(columns=[self.permission, self.options, self.data_version], where=[self.username == username], transaction=transaction)
        ret = dict()
        for row in rows:
            perm = row['permission']
            opt = row['options']
            ret[perm] = dict()
            ret[perm]['data_version'] = row['data_version']
            if opt:
                ret[perm]['options'] = json.loads(opt)
            else:
                ret[perm]['options'] = None
        return ret

    def getOptions(self, username, permission, transaction=None):
        ret = self.select(columns=[self.options], where=[self.username == username, self.permission == permission], transaction=transaction)
        if ret:
            if ret[0]['options']:
                return json.loads(ret[0]['options'])
            else:
                return {}
        else:
            raise ValueError('Permission "%s" doesn\'t exist' % permission)

    def hasPermission(self, username, thing, action, product=None, transaction=None):
        # Supporting product-wise admin permissions. If there are no options
        # with admin, we assume that the user has admin access over all
        # products.
        if self.select(where=[self.username == username, self.permission == 'admin'], transaction=transaction):
            options = self.getOptions(username, 'admin', transaction=transaction)
            if options.get("products") and product not in options["products"]:
                return False
            return True

        try:
            options = self.getOptions(username, thing, transaction=transaction)
        except ValueError:
            return False

        # If a user has a permission that doesn't explicitly limit the type of
        # actions they can perform, they are allowed to do any type of action.
        if options.get("actions") and action not in options["actions"]:
            return False
        # Similarly, permissions without products specified grant that
        # that permission without any limitation on the product.
        if options.get("products") and product not in options["products"]:
            return False

        return True


class Dockerflow(AUSTable):
    def __init__(self, db, metadata, dialect):
        self.table = Table('dockerflow', metadata, Column('watchdog', Integer))
        AUSTable.__init__(self, db, dialect, history=False, versioned=False)

    def getDockerflowEntry(self, transaction=None):
        return self.select(transaction=transaction)[0]

    def incrementWatchdogValue(self, changed_by, transaction=None, dryrun=False):
        try:
            value = self.getDockerflowEntry()
            where = [(self.watchdog == value['watchdog'])]
            value['watchdog'] += 1
        except IndexError:
            value = {'watchdog': 1}
            where = None

        if not dryrun:
            self._putWatchdogValue(changed_by=changed_by, value=value, where=where, transaction=transaction)

        return value['watchdog']

    def _putWatchdogValue(self, changed_by, value, where=None, transaction=None):
        if where is None:
            super(Dockerflow, self).insert(changed_by=changed_by, transaction=transaction, watchdog=value['watchdog'])
        else:
            super(Dockerflow, self).update(where=where, what=value, changed_by=changed_by, transaction=transaction)


class UTF8PrettyPrinter(pprint.PrettyPrinter):
    """Encodes strings as UTF-8 before printing to avoid ugly u'' style prints.
    Adapted from http://stackoverflow.com/questions/10883399/unable-to-encode-decode-pprint-output"""
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return pprint._safe_repr(object.encode('utf8'), context, maxlevels, level)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)


class UnquotedStr(str):
    def __repr__(self):
        return self.__str__()


def send_email(relayhost, port, username, password, to_addr, from_addr, table, subj,
               body):
    from email.mime.text import MIMEText
    from smtplib import SMTP

    msg = MIMEText("\n".join(body), "plain")
    msg["Subject"] = subj
    msg["from"] = from_addr

    try:
        conn = SMTP()
        conn.connect(relayhost, port)
        conn.ehlo()
        conn.starttls()
        conn.ehlo()
    except:
        table.log.exception("Failed to connect to SMTP server:")
        return
    try:
        if username and password:
            conn.login(username, password)
        conn.sendmail(from_addr, to_addr, msg.as_string())
    except:
        table.log.exception("Failed to send change notification:")
    finally:
        conn.quit()


def make_change_notifier(relayhost, port, username, password, to_addr, from_addr):
    def bleet(table, type_, changed_by, query):
        body = ["Changed by: %s" % changed_by]
        if type_ == "UPDATE":
            body.append("Row(s) to be updated as follows:")
            where = [c for c in query._whereclause.get_children()]
            for row in table.select(where=where):
                for k in row:
                    if query.parameters[k] != row[k]:
                        row[k] = UnquotedStr("%s ---> %s" % (repr(row[k]), repr(query.parameters[k])))
                    else:
                        row[k] = UnquotedStr("%s (unchanged)" % repr(row[k]))
                body.append(UTF8PrettyPrinter().pformat(row))
        elif type_ == "DELETE":
            body.append("Row(s) to be removed:")
            where = [c for c in query._whereclause.get_children()]
            for row in table.select(where=where):
                body.append(UTF8PrettyPrinter().pformat(row))
        elif type_ == "INSERT":
            body.append("Row to be inserted:")
            body.append(UTF8PrettyPrinter().pformat(query.parameters))

        subj = "%s to %s detected" % (type_, table.t.name)
        send_email(relayhost, port, username, password, to_addr, from_addr,
                   table, subj, body)
        table.log.debug("Sending change notification mail for %s to %s", table.t.name, to_addr)
    return bleet


def make_change_notifier_for_read_only(relayhost, port, username, password, to_addr, from_addr):
    def bleet(table, type_, changed_by, query):
        body = ["Changed by: %s" % changed_by]
        where = [c for c in query._whereclause.get_children()]
        row = table.select(where=where)[0]
        if not query.parameters['read_only'] and row['read_only']:
            body.append("Row(s) to be updated as follows:")
            data = {}
            data['name'] = UnquotedStr(repr(row['name']))
            data['product'] = UnquotedStr(repr(row['product']))
            data['read_only'] = UnquotedStr("%s ---> %s" %
                                            (repr(row['read_only']),
                                             repr(query.parameters['read_only'])))
            body.append(UTF8PrettyPrinter().pformat(data))

            subj = "Read only release %s changed to modifiable" % data['name']
            send_email(relayhost, port, username, password, to_addr, from_addr,
                       table, subj, body)
            table.log.debug("Sending change notification mail for %s to %s", table.t.name, to_addr)
    return bleet

# A helper that sets sql_mode. This should only be used with MySQL, and
# lets us put the database in a stricter mode that will disallow things like
# automatic data truncation.
# From http://www.enricozini.org/2012/tips/sa-sqlmode-traditional/
from sqlalchemy.interfaces import PoolListener


class SetSqlMode(PoolListener):

    def connect(self, dbapi_con, connection_record):
        cur = dbapi_con.cursor()
        cur.execute("SET SESSION sql_mode='TRADITIONAL'")


class AUSDatabase(object):
    engine = None
    migrate_repo = path.join(path.dirname(__file__), "migrate")

    def __init__(self, dburi=None, mysql_traditional_mode=False):
        """Create a new AUSDatabase. Before this object is useful, dburi must be
           set, either through the constructor or setDburi()"""
        if dburi:
            self.setDburi(dburi, mysql_traditional_mode)
        self.log = logging.getLogger(self.__class__.__name__)

    def setDburi(self, dburi, mysql_traditional_mode=False):
        """Setup the database connection. Note that SQLAlchemy only opens a connection
           to the database when it needs to, however."""
        if self.engine:
            raise AlreadySetupError()
        self.dburi = dburi
        self.metadata = MetaData()
        listeners = []
        if mysql_traditional_mode and "mysql" in dburi:
            listeners.append(SetSqlMode())
        self.engine = create_engine(self.dburi, pool_recycle=60, listeners=listeners)
        dialect = self.engine.name
        self.rulesTable = Rules(self, self.metadata, dialect)
        self.releasesTable = Releases(self, self.metadata, dialect)
        self.permissionsTable = Permissions(self, self.metadata, dialect)
        self.dockerflowTable = Dockerflow(self, self.metadata, dialect)
        self.metadata.bind = self.engine

    def setDomainWhitelist(self, domainWhitelist):
        self.releasesTable.setDomainWhitelist(domainWhitelist)

    def setupChangeMonitors(self, relayhost, port, username, password, to_addr, from_addr):
        bleeter = make_change_notifier(relayhost, port, username, password, to_addr, from_addr)
        read_only_bleeter = make_change_notifier_for_read_only(relayhost, port,
                                                               username,
                                                               password,
                                                               to_addr,
                                                               from_addr)
        self.rules.onInsert = bleeter
        self.rules.onUpdate = bleeter
        self.rules.onDelete = bleeter
        self.permissions.onInsert = bleeter
        self.permissions.onUpdate = bleeter
        self.permissions.onDelete = bleeter
        self.releases.onUpdate = read_only_bleeter

    def hasPermission(self, *args, **kwargs):
        return self.permissions.hasPermission(*args, **kwargs)

    def create(self, version=None):
        # Migrate's "create" merely declares a database to be under its control,
        # it doesn't actually create tables or upgrade it. So we need to call it
        # and then do the upgrade to get to the state we want. We also have to
        # tell create that we're creating at version 0 of the database, otherwise
        # uprgade will do nothing!
        migrate.versioning.schema.ControlledSchema.create(self.engine, self.migrate_repo, 0)
        self.upgrade(version)

    def upgrade(self, version=None):
        # This method was taken from Buildbot:
        # https://github.com/buildbot/buildbot/blob/87108ec4088dc7fd5394ac3c1d0bd3b465300d92/master/buildbot/db/model.py#L455
        # http://code.google.com/p/sqlalchemy-migrate/issues/detail?id=100
        # means  we cannot use the migrate.versioning.api module.  So these
        # methods perform similar wrapping functions to what is done by the API
        # functions, but without disposing of the engine.
        schema = migrate.versioning.schema.ControlledSchema(self.engine, self.migrate_repo)
        changeset = schema.changeset(version)
        for step, change in changeset:
            self.log.debug('migrating schema version %s -> %d' % (step, step + 1))
            schema.runchange(step, change, 1)

    def downgrade(self, version):
        schema = migrate.versioning.schema.ControlledSchema(self.engine, self.migrate_repo)
        changeset = schema.changeset(version)
        for step, change in changeset:
            self.log.debug('migrating schema version %s -> %d' % (step, step - 1))
            schema.runchange(step, change, -1)

    def reset(self):
        self.engine = None
        self.metadata.bind = None

    def begin(self):
        return AUSTransaction(self.engine)

    @property
    def rules(self):
        return self.rulesTable

    @property
    def releases(self):
        return self.releasesTable

    @property
    def permissions(self):
        return self.permissionsTable

    @property
    def dockerflow(self):
        return self.dockerflowTable
