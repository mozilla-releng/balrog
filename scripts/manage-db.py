#!/usr/bin/env python

import itertools
import logging
from os import path
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
        if todelete:
            print "Releases rows to be deleted:"
            print "\n".join(itertools.chain(*todelete))
    else:
        trans.execute("DELETE releases FROM releases" + query)


def cleanup_releases_history(trans, dryrun=True):
    query = """
WHERE name LIKE '%%%%latest%%%%'
AND timestamp<1000*UNIX_TIMESTAMP(NOW()-INTERVAL 14 DAY);
"""
    if dryrun:
        todelete = trans.execute("SELECT name, change_id FROM releases_history" + query).fetchall()
        if todelete:
            print "Releases history rows to be deleted:"
            for key, group in itertools.groupby(todelete, lambda x: x[0]):
                print "%s: %s history rows" % (key, len(list(group)))
    else:
        trans.execute("DELETE releases_history FROM releases_history")

    query = """
WHERE name NOT LIKE '%%%%latest%%%%' AND name LIKE '%%%%nightly%%%%'
AND timestamp<1000*UNIX_TIMESTAMP(NOW()-INTERVAL 7 DAY);
"""
    if dryrun:
        todelete = trans.execute("SELECT name, change_id FROM releases_history" + query).fetchall()
        if todelete:
            print "Releases history rows to be deleted:"
            for key, group in itertools.groupby(todelete, lambda x: x[0]):
                print "%s: %s history rows" % (key, len(list(group)))
    else:
        trans.execute("DELETE releases_history FROM releases_history")


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
    elif action.startswith("cleanup"):
        if len(args) < 2:
            parser.error("need to pass maximum nightly release age")
        nightly_age = int(args[1])
        with db.begin() as trans:
            cleanup_releases(trans, nightly_age, dryrun=True)
            cleanup_releases_history(trans, dryrun=True)
            if action == "cleanup":
                cleanup_releases(trans, nightly_age, dryrun=False)
                cleanup_releases_history(trans, dryrun=False)
