#!/usr/bin/env python

import itertools
import logging
from os import path, popen
from sqlalchemy.engine.url import make_url
import sys

logging.basicConfig(level=logging.INFO)

# Our parent directory should contain the auslib module, so we add it to the
# PYTHONPATH to make things easier on consumers.
sys.path.append(path.join(path.dirname(__file__), ".."))
sys.path.append(path.join(path.dirname(__file__), path.join("..", "vendor", "lib", "python")))

from auslib.db import AUSDatabase
from auslib.blobs.base import createBlob


def cleanup_releases(trans, nightly_age, dryrun=True):
    # This and the subsequent queries use "%%%%%" because we end up going
    # through two levels of Python string formatting. The first is here,
    # and the second happens at a low level of SQLAlchemy when the transaction
    # is being executed.
    query = """
LEFT JOIN rules rules_mapping ON (name=rules_mapping.mapping)
WHERE name LIKE '%%%%nightly%%%%'
AND name NOT LIKE '%%%%latest'
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


def chunk_list(list_object, n):
    """
    Yield successive n-sized chunks from list_object.
    """
    for i in xrange(0, len(list_object), n):
        yield list_object[i:i + n]


def mysql_command(host, user, password, db, cmd):
    # --protocol=tcp prevent's a socket from being used, so that balrogdb
    # in docker can be called from localhost (via port forwarding for instance)
    return "mysqldump -h {} -u {} -p{} --protocol=tcp --single-transaction --lock-tables=false {} {}".format(host, user, password, db, cmd)


def mysql_data_only_command(host, user, password, db, cmd):
    return mysql_command(host, user, password, db, "--skip-add-drop-table --no-create-info {}".format(cmd))


def extract_active_data(trans, url, dump_location='dump.sql'):
    """
    Stores sqldump data in the specified location. If not specified, stores it in current directory in file dump.sql
    If file already exists it will override that file and not append it.

    Function added in to enhance testing in Balrog's stage environment.

    :param trans: Transaction Object for an SQL connection
    :param url: Database. eg : mysql://balrogadmin:balrogadmin@balrogdb/balrog
    :param dump_location: location where sqldump file must be created
    """
    url = make_url(url)
    user = url.username
    password = url.password
    host = url.host
    db = url.database

    # Extract the entire database schema, without any rows.
    # This is done to ensure that any database dump generated can be
    # imported to an empty database without issue. From there, a Balrog
    # installation can be upgraded or downgraded to a different database
    # schema version if desired.
    # See https://bugzilla.mozilla.org/show_bug.cgi?id=1376331 for additional
    # background on this.
    popen("{} > {}".format(
        mysql_command(host, user, password, db, "--no-data"),
        dump_location,
    ))

    # Now extract the data we actually want....
    # We always want all the data from a few tables...
    popen("{} >> {}".format(
        mysql_data_only_command(host, user, password, db, "dockerflow rules rules_history migrate_version"),
        dump_location,
    ))

    # Because Releases are so massive, we only want the actively used ones,
    # and very little Release history. Specifically:
    #   - All releases referenced by a Rule or a Active Scheduled Rule Change
    #   - All releases referenced by a Release from the above query
    #   - 50 rows of history for the "Firefox-mozilla-central-nightly-latest" Release
    #   - Full history for the Release currently referenced by the "firefox-release" Rule.
    query_release_mapping = """SELECT DISTINCT releases.* \
        FROM releases, rules, rules_scheduled_changes \
        WHERE (releases.name IN (rules.mapping, rules.fallbackMapping))
          OR (rules_scheduled_changes.complete = 0 AND
              releases.name IN (rules_scheduled_changes.base_mapping, rules_scheduled_changes.base_fallbackMapping))
        """

    result = trans.execute(query_release_mapping).fetchall()
    release_names = set()
    for row in result:
        try:
            release_names.add(str(row['name']))
            release_blob = createBlob(row['data'])
            release_names.update(release_blob.getReferencedReleases())
        except ValueError:
            continue
    if release_names:
        batch_generator = chunk_list(list(release_names), 30)
        for batched_release_list in batch_generator:
            query = ", ".join("'" + names + "'" for names in batched_release_list)
            popen("{} >> {}".format(
                mysql_data_only_command(host, user, password, db, 'releases --where="releases.name IN ({})"'.format(query)),
                dump_location,
            ))

    popen("{} >> {}".format(
        mysql_data_only_command(host, user, password, db,
                                "releases_history --where=\"releases_history.name='Firefox-mozilla-central-nightly-latest' ORDER BY timestamp DESC LIMIT 50\""),
        dump_location,
    ))

    query = "SELECT rules.mapping FROM rules WHERE rules.alias='firefox-release'"
    popen("{} >> {}".format(
        mysql_data_only_command(host, user, password, db, 'releases_history --where="name = ({}) ORDER BY timestamp DESC LIMIT 50"'.format(query)),
        dump_location,
    ))

    # Notably absent from this dump are all Permissions, Roles, and Scheduled
    # Changes tables. Permissions & Roles are excluded to avoid leaking any
    # account information from production. Scheduled Changes are not included
    # to avoid any potential confusion when a dump is imported.
    # Eg: Scheduled Changes may enact shortly after a user starts their Balrog
    # instance without any interaction, which would be confusing.


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
                extract_active_data(trans, options.db)
            else:
                location = args[1]
                extract_active_data(trans, options.db, location)
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
