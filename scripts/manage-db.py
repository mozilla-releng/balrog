#!/usr/bin/env python

import itertools
import logging
from os import path, popen
from sqlalchemy.engine.url import make_url
import sys
import json

logging.basicConfig(level=logging.INFO)

# Our parent directory should contain the auslib module, so we add it to the
# PYTHONPATH to make things easier on consumers.
sys.path.append(path.join(path.dirname(__file__), ".."))
sys.path.append(path.join(path.dirname(__file__), path.join("..", "vendor", "lib", "python")))

from auslib.db import AUSDatabase


def cleanup_releases(trans, nightly_age, dryrun=True):
    # This and the subsequent queries use "%%%%%" because we end up going
    # through two levels of Python string formatting. The first is here,
    # and the second happens at a low level of SQLAlchemy when the transaction
    # is being executed.
    query = """
LEFT JOIN rules rules_mapping ON (name=rules_mapping.mapping)
LEFT JOIN rules rules_whitelist ON (name=rules_whitelist.whitelist)
WHERE name LIKE '%%%%nightly%%%%'
AND name NOT LIKE '%%%%latest'
AND rules_whitelist.whitelist IS NULL
AND rules_mapping.mapping IS NULL
AND (STR_TO_DATE(RIGHT(name, 14), "%%%%Y%%%%m%%%%d%%%%H%%%%i%%%%S") < NOW() - INTERVAL %s DAY);
""" % nightly_age
    if dryrun:
        todelete = trans.execute("SELECT name FROM releases" + query).fetchall()
        print "Releases rows to be deleted:"
        if todelete:
            print "\n".join(itertools.chain(*todelete))
        else:
            print "  - None"
    else:
        trans.execute("DELETE releases FROM releases" + query)


def cleanup_releases_history(trans, dryrun=True):
    num_to_delete = 100
    queries = dict(
        dated="""
            SELECT name, change_id
            FROM releases_history
            WHERE name LIKE '%%%%latest'
              AND timestamp<1000*UNIX_TIMESTAMP(NOW()-INTERVAL 14 DAY)
            ORDER BY change_id
            LIMIT %d """ % num_to_delete,
        nightly="""
            SELECT name, change_id
            FROM releases_history
            WHERE name LIKE '%%%%nightly%%%%'
              AND name NOT LIKE '%%%%latest'
              AND timestamp<1000*UNIX_TIMESTAMP(NOW()-INTERVAL 7 DAY)
            ORDER BY change_id
            LIMIT %d """ % num_to_delete
    )

    total_deleted = 0

    for name, query in queries.items():
        if dryrun:
            todelete = trans.execute(query).fetchall()
            if todelete:
                print "releases_history (%s) rows to be deleted:" % name
                for key, group in itertools.groupby(todelete, lambda x: x[0]):
                    print "  - %s: %s history rows" % (key, len(list(group)))
        else:
            del_query = """
                DELETE R.*
                FROM releases_history R
                WHERE R.change_id IN (   -- use a subquery to work around mysql limitation
                    SELECT X.change_id   -- of select'ing from the same table as a DML
                    FROM ( """ + query + ") X)"

            results = trans.execute(del_query)
            if results:
                print "Deleted %s '%s' records" % (results.rowcount, name)
                total_deleted += results.rowcount

    print "Total Deleted: %d" % total_deleted


def _extract_partials(json_object):
    """Returns a generator that contains \
    all value objects having key as 'partials'"""
    if isinstance(json_object, dict):
        for key, value in json_object.iteritems():
            if key == "partials":
                yield value
            else:
                for child_val in _extract_partials(value):
                    yield child_val

    elif isinstance(json_object, list):
        for item in json_object:
            for value in _extract_partials(item):
                yield value
    else:
        pass


def extract_active_data(trans,url, dump_location='dump.sql'):
    """
    Stores sqldump data in the specified location. If not specified, stores it in current directory in file dump.sql
    If file already exists it will override that file and not append it.

    Function added in to enhance testing in Balrog's stage environment.

    :param url: Database. eg : mysql://balrogadmin:balrogadmin@balrogdb/balrog
    :param dump_location: location where sqldump file must be created
    """
    url = make_url(url)
    user = url.username
    password = url.password
    host = url.host
    database = url.database
    port = url.port

    mysql_default_command = ' '.join((
        'mysqldump',
        '-h %s' % host,
        '-u %s' % user,
        '-p%s' % password,
        '' if port is None else '-P %s' % port,
        # Prevent socket from being used, so that balrogdb in docker can be called from localhost (via port forwarding for instance)
        '--protocol=tcp',
        '--single-transaction',
        '--lock-tables=false',
    ))

    popen(
        _strip_multiple_spaces('%s %s dockerflow rules rules_history rules_scheduled_changes rules_scheduled_changes_conditions \
        rules_scheduled_changes_conditions_history rules_scheduled_changes_signoffs rules_scheduled_changes_signoffs_history \
        rules_scheduled_changes_history migrate_version  > %s' % (mysql_default_command, database, dump_location))
    )

    popen(
        _strip_multiple_spaces('%s %s releases --where="EXISTS ( \
            SELECT * \
            FROM rules, rules_scheduled_changes \
            WHERE releases.name = rules.mapping \
               OR releases.name = rules.whitelist \
               OR releases.name = rules_scheduled_changes.base_mapping \
               OR releases.name = rules_scheduled_changes.base_whitelist \
            )" \
        >> %s' % (mysql_default_command, database, dump_location))
    )

    popen(
        _strip_multiple_spaces('%s %s releases_history --where="releases_history.name=\'Firefox-mozilla-central-nightly-latest\' \
        limit 50" >> %s' % (mysql_default_command, database, dump_location))
    )

    popen(
        _strip_multiple_spaces('%s --skip-add-drop-table --no-create-info %s releases_history --where "name = ( \
            SELECT rules.mapping \
            FROM rules \
            WHERE rules.alias=\'firefox-release\' \
        ) LIMIT 50" >> %s' % (mysql_default_command, database, dump_location))
    )

    query_release_mapping = """SELECT rules.mapping \
            FROM rules \
            WHERE rules.mapping IS NOT NULL \
            UNION \
            SELECT rules.fallbackMapping \
            FROM rules \
            WHERE rules.fallbackMapping IS NOT NULL \
            UNION \
            SELECT rules.whitelist \
            FROM rules \
            WHERE rules.whitelist IS NOT NULL"""

    popen(_strip_multiple_spaces('''%s %s releases --where="releases.name IN (%s)" \
        >> %s''' % (mysql_default_command, database, query_release_mapping, dump_location)))

    query_release = """SELECT * \
    FROM releases \
    WHERE releases.name IN (%s)""" % query_release_mapping

    result = trans.execute(query_release).fetchall()
    partial_release_names = []
    for row in result:
        row_data = None
        try:
            row_data = json.loads(row['data'])
        except ValueError:
            continue
        partials_generator = _extract_partials(row_data)
        for item in partials_generator:
            if isinstance(item, dict):
                partial_release_names.extend(list(item.keys()))
            elif isinstance(item, list):
                for list_item in item:
                    if 'from' in list_item:
                        partial_release_names.append(str(list_item['from']))
            else:
                pass
    if partial_release_names:
        qry = ', '.join('"' + release_names + '"' for release_names in partial_release_names)
        popen(_strip_multiple_spaces('''%s %s releases --where="releases.name IN (%s)" \
                >> %s''' % (mysql_default_command, database, qry, dump_location)))


def _strip_multiple_spaces(string):
    return ' '.join(string.split())


if __name__ == "__main__":
    from optparse import OptionParser
    usage = """%s --db dburi action [options]\n""" % sys.argv[0]
    usage += "Possible actions:\n"
    usage += "  create: Create all the tables required for a new Balrog database\n"
    usage += "  upgrade: Upgrade an existing balrog table to a newer version.\n"
    usage += "  downgrade: Downgrade an existing balrog table to an older version.\n"
    usage += "  extract: Extracts active data for testing. Enter an extra arg to specify the location and filename for\
            the data to stored in. "
    usage += "  cleanup: Cleanup old data from a database. Requires an extra arg of maximum age (in days) of nightly releases. " \
             "Anything older than this will be deleted.\n"
    usage += "  cleanup-dryrun: Show what would be removed if 'cleanup' is run."
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--db", dest="db", default=None, help="database to manage, in URI format")
    parser.add_option("--version", dest="version", default=None, type="int", help="Create/upgrade to this specific schema version rather than the latest.")
    options, args = parser.parse_args()

    if not options.db:
        parser.error("db is required")
    if len(args) < 1:
        parser.error("need an action to perform")

    action = args[0]

    db = AUSDatabase(options.db, mysql_traditional_mode=True)
    if action == 'create':
        db.create(options.version)
    elif action == 'upgrade':
        db.upgrade(options.version)
    elif action == 'downgrade':
        db.downgrade(options.version)
    elif action == 'extract':
        with db.begin() as trans:
            if len(args) < 2:
                extract_active_data(trans,options.db)
            else:
                location = args[1]
                extract_active_data(trans,options.db, location)
    elif action.startswith("cleanup"):
        if len(args) < 2:
            parser.error("need to pass maximum nightly release age")
        nightly_age = int(args[1])
        with db.begin() as trans:
            if action == "cleanup":
                cleanup_releases(trans, nightly_age, dryrun=False)
                cleanup_releases_history(trans, dryrun=False)
            else:
                cleanup_releases(trans, nightly_age, dryrun=True)
                cleanup_releases_history(trans, dryrun=True)
