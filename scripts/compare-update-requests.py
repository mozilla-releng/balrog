#!/usr/bin/env python

import os.path
import site
import sys

site.addsitedir(os.path.join(os.path.dirname(__file__), "../lib/python"))
site.addsitedir(os.path.join(os.path.dirname(__file__), "../lib/python/vendor"))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import requests

from auslib.util.testing import compare_snippets


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('aus_servers', metavar='aus_server', nargs=2,
        help='AUS Servers to make requests against. There must be two.')
    parser.add_argument('--paths-file', dest='paths_file', required=True)

    args = parser.parse_args()

    server1, server2 = args.aus_servers

    try:
        paths = requests.get(args.paths_file).content.splitlines()
    # Should be catching MissingSchema here, but our requests doesn't have it.
    except ValueError:
        paths = open(args.paths_file).readlines()

    rc = 0
    for url1, xml1, url2, xml2, diff in compare_snippets(server1, server2, paths):
        rc = 1
        print 'Unmatched snippets:'
        print url1.strip()
        print url2.strip()
        for line in diff:
            print line
        print '---- end of diff\n'

    sys.exit(rc)
