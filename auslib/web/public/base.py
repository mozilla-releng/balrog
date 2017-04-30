import cgi
import connexion
import logging

from flask import make_response, send_from_directory, Response

from raven.contrib.flask import Sentry

from auslib.AUS import AUS
from auslib.web.api_validator import BalrogParameterValidator

from auslib.errors import BadDataError

log = logging.getLogger(__name__)
AUS = AUS()
sentry = Sentry()

validator_map = {
    'parameter': BalrogParameterValidator
}

connexion_app = connexion.App(__name__, specification_dir='.', validator_map=validator_map)
connexion_app.add_api('api.yml', validate_responses=True, strict_validation=True)
app = connexion_app.app


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


# Keeping static files endpoints here due to an issue when returning response for static files.
# Similar issue: https://github.com/zalando/connexion/issues/401
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
