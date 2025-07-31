import html
import logging
import re
from os import path

import connexion
from flask import Response, g, make_response, request, send_from_directory
from sentry_sdk import capture_exception
from specsynthase.specbuilder import SpecBuilder
from statsd.defaults.env import statsd

import auslib.web
from auslib.errors import BadDataError
from auslib.web.admin.views.problem import problem

log = logging.getLogger(__name__)

current_dir = path.dirname(__file__)
web_dir = path.dirname(auslib.web.__file__)
spec = (
    SpecBuilder()
    .add_spec(path.join(current_dir, "swagger/api.yml"))
    .add_spec(path.join(current_dir, "swagger/public_api_spec.yml"))
    .add_spec(path.join(web_dir, "common/swagger/definitions.yml"))
    .add_spec(path.join(web_dir, "common/swagger/parameters.yml"))
    .add_spec(path.join(web_dir, "common/swagger/responses.yml"))
)


def create_app():
    connexion_app = connexion.App(__name__, specification_dir=".", options={"swagger_ui": False})
    flask_app = connexion_app.app

    # Response validation should be enabled when it actually works
    connexion_app.add_api(spec, strict_validation=True)

    @flask_app.after_request
    def apply_security_headers(response):
        # There's no use cases for content served by Balrog to load additional content
        # nor be embedded elsewhere, so we apply a strict Content Security Policy.
        # We also need to set X-Content-Type-Options to nosniff for Firefox to obey this.
        # See https://bugzilla.mozilla.org/show_bug.cgi?id=1332829#c4 for background.
        response.headers["Strict-Transport-Security"] = flask_app.config.get("STRICT_TRANSPORT_SECURITY", "max-age=31536000;")
        response.headers["X-Content-Type-Options"] = flask_app.config.get("CONTENT_TYPE_OPTIONS", "nosniff")
        if re.match("^/ui/", request.path):
            # This enables swagger-ui to dynamically fetch and
            # load the swagger specification JSON file containing API definition and examples.
            response.headers["X-Frame-Options"] = "SAMEORIGIN"
        else:
            response.headers["Content-Security-Policy"] = flask_app.config.get("CONTENT_SECURITY_POLICY", "default-src 'none'; frame-ancestors 'none'")
        return response

    @flask_app.errorhandler(404)
    def fourohfour(error):
        if re.match("^/update", request.path):
            """We don't return 404s for AUS /update endpoints. Instead, we return empty XML files"""
            response = make_response('<?xml version="1.0"?>\n<updates>\n</updates>')
            response.mimetype = "text/xml"
            return response
        return Response(status=404, mimetype="text/plain", response=error.description)

    # Connexion's error handling sometimes breaks when parameters contain
    # unicode characters (https://github.com/zalando/connexion/issues/604).
    # To work around, we catch them and return a 400 (which is what Connexion
    # would do if it didn't hit this error).
    @flask_app.errorhandler(UnicodeEncodeError)
    def unicode(error):
        return problem(400, "Unicode Error", "Connexion was unable to parse some unicode data correctly.")

    @flask_app.errorhandler(BadDataError)
    def baddata(error):
        """Deals with BadDataError exceptions by returning a 400,
        because BadDataErrors are considered to be the client's fault.
        """
        # Escape exception messages before replying with them, because they may
        # contain user input.
        # See https://bugzilla.mozilla.org/show_bug.cgi?id=1332829 for background.
        # We used to look at error.message here, but that disappeared from many
        # Exception classes in Python 3, so args is the safer bet.
        # We may want to stop returning messages like this to the client altogether
        # both because it's ugly and potentially can leak things, but it's also
        # extremely helpful for debugging BadDataErrors, because we don't send
        # information about them to Sentry.
        if hasattr(error, "args"):
            message = " ".join(str(a) for a in error.args)
        else:
            message = repr(error)

        return Response(status=400, mimetype="text/plain", response=html.escape(message, quote=False))

    @flask_app.errorhandler(Exception)
    def generic(error):
        """Deals with any unhandled exceptions. It will be sent to Sentry, and re-raised (which causes a 500)."""

        # Sentry doesn't handle exceptions for `@flask_app.errorhandler(Exception)`
        # implicitly. If Sentry is not configured, the following call returns None.
        capture_exception(error)

        raise

    # Keeping static files endpoints here due to an issue when returning response for static files.
    # Similar issue: https://github.com/zalando/connexion/issues/401
    @flask_app.route("/robots.txt")
    def robots():
        return send_from_directory(flask_app.static_folder, "robots.txt")

    @flask_app.route("/contribute.json")
    def contributejson():
        return send_from_directory(flask_app.static_folder, "contribute.json")

    @flask_app.before_request
    def create_statsd_pipeline():
        g.statsd = statsd.pipeline()

    @flask_app.after_request
    def send_statsd_pipeline(response):
        g.statsd.send()
        return response

    @flask_app.before_request
    def set_cache_control():
        # By default, we want a cache that can be shared across requests from
        # different users ("public").
        # and a maximum age of 90 seconds, to keep our TTL low.
        # We bumped this from 60s -> 90s in November, 2016.
        setattr(flask_app, "cacheControl", flask_app.config.get("CACHE_CONTROL", "public, max-age=90"))

    @flask_app.route("/debug/api.yml")
    def get_yaml():
        if flask_app.config.get("SWAGGER_DEBUG", False):
            import yaml

            app_spec = yaml.dump(spec)
            return Response(mimetype="text/plain", response=app_spec)
        return Response(status=404)

    # setting this up last means it will be called first. we do this because
    # an exception in an earlier `after_request` handler will prevent this from
    # being called.
    @flask_app.after_request
    def log_request(response):
        # we only expect GET requests; we don't care about anything else
        if request.method != "GET":
            return response
        # don't time dockerflow endpoints
        if request.path.startswith("/__"):
            return response

        # this is safe because even if the path is "/", we'll still get a 2 item list
        prefix = request.path.split("/")[1]
        if prefix not in ("update", "json", "api"):
            prefix = "unknown"
        g.statsd.incr(f"response.{prefix}.{response.status_code}")

        return response

    return connexion_app
