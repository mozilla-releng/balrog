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
    async with sem, session.get("{}/releases/{}/revisions".format(balrog_api, r)) as resp:
        return (await resp.json())["revisions"]


async def get_releases(session, balrog_api):
    async with session.get("{}/releases".format(balrog_api)) as resp:
        for r in (await resp.json())["releases"]:
            yield (r["name"], r["data_version"])


async def process_release(r, session, balrog_api, bucket, sem):
    futures = []

    for rev in await get_revisions(r, session, balrog_api, sem):
        async with sem:
            old_version = await (await session.get("{}/history/view/release/{}/data".format(balrog_api, rev["change_id"]))).text()
        old_version_hash = hashlib.md5(old_version.encode("ascii")).digest()
        try:
            current_blob = await bucket.get_blob("{}/{}-{}-{}.json".format(r, rev["data_version"], rev["timestamp"], rev["changed_by"]))
            current_blob_hash = base64.b64decode(current_blob.md5Hash)
        except aiohttp.ClientResponseError:
            current_blob_hash = None
        if old_version_hash != current_blob_hash:
            blob = bucket.new_blob("{}/{}-{}-{}.json".format(r, rev["data_version"], rev["timestamp"], rev["changed_by"]))
            futures.append(blob.upload(old_version, session))
        else:
            # The caller wants to be able to count the number of revisions that were uploaded
            # or already exist in GCS. Making sure we have a result to count for every
            # revision is the simplest way to do this.
            async def noop():
                return r
            futures.append(noop())

    return asyncio.gather(*futures)


async def main(loop, balrog_api, bucket_name):
    # limit the number of connections to balrog at any one time
    sem = asyncio.Semaphore(20)
    uploads = defaultdict(int)
    releases = {}

    n = 0

    # TODO: ok to share the session between balrog and gcs?
    async with aiohttp.ClientSession(loop=loop) as session:
        storage = Storage(session=session)
        bucket = storage.get_bucket(bucket_name)

        print(balrog_api)
        async with session.get("{}/releases".format(balrog_api)) as resp:
            for r in (await resp.json())["releases"]:
                releases[r["name"]] = r["data_version"]

        release_futures = []
        for r in releases:
            if any(pat in r for pat in skip_patterns):
                print("Skipping {} because it matches a skip pattern".format(r))
            n += 1
            if n == 10:
                break

            release_futures.append(process_release(r, session, balrog_api, bucket, sem))

        done, pending = await asyncio.wait(release_futures, timeout=30)
        for d in done:
            for res in await d.result():
                if "name" in res:
                    name = res["name"].split("/")[0]
                else:
                    name = res
                uploads[name] += 1

        while pending:
            print("{} releases left to process...".format(len(pending)))
            done, pending = await asyncio.wait(pending, timeout=30)
            for d in done:
                for res in await d.result():
                    if "name" in res:
                        name = res["name"].split("/")[0]
                    else:
                        name = res
                    uploads[name] += 1


    for r in releases:
        if r not in uploads:
            print("WARNING: {} was found in the Balrog API but does not exist in GCS".format(r))
        elif releases[r] != uploads[r]:
            print("WARNING: {} has a data version of {} in the Balrog API, but {} revisions exist in GCS".format(r, releases[r], uploads[r]))

balrog_api = sys.argv[1]
bucket_name = sys.argv[2]
loop = asyncio.get_event_loop()
ignore_aiohttp_ssl_error(loop)
loop.run_until_complete(main(loop, balrog_api, bucket_name))
