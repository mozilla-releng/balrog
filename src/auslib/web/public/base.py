import html
import logging
import re
from os import path

import connexion
from connexion import request
from connexion.options import SwaggerUIOptions
from flask import send_from_directory
from connexion.lifecycle import ConnexionRequest, ConnexionResponse
from sentry_sdk import capture_exception
from specsynthase.specbuilder import SpecBuilder

import auslib.web
from auslib.errors import BadDataError
from auslib.web.admin.views.problem import problem

log = logging.getLogger(__name__)

swagger_ui_options = SwaggerUIOptions(swagger_ui=False)

connexion_app = connexion.FlaskApp(__name__, specification_dir=".", swagger_ui_options=swagger_ui_options)
flask_app = connexion_app.app

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
# Response validation should be enabled when it actually works
connexion_app.add_api(spec, strict_validation=True)


from starlette.datastructures import MutableHeaders
from connexion.middleware import MiddlewarePosition

class SecurityHeadersMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def send_with_extra_headers(message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers["Strict-Transport-Security"] = flask_app.config.get("STRICT_TRANSPORT_SECURITY", "max-age=31536000;")
                headers["X-Content-Type-Options"] = flask_app.config.get("CONTENT_TYPE_OPTIONS", "nosniff")
                path = scope["path"]
                if re.match("^/ui/", path):
                    # This enables swagger-ui to dynamically fetch and
                    # load the swagger specification JSON file containing API definition and examples.
                    headers["X-Frame-Options"] = "SAMEORIGIN"
                else:
                    headers["Content-Security-Policy"] = flask_app.config.get("CONTENT_SECURITY_POLICY", "default-src 'none'; frame-ancestors 'none'")

            await send(message)

        await self.app(scope, receive, send_with_extra_headers)
connexion_app.add_middleware(SecurityHeadersMiddleware, position=MiddlewarePosition.BEFORE_EXCEPTION,)

def fourohfour(request, error):
    if re.match("^/update", request.url.path):
        """We don't return 404s for AUS /update endpoints. Instead, we return empty XML files"""
        response = ConnexionResponse(status_code=200, mimetype="text/xml", body='<?xml version="1.0"?>\n<updates>\n</updates>')
        return response
    return ConnexionResponse(status_code=404, mimetype="text/plain", body=error.detail)
connexion_app.add_error_handler(404, fourohfour)


# Connexion's error handling sometimes breaks when parameters contain
# unicode characters (https://github.com/zalando/connexion/issues/604).
# To work around, we catch them and return a 400 (which is what Connexion
# would do if it didn't hit this error).
def unicode_handler(request, error):
    return problem(400, "Unicode Error", "Connexion was unable to parse some unicode data correctly.")
connexion_app.add_error_handler(UnicodeEncodeError, unicode_handler)


def generic_handler(request, error):
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

    if hasattr(error, "args"):
        message = " ".join(str(a) for a in error.args)
    else:
        message = repr(error)
    if isinstance(error, BadDataError):
        return ConnexionResponse(status_code=400, mimetype="text/plain", body=html.escape(message, quote=False))

    # Sentry doesn't handle exceptions for `@app.errorhandler(Exception)`
    # implicitly. If Sentry is not configured, the following call returns None.
    capture_exception(error)

    return ConnexionResponse(status_code=500, mimetype="text/plain", body=html.escape(message, quote=False))
connexion_app.add_error_handler(Exception, generic_handler)


def robots():
    return send_from_directory(flask_app.static_folder, "robots.txt")


def contribute():
    return send_from_directory(flask_app.static_folder, "contribute.json")

#
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
        return ConnexionResponse(mimetype="text/plain", response=app_spec)
    return ConnexionResponse(status=404)
