#!/usr/bin/env python

import logging
from os import path
import sys

logging.basicConfig(level=logging.DEBUG)

# Our parent directory should contain the auslib module, so we add it to the
# PYTHONPATH to make things easier on consumers.
sys.path.append(path.join(path.dirname(__file__), ".."))
sys.path.append(path.join(path.dirname(__file__), path.join("..", "vendor", "lib", "python")))

from auslib.db import AUSDatabase

if __name__ == "__main__":
    from optparse import OptionParser
    usage = """%s --db dburi action [options]\n""" % sys.argv[0]
    usage += "Possible actions:\n"
    usage += "  create: Create all the tables required for a new Balrog database\n"
    usage += "  upgrade: Upgrade an existing balrog table to a newer version.\n"
    usage += "  downgrade: Downgrade an existing balrog table to an older version.\n"
    usage += "  cleanup: Cleanup old data from a database. Requires an extra arg of maximum age (in months) of releases. Anything older than this will be deleted."
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
    elif action == "cleanup":
        if len(args) < 2:
            parser.error("need to pass maximum nightly release age")
        nightly_age = int(args[1])
        with db.begin() as trans:
            trans.execute("""
DELETE releases FROM releases
LEFT OUTER JOIN releases_history USING (name)
LEFT JOIN rules ON (name=mapping)
WHERE name LIKE '%%%%nightly%%%%'
AND (rules.whitelist <> releases.name OR rules.whitelist IS NULL)
AND (rules.mapping <> releases.name OR rules.mapping IS NULL)
AND (timestamp<1000*UNIX_TIMESTAMP(NOW()-INTERVAL %s MONTH) OR change_id is NULL);
""" % nightly_age)
            trans.execute("""
DELETE releases_history FROM releases_history
WHERE name LIKE '%%%%latest%%%%'
AND timestamp<1000*UNIX_TIMESTAMP(NOW()-INTERVAL 14 DAY);
""")
            trans.execute("""
DELETE releases_history FROM releases_history
WHERE name NOT LIKE '%%%%latest%%%%' AND name LIKE '%%%%nightly%%%%'
AND timestamp<1000*UNIX_TIMESTAMP(NOW()-INTERVAL 7 DAY);
""")
