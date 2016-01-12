import logging
import os
import sys

import auslib.log


SYSTEM_ACCOUNTS = ["ffxbld", "tbirdbld", "b2gbld", "stage-ffxbld", "stage-tbirdbld", "stage-b2gbld"]
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

from auslib.admin.base import app as application
from auslib.global_state import cache, dbo

# TODO: How to do cef logging in CloudOps? Do we need to?
auslib.log.cef_config = auslib.log.get_cef_config("syslog")

cache.make_cache("blob", 500, 3600)
cache.make_cache("blob_version", 500, 60)

dbo.setDb(os.environ["DBURI"])
dbo.setupChangeMonitors(SYSTEM_ACCOUNTS)
dbo.setDomainWhitelist(DOMAIN_WHITELIST)
application.config["WHITELISTED_DOMAINS"] = DOMAIN_WHITELIST
application.config["PAGE_TITLE"] = "Balrog Administration"
application.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
