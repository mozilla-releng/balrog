#!/usr/bin/env python

import os.path
from Queue import Queue
import site
import sys
import traceback
from threading import Thread

site.addsitedir(os.path.join(os.path.dirname(__file__), "../lib/python"))
site.addsitedir(os.path.join(os.path.dirname(__file__), "../lib/python/vendor"))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import requests

from auslib.util.testing import compare_snippets


def worker(server1, server2, callback, failure_callback):
    while not q.empty():
        try:
            path = q.get()
            url1 = '%s/%s' % (server1, path)
            url2 = '%s/%s' % (server2, path)
            res = compare_snippets(url1, url2)
            callback(path, res)
        except:
            failure_callback(path, traceback.format_exc())

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('aus_servers', metavar='aus_server', nargs=2,
                        help='AUS Servers to make requests against. There must be two.')
    parser.add_argument('--paths-file', dest='paths_file', required=True)
    parser.add_argument('-j', dest='concurrency', default=1, type=int)

    args = parser.parse_args()

    server1, server2 = args.aus_servers

    try:
        paths = requests.get(args.paths_file).content.splitlines()
    # Should be catching MissingSchema here, but our requests doesn't have it.
    except ValueError:
        paths = open(args.paths_file).readlines()

    count = success = fail = error = rc = 0

    def printer(path, res):
        global success, fail, rc
        url1, _, url2, _, diff = res
        if diff:
            fail += 1
            rc = 1
            print 'FAIL: Unmatched snippets on %s:' % path
            for line in diff:
                print line
            print '---- end of diff'
        else:
            success += 1
            print 'PASS: %s' % path

    def failure(path, tb):
        global error, rc
        error += 1
        rc = 1
        print 'ERROR: %s' % path
        print tb

    q = Queue()
    for path in paths:
        count += 1
        q.put(path.strip())

    threads = []
    for i in range(args.concurrency):
        t = Thread(target=worker, args=(server1, server2, printer, failure))
        # Marking the threads as "daemon" means they can be killed. Without
        # this, the program will not exit until all threads exit naturally.
        # http://docs.python.org/2/library/threading.html#thread-objects
        t.daemon = True
        t.start()
        threads.append(t)

    for t in threads:
        while t.isAlive():
            t.join(1)

    print "Tested %d paths." % count
    print "Pass count: %d" % success
    print "Fail count: %d" % fail
    print "Error count: %d" % error
    sys.exit(rc)
