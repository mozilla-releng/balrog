import asyncio
import logging
import os
import os.path
import sys

import aiohttp
import sentry_sdk
import statsd.defaults
from gcloud.aio.storage import Storage
from google.cloud import storage
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from auslib.log import configure_logging

STAGING = bool(int(os.environ.get("STAGING", 0)))
LOCALDEV = bool(int(os.environ.get("LOCALDEV", 0)))

SYSTEM_ACCOUNTS = ["balrogagent", "balrog-ffxbld", "balrog-tbirdbld", "seabld", "balrog-xpibld"]
DOMAIN_ALLOWLIST = {
    "download.mozilla.org": ("Firefox", "Fennec", "Devedition", "Thunderbird", "Pinebuild"),
    "archive.mozilla.org": ("Firefox", "Fennec", "Devedition", "Thunderbird", "FirefoxVPN", "Pinebuild", "SystemAddons"),
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
    SYSTEM_ACCOUNTS.extend(["balrog-stage-ffxbld", "balrog-stage-tbirdbld", "balrog-stage-xpibld"])
    DOMAIN_ALLOWLIST.update(
        {
            "ciscobinarytest.openh264.org": ("OpenH264",),
            "ftp.stage.mozaws.net": ("Firefox", "Fennec", "Devedition", "SeaMonkey", "Thunderbird", "Pinebuild", "SystemAddons"),
            "bouncer-bouncer.stage.mozaws.net": ("Firefox", "Fennec", "Devedition", "SeaMonkey", "Thunderbird"),
            "bouncer-bouncer-releng.stage.mozaws.net": ("Firefox", "Fennec", "Devedition", "SeaMonkey", "Thunderbird", "Pinebuild"),
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

log = logging.getLogger(__file__)

# statsd environment also needs to be set up before importing the application
statsd.defaults.PREFIX = "balrog.admin"

from auslib.global_state import cache, dbo  # noqa: E402
from auslib.web.admin.base import create_app  # noqa: E402

cors_origins = [o.strip() for o in os.environ.get("CORS_ORIGINS", "").split(",")] or None
connexion_app = create_app(allow_origins=cors_origins)
application = connexion_app.app

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
# Users cache to identify if an user is known by Balrog and
# has at least one permission.
cache.make_cache("users", 1, 300)

if not os.environ.get("RELEASES_HISTORY_BUCKET") or not os.environ.get("NIGHTLY_HISTORY_BUCKET"):
    log.critical("RELEASES_HISTORY_BUCKET and NIGHTLY_HISTORY_BUCKET must be provided")
    sys.exit(1)
if not LOCALDEV:
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ and not os.path.exists(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")):
        log.critical("GOOGLE_APPLICATION_CREDENTIALS provided, but does not exist")
        sys.exit(1)

if LOCALDEV and not os.path.exists(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")):
    log.info("Disabling releases_history writes for localdev without google credentials specified")
    buckets = None
else:
    # We use this factory instead of creating an instance of Storage here
    # because the async Storage creates an aiohttp.ClientSession upon instantiation,
    # which grabs a reference to the current EventLoop. Because we're using
    # asyncio.run in some endpoints to wait on coroutines, we end up with a
    # new EventLoop each time it is called. This means that the second time
    # Storage attempts to use the ClientSession it has created, the EventLoop
    # it holds will be closed, which completely breaks it.
    # (It is technically possible to override the ClientSession that a Storage
    # object holds, but it involves digging into the implementation details
    # of that object, as well as other objects it holds - so it's not a very
    # robust solution.)
    #
    # Because this is a factory, consumers (notably, GCSHistoryAsync) must
    # instantiate the Storage object themselves before they use it.
    def BucketFactory(bucket):
        def factory(*args, use_gcloud_aio=True, **kwargs):
            if use_gcloud_aio:
                return Storage(*args, **kwargs).get_bucket(bucket)
            else:
                # We tried to use the async Storage class for the
                # synchronous GCSHistory class, but hit issues with
                # Event Loops. This code will be removed in the near
                # future, so in the meantime we'll just continue
                # using the synchronous client.
                return storage.Client().get_bucket(bucket)

        return factory

    bucket_factory = BucketFactory

    # Order is important here, we fall through to the last entry. This works because dictionary keys
    # are returned in insertion order when iterated on.
    # Turn off formatting because it is clearer to have these listed one after another
    # fmt: off
    buckets = {
        "nightly": bucket_factory(os.environ["NIGHTLY_HISTORY_BUCKET"]),
        "": bucket_factory(os.environ["RELEASES_HISTORY_BUCKET"]),
    }
    # fmt: on

    # Check if we have write access, and set the bucket configuration appropriately
    # There's basically two cases here:
    #   * Credentials have been provided and can write to the buckets, or no credentials have been provided -> enable writes
    #   * Credentials have not been provided, or they can't write to the bucket
    #     * If we're local dev disable writes
    #     * If we're anywhere else, raise an Exception (local dev is the only place where we can be sure we can safely disable them)
    for bucket in buckets.values():
        # Needs to be wrapped so we can use `async with` to make sure ClientSession
        # gets closed.
        async def wrapper():
            async with aiohttp.ClientSession() as session:
                blob = bucket(session=session).new_blob("startuptest")
                await blob.upload("startuptest")

        asyncio.run(wrapper())

dbo.setDb(os.environ["DBURI"], buckets)
dbo.setSystemAccounts(SYSTEM_ACCOUNTS)
dbo.setDomainAllowlist(DOMAIN_ALLOWLIST)
application.config["ALLOWLISTED_DOMAINS"] = DOMAIN_ALLOWLIST
application.config["PAGE_TITLE"] = "Balrog Administration"
application.config["SECRET_KEY"] = os.environ["SECRET_KEY"]


# Secure cookies should be enabled when we're using https.
# For now, this means disabling it for local development. In the future
# we should start using self signed SSL for local dev, so we can enable it.
if not os.environ.get("INSECURE_SESSION_COOKIE"):
    application.config["SESSION_COOKIE_SECURE"] = True

# HttpOnly cookies can only be accessed by the browser (not javascript).
# This helps mitigate XSS attacks.
# https://www.owasp.org/index.php/HttpOnly#What_is_HttpOnly.3F
application.config["SESSION_COOKIE_HTTPONLY"] = True

# Strict Samesite cookies means that the session cookie will never be sent
# when loading any page or making any request where the referrer is some
# other site. For example, a link to Balrog from Gmail will not send the session
# cookie. Our session cookies are only necessary for POST/PUT/DELETE, so this
# won't break anything in the UI, but it provides the most secure protection.
# When we re-work auth, we may need to switch to Lax samesite cookies.
# https://tools.ietf.org/html/draft-west-first-party-cookies-07#section-4.1.1
application.config["SESSION_COOKIE_SAMESITE"] = "Strict"

if os.environ.get("SENTRY_DSN"):
    sentry_sdk.init(os.environ["SENTRY_DSN"], integrations=[FlaskIntegration(), LoggingIntegration()])

# version.json is created when the Docker image is built, and contains details
# about the current code (version number, commit hash), but doesn't exist in
# the repo itself
application.config["VERSION_FILE"] = "/app/version.json"

auth0_config = {
    "AUTH0_CLIENT_ID": os.environ["AUTH0_CLIENT_ID"],
    "AUTH0_REDIRECT_URI": os.environ["AUTH0_REDIRECT_URI"],
    "AUTH0_DOMAIN": os.environ["AUTH0_DOMAIN"],
    "AUTH0_AUDIENCE": os.environ["AUTH0_AUDIENCE"],
    "AUTH0_SCOPE": os.environ["AUTH0_SCOPE"],
}
application.config["AUTH_DOMAIN"] = os.environ["AUTH0_DOMAIN"]
application.config["AUTH_AUDIENCE"] = os.environ["AUTH0_AUDIENCE"]

application.config["M2M_ACCOUNT_MAPPING"] = {
    # Local dev - managed by RelEng
    "41U6XJQdSa6CL8oGa6CXvO4aZWlnq5xg": "balrogagent",
    # Other environments - managed by IT
    # Dev
    "XvPN9fQDqIEuQ05tImVHtcjqjZ6fZ360": "balrogagent",
    # Stage
    "LJWEpDTYRIsnddSwa7rgeGZdczaNaIKd": "balrogagent",
    "UH57Bj8yfUyQjRehPCQlHbRjyZ38k526": "balrog-stage-ffxbld",
    "zPmNwPov86PcswvnjEfsoocmQrMMPnS3": "balrog-stage-tbirdbld",
    "A8hmiRzpGYo6N3VzOzsBHzijZQRrNlZb": "balrog-stage-xpibld",
    # Prod
    "8MQB51S7XgaswbpyprqcQjfOweiGm3h5": "balrogagent",
    "GaX7R2sfI38tlsOos6Z4f5OrZu8EjBUX": "balrog-ffxbld",
    "Oz9caB7d57xutcNf9CwaczYnDTvXPIIX": "balrog-tbirdbld",
    "Z8vYcCTtOjPRCHaQNCfoXSU5PzNQKmr5": "balrog-xpibld",
}
