import cgi
import connexion
import logging
import re

import auslib.web

from os import path

from connexion import request
from flask import make_response, send_from_directory, Response

from raven.contrib.flask import Sentry

from auslib.AUS import AUS
from auslib.web.admin.views.problem import problem
from specsynthase.specbuilder import SpecBuilder

from auslib.errors import BadDataError

log = logging.getLogger(__name__)
AUS = AUS()
sentry = Sentry()

connexion_app = connexion.App(__name__,
                              specification_dir='.')
app = connexion_app.app

current_dir = path.dirname(__file__)
web_dir = path.dirname(auslib.web.__file__)
spec = SpecBuilder().add_spec(path.join(current_dir, 'swagger/api.yml'))\
                    .add_spec(path.join(current_dir, 'swagger/public_api_spec.yml'))\
                    .add_spec(path.join(web_dir, 'common/swagger/definitions.yml'))\
                    .add_spec(path.join(web_dir, 'common/swagger/parameters.yml'))\
                    .add_spec(path.join(web_dir, 'common/swagger/responses.yml'))
connexion_app.add_api(spec,
                      validate_responses=True,
                      strict_validation=True)


@app.after_request
def apply_security_headers(response):
    # There's no use cases for content served by Balrog to load additional content
    # nor be embedded elsewhere, so we apply a strict Content Security Policy.
    # We also need to set X-Content-Type-Options to nosniff for Firefox to obey this.
    # See https://bugzilla.mozilla.org/show_bug.cgi?id=1332829#c4 for background.
    response.headers["Strict-Transport-Security"] = app.config.get("STRICT_TRANSPORT_SECURITY", "max-age=31536000;")
    response.headers["X-Content-Type-Options"] = app.config.get("CONTENT_TYPE_OPTIONS", "nosniff")
    if re.match("^/ui/", request.path):
        # This enables swagger-ui to dynamically fetch and
        # load the swagger specification JSON file containing API definition and examples.
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    else:
        response.headers["Content-Security-Policy"] = \
            app.config.get("CONTENT_SECURITY_POLICY", "default-src 'none'; frame-ancestors 'none'")
    return response


@app.errorhandler(404)
def fourohfour(error):
    if re.match("^/update", request.path):
        """We don't return 404s for AUS /update endpoints. Instead, we return empty XML files"""
        response = make_response('<?xml version="1.0"?>\n<updates>\n</updates>')
        response.mimetype = 'text/xml'
        return response
    return Response(status=404, mimetype="text/plain", response=error.description)


# Connexion's error handling sometimes breaks when parameters contain
# unicode characters (https://github.com/zalando/connexion/issues/604).
# To work around, we catch them and return a 400 (which is what Connexion
# would do if it didn't hit this error).
@app.errorhandler(UnicodeEncodeError)
def unicode(error):
    return problem(400, "Unicode Error", "Connexion was unable to parse some unicode data correctly.")


@app.errorhandler(Exception)
def generic(error):
    """Deals with any unhandled exceptions. If the exception is not a
    BadDataError, it will be sent to Sentry, and a 400 will be returned,
    because BadDataErrors are considered to be the client's fault.
    Otherwise, the error is just re-raised (which causes a 500)."""

    # Escape exception messages before replying with them, because they may
    # contain user input.
    # See https://bugzilla.mozilla.org/show_bug.cgi?id=1332829 for background.
    # We used to look at error.message here, but that disappeared from many
    # Exception classes in Python 3, so args is the safer better.
    # We may want to stop returning messages like this to the client altogether
    # both because it's ugly and potentially can leak things, but it's also
    # extremely helpful for debugging BadDataErrors, because we don't send
    # information about them to Sentry.
    message = " ".join(getattr(error, "args", repr(error)))
    if isinstance(error, BadDataError):
        return Response(status=400, mimetype="text/plain", response=cgi.escape(message))

    if sentry.client:
        sentry.captureException()

    return Response(status=500, mimetype="text/plain", response=cgi.escape(message))


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


@app.route('/debug/api.yml')
def get_yaml():
    if app.config.get('SWAGGER_DEBUG', False):
        import yaml
        app_spec = yaml.dump(spec)
        return Response(mimetype='text/plain', response=app_spec)
    return Response(status=404)
