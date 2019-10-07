import logging
import os

from auslib.log import configure_logging

SPECIAL_FORCE_HOSTS = ["http://download.mozilla.org"]
DOMAIN_WHITELIST = {
    "download.mozilla.org": ("Firefox", "Fennec", "Devedition", "Thunderbird"),
    "archive.mozilla.org": ("Firefox", "Fennec", "Devedition", "Thunderbird"),
    "download.cdn.mozilla.net": ("Firefox", "Fennec"),
    "mozilla-nightly-updates.s3.amazonaws.com": ("Firefox",),
    "ciscobinary.openh264.org": ("OpenH264",),
    "cdmdownload.adobe.com": ("CDM",),
    "clients2.googleusercontent.com": ("Widevine",),
    "redirector.gvt1.com": ("Widevine",),
    "ftp.mozilla.org": ("SystemAddons",),
    "fpn.firefox.com": ("Guardian",),
}
if os.environ.get("STAGING") or os.environ.get("LOCALDEV"):
    DOMAIN_WHITELIST.update(
        {
            "ftp.stage.mozaws.net": ("Firefox", "Fennec", "Devedition", "SeaMonkey", "Thunderbird"),
            "bouncer-bouncer-releng.stage.mozaws.net": ("Firefox", "Fennec", "Devedition", "SeaMonkey", "Thunderbird"),
        }
    )

# Logging needs to be set-up before importing the application to make sure that
# logging done from other modules uses our Logger.
logging_kwargs = {"level": os.environ.get("LOG_LEVEL", logging.INFO)}
if os.environ.get("LOG_FORMAT") == "plain":
    logging_kwargs["formatter"] = logging.Formatter
configure_logging(**logging_kwargs)

from auslib.global_state import cache, dbo  # noqa
from auslib.web.public.base import app as application  # noqa

cache.make_cache("blob", 500, 3600)
# There's probably no no need to ever expire items in the blob schema cache
# at all because they only change during deployments (and new instances of the
# apps will be created at that time, with an empty cache).
# Our cache doesn't support never expiring items, so we have set something.
cache.make_cache("blob_schema", 50, 24 * 60 * 60)
cache.make_cache("blob_version", 500, 60)

# 500 is probably a bit oversized for the rules cache, but the items are so
# small there sholudn't be any negative effect.
cache.make_cache("rules", 500, 30)

# Cache the emergency update state for a minute. We have less than 100
# product/channel combinations we care about.
cache.make_cache("updates_disabled", 100, 60)

dbo.setDb(os.environ["DBURI"])
dbo.setDomainWhitelist(DOMAIN_WHITELIST)
application.config["WHITELISTED_DOMAINS"] = DOMAIN_WHITELIST
application.config["SPECIAL_FORCE_HOSTS"] = SPECIAL_FORCE_HOSTS
# version.json is created when the Docker image is built, and contains details
# about the current code (version number, commit hash), but doesn't exist in
# the repo itself
application.config["VERSION_FILE"] = "/app/version.json"

if os.environ.get("SENTRY_DSN"):
    application.config["SENTRY_DSN"] = os.environ.get("SENTRY_DSN")
    from auslib.web.public.base import sentry

    sentry.init_app(application, register_signal=False)

if os.environ.get("CACHE_CONTROL"):
    application.config["CACHE_CONTROL"] = os.environ["CACHE_CONTROL"]

if os.environ.get("STAGING"):
    application.config["SWAGGER_DEBUG"] = True
