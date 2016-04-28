import logging
import os

from auslib.log import configure_logging


SYSTEM_ACCOUNTS = ["ffxbld", "tbirdbld", "b2gbld", "stage-ffxbld", "stage-tbirdbld", "stage-b2gbld"]
DOMAIN_WHITELIST = {
    "download.mozilla.org": ("Firefox", "Fennec", "Thunderbird"),
    "archive.mozilla.org": ("Firefox", "Fennec", "Thunderbird"),
    "download.cdn.mozilla.net": ("Firefox", "Fennec"),
    "mozilla-nightly-updates.s3.amazonaws.com": ("Firefox",),
    "ciscobinary.openh264.org": ("GMP",),
    "cdmdownload.adobe.com": ("GMP",),
    "clients2.googleusercontent.com": ("GMP",),
    "ftp.mozilla.org": ("SystemAddons",),
}

# Logging needs to be set-up before importing the application to make sure that
# logging done from other modules uses our Logger.
logging_kwargs = {
    "level": os.environ.get("LOG_LEVEL", logging.INFO)
}
if os.environ.get("LOG_FORMAT") == "plain":
    logging_kwargs["formatter"] = logging.Formatter
configure_logging(**logging_kwargs)

from auslib.admin.base import app as application
from auslib.global_state import cache, dbo

cache.make_copies = True
# We explicitly don't want a blob_version cache here because it will cause
# issues where we run multiple instances of the admin app. Even though each
# app will update its caches when it updates the db, the others would still
# be out of sync for up to the length of the blob_version cache timeout.
cache.make_cache("blob", 500, 3600)
# There's probably no no need to ever expire items in the blob schema cache
# at all because they only change during deployments (and new instances of the
# apps will be created at that time, with an empty cache).
# Our cache doesn't support never expiring items, so we have set something.
cache.make_cache("blob_schema", 50, 24 * 60 * 60)

dbo.setDb(os.environ["DBURI"])
if os.environ.get("NOTIFY_TO_ADDR"):
    dbo.setupChangeMonitors(
        os.environ["SMTP_HOST"],
        os.environ["SMTP_PORT"],
        os.environ["SMTP_USERNAME"],
        os.environ["SMTP_PASSWORD"],
        os.environ["NOTIFY_TO_ADDR"],
        os.environ["NOTIFY_FROM_ADDR"]
    )
dbo.setDomainWhitelist(DOMAIN_WHITELIST)
application.config["WHITELISTED_DOMAINS"] = DOMAIN_WHITELIST
application.config["PAGE_TITLE"] = "Balrog Administration"
application.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
# version.json is created when the Docker image is built, and contains details
# about the current code (version number, commit hash), but doesn't exist in
# the repo itself
application.config["VERSION_FILE"] = "/app/version.json"
