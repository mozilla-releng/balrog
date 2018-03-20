#!/usr/bin/env python

import logging
from os import path
import site

mydir = path.dirname(path.abspath(__file__))
site.addsitedir(path.join(mydir, ".."))
site.addsitedir(path.join(mydir, "..", "vendor/lib/python"))

from auslib.blobs.apprelease import ReleaseBlobV4
from auslib.config import AdminConfig
from auslib.db import AUSDatabase

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--db", dest="db", help="The database to use, in URI format. Incompatible with --ini.")
    parser.add_argument("--ini", dest="ini", help="The config file to look for the database in. Incompatible with --db.")
    parser.add_argument("--name", dest="name", required=True, help="The name of the person/script doing the migrations.")
    parser.add_argument("releases", metavar="release", nargs="+", help="The releases (aka blob names) to migrate.")

    args = parser.parse_args()

    if args.db and args.ini:
        parser.error("Cannot specify --db and --ini!")

    if args.ini:
        cfg = AdminConfig(args.ini)
        db = AUSDatabase(cfg.getDburi())
        db.setDomainWhitelist(cfg.getDomainWhitelist())
    else:
        db = AUSDatabase(args.db)

    for release in args.releases:
        try:
            rel = db.releases.getReleases(name=release)[0]
            blob = rel["data"]
        except Exception:
            log.debug("No such release '%s', skipping", release)

        if blob["schema_version"] == 4:
            log.debug("%s is already schema 4, skipping", release)
            continue
        elif blob["schema_version"] != 3:
            log.debug("%s is not schema 3, can't upgrade it", release)
            continue

        try:
            log.debug("Upgrading %s", release)
            v4Blob = ReleaseBlobV4.fromV3(blob)
            db.releases.updateRelease(release, args.name, rel["data_version"], blob=v4Blob)
            log.debug("Done")
        except Exception:
            log.exception("Failed to upgrade %s", release)
