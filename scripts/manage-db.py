#!/usr/bin/env python

import itertools
import logging
from os import path, popen
import sys

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

def extract_active_data( loc="."):
    popen('mysqldump -h balrogdb -u balrogadmin -pbalrogadmin balrog rules rules_history rules_scheduled_changes \
           rules_scheduled_changes_history permissions permissions_history migrate_version  > test.sql')
    popen('mysqldump -h balrogdb -u balrogadmin -pbalrogadmin --single-transaction balrog releases \
           --where="exists (select NULL from rules where releases.name = rules.mapping)" >> test.sql ')

if __name__ == "__main__":
    from optparse import OptionParser
    usage = """%s --db dburi action [options]\n""" % sys.argv[0]
    usage += "Possible actions:\n"
    usage += "  create: Create all the tables required for a new Balrog database\n"
    usage += "  upgrade: Upgrade an existing balrog table to a newer version.\n"
    usage += "  downgrade: Downgrade an existing balrog table to an older version.\n"
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
    elif action == 'extra':
        extract_active_data()
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
