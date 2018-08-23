#!/usr/bin/env python

import logging
from os import path
import sys

# Our parent directory should contain the auslib module, so we add it to the
# PYTHONPATH to make things easier on consumers.
sys.path.append(path.join(path.dirname(__file__), ".."))

from auslib.blobs.apprelease import ReleaseBlobV1
from auslib.db import AUSDatabase

if __name__ == "__main__":
    from optparse import OptionParser
    doc = "%s --db dburi -r release-name -v version -p product foo.json" % sys.argv[0]
    parser = OptionParser(doc)
    parser.add_option("-d", "--db", dest="db", default=None, help="database to manage, in URI format")
    parser.add_option("-r", "--release", dest="release", default=None, help="Release to put blob into")
    parser.add_option("-v", "--version", dest="version", default=None, help="Version of the release")
    parser.add_option("-p", "--product", dest="product", default=None, help="Product of the release")

    options, args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s: %(message)s")

    if not options.db or not options.release or not options.version or not options.product or len(args) != 1:
        print(doc)
        sys.exit(1)

    db = AUSDatabase(options.db)
    blob = ReleaseBlobV1()
    blob.loadJSON(open(args[0]).read())
    try:
        old = db.releases.getReleases(name=options.release)[0]
        db.releases.updateRelease(
            name=options.release, product=options.product, version=options.version, changed_by='import-json', old_data_version=old['data_version'], blob=blob
        )
    except IndexError:
        db.releases.addRelease(name=options.release, product=options.product, version=options.version, blob=blob, changed_by='import-json')
