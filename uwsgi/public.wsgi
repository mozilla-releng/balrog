import logging
import os

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

import statsd.defaults

from auslib.log import configure_logging

STAGING = bool(int(os.environ.get("STAGING", 0)))
LOCALDEV = bool(int(os.environ.get("LOCALDEV", 0)))

SPECIAL_FORCE_HOSTS = ["http://download.mozilla.org"]
DOMAIN_ALLOWLIST = {
    "download.mozilla.org": ("Firefox", "Fennec", "Devedition", "Thunderbird"),
    "archive.mozilla.org": (
        "Firefox",
        "Fennec",
        "Devedition",
        "Thunderbird",
        "FirefoxVPN",
        "SystemAddons",
    ),
    "download.cdn.mozilla.net": ("Firefox", "Fennec"),
    "ciscobinary.openh264.org": ("OpenH264",),
    "cdmdownload.adobe.com": ("CDM",),
    "clients2.googleusercontent.com": ("Widevine",),
    "edgedl.me.gvt1.com": (
        "Widevine",
        "Widevine-L1",
    ),
    "redirector.gvt1.com": (
        "Widevine",
        "Widevine-L1",
    ),
    "www.google.com": {
        "/dl/release2/chrome_component/[\\w\\.]+/[\\w\\.]+\\.crx3": (
            "Widevine",
            "Widevine-L1",
        ),
    },
    "ftp.mozilla.org": ("SystemAddons",),
    "fpn.firefox.com": ("FirefoxVPN", "Guardian"),
    "vpn.mozilla.org": ("FirefoxVPN", "Guardian"),
}
if STAGING or LOCALDEV:
    DOMAIN_ALLOWLIST.update(
        {
            "ftp.stage.mozaws.net": ("Firefox", "Fennec", "Devedition", "SeaMonkey", "Thunderbird"),
            "bouncer-bouncer.stage.mozaws.net": ("Firefox", "Fennec", "Devedition", "SeaMonkey", "Thunderbird"),
            "bouncer-bouncer-releng.stage.mozaws.net": ("Firefox", "Fennec", "Devedition", "SeaMonkey", "Thunderbird"),
            "dev.bouncer.nonprod.webservices.mozgcp.net": ("Firefox", "Fennec", "Devedition", "SeaMonkey", "Thunderbird", "Pinebuild"),
            "stage.guardian.nonprod.cloudops.mozgcp.net": ("FirefoxVPN", "Guardian"),
            "stage-vpn.guardian.nonprod.cloudops.mozgcp.net": ("FirefoxVPN", "Guardian"),
        }
    )

# Logging needs to be set-up before importing the application to make sure that
# logging done from other modules uses our Logger.
logging_kwargs = {"level": os.environ.get("LOG_LEVEL", logging.INFO)}
if os.environ.get("LOG_FORMAT") == "plain":
    logging_kwargs["formatter"] = logging.Formatter
configure_logging(**logging_kwargs)

# statsd environment also needs to be set up before importing the application
statsd.defaults.PREFIX = "balrog.public"

from auslib.global_state import cache, dbo  # noqa
from auslib.web.public.base import create_app

application = create_app().app

if os.environ.get("AUTOGRAPH_URL"):
    application.config["AUTOGRAPH_URL"] = os.environ["AUTOGRAPH_URL"]
    application.config["AUTOGRAPH_KEYID"] = os.environ["AUTOGRAPH_KEYID"]
    application.config["AUTOGRAPH_USERNAME"] = os.environ["AUTOGRAPH_USERNAME"]
    application.config["AUTOGRAPH_PASSWORD"] = os.environ["AUTOGRAPH_PASSWORD"]

    # Autograph responses
    # If additional types of responses require signing, consider increasing the size of this cache.
    # We cache for one day to make sure we resign once per day, because the signatures eventually expire.
    cache.make_cache("content_signatures", 200, 86400)

if os.environ.get("AUTOGRAPH_GMP_URL"):
    application.config["AUTOGRAPH_GMP_URL"] = os.environ["AUTOGRAPH_GMP_URL"]
    application.config["AUTOGRAPH_GMP_KEYID"] = os.environ["AUTOGRAPH_GMP_KEYID"]
    application.config["AUTOGRAPH_GMP_USERNAME"] = os.environ["AUTOGRAPH_GMP_USERNAME"]
    application.config["AUTOGRAPH_GMP_PASSWORD"] = os.environ["AUTOGRAPH_GMP_PASSWORD"]
elif "AUTOGRAPH_URL" in application.config:
    application.config["AUTOGRAPH_GMP_URL"] = application.config["AUTOGRAPH_URL"]
    application.config["AUTOGRAPH_GMP_KEYID"] = application.config["AUTOGRAPH_KEYID"]
    application.config["AUTOGRAPH_GMP_USERNAME"] = application.config["AUTOGRAPH_USERNAME"]
    application.config["AUTOGRAPH_GMP_PASSWORD"] = application.config["AUTOGRAPH_PASSWORD"]

cache.make_cache("blob", 500, 3600)
cache.make_cache("releases", 500, 3600)
cache.make_cache("releases_data_version", 500, 60)
cache.make_cache("release_assets", 500, 3600)
cache.make_cache("release_assets_data_versions", 5000, 60)
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
dbo.setDomainAllowlist(DOMAIN_ALLOWLIST)
application.config["ALLOWLISTED_DOMAINS"] = DOMAIN_ALLOWLIST
application.config["SPECIAL_FORCE_HOSTS"] = SPECIAL_FORCE_HOSTS
# version.json is created when the Docker image is built, and contains details
# about the current code (version number, commit hash), but doesn't exist in
# the repo itself
application.config["VERSION_FILE"] = "/app/version.json"
application.config["CONTENT_SIGNATURE_PRODUCTS"] = ["GMP"]

if os.environ.get("SENTRY_DSN"):
    sentry_sdk.init(os.environ["SENTRY_DSN"], integrations=[FlaskIntegration(), LoggingIntegration()])

if os.environ.get("CACHE_CONTROL"):
    application.config["CACHE_CONTROL"] = os.environ["CACHE_CONTROL"]

if STAGING:
    application.config["SWAGGER_DEBUG"] = True
