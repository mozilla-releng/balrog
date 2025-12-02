#!/usr/bin/env python

import itertools
import logging
import os
import sys
from os import path
from subprocess import run

from sqlalchemy.engine.url import make_url

from auslib.blobs.base import createBlob  # noqa: E402
from auslib.db import AUSDatabase  # noqa: E402

logging.basicConfig(level=logging.INFO)

# Our parent directory should contain the auslib module, so we add it to the
# PYTHONPATH to make things easier on consumers.
sys.path.append(path.join(path.dirname(__file__), ".."))
sys.path.append(path.join(path.dirname(__file__), path.join("..", "vendor", "lib", "python")))


# TODO: filter out things that don't end in 14 digits
RELEASES_CLEANUP_CONDITION = """
LEFT JOIN rules rules_mapping ON (name=rules_mapping.mapping)
WHERE name LIKE '%%nightly%%'
AND name NOT LIKE '%%latest'
AND rules_mapping.mapping IS NULL
AND RIGHT(name, 14) REGEXP '^[[:digit:]]*$'
AND (STR_TO_DATE(RIGHT(name, 14), "%%Y%%m%%d%%H%%i%%S") < NOW() - INTERVAL {nightly_age} DAY);
"""


def cleanup_releases(trans, nightly_age, dryrun=True):
    # This and the subsequent queries use "%%%%%" because we end up going
    # through two levels of Python string formatting. The first is here,
    # and the second happens at a low level of SQLAlchemy when the transaction
    # is being executed.
    query = RELEASES_CLEANUP_CONDITION.format(nightly_age=nightly_age)
    if dryrun:
        todelete = trans.execute("SELECT name FROM releases" + query).fetchall()
        print("Releases rows to be deleted:")
        if todelete:
            print("\n".join(itertools.chain(*todelete)))
        else:
            print("  - None")
    else:
        trans.execute("DELETE releases FROM releases" + query)


def cleanup_releases_json(trans, nightly_age, dryrun=True):
    query = RELEASES_CLEANUP_CONDITION.format(nightly_age=nightly_age)
    if dryrun:
        todelete = trans.execute("SELECT name FROM releases_json" + query).fetchall()
        print("Releases JSON rows to be deleted:")
        if todelete:
            print("\n".join(itertools.chain(*todelete)))
        else:
            print("  - None")
    else:
        trans.execute("DELETE releases_json FROM releases_json" + query)
        trans.execute("DELETE release_assets FROM release_assets" + query)


def chunk_list(list_object, n):
    """
    Yield successive n-sized chunks from list_object.
    """
    for i in range(0, len(list_object), n):
        yield list_object[i : i + n]


def mysql_command(host, user, password, db, cmd):
    # --protocol=tcp prevent's a socket from being used, so that balrogdb
    # in docker can be called from localhost (via port forwarding for instance)
    return "mysqldump -h {} -u {} -p{} --protocol=tcp --single-transaction --lock-tables=false --no-tablespaces {} {}".format(host, user, password, db, cmd)


def mysql_data_only_command(host, user, password, db, cmd):
    return mysql_command(host, user, password, db, "--complete-insert --skip-add-drop-table --no-create-info {}".format(cmd))


def extract_releases(release_names, url, dump_file, source_tables="releases_json release_assets"):
    if release_names:
        batch_generator = chunk_list(list(release_names), 30)
        for batched_release_list in batch_generator:
            query = ", ".join("'" + names + "'" for names in batched_release_list)
            cmd = mysql_data_only_command(url.host, url.username, url.password, url.database, source_tables).split()
            cmd.append("--where=name IN ({})".format(query))
            run(cmd, stdout=dump_file, check=True)


def extract_pins(release_names, url, dump_file):
    if release_names:
        batch_generator = chunk_list(list(release_names), 30)
        for batched_release_list in batch_generator:
            query = ", ".join(f"'{name}'" for name in batched_release_list)
            cmd = mysql_data_only_command(url.host, url.username, url.password, url.database, "pinnable_releases").split()
            cmd.append(f"--where=mapping IN ({query})")
            run(cmd, stdout=dump_file, check=True)


def get_active_release_names(trans, source_table="releases_json"):
    # Because Releases are so massive, we only want the actively used ones. Specifically:
    #   - All releases referenced by a Rule or a Active Scheduled Rule Change
    #   - All releases referenced by a Release from the above query
    query_release_mapping = f"""SELECT DISTINCT releases.*
                FROM {source_table} as releases
                INNER JOIN (
                    SELECT mapping FROM rules WHERE mapping IS NOT NULL
                    UNION
                    SELECT fallbackMapping FROM rules WHERE fallbackMapping IS NOT NULL
                    UNION
                    SELECT base_mapping FROM rules_scheduled_changes WHERE complete = 0 AND base_mapping IS NOT NULL
                    UNION
                    SELECT base_fallbackMapping FROM rules_scheduled_changes WHERE complete = 0 AND base_fallbackMapping IS NOT NULL
                ) active_names ON releases.name = active_names.mapping
                """
    result = trans.execute(query_release_mapping).fetchall()
    release_names = set()
    for row in result:
        try:
            release_names.add(str(row["name"]))
            release_blob = createBlob(row["data"])
            release_names.update(release_blob.getReferencedReleases())
        except ValueError:
            continue
    return release_names


def extract_active_data(trans, url, dump_location="dump.sql"):
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
    with open(dump_location, "w+") as dump_file:
        run(mysql_command(host, user, password, db, "--no-data").split(), stdout=dump_file, check=True)

        # Now extract the data we actually want....
        # We always want all the data from a few tables...
        run(mysql_data_only_command(host, user, password, db, "dockerflow rules rules_history migrate_version").split(), stdout=dump_file, check=True)

        release_names = get_active_release_names(trans)
        extract_releases(release_names, url, dump_file)
        extract_pins(release_names, url, dump_file)

        release_names = get_active_release_names(trans, "releases")
        extract_releases(release_names, url, dump_file, "releases")

        # Notably absent from this dump are all Permissions, Roles, and Scheduled
        # Changes tables. Permissions & Roles are excluded to avoid leaking any
        # account information from production. Scheduled Changes are not included
        # to avoid any potential confusion when a dump is imported.
        # Eg: Scheduled Changes may enact shortly after a user starts their Balrog
        # instance without any interaction, which would be confusing.


def _strip_multiple_spaces(string):
    return " ".join(string.split())


if __name__ == "__main__":
    from optparse import OptionParser

    usage = """%s --db dburi action [options]\n""" % sys.argv[0]
    usage += "Possible actions:\n"
    usage += "  create: Create all the tables required for a new Balrog database\n"
    usage += "  upgrade: Upgrade an existing balrog table to a newer version.\n"
    usage += "  downgrade: Downgrade an existing balrog table to an older version.\n"
    usage += "  extract: Extracts active data for testing. Enter an extra arg to specify the location and filename for\
            the data to stored in. "
    usage += (
        "  cleanup: Cleanup old data from a database. Requires an extra arg of maximum age (in days) of nightly releases. "
        "Anything older than this will be deleted.\n"
    )
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

    if os.environ.get("SENTRY_DSN"):
        import sentry_sdk

        sentry_sdk.init(os.environ["SENTRY_DSN"])

    db = AUSDatabase(options.db, mysql_traditional_mode=True)
    if action == "create":
        db.create(options.version)
    elif action == "upgrade":
        db.upgrade(options.version)
    elif action == "downgrade":
        db.downgrade(options.version)
    elif action == "extract":
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
                cleanup_releases_json(trans, nightly_age, dryrun=False)
            else:
                cleanup_releases(trans, nightly_age, dryrun=True)
                cleanup_releases_json(trans, nightly_age, dryrun=True)
