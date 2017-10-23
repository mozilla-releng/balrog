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

from auslib.global_state import cache
from auslib.blobs.base import createBlob, merge_dicts
from auslib.util.comparison import string_compare, version_compare, int_compare
from auslib.util.timestamp import getMillisecondTimestamp

import logging


def rows_to_dicts(rows):
    """Converts SQL Alchemy result rows to dicts.

    You might want this if you want to mutate objects (SQLAlchemy rows
    are immutable), or if you want to serialize them to JSON
    (SQLAlchemy rows get confused if you try to serialize them).
    """
    return map(dict, rows)


class AlreadySetupError(Exception):

    def __str__(self):
        return "Can't connect to new database, still connected to previous one"


class PermissionDeniedError(Exception):
    pass


class SignoffRequiredError(Exception):
    """Raised when someone attempts to directly modify an object that requires
    signoff."""


class TransactionError(SQLAlchemyError):
    """Raised when a transaction fails for any reason."""


class OutdatedDataError(SQLAlchemyError):
    """Raised when an update or delete fails because of outdated data."""


class MismatchedDataVersionError(SQLAlchemyError):
    """Raised when the data version of a scheduled change and its associated conditions
    row do not match after an insert or update."""


class WrongNumberOfRowsError(SQLAlchemyError):
    """Raised when an update or delete fails because the clause matches more than one row."""


class UpdateMergeError(SQLAlchemyError):
    pass


class ReadOnlyError(SQLAlchemyError):
    """Raised when a release marked as read-only is attempted to be changed."""


class ChangeScheduledError(SQLAlchemyError):
    """Raised when a Scheduled Change cannot be created, modified, or deleted
    for data consistency reasons."""


class JSONColumn(sqlalchemy.types.TypeDecorator):
    """JSONColumns are used for types that are deserialized JSON (usually
    dicts) in memory, but need to be serialized to text before storage.
    JSONColumn handles the conversion both ways, serialized just before
    storage, and deserialized just after retrieval."""

    impl = Text

    def process_bind_param(self, value, dialect):
        if value:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value:
            value = json.loads(value)
        return value


class CompatibleBooleanColumn(sqlalchemy.types.TypeDecorator):
    """A Boolean column that is compatible with all of our supported
    database engines (mysql, sqlite). SQLAlchemy's built-in Boolean
    does not work because it creates a CHECK constraint that makes
    it impossible to downgrade a database with sqlalchemy-migrate."""

    impl = Integer

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not isinstance(value, bool):
                raise TypeError("{} is invalid type ({}), must be bool".format(value, type(value)))

            if value is True:
                value = 1
            else:
                value = 0
        return value

    def process_result_value(self, value, dialect):
        # Boolean columns may be nullable, we need to be sure to preserve nulls
        # in case consumers treat them differently than False.
        if value is not None:
            value = bool(value)
        return value


def BlobColumn(impl=Text):
    """BlobColumns are used to store Release Blobs, which are ultimately dicts.
    Release Blobs must be serialized before storage, and deserialized upon
    retrevial. This type handles both conversions. Some database engines
    (eg: mysql) may require a different underlying type than Text. The
    desired type may be passed in as an argument."""
    class cls(sqlalchemy.types.TypeDecorator):

        def process_bind_param(self, value, dialect):
            if value:
                value = value.getJSON()
            return value

        def process_result_value(self, value, dialect):
            if value:
                value = createBlob(value)
            return value

    cls.impl = impl
    return cls


def verify_signoffs(potential_required_signoffs, signoffs):
    """Determines whether or not something is signed off given:
    * A list of potential required signoffs
    * A list of signoffs that have been made

    The real number of signoffs required is found by looking through the
    potential required signoffs and finding the highest number required for each
    role. If there are not enough signoffs provided for any of the groups,
    a SignoffRequiredError is raised."""

    signoffs_given = defaultdict(int)
    required_signoffs = {}
    if not potential_required_signoffs:
        return
    if not signoffs:
        raise SignoffRequiredError("No Signoffs given")
    for signoff in signoffs:
        signoffs_given[signoff["role"]] += 1
    for rs in potential_required_signoffs:
        required_signoffs[rs["role"]] = max(required_signoffs.get(rs["role"], 0), rs["signoffs_required"])
    for role, signoffs_required in required_signoffs.iteritems():
        if signoffs_given[role] < signoffs_required:
            raise SignoffRequiredError("Not enough signoffs for role '{}'".format(role))


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
                 scheduled_changes_kwargs={}, onInsert=None, onUpdate=None, onDelete=None):
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
            self.scheduled_changes = ScheduledChangeTable(db, dialect, self.t.metadata, self, **scheduled_changes_kwargs)
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

    def select(self, where=None, transaction=None, **kwargs):
        """Perform a SELECT statement on this table.
           See AUSTable._selectStatement for possible arguments.

           @param where: A list of SQLAlchemy clauses, or a key/value pair of columns and values.
           @type where: list of clauses or key/value pairs.

           @param transaction: A transaction object to add the update statement (and history changes) to.
                               If provided, you must commit the transaction yourself. If None, they will
                               be added to a locally-scoped transaction and committed.

           @rtype: sqlalchemy.engine.base.ResultProxy
        """

        # If "where" is key/value pairs, we need to convert it to SQLAlchemy
        # clauses before proceeding.
        if hasattr(where, "keys"):
            where = [getattr(self, k) == v for k, v in where.iteritems()]

        query = self._selectStatement(where=where, **kwargs)

        if transaction:
            result = transaction.execute(query).fetchall()
        else:
            with AUSTransaction(self.getEngine()) as trans:
                result = trans.execute(query).fetchall()

        return rows_to_dicts(result)

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
            self.onInsert(self, "INSERT", changed_by, query, trans)

        ret = trans.execute(query)
        if self.history:
            for q in self.history.forInsert(ret.inserted_primary_key, data, changed_by):
                trans.execute(q)
        return ret

    def insert(self, changed_by=None, transaction=None, dryrun=False, **columns):
        """Perform an INSERT statement on this table. See AUSTable._insertStatement for
           a description of columns.

           @param changed_by: The username of the person inserting the row. Required when
                              history is enabled. Unused otherwise. No authorization checks are done
                              at this level.
           @type changed_by: str
           @param transaction: A transaction object to add the insert statement (and history changes) to.
                               If provided, you must commit the transaction yourself. If None, they will
                               be added to a locally-scoped transaction and committed.
           @param dryrun: If true, this insert statement will not actually be run.
           @type dryrun: bool

           @rtype: sqlalchemy.engine.base.ResultProxy
        """
        if self.history and not changed_by:
            raise ValueError("changed_by must be passed for Tables that have history")

        if dryrun:
            self.log.debug("In dryrun mode, not doing anything...")
            return

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
        """Prepare a DELETE statement for commit. If this table has history enabled,
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
            self.onDelete(self, "DELETE", changed_by, query, trans)

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

    def delete(self, where, changed_by=None, old_data_version=None, transaction=None, dryrun=False):
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
           @param transaction: A transaction object to add the delete statement (and history changes) to.
                               If provided, you must commit the transaction yourself. If None, they will
                               be added to a locally-scoped transaction and committed.
           @param dryrun: If true, this insert statement will not actually be run.
           @type dryrun: bool

           @rtype: sqlalchemy.engine.base.ResultProxy
        """
        # If "where" is key/value pairs, we need to convert it to SQLAlchemy
        # clauses before proceeding.
        if hasattr(where, "keys"):
            where = [getattr(self, k) == v for k, v in where.iteritems()]

        if self.history and not changed_by:
            raise ValueError("changed_by must be passed for Tables that have history")
        if self.versioned and not old_data_version:
            raise ValueError("old_data_version must be passed for Tables that are versioned")

        if dryrun:
            self.log.debug("In dryrun mode, not doing anything...")
            return

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
            self.onUpdate(self, "UPDATE", changed_by, query, trans)

        ret = trans.execute(query)
        # It's important that OutdatedDataError is raised as early as possible
        # because callers may be able to handle it gracefully (and continue
        # with their update). If we raise this _after_ adding history or merging
        # with Scheduled Changes, we may end up altering the history or
        # scheduled changes more than once if the caller ends up re-calling
        # AUSTable.update() after handling the OutdatedDataError.
        if ret.rowcount != 1:
            raise OutdatedDataError("Failed to update row, old_data_version doesn't match current data_version")
        if self.history:
            trans.execute(self.history.forUpdate(new_row, changed_by))
        if self.scheduled_changes:
            self.scheduled_changes.mergeUpdate(orig_row, what, changed_by, trans)
        return ret

    def update(self, where, what, changed_by=None, old_data_version=None, transaction=None, dryrun=False):
        """Perform an UPDATE statement on this stable. See AUSTable._updateStatement for
           a description of `where' and `what'. This method can only update a single row
           per invocation. If the where clause given would update zero or multiple rows, a
           WrongNumberOfRowsError is raised.

           @param where: A list of SQLAlchemy clauses, or a key/value pair of columns and values.
           @type where: list of clauses or key/value pairs.
           @param what: Key/value pairs containing new values for the given columns.
           @type what: key/value pairs
           @param changed_by: The username of the person inserting the row. Required when
                              history is enabled. Unused otherwise. No authorization checks are done
                              at this level.
           @type changed_by: str
           @param old_data_version: Previous version of the row to be deleted. If this version doesn't
                                    match the current version of the row, an OutdatedDataError will be
                                    raised and the delete will fail. Required when versioning is enabled.
           @type old_data_version: int
           @param transaction: A transaction object to add the update statement (and history changes) to.
                               If provided, you must commit the transaction yourself. If None, they will
                               be added to a locally-scoped transaction and committed.
           @param dryrun: If true, this insert statement will not actually be run.
           @type dryrun: bool

           @rtype: sqlalchemy.engine.base.ResultProxy
        """
        # If "where" is key/value pairs, we need to convert it to SQLAlchemy
        # clauses before proceeding.
        if hasattr(where, "keys"):
            where = [getattr(self, k) == v for k, v in where.iteritems()]

        if self.history and not changed_by:
            raise ValueError("changed_by must be passed for Tables that have history")
        if self.versioned and not old_data_version:
            raise ValueError("update: old_data_version must be passed for Tables that are versioned")

        if dryrun:
            self.log.debug("In dryrun mode, not doing anything...")
            return

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
                # Setting unique to None because SQLAlchemy marks column attribute as None
                # unless they have been explicitely set to True or False.
                newcol.unique = None
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
            self.log.debug("Querying for change_id by:")
            self.log.debug("data_version: %s", data_version)
            for col in column_names.keys():
                self.log.debug("%s: %s", column_names[col], column_values[col])
                where.append(column_names[col] == column_values[col])

            # To improve query efficiency we first get the change_id,
            # and _then_ get the entire row. This is because we may not be able
            # to query by an index depending which column_values we were given.
            # If we end up querying by column_values that don't have an index,
            # mysql will read many more rows than will be returned. This is
            # particularly bad on the releases_history table, where the "data"
            # column is often hundreds of kilobytes per row.
            # Additional details in https://github.com/mozilla/balrog/pull/419#issuecomment-334851038
            change_ids = self.select(columns=[self.change_id], where=where,
                                     transaction=transaction)
            if len(change_ids) != 1:
                self.log.debug("Found %s changes when not querying by change_id, should have been 1", len(change_ids))
                return None
            change_id = change_ids[0]["change_id"]

        self.log.debug("Querying for full change by change_id %s", change_id)
        changes = self.select(where=[self.change_id == change_id], transaction=transaction)
        if len(changes) != 1:
            self.log.debug("Found %s changes when querying by change_id, should have been 1", len(changes))
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


class ConditionsTable(AUSTable):
    # Scheduled changes may only have a single type of condition, but some
    # conditions require mulitple arguments. This data structure defines
    # each type of condition, and groups their args together for easier
    # processing.
    condition_groups = {
        "time": ("when",),
        "uptake": ("telemetry_product", "telemetry_channel", "telemetry_uptake"),
    }

    def __init__(self, db, dialect, metadata, baseName, conditions, history=True):
        if not conditions:
            raise ValueError("No conditions enabled, cannot initialize conditions for for {}".format(baseName))
        if set(conditions) - set(self.condition_groups):
            raise ValueError("Unknown conditions in: {}".format(conditions))

        self.enabled_condition_groups = {k: v for k, v in self.condition_groups.iteritems() if k in conditions}

        self.table = Table("{}_conditions".format(baseName), metadata,
                           Column("sc_id", Integer, primary_key=True),
                           )

        if "uptake" in conditions:
            self.table.append_column(Column("telemetry_product", String(15)))
            self.table.append_column(Column("telemetry_channel", String(75)))
            self.table.append_column(Column("telemetry_uptake", Integer))

        if "time" in conditions:
            if dialect == "sqlite":
                self.table.append_column(Column("when", Integer))
            else:
                self.table.append_column(Column("when", BigInteger))

        super(ConditionsTable, self).__init__(db, dialect, history=history, versioned=True)

    def validate(self, conditions):
        conditions = {k: v for k, v in conditions.iteritems() if conditions[k]}
        if not conditions:
            raise ValueError("No conditions found")

        for c in conditions:
            for condition, args in self.condition_groups.iteritems():
                if c in args:
                    if c in itertools.chain(*self.enabled_condition_groups.values()):
                        break
                    else:
                        raise ValueError("{} condition is disabled".format(condition))
            else:
                raise ValueError("Invalid condition: %s", c)

        for group in self.enabled_condition_groups.values():
            if set(group) == set(conditions.keys()):
                break
        else:
            raise ValueError("Invalid combination of conditions: {}".format(conditions.keys()))

        if "when" in conditions:
            try:
                time.gmtime(conditions["when"] / 1000)
            except:
                raise ValueError("Cannot parse 'when' as a unix timestamp.")

            if conditions["when"] < getMillisecondTimestamp():
                raise ValueError("Cannot schedule changes in the past")


class ScheduledChangeTable(AUSTable):
    """A Table that stores the necessary information to schedule changes
    to the baseTable provided. A ScheduledChangeTable ends up mirroring the
    columns of its base, and adding the necessary ones to provide the schedule.
    By default, ScheduledChangeTables enable History on themselves."""

    def __init__(self, db, dialect, metadata, baseTable, conditions=("time", "uptake"), history=True):
        table_name = "{}_scheduled_changes".format(baseTable.t.name)
        self.baseTable = baseTable
        self.table = Table(table_name, metadata,
                           Column("sc_id", Integer, primary_key=True, autoincrement=True),
                           Column("scheduled_by", String(100), nullable=False),
                           Column("complete", Boolean, default=False),
                           Column("change_type", String(50), nullable=False),
                           )
        self.conditions = ConditionsTable(db, dialect, metadata, table_name, conditions, history=history)
        # Signoffs are configurable at runtime, which means that we always need
        # a Signoffs table, even if it may not be used immediately.
        self.signoffs = SignoffsTable(db, metadata, dialect, table_name)

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
            # 2) Primary Key Integer Autoincrement columns from the baseTable become normal nullable
            # columns in ScheduledChanges because we can schedule changes that insert into baseTable
            # and the DB will handle inserting the correct value. However, nulls aren't allowed when
            # we schedule updates or deletes -this is enforced in self.validate().
            # For Primary Key columns that aren't Integer or Autoincrement but are nullable, we preserve
            # this non-nullability because we need a value to insert into the baseTable when the
            # scheduled change gets executed.
            # Non-Primary Key columns from the baseTable become nullable and non-unique in ScheduledChanges
            # because they aren't part of the ScheduledChanges business logic and become simple data storage.
            if col.primary_key:
                newcol.primary_key = False

                # Only integer columns can be AUTOINCREMENT. The isinstance statement guards
                # against false positives from SQLAlchemy.
                if col.autoincrement and isinstance(col.type, Integer):
                    newcol.nullable = True
            else:
                newcol.unique = None
                newcol.nullable = True

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

    def _splitColumns(self, columns):
        """Because Scheduled Changes are stored across two Tables, we need to
        split out the parts that are in the main table from the parts that
        are stored in the conditions table in a few different places."""
        base_columns = {}
        condition_columns = {}
        for cond_type in columns:
            if cond_type in itertools.chain(*self.conditions.condition_groups.values()):
                condition_columns[cond_type] = columns[cond_type]
            else:
                base_columns[cond_type] = columns[cond_type]

        return base_columns, condition_columns

    def _checkBaseTablePermissions(self, base_table_where, new_row, changed_by, transaction):
        if "change_type" not in new_row:
            raise ValueError("change_type needed to check Permission")

        if new_row.get("change_type") == "update":
            self.baseTable.update(base_table_where, new_row, changed_by, new_row["data_version"], transaction=transaction, dryrun=True)
        elif new_row.get("change_type") == "insert":
            self.baseTable.insert(changed_by, transaction=transaction, dryrun=True, **new_row)
        elif new_row.get("change_type") == "delete":
            self.baseTable.delete(base_table_where, changed_by, new_row["data_version"], transaction=transaction, dryrun=True)
        else:
            raise ValueError("Unknown Change Type")

    def _dataVersionsAreSynced(self, sc_id, transaction):
        sc_row = super(ScheduledChangeTable, self).select(where=[self.sc_id == sc_id], transaction=transaction, columns=[self.data_version])
        conditions_row = self.conditions.select(where=[self.conditions.sc_id == sc_id], transaction=transaction, columns=[self.conditions.data_version])
        if not sc_row or len(sc_row) != 1 or not conditions_row or len(conditions_row) != 1:
            return False
        self.log.debug("sc_row data version is %s", sc_row[0].get("data_version"))
        self.log.debug("conditions_row data version is %s", conditions_row[0].get("data_version"))
        if sc_row[0].get("data_version") != conditions_row[0].get("data_version"):
            return False

        return True

    def validate(self, base_columns, condition_columns, changed_by, sc_id=None, transaction=None):
        # Depending on the change type, we may do some additional checks
        # against the base table PK columns. It's cleaner to build up these
        # early than do it later.
        base_table_where = []
        sc_table_where = []

        for pk in self.base_primary_key:
            base_column = getattr(self.baseTable, pk)
            if pk in base_columns:
                sc_table_where.append(getattr(self, "base_%s" % pk) == base_columns[pk])
                base_table_where.append(getattr(self.baseTable, pk) == base_columns[pk])
            # Non-Integer columns can have autoincrement set to True for some reason.
            # Any non-integer columns in the primary key are always required (because
            # autoincrement actually isn't a thing for them), and any Integer columns
            # that _aren't_ autoincrement are required as well.
            elif not isinstance(base_column.type, (sqlalchemy.types.Integer,)) or not base_column.autoincrement:
                raise ValueError("Missing primary key column '%s' which is not autoincrement", pk)

        if base_columns["change_type"] == "delete":
            for pk in self.base_primary_key:
                if pk not in base_columns:
                    raise ValueError("Missing primary key column %s. PK values needed for deletion" % (pk))
                if base_columns[pk] is None:
                    raise ValueError("%s value found to be None. PK value can not be None for deletion" % (pk))
        elif base_columns["change_type"] == "update":
            # For updates, we need to make sure that the baseTable row already
            # exists, and that the data version provided matches the current
            # version to ensure that someone isn't trying to schedule a change
            # against out-of-date data.
            current_data_version = self.baseTable.select(columns=(self.baseTable.data_version,), where=base_table_where, transaction=transaction)
            if not current_data_version:
                raise ValueError("Cannot create scheduled change with data_version for non-existent row")

            if current_data_version and current_data_version[0]["data_version"] != base_columns.get("data_version"):
                raise OutdatedDataError("Wrong data_version given for base table, cannot create scheduled change.")
        elif base_columns["change_type"] == "insert" and base_table_where:
            # If the base table row shouldn't already exist, we need to make sure they don't
            # to avoid getting an IntegrityError when the change is enacted.
            if self.baseTable.select(columns=(self.baseTable.data_version,), where=base_table_where, transaction=transaction):
                raise ValueError("Cannot schedule change for duplicate PK")

        # If we're validating a new scheduled change (sc_id is None), we need
        # to make sure that no other scheduled change already exists if a
        # primary key for the base table was provided (sc_table_where is not empty).
        if not sc_id and sc_table_where:
            sc_table_where.append(self.complete == False) # noqa because we need to use == for sqlalchemy operator overloading to work
            if len(self.select(columns=[self.sc_id], where=sc_table_where)) > 0:
                raise ChangeScheduledError("Cannot scheduled a change for a row with one already scheduled")

        self.conditions.validate(condition_columns)
        self._checkBaseTablePermissions(base_table_where, base_columns, changed_by, transaction)

    def select(self, where=None, transaction=None, **kwargs):
        ret = []
        # We'll be retrieving condition information for each Scheduled Change,
        # and we'll need sc_id to do so.
        if kwargs.get("columns") is not None:
            # Columns can be specified as names or Column instances, so we must check for both.
            if "sc_id" not in kwargs["columns"] and self.sc_id not in kwargs["columns"]:
                kwargs["columns"].append(self.sc_id)
        for row in super(ScheduledChangeTable, self).select(where=where, transaction=transaction, **kwargs):
            columns = [getattr(self.conditions, c) for c in itertools.chain(*self.conditions.enabled_condition_groups.values())]
            conditions = self.conditions.select([self.conditions.sc_id == row["sc_id"]], transaction=transaction, columns=columns)
            row.update(conditions[0])
            ret.append(row)
        return ret

    def insert(self, changed_by, transaction=None, dryrun=False, **columns):
        base_columns, condition_columns = self._splitColumns(columns)
        if "change_type" not in base_columns:
            raise ValueError("Change type is required")

        self.validate(base_columns=base_columns, condition_columns=condition_columns, changed_by=changed_by, transaction=transaction)

        base_columns = self._prefixColumns(base_columns)
        base_columns["scheduled_by"] = changed_by

        ret = super(ScheduledChangeTable, self).insert(changed_by=changed_by, transaction=transaction, dryrun=dryrun, **base_columns)
        if not dryrun:
            sc_id = ret.inserted_primary_key[0]
            self.conditions.insert(changed_by, transaction, dryrun, sc_id=sc_id, **condition_columns)
            if not self._dataVersionsAreSynced(sc_id, transaction):
                raise MismatchedDataVersionError("Conditions data version is out of sync with main table for sc_id %s",
                                                 sc_id)

            # - If the User scheduling a change only holds one Role, record a signoff with it.
            # - If the User scheduling a change holds more than one Role, we cannot a Signoff, because
            #   we don't know which Role we'd want to signoff with. The user will need to signoff
            #   manually in these cases.
            user_roles = self.db.getUserRoles(username=changed_by, transaction=transaction)
            required_roles = set()
            required_signoffs = self.baseTable.getPotentialRequiredSignoffs([columns], transaction=transaction)
            if required_signoffs:
                required_roles.update([rs["role"] for rs in required_signoffs])
            if len(user_roles) == 1 and user_roles[0]["role"] in required_roles:
                self.signoffs.insert(changed_by=changed_by, transaction=transaction, dryrun=dryrun,
                                     sc_id=sc_id, role=user_roles[0].get("role"))
            return sc_id

    def update(self, where, what, changed_by, old_data_version, transaction=None, dryrun=False):
        base_what, condition_what = self._splitColumns(what)

        affected_ids = []
        # We need to check each Scheduled Change that would be affected by this
        # to ensure the new row will be valid.
        for row in self.select(where=where, transaction=transaction):
            # verify whether the scheduled change has already been completed or not. If completed,
            # then cannot modify the scheduled change anymore.
            if row.get("complete"):
                raise ValueError("Scheduled change already completed. Cannot update now.")

            affected_ids.append(row["sc_id"])
            # Before validation, we need to create the new version of the
            # Scheduled Change by combining the old one with the new data.
            # To do this, we need to split the columns up a bit. First,
            # separating the primary scheduled changes columns from the conditions...
            sc_columns, condition_columns = self._splitColumns(row)
            # ...and then combine taking the baseTable parts of sc_columns
            # and combining them with any new values provided in base_what.
            base_columns = {}
            for col in sc_columns:
                if not col.startswith("base_"):
                    continue
                base_col = col.replace("base_", "")
                if base_col in base_what:
                    base_columns[base_col] = base_what[base_col]
                elif sc_columns.get(col):
                    base_columns[base_col] = sc_columns[col]

            # As we need change_type in base_columns and it does not start with "base_". We assign it outside the loop
            base_columns["change_type"] = sc_columns["change_type"]

            # Similarly, we need to integrate the new values for any conditions
            # with the existing ones.
            condition_columns.update(condition_what)

            # Now that we have all that sorted out, we can validate the new values for everything.
            self.validate(base_columns, condition_columns, changed_by, sc_id=sc_columns["sc_id"], transaction=transaction)

            self.conditions.update([self.conditions.sc_id == sc_columns["sc_id"]], condition_columns, changed_by, old_data_version, transaction,
                                   dryrun=dryrun)

        base_what = self._prefixColumns(base_what)
        base_what["scheduled_by"] = changed_by
        super(ScheduledChangeTable, self).update(where, base_what, changed_by, old_data_version, transaction, dryrun=dryrun)

        for sc_id in affected_ids:
            if not self._dataVersionsAreSynced(sc_id, transaction):
                raise MismatchedDataVersionError("Conditions data version is out of sync with main table for sc_id %s" % sc_id)

        for sc_id in affected_ids:
            where_signOff = {"sc_id": sc_id}
            signOffs = self.signoffs.select(where=where_signOff, transaction=transaction, columns=["sc_id", "username"])
            for signOff in signOffs:
                where_signOff.update({"username": signOff["username"]})
                self.signoffs.delete(where=where_signOff, changed_by=changed_by, transaction=transaction)

    def delete(self, where, changed_by=None, old_data_version=None, transaction=None, dryrun=False):
        conditions_where = []
        for row in self.select(where=where, transaction=transaction):
            # verify whether the scheduled change has already been completed or not. If completed,
            # then cannot modify the scheduled change anymore.
            if row.get("complete"):
                raise ValueError("Scheduled change already completed. Cannot delete now.")

            conditions_where.append(self.conditions.sc_id == row["sc_id"])
            base_row = {col[5:]: row[col] for col in row if col.startswith("base_")}
            # we also need change_type in base_row to check permission
            base_row["change_type"] = row["change_type"]
            base_table_where = {pk: row["base_%s" % pk] for pk in self.base_primary_key}
            # TODO: What permissions *should* be required to delete a scheduled change?
            # It seems a bit odd to be checking base table update/insert here. Maybe
            # something broader should be required?
            self._checkBaseTablePermissions(base_table_where, base_row, changed_by, transaction)

        ret = super(ScheduledChangeTable, self).delete(where, changed_by, old_data_version, transaction, dryrun=dryrun)
        self.conditions.delete(conditions_where, changed_by, old_data_version, transaction, dryrun=dryrun)
        return ret

    def enactChange(self, sc_id, enacted_by, transaction=None):
        """Enacts a previously scheduled change by running update or insert on
        the base table."""
        if not self.db.hasPermission(enacted_by, "scheduled_change", "enact", transaction=transaction):
            raise PermissionDeniedError("%s is not allowed to enact scheduled changes", enacted_by)

        sc = self.select(where=[self.sc_id == sc_id], transaction=transaction)[0]
        what = {}
        change_type = sc["change_type"]
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
        # Updating in conditions table also so that history view can work
        # See : https://bugzilla.mozilla.org/show_bug.cgi?id=1333876
        self.conditions.update(where=[self.conditions.sc_id == sc_id], what={},
                               changed_by=sc["scheduled_by"], old_data_version=sc["data_version"],
                               transaction=transaction
                               )
        super(ScheduledChangeTable, self).update(
            where=[self.sc_id == sc_id], what={"complete": True}, changed_by=sc["scheduled_by"], old_data_version=sc["data_version"],
            transaction=transaction
        )

        signoffs = self.signoffs.select(where=[self.signoffs.sc_id == sc_id], transaction=transaction)

        # If the scheduled change had a data version, it means the row already
        # exists, and we need to use update() to enact it.
        if change_type == "delete":
            where = []
            for col in self.base_primary_key:
                where.append((getattr(self.baseTable, col) == sc["base_%s" % col]))
            self.baseTable.delete(where, sc["scheduled_by"], sc["base_data_version"], transaction=transaction, signoffs=signoffs)
        elif change_type == "update":
            where = []
            for col in self.base_primary_key:
                where.append((getattr(self.baseTable, col) == sc["base_%s" % col]))
            self.baseTable.update(where, what, sc["scheduled_by"], sc["base_data_version"], transaction=transaction, signoffs=signoffs)
        elif change_type == "insert":
            self.baseTable.insert(sc["scheduled_by"], transaction=transaction, signoffs=signoffs, **what)
        else:
            raise ValueError("Unknown Change Type")

    def mergeUpdate(self, old_row, what, changed_by, transaction=None):
        """Merges an update to the base table into any changes that may be
        scheduled for the affected row. If the changes are unmergable
        (meaning: the scheduled change and the new version of the row modify
        the same columns), an UpdateMergeError is raised."""

        # Filter the update to only include fields that are different than
        # what's in the base (old_row).
        what = {k: v for k, v in what.items() if v != old_row.get(k)}

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
                if sc["base_%s" % col] != old_row.get(col) and what.get(col) != old_row.get(col):
                    raise UpdateMergeError("Cannot safely merge change to '%s' with scheduled change '%s'", col, sc["sc_id"])

            # If we get here, the change is safely mergeable
            self.update(where=[self.sc_id == sc["sc_id"]], what=what, changed_by=sc["scheduled_by"],
                        old_data_version=sc["data_version"], transaction=transaction)
            self.log.debug("Merged %s into scheduled change '%s'", what, sc["sc_id"])


class RequiredSignoffsTable(AUSTable):
    """RequiredSignoffsTables store and validate information about what types
    and how many signoffs are required for the data provided in
    `decisionColumns`. Subclasses are required to create a Table with the
    necessary columns, and add those columns names to `decisionColumns`.
    When changes are made to a RequiredSignoffsTable, it will look at its own
    rows to determine whether or not that change needs signoff."""

    decisionColumns = []

    def __init__(self, db, dialect):
        self.table.append_column(Column("role", String(50), primary_key=True))
        self.table.append_column(Column("signoffs_required", Integer, nullable=False))

        super(RequiredSignoffsTable, self).__init__(db, dialect, scheduled_changes=True, scheduled_changes_kwargs={"conditions": ["time"]})

    def getPotentialRequiredSignoffs(self, affected_rows, transaction=None):
        potential_required_signoffs = []
        for row in affected_rows:
            if not row:
                continue
            where = {col: row[col] for col in self.decisionColumns}
            potential_required_signoffs.extend(self.select(where=where, transaction=transaction))
        return potential_required_signoffs

    def validate(self, columns, transaction=None):
        for col in self.decisionColumns:
            if columns[col] is None:
                raise ValueError("{} are required.".format(self.decisionColumns))

        if transaction:
            users_with_role, = transaction.execute(
                self.db.permissions.user_roles.t.count().where(self.db.permissions.user_roles.role == columns["role"])
            ).fetchone()
        else:
            users_with_role, = self.getEngine().execute(
                self.db.permissions.user_roles.t.count().where(self.db.permissions.user_roles.role == columns["role"])
            ).fetchone()
        if users_with_role < columns["signoffs_required"]:
            msg = ", ".join([columns[col] for col in self.decisionColumns])
            raise ValueError("Cannot require {} signoffs for {} - only {} users hold the {} role".format(
                columns["signoffs_required"], msg, users_with_role, columns["role"]
            ))

    def insert(self, changed_by, transaction=None, dryrun=False, signoffs=None, **columns):
        self.validate(columns, transaction=transaction)

        if not self.db.hasPermission(changed_by, "required_signoff", "create", transaction=transaction):
            raise PermissionDeniedError("{} is not allowed to create new Required Signoffs.".format(changed_by))

        if not dryrun:
            potential_required_signoffs = self.getPotentialRequiredSignoffs([columns], transaction=transaction)
            verify_signoffs(potential_required_signoffs, signoffs)

        return super(RequiredSignoffsTable, self).insert(changed_by=changed_by, transaction=transaction, dryrun=dryrun, **columns)

    def update(self, where, what, changed_by, old_data_version, transaction=None, dryrun=False, signoffs=None):
        for rs in self.select(where=where, transaction=transaction):
            new_rs = rs.copy()
            new_rs.update(what)
            self.validate(new_rs, transaction=transaction)

            if not self.db.hasPermission(changed_by, "required_signoff", "modify", transaction=transaction):
                raise PermissionDeniedError("{} is not allowed to modify Required Signoffs.".format(changed_by))

            if not dryrun:
                potential_required_signoffs = self.getPotentialRequiredSignoffs([rs, new_rs], transaction=transaction)
                verify_signoffs(potential_required_signoffs, signoffs)

        return super(RequiredSignoffsTable, self).update(where=where, what=what, changed_by=changed_by, old_data_version=old_data_version,
                                                         transaction=transaction, dryrun=dryrun)

    def delete(self, where, changed_by=None, old_data_version=None, transaction=None, dryrun=False, signoffs=None):
        if not self.db.hasPermission(changed_by, "required_signoff", "delete", transaction=transaction):
            raise PermissionDeniedError("{} is not allowed to remove Required Signoffs.".format(changed_by))

        if not dryrun:
            for rs in self.select(where=where, transaction=transaction):
                potential_required_signoffs = self.getPotentialRequiredSignoffs([rs], transaction=transaction)
                verify_signoffs(potential_required_signoffs, signoffs)

        return super(RequiredSignoffsTable, self).delete(where=where, changed_by=changed_by, old_data_version=old_data_version,
                                                         transaction=transaction, dryrun=dryrun)


class ProductRequiredSignoffsTable(RequiredSignoffsTable):

    decisionColumns = ["product", "channel"]

    def __init__(self, db, metadata, dialect):
        self.table = Table("product_req_signoffs", metadata,
                           Column("product", String(15), primary_key=True),
                           Column("channel", String(75), primary_key=True),
                           )
        super(ProductRequiredSignoffsTable, self).__init__(db, dialect)


class PermissionsRequiredSignoffsTable(RequiredSignoffsTable):

    decisionColumns = ["product"]

    def __init__(self, db, metadata, dialect):
        self.table = Table("permissions_req_signoffs", metadata,
                           Column("product", String(15), primary_key=True),
                           )
        super(PermissionsRequiredSignoffsTable, self).__init__(db, dialect)


class SignoffsTable(AUSTable):

    def __init__(self, db, metadata, dialect, baseName):
        self.table = Table("{}_signoffs".format(baseName), metadata,
                           Column("sc_id", Integer, primary_key=True, autoincrement=False),
                           Column("username", String(100), primary_key=True),
                           Column("role", String(50), nullable=False),
                           )
        # Because Signoffs cannot be modified, there's no possibility of an
        # update race, so they do not need to be versioned.
        super(SignoffsTable, self).__init__(db, dialect, versioned=False)

    def insert(self, changed_by=None, transaction=None, dryrun=False, **columns):
        if "sc_id" not in columns or "role" not in columns:
            raise ValueError("sc_id and role must be provided when signing off")
        if "username" in columns and columns["username"] != changed_by:
            raise PermissionDeniedError("Cannot signoff on behalf of another user")
        if not self.db.hasRole(changed_by, columns["role"], transaction=transaction):
            raise PermissionDeniedError("{} cannot signoff with role '{}'".format(changed_by, columns["role"]))

        existing_signoff = self.select({"sc_id": columns["sc_id"], "username": changed_by}, transaction)
        if existing_signoff:
            # It shouldn't be possible for there to be more than one signoff,
            # so not iterating over this should be fine.
            existing_signoff = existing_signoff[0]
            if existing_signoff["role"] != columns["role"]:
                raise PermissionDeniedError("Cannot signoff with a second role")
            # Signoff already made under the same role, we don't need to do
            # anything!
            return

        columns["username"] = changed_by
        super(SignoffsTable, self).insert(changed_by=changed_by, transaction=transaction, dryrun=dryrun, **columns)

    def update(self, where, what, changed_by=None, transaction=None, dryrun=False):
        raise AttributeError("Signoffs cannot be modified (only granted and revoked)")

    def delete(self, where, changed_by=None, transaction=None, dryrun=False):
        for row in self.select(where, transaction):
            if not self.db.hasRole(changed_by, row["role"], transaction=transaction) and not self.db.isAdmin(changed_by, transaction=transaction):
                raise PermissionDeniedError("Cannot revoke a signoff made by someone in a group you do not belong to")

        super(SignoffsTable, self).delete(where, changed_by=changed_by, transaction=transaction, dryrun=dryrun)


class Rules(AUSTable):

    def __init__(self, db, metadata, dialect):
        self.table = Table('rules', metadata,
                           Column('rule_id', Integer, primary_key=True, autoincrement=True),
                           Column('alias', String(50), unique=True),
                           Column('priority', Integer),
                           Column('mapping', String(100)),
                           Column('fallbackMapping', String(100)),
                           Column('backgroundRate', Integer),
                           Column('update_type', String(15), nullable=False),
                           Column('product', String(15)),
                           Column('version', String(75)),
                           Column('channel', String(75)),
                           Column('buildTarget', String(75)),
                           Column('buildID', String(20)),
                           Column('locale', String(200)),
                           Column('osVersion', String(1000)),
                           Column('memory', String(100)),
                           Column('instructionSet', String(1000)),
                           Column('jaws', CompatibleBooleanColumn),
                           Column('mig64', CompatibleBooleanColumn),
                           Column('distribution', String(100)),
                           Column('distVersion', String(100)),
                           Column('headerArchitecture', String(10)),
                           Column('comment', String(500)),
                           )

        AUSTable.__init__(self, db, dialect, scheduled_changes=True)

    def getPotentialRequiredSignoffs(self, affected_rows, transaction=None):
        potential_required_signoffs = []
        # The new row may change the product or channel, so we must look for
        # Signoffs for both.
        for row in affected_rows:
            if not row:
                continue
            where = {}
            # If product isn't present, or is None, it means the Rule affects
            # all products, and we must leave it out of the where clause. If
            # we included it, the query would only match rows where product is
            # NULL.
            if row.get("product"):
                where["product"] = row["product"]
            for rs in self.db.productRequiredSignoffs.select(where=where, transaction=transaction):
                # Channel supports globbing, so we must take that into account
                # before deciding whether or not this is a match.
                if not row.get("channel") or self._matchesRegex(row["channel"], rs["channel"]):
                    potential_required_signoffs.append(rs)
        return potential_required_signoffs

    def _matchesRegex(self, foo, bar):
        # Expand wildcards and use ^/$ to make sure we don't succeed on partial
        # matches. Eg, 3.6* matches 3.6, 3.6.1, 3.6b3, etc.
        # Channel length must be strictly greater than two
        # And globbing is allowed at the end of channel-name only
        if foo.endswith('*'):
            if(len(foo) >= 3):
                test = foo.replace('.', '\.').replace('*', '\*', foo.count('*') - 1)
                test = '^{}.*$'.format(test[:-1])
                if re.match(test, bar):
                    return True
                return False
            else:
                return False
        elif (foo == bar):
            return True
        else:
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

    def _versionMatchesRule(self, ruleVersion, queryVersion):
        """Decides whether a version from the rules matches an incoming version.
           If the ruleVersion is null, we match any queryVersion. If it's not
           null, we must either match exactly, or match a comparison operator."""
        self.log.debug('ruleVersion: %s, queryVersion: %s', ruleVersion, queryVersion)
        if ruleVersion is None:
            return True
        rulesVersionList = ruleVersion.split(",")
        for rule in rulesVersionList:
            if version_compare(queryVersion, rule):
                return True
        return False

    def _buildIDMatchesRule(self, ruleBuildID, queryBuildID):
        """Decides whether a buildID from the rules matches an incoming one.
           If the ruleBuildID is null, we match any queryBuildID. If it's not
           null, we must either match exactly, or match with a camparison
           operator."""
        if ruleBuildID is None:
            return True
        return string_compare(queryBuildID, ruleBuildID)

    def _memoryMatchesRule(self, ruleMemory, queryMemory):
        """Decides whether a memory value from the rules matches an incoming one.
           If the ruleMemory is null, we match any queryMemory. If it's not
           null, we must either match exactly, or match with a camparison
           operator."""
        if ruleMemory is None:
            return True
        return int_compare(queryMemory, ruleMemory)

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

    def _booleanMatchesRule(self, ruleValue, queryValue):
        """As with all other columns, if the value isn't present in the Rule, the Rule matches.
        Unlike other columns, the non-existence of a boolean field in the updateQuery evaluates
        to False, so we need to handle True, False, and None explicitly. Note that None in the
        updateQuery is treated as "unknown", and will cause any Rule without an explicit value
        for the field to match.
        The full truth table is:
        rule | query | matches?
          F      0        Y
          F      1        N
          F     null      N
          T      0        N
          T      1        Y
          T     null      N
        null     0        Y
        null     1        Y
        null    null      Y

        Additional context in https://bugzilla.mozilla.org/show_bug.cgi?id=1386756"""

        if ruleValue is not None:
            if queryValue is None or ruleValue != queryValue:
                return False
        return True

    def _simpleExpressionMatchesSubRule(self, subRuleString, queryString, substring):
        """Performs the actual logical 'AND' operation on a rule as well as partial/full string matching
           for each section of a rule.
           If all parts of the subRuleString match the queryString, then we have successfully resolved the
           logical 'AND' operation and return True.
           Partial matching makes use of Python's "<substring> in <string>" functionality, giving us the ability
           for an incoming rule to match only a substring of a rule.
           Full matching makes use of Python's "<string> in <list>" functionality, giving us the ability for
           an incoming rule to exactly match the whole rule. Currently, incoming rules are comma-separated strings."""
        for rule in subRuleString:
            if substring and rule not in queryString:
                return False
            elif not substring and rule not in queryString.split(','):
                return False
        return True

    def _simpleExpressionMatchesRule(self, ruleString, queryString, substring=True):
        """Decides whether a column from a rule matches an incoming one using simplified boolean logic.
           Only two operators are supported: '&&' (and), ',' (or). A rule like 'AMD,SSE' will match incoming
           rules that contain either 'AMD' or 'SSE'. A rule like 'AMD&&SSE' will only match incoming rules
           that contain both 'AMD' and 'SSE'.
           This function can do substring matching or full string matching. When doing substring matching, a rule
           specifying 'AMD,Windows 10' WILL match an incoming rule such as 'Windows 10.1.2'. When doing full string
           matching, a rule specifying 'AMD,SSE' will NOT match an incoming rule that contains 'SSE3', but WILL match
           an incoming rule that contains either 'AMD' or 'SSE3'."""
        if ruleString is None:
            return True

        decomposedRules = [[rule.strip() for rule in subRule.split('&&')] for subRule in ruleString.split(',')]

        for subRule in decomposedRules:
            if self._simpleExpressionMatchesSubRule(subRule, queryString, substring):
                # We can immediately return True on the first match because this loop is iterating over an OR expression
                # so we need just one match to pass.
                return True
        return False

    def _localeMatchesRule(self, ruleLocales, queryLocale):
        """Decides if a comma seperated list of locales in a rule matches an
        update request"""
        return self._csvMatchesRule(ruleLocales, queryLocale, substring=False)

    def _isAlias(self, id_or_alias):
        if re.match("^[a-zA-Z][a-zA-Z0-9-]*$", str(id_or_alias)):
            return True
        return False

    def insert(self, changed_by, transaction=None, dryrun=False, signoffs=None, **columns):
        if not self.db.hasPermission(changed_by, "rule", "create", columns.get("product"), transaction):
            raise PermissionDeniedError("%s is not allowed to create new rules for product %s" % (changed_by, columns.get("product")))

        if not dryrun:
            potential_required_signoffs = self.getPotentialRequiredSignoffs([columns], transaction=transaction)
            verify_signoffs(potential_required_signoffs, signoffs)

        ret = super(Rules, self).insert(changed_by=changed_by, transaction=transaction, dryrun=dryrun, **columns)
        if not dryrun:
            return ret.inserted_primary_key[0]

    def getOrderedRules(self, where=None, transaction=None):
        """Returns all of the rules, sorted in ascending order"""
        return self.select(where=where, order_by=(self.priority, self.version, self.mapping), transaction=transaction)

    def countRules(self, transaction=None):
        """Returns a number of the count of rules"""
        if transaction:
            count, = transaction.execute(self.t.count()).fetchone()
        else:
            count, = self.getEngine().execute(self.t.count()).fetchone()
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
            if not self._memoryMatchesRule(rule['memory'], updateQuery.get("memory", "")):
                self.log.debug("%s doesn't match %s", rule['memory'], updateQuery.get("memory"))
                continue
            # To help keep the rules table compact, multiple OS versions may be
            # specified in a single rule. They are comma delimited, so we need to
            # break them out and create clauses for each one.
            if not self._simpleExpressionMatchesRule(rule['osVersion'], updateQuery['osVersion']):
                self.log.debug("%s doesn't match %s", rule['osVersion'], updateQuery['osVersion'])
                continue
            if not self._csvMatchesRule(rule['instructionSet'], updateQuery.get('instructionSet', ""), substring=False):
                self.log.debug("%s doesn't match %s", rule['instructionSet'], updateQuery.get('instructionSet'))
                continue
            # Locales may be a comma delimited rule too, exact matches only
            if not self._localeMatchesRule(rule['locale'], updateQuery['locale']):
                self.log.debug("%s doesn't match %s", rule['locale'], updateQuery['locale'])
                continue
            if not self._booleanMatchesRule(rule["mig64"], updateQuery.get("mig64")):
                self.log.debug("%s doesn't match %s", rule['mig64'], updateQuery['mig64'])
                continue
            if not self._booleanMatchesRule(rule["jaws"], updateQuery.get("jaws")):
                self.log.debug("%s doesn't match %s", rule['jaws'], updateQuery['jaws'])
                continue

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

    def update(self, where, what, changed_by, old_data_version, transaction=None, dryrun=False, signoffs=None):
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

        for current_rule in self.select(where=where, transaction=transaction):
            if not self.db.hasPermission(changed_by, "rule", "modify", current_rule["product"], transaction):
                raise PermissionDeniedError("%s is not allowed to modify rules for product %s" % (changed_by, current_rule["product"]))

            new_rule = current_rule.copy()
            new_rule.update(what)
            if not dryrun:
                potential_required_signoffs = self.getPotentialRequiredSignoffs([current_rule, new_rule], transaction=transaction)
                verify_signoffs(potential_required_signoffs, signoffs)

        return super(Rules, self).update(changed_by=changed_by, where=where, what=what, old_data_version=old_data_version,
                                         transaction=transaction, dryrun=dryrun)

    def delete(self, where, changed_by=None, old_data_version=None, transaction=None, dryrun=False, signoffs=None):
        if "rule_id" in where and self._isAlias(where["rule_id"]):
            where["alias"] = where["rule_id"]
            del where["rule_id"]

        product = self.select(where=where, columns=[self.product], transaction=transaction)[0]["product"]
        if not self.db.hasPermission(changed_by, "rule", "delete", product, transaction):
            raise PermissionDeniedError("%s is not allowed to delete rules for product %s" % (changed_by, product))

        if not dryrun:
            for current_rule in self.select(where=where, transaction=transaction):
                potential_required_signoffs = self.getPotentialRequiredSignoffs([current_rule], transaction=transaction)
                verify_signoffs(potential_required_signoffs, signoffs)

        super(Rules, self).delete(changed_by=changed_by, where=where, old_data_version=old_data_version, transaction=transaction, dryrun=dryrun)


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
        self.table.append_column(Column('data', BlobColumn(dataType), nullable=False))
        AUSTable.__init__(self, db, dialect, scheduled_changes=True, scheduled_changes_kwargs={"conditions": ["time"]})

    def getPotentialRequiredSignoffs(self, affected_rows, transaction=None):
        potential_required_signoffs = []
        for row in affected_rows:
            if not row:
                continue
            # Releases do not affect live updates on their own, only the
            # product+channel combinations specified in Rules that point
            # to them. We need to find these Rules, and then return _their_
            # Required Signoffs.
            info = self.getReleaseInfo(name=row["name"], transaction=transaction)
            if info:
                info = info[0]
                for rule_id in info["rule_ids"]:
                    rule = self.db.rules.select(where=[self.db.rules.rule_id == rule_id], transaction=transaction)[0]
                    potential_required_signoffs.extend(self.db.rules.getPotentialRequiredSignoffs([rule], transaction=transaction))
        return potential_required_signoffs

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
        if transaction:
            count, = transaction.execute(self.t.count()).fetchone()
        else:
            count, = self.getEngine().execute(self.t.count()).fetchone()
        return count

    def getReleaseInfo(self, name=None, product=None, limit=None,
                       transaction=None, nameOnly=False, name_prefix=None):
        where = []
        if name:
            where.append(self.name == name)
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
            j = join(self.db.releases.t, self.db.rules.t, ((self.db.releases.name == self.db.rules.mapping) |
                                                           (self.db.releases.name == self.db.rules.fallbackMapping)))
            if transaction:
                ref_list = transaction.execute(select([self.db.releases.name, self.db.rules.rule_id]).select_from(j)).fetchall()
            else:
                ref_list = self.getEngine().execute(select([self.db.releases.name, self.db.rules.rule_id]).select_from(j)).fetchall()

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
                blob = row['data']
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

    def insert(self, changed_by, transaction=None, dryrun=False, signoffs=None, **columns):
        if "name" not in columns or "product" not in columns or "data" not in columns:
            raise ValueError("name, product, and data are all required")

        blob = columns["data"]

        blob.validate(columns["product"], self.domainWhitelist)
        if columns["name"] != blob["name"]:
            raise ValueError("name in database (%s) does not match name in blob (%s)" % (columns["name"], blob["name"]))

        if not self.db.hasPermission(changed_by, "release", "create", columns["product"], transaction):
            raise PermissionDeniedError("%s is not allowed to create releases for product %s" % (changed_by, columns["product"]))

        if not dryrun:
            potential_required_signoffs = self.getPotentialRequiredSignoffs([columns], transaction=transaction)
            verify_signoffs(potential_required_signoffs, signoffs)

        ret = super(Releases, self).insert(changed_by=changed_by, transaction=transaction, dryrun=dryrun, **columns)
        if not dryrun:
            cache.put("blob", columns["name"], {"data_version": 1, "blob": blob})
            cache.put("blob_version", columns["name"], 1)
            return ret.inserted_primary_key[0]

    def update(self, where, what, changed_by, old_data_version, transaction=None, dryrun=False, signoffs=None):
        blob = what.get("data")

        current_releases = self.select(where=where, columns=[self.name, self.product, self.read_only], transaction=transaction)
        for current_release in current_releases:
            name = current_release["name"]
            if "product" in what or "data" in what:
                self._proceedIfNotReadOnly(current_release["name"], transaction=transaction)

            if blob:
                blob.validate(what.get("product", current_release["product"]),
                              self.domainWhitelist)
                name = what.get("name", name)
                if name != blob["name"]:
                    raise ValueError("name in database (%s) does not match name in blob (%s)" % (name, blob.get("name")))

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
                product = what.get("product", current_release["product"])
                # In addition to being able to modify the release overall, users
                # need to be granted explicit access to manipulate the read_only
                # flag. This lets us give out very granular access, which can be
                # very helpful particularly in automation.
                if what["read_only"] is False:
                    if not self.db.hasPermission(changed_by, "release_read_only", "unset", product, transaction):
                        raise PermissionDeniedError("%s is not allowed to mark %s products read write" % (changed_by, what.get("product")))
                elif what["read_only"] is True:
                    if not self.db.hasPermission(changed_by, "release_read_only", "set", product, transaction):
                        raise PermissionDeniedError("%s is not allowed to mark %s products read only" % (changed_by, what.get("product")))

            new_release = current_release.copy()
            new_release.update(what)
            if not dryrun:
                potential_required_signoffs = self.getPotentialRequiredSignoffs([current_release, new_release], transaction=transaction)
                verify_signoffs(potential_required_signoffs, signoffs)

        for release in current_releases:
            name = current_release["name"]
            new_data_version = old_data_version + 1
            try:
                super(Releases, self).update(where={"name": name}, what=what, changed_by=changed_by, old_data_version=old_data_version,
                                             transaction=transaction, dryrun=dryrun)
            except OutdatedDataError as e:
                self.log.warning("Trying to merge update to release %s at data_version %s with the latest version.", name, old_data_version)
                if blob is not None:
                    ancestor_change = self.history.getChange(data_version=old_data_version,
                                                             column_values={'name': name},
                                                             transaction=transaction)
                    # if we have no historical information about the ancestor blob
                    if ancestor_change is None:
                        self.log.exception("Couldn't find history for release %s at data_version %s", name, old_data_version)
                        raise
                    ancestor_blob = ancestor_change.get('data')
                    tip_release = self.getReleases(name=name, transaction=transaction)[0]
                    tip_blob = tip_release.get('data')
                    try:
                        what['data'] = createBlob(merge_dicts(ancestor_blob, tip_blob, blob))
                        self.log.warning("Successfully merged release %s at data_version %s with the latest version.", name, old_data_version)
                    except ValueError:
                        self.log.exception("Couldn't merge release %s at data_version %s with the latest version.", name, old_data_version)
                        # ancestor_change is checked for None a few lines up
                        self.log.warning("ancestor_change is change_id %s, data_version %s",
                                         ancestor_change.get("change_id"), ancestor_change.get("data_version"))
                        self.log.warning("tip release is data_version %s", tip_release.get("data_version"))
                        raise e
                    # we want the data_version for the dictdiffer.merged blob to be one
                    # more than that of the latest blob
                    tip_data_version = tip_release['data_version']
                    super(Releases, self).update(where={"name": name}, what=what, changed_by=changed_by, old_data_version=tip_data_version,
                                                 transaction=transaction, dryrun=dryrun)
                    # cache will have a data_version of one plus the tip
                    # data_version
                    new_data_version = tip_data_version + 1

            if not dryrun:
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
        what = dict(data=releaseBlob)

        self.update(where=where, what=what, changed_by=changed_by, old_data_version=old_data_version,
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

    def isMappedTo(self, name, transaction=None):
        if transaction:
            mapping_count = transaction.execute(self.db.rules.t.count().where(self.db.rules.mapping == name)).fetchone()[0]
            fallbackMapping_count = transaction.execute(self.db.rules.t.count().where(self.db.rules.fallbackMapping == name)).fetchone()[0]
        else:
            mapping_count = self.getEngine().execute(self.db.rules.t.count().where(self.db.rules.mapping == name)).fetchone()[0]
            fallbackMapping_count = self.getEngine().execute(self.db.rules.t.count().where(self.db.rules.fallbackMapping == name)).fetchone()[0]
        if mapping_count > 0 or fallbackMapping_count > 0:
            return True

        return False

    def delete(self, where, changed_by, old_data_version, transaction=None, dryrun=False, signoffs=None):
        release = self.select(where=where, columns=[self.name, self.product], transaction=transaction)
        if len(release) != 1:
            raise ValueError("Where clause must match exactly one release to delete.")
        release = release[0]

        if self.isMappedTo(release["name"], transaction):
            msg = "%s has rules pointing to it. Hence it cannot be deleted." % (release["name"])
            raise ValueError(msg)

        self._proceedIfNotReadOnly(release["name"], transaction=transaction)
        if not self.db.hasPermission(changed_by, "release", "delete", release["product"], transaction):
            raise PermissionDeniedError("%s is not allowed to delete releases for product %s" % (changed_by, release["product"]))

        if not dryrun:
            potential_required_signoffs = self.getPotentialRequiredSignoffs([release], transaction=transaction)
            verify_signoffs(potential_required_signoffs, signoffs)

        super(Releases, self).delete(where=where, changed_by=changed_by, old_data_version=old_data_version, transaction=transaction,
                                     dryrun=dryrun)
        if not dryrun:
            cache.invalidate("blob", release["name"])
            cache.invalidate("blob_version", release["name"])

    def isReadOnly(self, name, limit=None, transaction=None):
        where = [self.name == name]
        column = [self.read_only]
        row = self.select(where=where, columns=column, limit=limit, transaction=transaction)[0]
        return row['read_only']

    def _proceedIfNotReadOnly(self, name, limit=None, transaction=None):
        if self.isReadOnly(name, limit, transaction):
            raise ReadOnlyError("Release '%s' is read only" % name)


class UserRoles(AUSTable):

    def __init__(self, db, metadata, dialect):
        self.table = Table("user_roles", metadata,
                           Column("username", String(100), primary_key=True),
                           Column("role", String(50), primary_key=True),
                           )
        super(UserRoles, self).__init__(db, dialect)

    def update(self, where, what, changed_by, old_data_version, transaction=None, dryrun=False):
        raise AttributeError("User roles cannot be modified (only granted and revoked)")


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
        "required_signoff": ["products"],
        "scheduled_change": ["actions"],
    }

    def __init__(self, db, metadata, dialect):
        self.table = Table('permissions', metadata,
                           Column('permission', String(50), primary_key=True),
                           Column('username', String(100), primary_key=True),
                           Column('options', JSONColumn)
                           )
        self.user_roles = UserRoles(db, metadata, dialect)
        AUSTable.__init__(self, db, dialect, scheduled_changes=True, scheduled_changes_kwargs={"conditions": ["time"]})

    def getPotentialRequiredSignoffs(self, affected_rows, transaction=None):
        potential_required_signoffs = []
        for row in affected_rows:
            if not row:
                continue
            # XXX: This kindof sucks because it means that we don't have great control
            # over the signoffs required permissions that don't specify products, or
            # don't support them.
            if "products" in self.allPermissions[row["permission"]] and row.get("options") and row["options"].get("products"):
                for product in row["options"]["products"]:
                    potential_required_signoffs.extend(self.db.permissionsRequiredSignoffs.select(where={"product": product}, transaction=transaction))
            else:
                potential_required_signoffs.extend(self.db.permissionsRequiredSignoffs.select(transaction=transaction))
        return potential_required_signoffs

    def assertPermissionExists(self, permission):
        if permission not in self.allPermissions.keys():
            raise ValueError('Unknown permission "%s"' % permission)

    def assertOptionsExist(self, permission, options):
        for opt in options:
            if opt not in self.allPermissions[permission]:
                raise ValueError('Unknown option "%s" for permission "%s"' % (opt, permission))

    def getAllUsers(self, transaction=None):
        res_permissions = self.select(columns=[self.username], distinct=True, transaction=transaction)
        res_roles = self.user_roles.select(columns=[self.user_roles.username], transaction=transaction)
        res = res_roles + res_permissions
        return list(set([r['username'] for r in res]))

    def getAllPermissions(self, transaction=None):
        ret = defaultdict(dict)
        for r in self.select(transaction=transaction):
            ret[r["username"]][r["permission"]] = r["options"]
        return ret

    def countAllUsers(self, transaction=None):
        res = self.select(columns=[self.username], distinct=True, transaction=transaction)
        return len(res)

    def insert(self, changed_by, transaction=None, dryrun=False, signoffs=None, **columns):
        if "permission" not in columns or "username" not in columns:
            raise ValueError("permission and username are required")

        self.assertPermissionExists(columns["permission"])
        if columns.get("options"):
            self.assertOptionsExist(columns["permission"], columns["options"])

        if not self.db.hasPermission(changed_by, "permission", "create", transaction=transaction):
            raise PermissionDeniedError("%s is not allowed to grant permissions" % changed_by)

        if not dryrun:
            potential_required_signoffs = self.getPotentialRequiredSignoffs([columns], transaction=transaction)
            verify_signoffs(potential_required_signoffs, signoffs)

        self.log.debug("granting %s to %s with options %s", columns["permission"], columns["username"],
                       columns.get("options"))
        super(Permissions, self).insert(changed_by=changed_by, transaction=transaction, dryrun=dryrun, **columns)
        self.log.debug("successfully granted %s to %s with options %s", columns["permission"],
                       columns["username"], columns.get("options"))

    def grantRole(self, username, role, changed_by, transaction=None):
        if not self.hasPermission(changed_by, "permission", "create", transaction=transaction):
            raise PermissionDeniedError("%s is not allowed to grant user roles" % changed_by)

        if len(self.getUserPermissions(username, transaction)) < 1:
            raise ValueError("Cannot grant a role to a user without any permissions")

        self.log.debug("granting {} role to {}".format(role, username))
        return self.user_roles.insert(changed_by, transaction, username=username, role=role)

    def update(self, where, what, changed_by, old_data_version, transaction=None, dryrun=False, signoffs=None):
        if "permission" in what:
            self.assertPermissionExists(what["permission"])

        for current_permission in self.select(where=where, transaction=transaction):
            if what.get("options"):
                self.assertOptionsExist(what.get("permission", current_permission["permission"]), what["options"])

            if not self.db.hasPermission(changed_by, "permission", "modify", transaction=transaction):
                raise PermissionDeniedError("%s is not allowed to modify permissions" % changed_by)

            new_permission = current_permission.copy()
            new_permission.update(what)
            if not dryrun:
                potential_required_signoffs = self.getPotentialRequiredSignoffs([current_permission, new_permission], transaction=transaction)
                verify_signoffs(potential_required_signoffs, signoffs)

        super(Permissions, self).update(where=where, what=what, changed_by=changed_by, old_data_version=old_data_version,
                                        transaction=transaction, dryrun=dryrun)

    def delete(self, where, changed_by=None, old_data_version=None, transaction=None, dryrun=False, signoffs=None):
        if not self.db.hasPermission(changed_by, "permission", "delete", transaction=transaction):
            raise PermissionDeniedError("%s is not allowed to revoke permissions", changed_by)

        usernames = set()
        for current_permission in self.select(where=where, transaction=transaction):
            usernames.add(current_permission["username"])
            if not dryrun:
                potential_required_signoffs = self.getPotentialRequiredSignoffs([current_permission], transaction=transaction)
                verify_signoffs(potential_required_signoffs, signoffs)

        if not dryrun:
            super(Permissions, self).delete(changed_by=changed_by, where=where, old_data_version=old_data_version, transaction=transaction)

            for u in usernames:
                if len(self.getUserPermissions(u, transaction)) == 0:
                    for role in self.user_roles.select([self.user_roles.username == u], transaction=transaction):
                        self.revokeRole(u, role["role"], changed_by=changed_by, old_data_version=role["data_version"], transaction=transaction)

    def revokeRole(self, username, role, changed_by=None, old_data_version=None, transaction=None):
        if not self.hasPermission(changed_by, "permission", "delete", transaction=transaction):
            raise PermissionDeniedError("%s is not allowed to revoke user roles", changed_by)

        role_signoffs = self.db.permissionsRequiredSignoffs.select(where={"role": role}, transaction=transaction)
        role_signoffs += self.db.productRequiredSignoffs.select(where={"role": role}, transaction=transaction)
        if role_signoffs:
            required = max([rs["signoffs_required"] for rs in role_signoffs])
            users_with_role = len(self.user_roles.select(where={"role": role}, transaction=transaction))
            if required > (users_with_role - 1):
                raise ValueError("Revoking {} role would make it impossible for Required Signoffs to be fulfilled".format(role))

        return self.user_roles.delete({"username": username, "role": role}, changed_by=changed_by, old_data_version=old_data_version, transaction=transaction)

    def getPermission(self, username, permission, transaction=None):
        try:
            return self.select(where=[self.username == username, self.permission == permission], transaction=transaction)[0]
        except IndexError:
            return {}

    def getUserPermissions(self, username, transaction=None):
        rows = self.select(columns=[self.permission, self.options, self.data_version], where=[self.username == username], transaction=transaction)
        ret = dict()
        for row in rows:
            ret[row["permission"]] = {
                "options": row["options"],
                "data_version": row["data_version"]
            }
        return ret

    def getOptions(self, username, permission, transaction=None):
        ret = self.select(columns=[self.options], where=[self.username == username, self.permission == permission], transaction=transaction)
        if ret:
            return ret[0]["options"]
        else:
            raise ValueError('Permission "%s" doesn\'t exist' % permission)

    def getUserRoles(self, username, transaction=None):
        res = self.user_roles.select(where=[self.user_roles.username == username],
                                     columns=[self.user_roles.role, self.user_roles.data_version],
                                     distinct=True, transaction=transaction)
        return [{"role": r["role"], "data_version": r["data_version"]} for r in res]

    def getAllRoles(self, transaction=None):
        res = self.user_roles.select(columns=[self.user_roles.role], distinct=True, transaction=transaction)
        return [r["role"] for r in res]

    def isAdmin(self, username, transaction=None):
        return bool(self.getPermission(username, "admin", transaction))

    def hasPermission(self, username, thing, action, product=None, transaction=None):
        perm = self.getPermission(username, "admin", transaction=transaction)
        if perm:
            options = perm["options"]
            if options and options.get("products") and product not in options["products"]:
                # Supporting product-wise admin permissions. If there are no options
                # with admin, we assume that the user has admin access over all
                # products.
                return False
            return True

        perm = self.getPermission(username, thing, transaction=transaction)
        if perm:
            options = perm["options"]
            if options:
                # If a user has a permission that doesn't explicitly limit the type of
                # actions they can perform, they are allowed to do any type of action.
                if options.get("actions") and action not in options["actions"]:
                    return False
                # Similarly, permissions without products specified grant that
                # that permission without any limitation on the product.
                if options.get("products") and product not in options["products"]:
                    return False
            return True

        return False

    def hasRole(self, username, role, transaction=None):
        roles_list = [r['role'] for r in self.getUserRoles(username, transaction)]
        return role in roles_list


class Dockerflow(AUSTable):
    def __init__(self, db, metadata, dialect):
        self.table = Table('dockerflow', metadata, Column('watchdog', Integer, nullable=False))
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

        self._putWatchdogValue(changed_by=changed_by, value=value, where=where, transaction=transaction, dryrun=dryrun)

        return value['watchdog']

    def _putWatchdogValue(self, changed_by, value, where=None, transaction=None, dryrun=False):
        if where is None:
            super(Dockerflow, self).insert(changed_by=changed_by, transaction=transaction, dryrun=dryrun, watchdog=value['watchdog'])
        else:
            super(Dockerflow, self).update(where=where, what=value, changed_by=changed_by, transaction=transaction, dryrun=dryrun)


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
               body, use_tls):
    from email.mime.text import MIMEText
    from smtplib import SMTP

    msg = MIMEText("\n".join(body), "plain")
    msg["Subject"] = subj
    msg["from"] = from_addr

    try:
        conn = SMTP()
        conn.connect(relayhost, port)
        conn.ehlo()
        if use_tls:
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


def make_change_notifier(relayhost, port, username, password, to_addr, from_addr, use_tls):
    def bleet(table, type_, changed_by, query, transaction):
        body = ["Changed by: %s" % changed_by]
        if type_ == "UPDATE":
            body.append("Row(s) to be updated as follows:")
            where = [c for c in query._whereclause.get_children()]
            changed = {}
            unchanged = {}
            for row in table.select(where=where, transaction=transaction):
                for k in row:
                    if query.parameters[k] != row[k]:
                        changed[k] = UnquotedStr("%s ---> %s" % (repr(row[k]), repr(query.parameters[k])))
                    else:
                        unchanged[k] = UnquotedStr("%s" % repr(row[k]))
                body.append('Changed values:')
                body.append(UTF8PrettyPrinter().pformat(changed))
                body.append('\nUnchanged:')
                body.append(UTF8PrettyPrinter().pformat(unchanged))
            body.append('\n\n')
        elif type_ == "DELETE":
            body.append("Row(s) to be removed:")
            where = [c for c in query._whereclause.get_children()]
            for row in table.select(where=where, transaction=transaction):
                body.append(UTF8PrettyPrinter().pformat(row))
        elif type_ == "INSERT":
            body.append("Row to be inserted:")
            body.append(UTF8PrettyPrinter().pformat(query.parameters))

        subj = "%s to %s detected %s" % (type_, table.t.name, generate_random_string(6))
        send_email(relayhost, port, username, password, to_addr, from_addr,
                   table, subj, body, use_tls)
        table.log.debug("Sending change notification mail for %s to %s", table.t.name, to_addr)
    return bleet


def generate_random_string(length):
    import string
    import random

    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                   for _ in range(length))


def make_change_notifier_for_read_only(relayhost, port, username, password, to_addr, from_addr, use_tls):
    def bleet(table, type_, changed_by, query, transaction):
        body = ["Changed by: %s" % changed_by]
        where = [c for c in query._whereclause.get_children()]
        # TODO: How are we sometimes (always?) getting no rows for this. It shouldn't be possible...
        # It's possible that the where clause is not getting extracted properly.
        rows = table.select(where=where, transaction=transaction)
        if rows:
            row = rows[0]
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
                           table, subj, body, use_tls)
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
        self.productRequiredSignoffsTable = ProductRequiredSignoffsTable(self, self.metadata, dialect)
        self.permissionsRequiredSignoffsTable = PermissionsRequiredSignoffsTable(self, self.metadata, dialect)
        self.metadata.bind = self.engine

    def setDomainWhitelist(self, domainWhitelist):
        self.releasesTable.setDomainWhitelist(domainWhitelist)

    def setupChangeMonitors(self, relayhost, port, username, password, to_addr, from_addr, use_tls=False, notify_tables=None):
        bleeter = make_change_notifier(relayhost, port, username, password, to_addr, from_addr, use_tls)
        if notify_tables is None:
            notify_tables = (
                self.rules, self.rules.scheduled_changes, self.rules.scheduled_changes.signoffs,
                self.permissions, self.permissions.user_roles, self.permissions.scheduled_changes, self.permissions.scheduled_changes.signoffs,
                self.productRequiredSignoffs, self.productRequiredSignoffs.scheduled_changes, self.productRequiredSignoffs.scheduled_changes.signoffs,
                self.permissionsRequiredSignoffs, self.permissionsRequiredSignoffs.scheduled_changes,
                self.permissionsRequiredSignoffs.scheduled_changes.signoffs,
                self.releases.scheduled_changes, self.releases.scheduled_changes.signoffs,
            )

        for t in notify_tables:
            t.onInsert = bleeter
            t.onUpdate = bleeter
            t.onDelete = bleeter

        read_only_bleeter = make_change_notifier_for_read_only(relayhost, port,
                                                               username,
                                                               password,
                                                               to_addr,
                                                               from_addr,
                                                               use_tls)
        self.releases.onUpdate = read_only_bleeter

    def isAdmin(self, *args, **kwargs):
        return self.permissions.isAdmin(*args, **kwargs)

    def hasPermission(self, *args, **kwargs):
        return self.permissions.hasPermission(*args, **kwargs)

    def hasRole(self, *args, **kwargs):
        return self.permissions.hasRole(*args, **kwargs)

    def getUserRoles(self, *args, **kwargs):
        return self.permissions.getUserRoles(*args, **kwargs)

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
        if version < 21:
            raise ValueError("Cannot downgrade below version 21")
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
    def productRequiredSignoffs(self):
        return self.productRequiredSignoffsTable

    @property
    def permissionsRequiredSignoffs(self):
        return self.permissionsRequiredSignoffsTable

    @property
    def dockerflow(self):
        return self.dockerflowTable
