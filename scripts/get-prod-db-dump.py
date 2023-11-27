#!/usr/bin/env python

import logging
import os
import time
from calendar import timegm
from datetime import datetime
from http.client import HTTPSConnection
from socket import gaierror
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

HOST = "https://storage.googleapis.com"
PATH = "/balrog-prod-dbdump-v1/dump.sql.txt.xz"
LOCAL_DB_PATH = os.getenv("LOCAL_DUMP", "/app/scripts/prod_db_dump.sql.xz")
TIMEOUT = 10


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s: %(message)s")


def getRemoteDBModifiedTS():
    """
    Performs a HEAD request to get the Last-Modified date-time
    of a database dump file and parses it into a UNIX timestamp.
    """
    debug_msg = "Unable to get timestamp of remote database dump - {0}"
    logging.info("Getting timestamp of database dump at '%s'", HOST + PATH)
    try:
        # Removing the scheme from the URL
        conn = HTTPSConnection(HOST[8:], timeout=TIMEOUT)
        conn.request("HEAD", PATH)
    except gaierror as e:
        logging.debug(debug_msg.format("Cannot connect to '%s', error: %s"), HOST + PATH, e)
        exit(1)

    rsp = conn.getresponse()

    if rsp.status != 200:
        logging.debug(debug_msg.format("Server responded with: %d %s"), rsp.status, rsp.reason)
        exit(1)

    last_modified = rsp.getheader("last-modified", None)
    if last_modified is None:
        logging.debug(debug_msg.format("Response doesnt include Last-Modified Header"))
        exit(1)

    last_m_dt = datetime.strptime(last_modified.split(", ")[1], "%d %b %Y %H:%M:%S %Z")
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
    os.utime(LOCAL_DB_PATH, (now_ts, prod_db_ts))


def setLocalDBPermissions():
    os.chmod(LOCAL_DB_PATH, 0o666)


if __name__ == "__main__":
    prod_db_ts = getRemoteDBModifiedTS()
    local_db_ts = getLocalDBModifiedTS()

    if prod_db_ts > 0:
        if not os.path.exists(LOCAL_DB_PATH) or (prod_db_ts > local_db_ts):
            logging.info("Downloading latest database dump to '%s'", LOCAL_DB_PATH)
            try:
                rsp = urlopen(HOST + PATH, timeout=TIMEOUT)
            except (HTTPError, URLError) as e:
                logging.debug("Downloading the latest database dump failed" "due to network error: %s", e)
                exit(1)

            with open(LOCAL_DB_PATH, "wb") as f:
                f.write(rsp.read())

            setLocalDBTimestamp(prod_db_ts)
            setLocalDBPermissions()
        else:
            logging.info("Cached dump is up-to-date")
