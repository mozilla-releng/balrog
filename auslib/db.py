from datetime import datetime
import re
import simplejson as json

from sqlalchemy import Table, Column, Integer, Text, String, MetaData, \
  CheckConstraint, create_engine, select, Boolean, DateTime
from sqlalchemy.exc import IntegrityError

import logging
log = logging.getLogger(__name__)

def convertRows(fn):
    def rowsToDict(*args, **kwargs):
        ret = []
        for row in fn(*args, **kwargs):
            d = {}
            for key in row.keys():
                d[key] = row[key]
            ret.append(d)
        return ret
    return rowsToDict

class AlreadySetupError(Exception):
    def __str__(self):
        return "Can't connect to new database, still connected to previous one"

class PermissionDeniedError(Exception):
    pass

class AUSTable(object):
    def __init__(self, history=True):
        # Mirror the columns as attributes for easy access
        for col in self.table.get_children():
            setattr(self, col.name, col)
        self.t = self.table
        # Set-up a history table to do logging in, if required
        if history:
            self.history = History(self.t.metadata, self)

    # Can't do this in the constructor, because the engine is always
    # unset when we're instantiated
    def getEngine(self):
        return self.t.metadata.bind

    @convertRows
    def select(self, columns=None, where=None, order_by=None, limit=None, distinct=False):
        if columns:
            query = select(columns, order_by=order_by, limit=limit, distinct=distinct)
        else:
            query = self.t.select(order_by=order_by, limit=limit, distinct=distinct)
        if where:
            for cond in where:
                query = query.where(cond)
        return query.execute().fetchall()

    def insert(self, changed_by, **columns):
        conn = self.getEngine().connect()
        trans = conn.begin()
        try:
            if self.history:
                conn.execute(self.history.t.insert(values=dict(changed_by=changed_by, timestamp=datetime.now())))
            ret = conn.execute(self.t.insert(values=columns))
            trans.commit()
            return ret
        except:
            trans.rollback()
            raise

    def delete(self, changed_by, where):
        conn = self.getEngine().connect()
        trans = conn.begin()
        try:
            if self.history:
                for row in self.select(where=where):
                    # Tack on history table information to the row
                    row['changed_by'] = changed_by
                    row['timestamp'] = datetime.now()
                    # XXX: would be nice if we could use self.history.insert()
                    conn.execute(self.history.t.insert(values=row))
            query = self.t.delete()
            if where:
                for cond in where:
                    query = query.where(cond)
            ret = conn.execute(query)
            trans.commit()
            return ret
        except:
            trans.rollback()
            raise

    def update(self, changed_by, where, what):
        conn = self.getEngine().connect()
        trans = conn.begin()
        try:
            if self.history:
                for row in self.select(where=where):
                    row['changed_by'] = changed_by
                    row['timestamp'] = datetime.now()
                    conn.execute(self.history.t.insert(values=row))
            query = self.t.update(values=what)
            if where:
                for cond in where:
                    query = query.where(cond)
            ret = conn.execute(query)
            trans.commit()
            return ret
        except:
            trans.rollback()
            raise

class History(AUSTable):
    def __init__(self, metadata, baseTable):
        self.table = Table('%s_history' % baseTable.t.name, metadata,
            Column('change_id', Integer, primary_key=True, autoincrement=True),
            Column('changed_by', String),
            Column('timestamp', DateTime)
        )
        for col in baseTable.t.get_children():
            newcol = col.copy()
            newcol.primary_key = False
            newcol.nullable = True
            self.table.append_column(newcol)
        AUSTable.__init__(self, history=False)

class UpdatePaths(AUSTable):
    def __init__(self, metadata):
        self.table = Table('update_paths', metadata,
            Column('rule_id', Integer, primary_key=True, autoincrement=True),
            Column('priority', Integer),
            Column('mapping', String),
            Column('throttle', Integer, CheckConstraint('0 <= throttle <= 100')),
            Column('update_type', String),
            Column('product', String),
            Column('version', String),
            Column('channel', String),
            Column('buildTarget', String),
            Column('buildID', String),
            Column('locale', String),
            Column('osVersion', String),
            Column('distribution', String),
            Column('distVersion', String),
            Column('headerArchitecture', String),
            Column('comment', String)
        )
        AUSTable.__init__(self)

    def matchesRegex(self, foo, bar):
        # Expand wildcards and use ^/$ to make sure we don't succeed on partial
        # matches.
        test = foo.replace('.','\.').replace('*','.*')
        test = '^%s$' % test
        if re.match(test, bar):
            return True
        return False

    def _versionMatchesRule(self, ruleVersion, queryVersion):
        """Decides whether a version from the rules matches an incoming version.
           If the ruleVersion is null, we match any queryVersion. If it's not
           null, we must either match exactly, or match a potential wildcard."""
        if ruleVersion == None:
            return True
        if self.matchesRegex(ruleVersion, queryVersion):
            return True

    def _channelMatchesRule(self, ruleChannel, queryChannel, fallbackChannel):
        """Decides whether a channel from the rules matchs an incoming one.
           If the ruleChannel is null, we match any queryChannel. We also match
           if the channels match exactly, or match after wildcards in ruleChannel
           are resolved. Channels may have a fallback specified, too, so we must
           check if the fallback version of the queryChannel matches the ruleChannel."""
        if ruleChannel == None:
            return True
        if self.matchesRegex(ruleChannel, queryChannel):
            return True
        if self.matchesRegex(ruleChannel, fallbackChannel):
            return True

    def getOrderedRules(self):
        """Returns all of the rules, sorted in ascending order"""
        return self.select(order_by=(self.priority, self.version, self.mapping))

    def getRulesMatchingQuery(self, name, product, version, channel, fallbackChannel,
                              buildTarget, buildID, locale, osVersion,
                              distribution, distVersion, headerArchitecture):
        """Returns all of the rules that match the given update query"""
        matchingRules = []
        rules = self.select(
            where=[
                (self.throttle > 0) &
                ((self.product==product) | (self.product==None)) &
                ((self.buildTarget==buildTarget) | (self.buildTarget==None)) &
                ((self.buildID==buildID) | (self.buildID==None)) &
                ((self.locale==locale) | (self.locale==None)) &
                ((self.osVersion==osVersion) | (self.osVersion==None)) &
                ((self.distribution==distribution) | (self.distribution==None)) &
                ((self.distVersion==distVersion) | (self.distVersion==None)) &
                ((self.headerArchitecture==headerArchitecture) | (self.headerArchitecture==None))
            ]
        )
        log.debug("UpdatePaths.getRulesMatchingQuery: Raw matches:")
        for rule in rules:
            log.debug("UpdatePaths.getRulesMatchingQuery: %s", rule)
            # Resolve special means for version and channel, dropping
            # rules that don't match after resolution.
            if not self._versionMatchesRule(rule['version'], version):
                log.debug("UpdatePaths.getRulesMatchingQuery: %s doesn't match %s", rule['version'], version)
                continue
            if not self._channelMatchesRule(rule['channel'], channel, fallbackChannel):
                log.debug("UpdatePaths.getRulesMatchingQuery: %s doesn't match %s", rule['channel'], channel)
                continue
            # Drop any rules which would update ourselves to the same version
            if rule['mapping'] == name:
                continue
            matchingRules.append(rule)
        log.debug("UpdatePaths.getRulesMatchingQuery: Reduced matches:")
        for r in matchingRules:
            log.debug("UpdatePaths.getRulesMatchingQuery: %s", r)
        return matchingRules

class Releases(AUSTable):
    def __init__(self, metadata):
        self.table = Table('releases', metadata,
            Column('name', String),
            Column('product', String),
            Column('version', String),
            Column('data', Text)
        )
        AUSTable.__init__(self)

    def getReleases(self, name=None, product=None, version=None, limit=None):
        where = []
        if name:
            where.append(self.name==name)
        if product:
            where.append(self.product==product)
        if version:
            where.append(self.version==version)
        rows = AUSTable.select(self, where=where, limit=limit)
        for row in rows:
            row['data'] = json.loads(row['data'])
        return rows

class Permissions(AUSTable):
    def __init__(self, metadata):
        self.table = Table('permissions', metadata,
            Column('permission', String, primary_key=True),
            Column('username', String, primary_key=True),
            Column('options', String)
        )
        AUSTable.__init__(self)

    def canEditUsers(self, username):
        where=[
            (self.username==username) &
            ((self.permission=='editusers') | (self.permission=='admin'))
        ]
        if self.select(where=where):
            return True
        return False

    def getAllUsers(self):
        res = self.select(columns=[self.username], distinct=True)
        return [r['username'] for r in res]

    def grantPermission(self, changed_by, username, permission, options=None):
        if not self.canEditUsers(changed_by):
            raise PermissionDeniedError('%s is not allowed to grant permissions' % changed_by)
        columns = dict(username=username, permission=permission)
        if options:
            columns['options'] = options
        self.insert(changed_by=changed_by, **columns)

    def updatePermission(self, changed_by, username, orig_permission, new_permission, options=None):
        where = [self.username==username, self.permission==orig_permission]
        what = dict(permission=new_permission)
        if options:
            what['options'] = options
        self.update(changed_by=changed_by, where=where, what=what)

    def revokePermission(self, changed_by, username, permission, options=None):
        where = [self.username==username, self.permission==permission]
        if options:
            where.append(self.options==options)
        self.delete(changed_by=changed_by, where=where)

    def getUserPermissions(self, username):
        return self.select(columns=['permission', 'options'], where=[self.username==username])

    def getPermission(self, username, permission):
        ret = self.select(columns=['options'], where=[self.username==username, self.permission==permission])
        if ret:
            return ret[0]

class AUSDatabase(object):
    engine = None
    metadata = MetaData()
    updatePathsTable = UpdatePaths(metadata)
    releasesTable = Releases(metadata)
    permissionsTable = Permissions(metadata)

    def __init__(self, dburi=None):
        """Create a new AUSDatabase. Before this object is useful, dburi must be
           set, either through the constructor or setDburi()"""
        if dburi:
            self.setDburi(dburi)

    def setDburi(self, dburi):
        """Setup the database connection. Note that SQLAlchemy only opens a connection
           to the database when it needs to, however."""
        self.dburi = dburi
        if self.engine:
            raise AlreadySetupError()
        self.engine = create_engine(self.dburi)
        self.metadata.bind = self.engine
        self.metadata.create_all()

    def reset(self):
        self.engine = None
        self.metadata.bind = None

    @property
    def updatePaths(self):
        return self.updatePathsTable

    @property
    def releases(self):
        return self.releasesTable

    @property
    def permissions(self):
        return self.permissionsTable
