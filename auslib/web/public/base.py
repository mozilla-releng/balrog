import cgi
import connexion
import logging
log = logging.getLogger(__name__)

from flask import make_response, send_from_directory, abort, Response

from raven.contrib.flask import Sentry

from auslib.AUS import AUS
from auslib.dockerflow import create_dockerflow_endpoints

connexion_app = connexion.App(__name__)
connexion_app.add_api('api.yml')
app = connexion_app.app
AUS = AUS()
sentry = Sentry()

# from auslib.web.public.views.client import ClientRequestView
from auslib.errors import BadDataError


def heartbeat_database_function(dbo):
    # web has only a read access to the database. That's why we don't use
    # the default database function.
    # Counting the rules should be a trivial enough operation that it won't
    # cause notable load, but will verify that the database works.
    return dbo.rules.countRules()


create_dockerflow_endpoints(app, heartbeat_database_function)


@app.after_request
def apply_security_headers(response):
    # There's no use cases for content served by Balrog to load additional content
    # nor be embedded elsewhere, so we apply a strict Content Security Policy.
    # We also need to set X-Content-Type-Options to nosniff for Firefox to obey this.
    # See https://bugzilla.mozilla.org/show_bug.cgi?id=1332829#c4 for background.
    response.headers["Content-Security-Policy"] = app.config.get("CONTENT_SECURITY_POLICY", "default-src 'none'; frame-ancestors 'none'")
    response.headers["Strict-Transport-Security"] = app.config.get("STRICT_TRANSPORT_SECURITY", "max-age=31536000;")
    response.headers["X-Content-Type-Options"] = app.config.get("CONTENT_TYPE_OPTIONS", "nosniff")
    return response


@app.errorhandler(404)
def fourohfour(error):
    """We don't return 404s in AUS. Instead, we return empty XML files"""
    response = make_response('<?xml version="1.0"?>\n<updates>\n</updates>')
    response.mimetype = 'text/xml'
    return response


@app.errorhandler(Exception)
def generic(error):
    """Deals with any unhandled exceptions. If the exception is not a
    BadDataError, it will be sent to Sentry, and a 400 will be returned,
    because BadDataErrors are considered to be the client's fault.
    Otherwise, the error is just re-raised (which causes a 500)."""

    # Escape exception messages before replying with them, because they may
    # contain user input.
    # See https://bugzilla.mozilla.org/show_bug.cgi?id=1332829 for background.
    error.message = cgi.escape(error.message)
    if isinstance(error, BadDataError):
        return Response(status=400, mimetype="text/plain", response=error.message)

    if sentry.client:
        sentry.captureException()

    return Response(status=500, mimetype="text/plain", response=error.message)


@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, "robots.txt")


@app.route('/contribute.json')
def contributejson():
    return send_from_directory(app.static_folder, "contribute.json")


@app.before_request
def set_cache_control():
    # By default, we want a cache that can be shared across requests from
    # different users ("public").
    # and a maximum age of 90 seconds, to keep our TTL low.
    # We bumped this from 60s -> 90s in November, 2016.
    setattr(app, 'cacheControl', app.config.get("CACHE_CONTROL", "public, max-age=90"))


@app.route('/update/1/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/update.xml')
@app.route('/update/2/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/update.xml')
@app.route('/update/3/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/update.xml')
@app.route('/update/4/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/%MOZ_VERSION%'
           '/update.xml')
@app.route('/update/5/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/%IMEI%/update.xml')
@app.route('/update/6/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%SYSTEM_CAPABILITIES%/%DISTRIBUTION%'
           '/%DISTRIBUTION_VERSION%/update.xml')
def unsubstituted_url_variables():
    abort(404)
