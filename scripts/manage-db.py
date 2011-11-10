#!/usr/bin/env python

from os import path
import sys

# Our parent directory should contain the auslib module, so we add it to the
# PYTHONPATH to make things easier on consumers.
sys.path.append(path.join(path.dirname(__file__), ".."))

from auslib.db import AUSDatabase

def create_db(db):
    db.createTables()

actions = {
    'create': {
        'help': 'Create all the tables required for a new Balrog database',
        'meth': create_db,
    }
}

if __name__ == "__main__":
    from optparse import OptionParser
    doc = """%s --db dburi action [...]""" % sys.argv[0]
    doc += "\nPossible actions:"
    for a in actions:
        doc += "\n  %s: %s" % (a, actions[a]['help'])
    parser = OptionParser(doc)
    parser.add_option("-d", "--db", dest="db", default=None, help="database to manage, in URI format")
    options, args = parser.parse_args()

    if not options.db:
        print "db is required"
        print __doc__
        sys.exit(1)
    for arg in args:
        if arg not in actions:
            print "don't know how to perform action '%s'" % arg
            print __doc__
            sys.exit(1)

    db = AUSDatabase(options.db)
    for arg in args:
        actions[arg]['meth'](db)
