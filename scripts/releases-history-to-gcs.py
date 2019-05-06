#!/usr/bin/env python3

import asyncio
import base64
from collections import defaultdict
import hashlib
import ssl
import sys

import aiohttp

from gcloud.aio.storage import Storage


def ignore_aiohttp_ssl_error(loop, aiohttpversion='3.5.4'):
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
        if context.get('message') == 'SSL error in data received':
            # validate we have the right exception, transport and protocol
            exception = context.get('exception')
            protocol = context.get('protocol')
            if (
                isinstance(exception, ssl.SSLError) and exception.reason == 'KRB5_S_INIT' and
                isinstance(protocol, asyncio.sslproto.SSLProtocol) and
                isinstance(protocol._app_protocol, aiohttp.client_proto.ResponseHandler)
            ):
                if loop.get_debug():
                    asyncio.log.logger.debug('Ignoring aiohttp SSL KRB5_S_INIT error')
                return
        orig_handler(context)

    loop.set_exception_handler(ignore_ssl_error)

skip_patterns = ("-nightly-",)


async def get_revisions(r, session, balrog_api, sem):
    async with sem, session.get("{}/releases/{}/revisions?limit=10000".format(balrog_api, r)) as resp:
        return (await resp.json())["revisions"]


async def get_releases(session, balrog_api):
    async with session.get("{}/releases".format(balrog_api)) as resp:
        for r in (await resp.json())["releases"]:
            yield (r["name"], r["data_version"])


async def process_release(r, session, balrog_api, bucket, sem):
    releases = defaultdict(int)
    uploads = defaultdict(lambda: defaultdict(int))

    for rev in await get_revisions(r, session, balrog_api, sem):
        releases[r] += 1
        async with sem:
            old_version = await (await session.get("{}/history/view/release/{}/data".format(balrog_api, rev["change_id"]))).text()
        old_version_hash = hashlib.md5(old_version.encode("ascii")).digest()
        try:
            async with sem:
                # TODO: need to handle errors here somehow. they keep crashing the script
                current_blob = await bucket.get_blob("{}/{}-{}-{}.json".format(r, rev["data_version"], rev["timestamp"], rev["changed_by"]))
            current_blob_hash = base64.b64decode(current_blob.md5Hash)
        except aiohttp.ClientResponseError:
            current_blob_hash = None
        if old_version_hash != current_blob_hash:
            async with sem:
                # TODO: need to handle errors here somehow. they keep crashing the script
                blob = bucket.new_blob("{}/{}-{}-{}.json".format(r, rev["data_version"], rev["timestamp"], rev["changed_by"]))
                await blob.upload(old_version, session)
            uploads[r]["uploaded"] += 1
        else:
            uploads[r]["existing"] += 1

    return releases, uploads


async def main(loop, balrog_api, bucket_name, concurrency):
    # limit the number of connections at any one time
    sem = asyncio.Semaphore(concurrency)
    releases = defaultdict(int)
    uploads = defaultdict(lambda: defaultdict(int))

    n = 0

    async with aiohttp.ClientSession(loop=loop) as session:
        storage = Storage(session=session)
        bucket = storage.get_bucket(bucket_name)

        async with session.get("{}/releases".format(balrog_api)) as resp:
            for r in (await resp.json())["releases"]:
                release_name = r["name"]
                release_futures = []

                if any(pat in release_name for pat in skip_patterns):
                    print("Skipping {} because it matches a skip pattern".format(release_name), flush=True)
                    continue
                n += 1
                if n == 5:
                    break

                print("Processing {}".format(release_name), flush=True)
                processed_releases, processed_uploads = await process_release(release_name, session, balrog_api, bucket, sem)
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

balrog_api = sys.argv[1]
bucket_name = sys.argv[2]
if len(sys.argv) > 3:
    concurrency = sys.argv[3]
else:
    concurrency = 100
loop = asyncio.get_event_loop()
ignore_aiohttp_ssl_error(loop)
loop.run_until_complete(main(loop, balrog_api, bucket_name, concurrency))
