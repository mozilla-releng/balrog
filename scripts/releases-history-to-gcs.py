#!/usr/bin/env python3

import asyncio
import base64
from collections import defaultdict
import hashlib
import os
import ssl
import sys

import aiohttp

from sqlalchemy import create_engine

from gcloud.aio.storage import Storage


def ignore_aiohttp_ssl_error(loop, aiohttpversion="3.5.4"):
    """Ignore aiohttp #3535 issue with SSL data after close

    There appears to be an issue on Python 3.7 and aiohttp SSL that throws a
    ssl.SSLError fatal error (ssl.SSLError: [SSL: KRB5_S_INIT] application data
    after close notify (_ssl.c:2609)) after we are already done with the
    connection. See GitHub issue aio-libs/aiohttp#3535

    Given a loop, this sets up a exception handler that ignores this specific
    exception, but passes everything else on to the previous exception handler
    this one replaces.

    If the current aiohttp version is not exactly equal to aiohttpversion
    nothing is done, assuming that the next version will have this bug fixed.
    This can be disabled by setting this parameter to None

    """
    if aiohttpversion is not None and aiohttp.__version__ != aiohttpversion:
        return

    orig_handler = loop.get_exception_handler() or loop.default_exception_handler

    def ignore_ssl_error(loop, context):
        if context.get("message") == "SSL error in data received":
            # validate we have the right exception, transport and protocol
            exception = context.get("exception")
            protocol = context.get("protocol")
            if (
                isinstance(exception, ssl.SSLError)
                and exception.reason == "KRB5_S_INIT"
                and isinstance(protocol, asyncio.sslproto.SSLProtocol)
                and isinstance(protocol._app_protocol, aiohttp.client_proto.ResponseHandler)
            ):
                if loop.get_debug():
                    asyncio.log.logger.debug("Ignoring aiohttp SSL KRB5_S_INIT error")
                return
        orig_handler(context)

    loop.set_exception_handler(ignore_ssl_error)


skip_patterns = ("-nightly-",)


def timeout_monkeypatch(storage, timeout_override):
    orig_download_metadata = storage.download_metadata
    orig_upload = storage.upload

    async def download_metadata(self, *args, **kwargs):
        kwargs["timeout"] = timeout_override
        return await orig_download_metadata(self, *args, **kwargs)

    async def upload(self, *args, **kwargs):
        kwargs["timeout"] = timeout_override
        return await orig_upload(self, *args, **kwargs)

    storage.download_metadata = download_metadata
    storage.upload = upload

    return storage


async def process_release(r, session, balrog_db, bucket, mysql_sem, gcs_sem, loop):
    releases = defaultdict(int)
    uploads = defaultdict(lambda: defaultdict(int))

    print("Processing {}".format(r), flush=True)
    async with mysql_sem:
        revisions = await loop.run_in_executor(
            None, balrog_db.execute, f"SELECT data_version, timestamp, changed_by, data FROM releases_history WHERE name='{r}'"
        )
    for rev in revisions:
        releases[r] += 1
        if rev["data"] is None:
            old_version_hash = None
        else:
            old_version_hash = hashlib.md5(rev["data"].encode("ascii")).digest()
        try:
            async with gcs_sem:
                current_blob = await bucket.get_blob("{}/{}-{}-{}.json".format(r, rev["data_version"], rev["timestamp"], rev["changed_by"]))
            current_blob_hash = base64.b64decode(current_blob.md5Hash)
        except aiohttp.ClientResponseError:
            current_blob_hash = None
        if old_version_hash != current_blob_hash:
            async with gcs_sem:
                blob = bucket.new_blob("{}/{}-{}-{}.json".format(r, rev["data_version"], rev["timestamp"], rev["changed_by"]))
            await blob.upload(rev["data"], session)
            uploads[r]["uploaded"] += 1
        else:
            uploads[r]["existing"] += 1

    return releases, uploads


async def main(loop, balrog_db, bucket_name, limit_to, mysql_concurrency, gcs_concurrency, skip_toplevel_keys, whitelist, gcs_timeout):
    # limit the number of connections at any one time
    mysql_sem = asyncio.Semaphore(mysql_concurrency)
    gcs_sem = asyncio.Semaphore(gcs_concurrency)
    releases = defaultdict(int)
    uploads = defaultdict(lambda: defaultdict(int))
    tasks = []

    n = 0

    async with aiohttp.ClientSession(loop=loop) as session:
        storage = timeout_monkeypatch(Storage(session=session), gcs_timeout)
        bucket = storage.get_bucket(bucket_name)

        toplevel_keys = []
        if skip_toplevel_keys:
            batch = await storage.list_objects(bucket_name, params={"delimiter": "/"})
            while batch:
                toplevel_keys.extend([name.rstrip("/") for name in batch.get("prefixes")])
                if batch.get("nextPageToken"):
                    batch = await storage.list_objects(bucket_name, params={"delimiter": "/", "pageToken": batch["nextPageToken"]})
                else:
                    batch = None

        to_process = balrog_db.execute("SELECT DISTINCT name FROM releases_history").fetchall()
        for r in to_process:
            release_name = r[0]

            if skip_toplevel_keys and release_name in toplevel_keys:
                print("Skipping {} because it is an existing toplevel key".format(release_name), flush=True)
                continue

            if whitelist and release_name not in whitelist:
                print("Skipping {} because it is not in the whitelist".format(release_name), flush=True)
                continue

            if limit_to and n >= limit_to:
                break

            n += 1

            if any(pat in release_name for pat in skip_patterns):
                print("Skipping {} because it matches a skip pattern".format(release_name), flush=True)
                continue

            tasks.append(loop.create_task(process_release(release_name, session, balrog_db, bucket, mysql_sem, gcs_sem, loop)))

        for processed_releases, processed_uploads in await asyncio.gather(*tasks, loop=loop):
            for rel in processed_releases:
                releases[rel] += processed_releases[rel]
            for u in processed_uploads:
                uploads[u]["uploaded"] += processed_uploads[u]["uploaded"]
                uploads[u]["existing"] += processed_uploads[u]["existing"]

    for r in releases:
        revs_in_gcs = uploads[r]["uploaded"] + uploads[r]["existing"]
        print("INFO: {}: Found {} existing revisions, uploaded {} new ones".format(r, uploads[r]["existing"], uploads[r]["uploaded"]))
        if r not in uploads:
            print("WARNING: {} was found in the Balrog API but does not exist in GCS".format(r))
        elif releases[r] != revs_in_gcs:
            print("WARNING: {} has a data version of {} in the Balrog API, but {} revisions exist in GCS".format(r, releases[r], revs_in_gcs))


if __name__ == "__main__":
    dburi = sys.argv[1]
    bucket_name = sys.argv[2]
    if len(sys.argv) > 3:
        limit_to = int(sys.argv[3])
    else:
        limit_to = None

    mysql_concurrency = int(os.environ.get("MYSQL_CONCURRENCY", 10))
    gcs_concurrency = int(os.environ.get("GCS_SYNC_CONCURRENCY", 10))
    skip_toplevel_keys = bool(int(os.environ.get("SKIP_TOPLEVEL_KEYS", True)))
    whitelist = os.environ.get("ONLY_SYNC_RELEASES", None)
    gcs_timeout = int(os.environ.get("GCS_TIMEOUT", 60))
    if whitelist:
        whitelist = whitelist.split()
    loop = asyncio.get_event_loop()
    ignore_aiohttp_ssl_error(loop)

    balrog_db = create_engine(dburi)
    loop.run_until_complete(main(loop, balrog_db, bucket_name, limit_to, mysql_concurrency, gcs_concurrency, skip_toplevel_keys, whitelist, gcs_timeout))
