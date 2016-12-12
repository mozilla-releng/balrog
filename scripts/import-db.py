#!/usr/bin/env python

from calendar import timegm
from datetime import datetime
from httplib import HTTPSConnection
import os
from socket import gaierror
import time
from urllib2 import urlopen, HTTPError, URLError


HOST = 'https://balrog-public-dump-prod.s3.amazonaws.com'
PATH = '/dump.sql.txt'
LOCAL_DB_PATH = os.getenv('LOCAL_DUMP', '/app/scripts/prod_db_dump.sql')
TIMEOUT = 10


def getRemoteDBModifiedTS():
    """
    Performs a HEAD request to get the Last-Modified date-time
    of a database dump file and parses it into a UNIX timestamp.
    Returns 0 on error.
    """
    try:
        # Removing the scheme from the URL
        conn = HTTPSConnection(HOST[8:], timeout=TIMEOUT)
        conn.request('HEAD', PATH)
    except gaierror:
        print 'Unable to check remote database dump timestamp, network error'
        exit()

    rsp = conn.getresponse()

    if rsp.status != 200:
        return 0

    last_modified = rsp.getheader('last-modified', None)
    if last_modified is None:
        return 0

    last_m_dt = datetime.strptime(
        last_modified.split(', ')[1], '%d %b %Y %H:%M:%S %Z')
    return timegm(last_m_dt.timetuple())


def getLocalDBModifiedTS():
    """
    Gets the UNIX timestamp of the local database dump file.
    Returns 0 on error.
    """
    try:
        return int(os.path.getmtime(LOCAL_DB_PATH))
    except OSError:
        return 0


def setLocalDBTimestamp(prod_db_ts):
    """
    Sets mtime on the local database dump file to the remote database dump
    file's mtime. Sets atime to now.
    """
    now_ts = int(time.time())
    os.utime(LOCAL_DB_PATH, (now_ts, prod_db_ts,))


def setLocalDBPermissions():
    os.chmod(LOCAL_DB_PATH, 0666)


if __name__ == '__main__':
    prod_db_ts = getRemoteDBModifiedTS()
    local_db_ts = getLocalDBModifiedTS()

    if prod_db_ts > 0:
        if not os.path.exists(LOCAL_DB_PATH) or (prod_db_ts > local_db_ts):
            print 'Downloading latest database'
            try:
                rsp = urlopen(HOST + PATH, timeout=TIMEOUT)
            except (HTTPError, URLError) as e:
                print 'Error when downloading latest db: {}'.format(e)
                exit()

            with open(LOCAL_DB_PATH, 'wb') as f:
                f.write(rsp.read())

            setLocalDBTimestamp(prod_db_ts)
            setLocalDBPermissions()
