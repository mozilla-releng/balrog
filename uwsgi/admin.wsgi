import logging
import os

import six
from flask_wtf.csrf import CSRFProtect

from auslib.global_state import cache, dbo
from auslib.log import configure_logging
from auslib.web.admin.base import app as application

SYSTEM_ACCOUNTS = ["balrogagent", "balrog-ffxbld", "balrog-tbirdbld", "seabld"]
DOMAIN_WHITELIST = {
    "download.mozilla.org": ("Firefox", "Fennec", "Devedition", "SeaMonkey", "Thunderbird"),
    "archive.mozilla.org": ("Firefox", "Fennec", "Devedition", "SeaMonkey", "Thunderbird"),
    "download.cdn.mozilla.net": ("Firefox", "Fennec", "SeaMonkey"),
    "mozilla-nightly-updates.s3.amazonaws.com": ("Firefox",),
    "ciscobinary.openh264.org": ("OpenH264",),
    "cdmdownload.adobe.com": ("CDM",),
    "clients2.googleusercontent.com": ("Widevine",),
    "redirector.gvt1.com": ("Widevine",),
    "ftp.mozilla.org": ("SystemAddons",),
}
if os.environ.get("STAGING"):
    SYSTEM_ACCOUNTS.extend(["balrog-stage-ffxbld", "balrog-stage-tbirdbld"])
    DOMAIN_WHITELIST.update({
        "ftp.stage.mozaws.net": ("Firefox", "Fennec", "Devedition", "SeaMonkey", "Thunderbird"),
        "bouncer-bouncer-releng.stage.mozaws.net": ("Firefox", "Fennec", "Devedition", "SeaMonkey", "Thunderbird"),
    })

# Logging needs to be set-up before importing the application to make sure that
# logging done from other modules uses our Logger.
logging_kwargs = {
    "level": os.environ.get("LOG_LEVEL", logging.INFO)
}
if os.environ.get("LOG_FORMAT") == "plain":
    logging_kwargs["formatter"] = logging.Formatter
configure_logging(**logging_kwargs)


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
cache.make_cache('users', 1, 300)

dbo.setDb(os.environ["DBURI"])
if os.environ.get("NOTIFY_TO_ADDR"):
    use_tls = False
    if os.environ.get("SMTP_TLS"):
        use_tls = True
    dbo.setupChangeMonitors(
        os.environ["SMTP_HOST"],
        os.environ["SMTP_PORT"],
        os.environ.get("SMTP_USERNAME"),
        os.environ.get("SMTP_PASSWORD"),
        os.environ["NOTIFY_TO_ADDR"],
        os.environ["NOTIFY_FROM_ADDR"],
        use_tls,
    )
dbo.setSystemAccounts(SYSTEM_ACCOUNTS)
dbo.setDomainWhitelist(DOMAIN_WHITELIST)
application.config["WHITELISTED_DOMAINS"] = DOMAIN_WHITELIST
application.config["PAGE_TITLE"] = "Balrog Administration"
application.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

class JSONCSRFProtect(CSRFProtect):
    def _get_csrf_token(self):
        from flask import current_app, request

        def get_token():
            token = CSRFProtect._get_csrf_token(self)
            yield token
            field_name = current_app.config["WTF_CSRF_FIELD_NAME"]
            if request.json:
                token = request.json.get(field_name)
                yield token
            token = request.args.get(field_name)
            yield token

        for token in get_token():
            if token:
                return token


JSONCSRFProtect(application)


# Secure cookies should be enabled when we're using https (otherwise the
# session cookie won't get set, and that will cause CSRF failures).
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
    application.config["SENTRY_DSN"] = os.environ.get("SENTRY_DSN")
    from auslib.web.admin.base import sentry
    sentry.init_app(application)

# version.json is created when the Docker image is built, and contains details
# about the current code (version number, commit hash), but doesn't exist in
# the repo itself
application.config["VERSION_FILE"] = "/app/version.json"

auth0_config = {
    "AUTH0_CLIENT_ID": os.environ["AUTH0_CLIENT_ID"],
    "AUTH0_REDIRECT_URI": os.environ["AUTH0_REDIRECT_URI"],
    "AUTH0_DOMAIN": os.environ["AUTH0_DOMAIN"],
    "AUTH0_AUDIENCE": os.environ["AUTH0_AUDIENCE"],
    "AUTH0_RESPONSE_TYPE": os.environ["AUTH0_RESPONSE_TYPE"],
    "AUTH0_SCOPE": os.environ["AUTH0_SCOPE"],
}
application.config["AUTH_DOMAIN"] = os.environ["AUTH0_DOMAIN"]
application.config["AUTH_AUDIENCE"] = os.environ["AUTH0_AUDIENCE"]

application.config["M2M_ACCOUNT_MAPPING"] = {
    # Local dev
    "41U6XJQdSa6CL8oGa6CXvO4aZWlnq5xg": "balrogagent",
    # Dev
    "R6Tpyx7clqQFmR6bvkAUJodV4J8V8LdQ": "balrogagent",
    # Stage
    "tKirJIJUQ5D5wU1oxPoA1qxEzmMHnB4h": "balrogagent",
    "tGbG2QUboAQpF35j1p40dpD2XYiC4AB7": "balrog-stage-ffxbld",
    "nyfi9KOMJZXAq3xjkF57wSwkJS2gUkHO": "balrog-stage-tbirdbld",
    # Prod
    "6TpOQiDH9UhSUouLrxlLP7PbWyJ8epsa": "balrogagent",
    "DqmXymgjiz6XuRXIewDnuR7oB8bOxkf0": "balrog-ffxbld",
    "ztM3MdGFNjbPYOq7R4br2EukKhuL6qlY": "balrog-tbirdbld",
}

# Generate frontend config
# It feels a bit hacky to be writing out a frontend config on the fly, but none
# of the alternatives seemed better (baking dev/stage/prod configs into one image,
# building separate images for those environments, cloudops maintaining this config).
frontend_config = os.environ.get("FRONTEND_CONFIG", "/app/ui/dist/js/config.js")
config_dir = os.path.dirname(frontend_config)
if not os.path.exists(config_dir):
    os.makedirs(config_dir)
with open(frontend_config, "w+") as f:
    f.write("""
angular.module('config', [])

.constant('Auth0Config', {});
""".format(auth0_config))
