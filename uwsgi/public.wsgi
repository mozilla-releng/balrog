import logging
import os
import sys

import auslib.log


SYSTEM_ACCOUNTS = ["ffxbld", "tbirdbld", "b2gbld", "stage-ffxbld", "stage-tbirdbld", "stage-b2gbld"]
SPECIAL_FORCE_HOSTS = ["http://download.mozilla.org"]
DOMAIN_WHITELIST = [
    "download.mozilla.org", "stage.mozilla.org", "ftp.mozilla.org",
    "ciscobinary.openh264.org", "cdmdownload.adobe.com",
    "queue.taskcluster.net", "download.cdn.mozilla.net",
    "mozilla-nightly-updates.s3.amazonaws.com",
    "archive.mozilla.org",
    "mozilla-releng-nightly-promotion-mozilla-central.b2gdroid.s3.amazonaws.com",
]

# Logging needs to be set-up before importing the application to make sure that
# logging done from other modules uses our Logger.
logging.setLoggerClass(auslib.log.BalrogLogger)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format=auslib.log.log_format)

from auslib.global_state import cache, dbo
from auslib.web.base import app as application

# TODO: How to do cef logging in CloudOps? Do we need to?
auslib.log.cef_config = auslib.log.get_cef_config("syslog")

cache.make_cache("blob", 500, 3600)
# There's probably no no need to ever expire items in the blob schema cache
# at all because they only change during deployments (and new instances of the
# apps will be created at that time, with an empty cache).
# Our cache doesn't support never expiring items, so we have set something.
cache.make_cache("blob_schema", 50, 24 * 60 * 60)
cache.make_cache("blob_version", 500, 60)

dbo.setDb(os.environ["DBURI"])
dbo.setDomainWhitelist(DOMAIN_WHITELIST)
application.config["WHITELISTED_DOMAINS"] = DOMAIN_WHITELIST
application.config["SPECIAL_FORCE_HOSTS"] = SPECIAL_FORCE_HOSTS
# version.json is created when the Docker image is built, and contains details
# about the current code (version number, commit hash), but doesn't exist in
# the repo itself
application.config["VERSION_FILE"] = "/app/version.json"
