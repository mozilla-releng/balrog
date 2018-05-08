#!/usr/bin/env python

from os import path
import sys

import simplejson as json

# Our parent directory should contain the auslib module, so we add it to the
# PYTHONPATH to make things easier on consumers.
sys.path.append(path.join(path.dirname(__file__), ".."))

from auslib.db import AUSDatabase

if __name__ == "__main__":
    from optparse import OptionParser
    doc = "%s --db dburi -r release-name" % sys.argv[0]
    parser = OptionParser(doc)
    parser.add_option("-d", "--db", dest="db", default=None, help="database to manage, in URI format")
    parser.add_option("-r", "--release", dest="release", default=None, help="Release to retrieve blob for")
    parser.add_option("-u", "--ugly", dest="ugly", default=False, action="store_true", help="Don't format output")
    options, args = parser.parse_args()

    if not options.db or not options.release:
        print("db and release are required")
        print(__doc__)
        sys.exit(1)

    db = AUSDatabase(options.db)
    blob = db.releases.getReleaseBlob(options.release)
    if options.ugly:
        print(json.dumps(blob))
    else:
        print(json.dumps(blob, indent=4))
