from copy import copy
from os import path
import re
import simplejson as json
import sys
import time

from sqlalchemy import Table, Column, Integer, Text, String, MetaData, \
  CheckConstraint, create_engine, select, BigInteger
from sqlalchemy.exc import SQLAlchemyError

import migrate.versioning.schema
import migrate.versioning.api

from auslib.blob import ReleaseBlobV1

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
            self.log.debug("exc is:", exc_info=True)
            if exc[0]:
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
    """
    def __init__(self, dialect, history=True, versioned=True):
        self.t = self.table
        # Enable versioning, if required
        if versioned:
            self.t.append_column(Column('data_version', Integer, nullable=False))
        self.versioned = versioned
        # Mirror the columns as attributes for easy access
        self.primary_key = []
        for col in self.table.get_children():
            setattr(self, col.name, col)
            if col.primary_key:
                self.primary_key.append(col)
        # Set-up a history table to do logging in, if required
        if history:
            self.history = History(dialect, self.t.metadata, self)
        else:
            self.history = None
        self.log = logging.getLogger(self.__class__.__name__)

    # Can't do this in the constructor, because the engine is always
    # unset when we're instantiated
    def getEngine(self):
        return self.t.metadata.bind

    def wherePkMatches(self, primary_key_values):
        """Generates a list of where clauses that match all of the key parts of this table."""
        cond = []
        for col in self.primary_key:
            cond.append(col==primary_key_values[col.name])
        return cond

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
           @param where: Conditions to apply on this select. Defaults to None, meaning no conditions
           @type where: A sequence of sqlalchemy.sql.expression.ClauseElement objects
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
    def select(self, transaction=None, **kwargs):
        """Perform a SELECT statement on this table.
           See AUSTable._selectStatement for possible arguments.

           @rtype: sqlalchemy.engine.base.ResultProxy
        """
        query = self._selectStatement(**kwargs)
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
            where.append(self.data_version==old_data_version)

        query = self._deleteStatement(where)
        ret = trans.execute(query)
        if ret.rowcount != 1:
            raise OutdatedDataError("Failed to delete row, old_data_version doesn't match current data_version")
        if self.history:
            trans.execute(self.history.forDelete(row, changed_by))
        return ret

    def delete(self, where, changed_by=None, old_data_version=None, transaction=None):
        """Perform a DELETE statement on this table. See AUSTable._deleteStatement for
           a description of `where'. To simplify versioning, this method can only
           delete a single row per invocation. If the where clause given would delete
           zero or multiple rows, a WrongNumberOfRowsError is raised.

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
        row = self._returnRowOrRaise(where=where, transaction=trans)
        if self.versioned:
            where = copy(where)
            where.append(self.data_version==old_data_version)
            row['data_version'] += 1

        # Copy the new data into the row
        for col in what:
            row[col] = what[col]

        query = self._updateStatement(where, row)
        ret = trans.execute(query)
        if self.history:
            trans.execute(self.history.forUpdate(row, changed_by))
        if ret.rowcount != 1:
            raise OutdatedDataError("Failed to update row, old_data_version doesn't match current data_version")
        return ret

    def update(self, where, what, changed_by=None, old_data_version=None, transaction=None):
        """Perform an UPDATE statement on this stable. See AUSTable._updateStatement for
           a description of `where' and `what'. This method can only update a single row
           per invocation. If the where clause given would update zero or multiple rows, a
           WrongNumberOfRowsError is raised.

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
    def __init__(self, dialect, metadata, baseTable):
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
        AUSTable.__init__(self, dialect, history=False, versioned=False)

    def getTimestamp(self):
        t = int(time.time() * 1000)
        return t

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
            columns[name]=insertedKeys[i]

        ts = self.getTimestamp()
        queries.append(self._insertStatement(changed_by=changed_by, timestamp=ts-1, **primary_key_data))
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
        row['timestamp'] = self.getTimestamp()
        return self._insertStatement(**row)

    def forUpdate(self, rowData, changed_by):
        """Updates cause a single row to be created, which contains the full,
           new data of the row at the time of the update."""
        row = {}
        for k in rowData:
            row[str(k)] = rowData[k]
        row['changed_by'] = changed_by
        row['timestamp'] = self.getTimestamp()
        return self._insertStatement(**row)

    def getChange(self, change_id, transaction=None):
        """ Returns the unique change that matches the give change_id """
        changes = self.select( where=[self.change_id==change_id], transaction=transaction)
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

        changes = self.select( where=where, transaction=transaction, limit=1, order_by=self.change_id.desc())
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
            if change[key] == None:
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
        return (not self._isNull(cur_base_state.copy(), row_primary_keys) ) and (not self._isNull(prev_base_state.copy(), row_primary_keys))

    def rollbackChange(self, change_id, changed_by, transaction=None):
        """ Rollback the change given by the change_id,
        Will handle all cases: insert, delete, update """

        change = self.getChange(change_id , transaction)

        # Get the values of the primary keys for the given row
        row_primary_keys = [0]*len(self.base_primary_key)
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

                self.baseTable.delete(changed_by = changed_by, transaction=transaction, where=where, old_data_version = change['data_version'])

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


class Rules(AUSTable):
    def __init__(self, metadata, dialect):
        self.table = Table('rules', metadata,
            Column('rule_id', Integer, primary_key=True, autoincrement=True),
            Column('priority', Integer),
            Column('mapping', String(100)),
            Column('throttle', Integer, CheckConstraint('0 <= throttle <= 100')),
            Column('update_type', String(15), nullable=False),
            Column('product', String(15)),
            Column('version', String(10)),
            Column('channel', String(75)),
            Column('buildTarget', String(75)),
            Column('buildID', String(20)),
            Column('locale', String(10)),
            Column('osVersion', String(100)),
            Column('distribution', String(100)),
            Column('distVersion', String(100)),
            Column('headerArchitecture', String(10)),
            Column('comment', String(500))
        )
        AUSTable.__init__(self, dialect)

    def _matchesRegex(self, foo, bar):
        # Expand wildcards and use ^/$ to make sure we don't succeed on partial
        # matches. Eg, 3.6* matches 3.6, 3.6.1, 3.6b3, etc.
        test = foo.replace('.','\.').replace('*','.*')
        test = '^%s$' % test
        if re.match(test, bar):
            return True
        return False

    def _versionMatchesRule(self, ruleVersion, queryVersion):
        """Decides whether a version from the rules matches an incoming version.
           If the ruleVersion is null, we match any queryVersion. If it's not
           null, we must either match exactly, or match a potential wildcard."""
        if ruleVersion is None:
            return True
        if self._matchesRegex(ruleVersion, queryVersion):
            return True

    def _channelMatchesRule(self, ruleChannel, queryChannel, fallbackChannel):
        """Decides whether a channel from the rules matchs an incoming one.
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

    def addRule(self, changed_by, what, transaction=None):
        ret = self.insert(changed_by=changed_by, transaction=transaction, **what)
        return ret.inserted_primary_key

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
        matchingRules = []
        where=[
            ((self.product==updateQuery['product']) | (self.product==None)) &
            ((self.buildTarget==updateQuery['buildTarget']) | (self.buildTarget==None)) &
            ((self.buildID==updateQuery['buildID']) | (self.buildID==None)) &
            ((self.locale==updateQuery['locale']) | (self.locale==None)) &
            ((self.osVersion==updateQuery['osVersion']) | (self.osVersion==None)) &
            ((self.headerArchitecture==updateQuery['headerArchitecture']) | (self.headerArchitecture==None))
        ]
        # Query version 2 doesn't have distribution information, and to keep
        # us maximally flexible, we won't match any rules that have
        # distribution update set.
        if updateQuery['queryVersion'] == 2:
            where.extend([(self.distribution==None) & (self.distVersion==None)])
        # Only query versions 3 and 4 have distribution information, so we
        # need to consider it.
        if updateQuery['queryVersion'] in (3, 4):
            where.extend([
                ((self.distribution==updateQuery['distribution']) | (self.distribution==None)) &
                ((self.distVersion==updateQuery['distVersion']) | (self.distVersion==None))
            ])
        if updateQuery['force'] == False:
            where.append(self.throttle > 0)
        rules = self.select(where=where, transaction=transaction)
        self.log.debug("where: %s" % where)
        self.log.debug("Raw matches:")
        for rule in rules:
            self.log.debug(rule)
            # Resolve special means for version and channel, dropping
            # rules that don't match after resolution.
            if not self._versionMatchesRule(rule['version'], updateQuery['version']):
                self.log.debug("%s doesn't match %s", rule['version'], updateQuery['version'])
                continue
            if not self._channelMatchesRule(rule['channel'], updateQuery['channel'], fallbackChannel):
                self.log.debug("%s doesn't match %s", rule['channel'], updateQuery['channel'])
                continue
            matchingRules.append(rule)
        self.log.debug("Reduced matches:")
        if self.log.isEnabledFor(logging.DEBUG):
            for r in matchingRules:
                self.log.debug(r)
        return matchingRules

    def getRuleById(self, rule_id, transaction=None):
        """ Returns the unique rule that matches the give rule_id """
        rules = self.select( where=[self.rule_id==rule_id], transaction=transaction)
        found = len(rules)
        if found > 1 or found == 0:
            self.log.debug("Found %s rules, should have been 1", found)
            return None
        return rules[0]

    def updateRule(self, changed_by, rule_id, what, old_data_version, transaction=None):
        """ Update the rule given by rule_id with the parameter what """
        where = [self.rule_id==rule_id]
        self.update(changed_by=changed_by, where=where, what=what, old_data_version=old_data_version, transaction=transaction)


class Releases(AUSTable):
    def __init__(self, metadata, dialect):
        self.table = Table('releases', metadata,
            Column('name', String(100), primary_key=True),
            Column('product', String(15), nullable=False),
            Column('version', String(25), nullable=False),
        )
        if dialect == 'mysql':
            from sqlalchemy.dialects.mysql import LONGTEXT
            dataType = LONGTEXT
        else:
            dataType = Text
        self.table.append_column(Column('data', dataType, nullable=False))
        AUSTable.__init__(self, dialect)

    def getReleases(self, name=None, product=None, version=None, limit=None, transaction=None):
        self.log.debug("Looking for releases with:")
        self.log.debug("name: %s", name)
        self.log.debug("product: %s", product)
        self.log.debug("version: %s", version)
        where = []
        if name:
            where.append(self.name==name)
        if product:
            where.append(self.product==product)
        if version:
            where.append(self.version==version)
        rows = self.select(where=where, limit=limit, transaction=transaction)
        for row in rows:
            blob = ReleaseBlobV1()
            blob.loadJSON(row['data'])
            row['data'] = blob
        return rows

    def countReleases(self, transaction=None):
        """Returns a number of the count of releases"""
        count, = self.t.count().execute().fetchone()
        return count

    def getReleaseInfo(self, product=None, version=None, limit=None, transaction=None, nameOnly=False):
        where = []
        if product:
            where.append(self.product==product)
        if version:
            where.append(self.version==version)
        if nameOnly:
            column = [self.name]
        else:
            column = [self.name, self.product, self.version]
        rows = self.select(where=where, columns=column, limit=limit, transaction=transaction)
        return rows

    def getReleaseNames(self, **kwargs):
        return self.getReleaseInfo(nameOnly=True, **kwargs)

    def getReleaseBlob(self, name, transaction=None):
        try:
            row = self.select(where=[self.name==name], columns=[self.data], limit=1, transaction=transaction)[0]
        except IndexError:
            raise KeyError("Couldn't find release with name '%s'" % name)
        blob = ReleaseBlobV1()
        blob.loadJSON(row['data'])
        return blob

    def addRelease(self, name, product, version, blob, changed_by, transaction=None):
        if not blob.isValid():
            raise ValueError("Release blob is invalid.")
        columns = dict(name=name, product=product, version=version, data=blob.getJSON())
        # Raises DuplicateDataError if the release already exists.
        self.insert(changed_by=changed_by, transaction=transaction, **columns)

    def updateRelease(self, name, changed_by, old_data_version, product=None, version=None, blob=None, transaction=None):
        what = {}
        if product:
            what['product'] = product
        if version:
            what['version'] = version
        if blob:
            if not blob.isValid():
                raise ValueError("Release blob is invalid.")
            what['data'] = blob.getJSON()
        self.update(where=[self.name==name], what=what, changed_by=changed_by, old_data_version=old_data_version, transaction=transaction)

    def addLocaleToRelease(self, name, platform, locale, data, old_data_version, changed_by, transaction=None, alias=None):
        """Adds or update's the existing data for a specific platform + locale
           combination, in the release identified by 'name'. The data is
           validated before commiting it, and a ValueError is raised if it is
           invalid.
        """
        releaseBlob = self.getReleaseBlob(name, transaction=transaction)
        if 'platforms' not in releaseBlob:
            releaseBlob['platforms'] = {
                platform: {
                    'locales': {
                    }
                }
            }

        if platform in releaseBlob['platforms']:
            # If the platform we're given is aliased to another one, we need
            # to resolve that before doing any updating. If we don't, the data
            # will go into an aliased platform and be ignored!
            platform = releaseBlob.getResolvedPlatform(platform)
        else:
            releaseBlob['platforms'][platform] = dict(locales=dict())
        releaseBlob['platforms'][platform]['locales'][locale] = data

        # we don't allow modification of existing platforms (aliased or not)
        if alias:
            for a in alias:
                if a not in releaseBlob['platforms']:
                    releaseBlob['platforms'][a] = {'alias': platform}

        if not releaseBlob.isValid():
            raise ValueError("New release blob is invalid.")
        where = [self.name==name]
        what = dict(data=releaseBlob.getJSON())
        self.update(where=where, what=what, changed_by=changed_by, old_data_version=old_data_version,
            transaction=transaction)

    def getLocale(self, name, platform, locale, transaction=None):
        try:
            blob = self.getReleaseBlob(name, transaction=transaction)
            return blob['platforms'][platform]['locales'][locale]
        except KeyError:
            raise KeyError("Couldn't find locale identified by: %s, %s, %s" % (name, platform ,locale))

    def localeExists(self, name, platform, locale, transaction=None):
        try:
            self.getLocale(name, platform, locale, transaction)
            return True
        except KeyError:
            return False

class Permissions(AUSTable):
    """allPermissions defines the structure and possible options for all
       available permissions. Most permissions are identified by an URL,
       potentially with variables in it. All URL based permissions can be
       augmented by using the "product" option. When specified, only requests
       involving the named product will be permitted. Additionally, any URL
       that supports more than one of: PUT, POST, or DELETE can by augmented
       by using the option "method". When specified, the permission with this
       option is only valid for requests through that HTTP method."""
    allPermissions = {
        'admin': [],
        '/releases/:name': ['method', 'product'],
        '/releases/:name/rollback': ['product'],
        '/releases/:name/builds/:platform/:locale': ['method', 'product'],
        '/rules': ['product'],
        '/rules/:id': ['method', 'product'],
        '/rules/:id/rollback': ['product'],
        '/users/:id/permissions/:permission': ['method']
    }

    def __init__(self, metadata, dialect):
        self.table = Table('permissions', metadata,
            Column('permission', String(50), primary_key=True),
            Column('username', String(100), primary_key=True),
            Column('options', Text)
        )
        AUSTable.__init__(self, dialect)

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

    def countAllUsers(self, transaction=None):
        res = self.select(columns=[self.username], distinct=True, transaction=transaction)
        return len(res)

    def grantPermission(self, changed_by, username, permission, options=None, transaction=None):
        self.assertPermissionExists(permission)
        if options:
            self.assertOptionsExist(permission, options)
        columns = dict(username=username, permission=permission)
        if options:
            columns['options'] = json.dumps(options)
        self.log.debug("granting %s to %s with options %s" % (permission, username, options))
        self.insert(changed_by=changed_by, transaction=transaction, **columns)
        self.log.debug("successfully granted %s to %s with options %s" % (permission, username, options))

    def updatePermission(self, changed_by, username, permission, old_data_version, options=None, transaction=None):
        self.assertPermissionExists(permission)
        if options:
            self.assertOptionsExist(permission, options)
            what = dict(options=json.dumps(options))
        else:
            what = dict(options=None)
        where = [self.username==username, self.permission==permission]
        self.update(changed_by=changed_by, where=where, what=what, old_data_version=old_data_version, transaction=transaction)

    def revokePermission(self, changed_by, username, permission, old_data_version, transaction=None):
        where = [self.username==username, self.permission==permission]
        self.delete(changed_by=changed_by, where=where, old_data_version=old_data_version, transaction=transaction)

    def getPermission(self, username, permission, transaction=None):
        try:
            row = self.select(where=[self.username==username, self.permission==permission], transaction=transaction)[0]
            if row['options']:
                row['options'] = json.loads(row['options'])
            return row
        except IndexError:
            return {}

    def getUserPermissions(self, username, transaction=None):
        rows = self.select(columns=[self.permission, self.options, self.data_version], where=[self.username==username], transaction=transaction)
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
        ret = self.select(columns=[self.options], where=[self.username==username, self.permission==permission], transaction=transaction)
        if ret:
            if ret[0]['options']:
                return json.loads(ret[0]['options'])
            else:
                return {}
        else:
            raise ValueError('Permission "%s" doesn\'t exist' % permission)

    def hasUrlPermission(self, username, url, method, urlOptions={}, transaction=None):
        """Check if a user has access to an URL via a specific HTTP method.
           GETs are always allowed, and admins can always access everything."""
        if self.select(where=[self.username==username, self.permission=='admin'], transaction=transaction):
            return True
        try:
            options = self.getOptions(username, url, transaction=transaction)
        except ValueError:
            return False

        # GETs to any URL are always allowed
        if method == 'GET':
            return True
        # Methods are also subject to the same rules other options are,
        # so we can put them in the same loop
        allOptions = urlOptions.copy()
        allOptions['method'] = method
        ret = True
        for opt in allOptions:
            allowedOpts = options.get(opt, None)
            # When a permission doesn't have the option specified, we treat that
            # it as allowed. When it does have it specified, the incoming option
            # must match the one in the permission.
            if allowedOpts and allOptions[opt] not in allowedOpts:
                ret = False
        return ret

class AUSDatabase(object):
    engine = None
    migrate_repo = path.join(path.dirname(__file__), "migrate")

    def __init__(self, dburi=None):
        """Create a new AUSDatabase. Before this object is useful, dburi must be
           set, either through the constructor or setDburi()"""
        if dburi:
            self.setDburi(dburi)
        self.log = logging.getLogger(self.__class__.__name__)

    def setDburi(self, dburi):
        """Setup the database connection. Note that SQLAlchemy only opens a connection
           to the database when it needs to, however."""
        if self.engine:
            raise AlreadySetupError()
        self.dburi = dburi
        self.metadata = MetaData()
        self.engine = create_engine(self.dburi, pool_recycle=60)
        dialect = self.engine.name
        self.rulesTable = Rules(self.metadata, dialect)
        self.releasesTable = Releases(self.metadata, dialect)
        self.permissionsTable = Permissions(self.metadata, dialect)
        self.metadata.bind = self.engine

    def create(self, version=None):
        # Migrate's "create" merely declares a database to be under its control,
        # it doesn't actually create tables or upgrade it. So we need to call it
        # and then do the upgrade to get to the state we want. We also have to
        # tell create that we're creating at version 0 of the database, otherwise
        # uprgade will do nothing!
        migrate.versioning.schema.ControlledSchema.create(self.engine, self.migrate_repo, 0)
        self.upgrade(version)

    def upgrade(self, version=None):
        # This method was taken from Buildbot: https://github.com/buildbot/buildbot/blob/87108ec4088dc7fd5394ac3c1d0bd3b465300d92/master/buildbot/db/model.py#L455
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
