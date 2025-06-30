import logging
import re
from os import path

import connexion
from flask import request
from sentry_sdk import capture_exception
from specsynthase.specbuilder import SpecBuilder

import auslib
from auslib.dockerflow import create_dockerflow_endpoints
from auslib.errors import BlobValidationError, PermissionDeniedError, ReadOnlyError, SignoffRequiredError
from auslib.util.auth import verified_userinfo
from auslib.web.admin.views.problem import problem
from auslib.web.admin.views.validators import BalrogRequestBodyValidator

log = logging.getLogger(__name__)

current_dir = path.dirname(__file__)
web_dir = path.dirname(auslib.web.__file__)

spec = (
    SpecBuilder()
    .add_spec(path.join(current_dir, "swagger/api.yml"))
    .add_spec(path.join(web_dir, "common/swagger/definitions.yml"))
    .add_spec(path.join(web_dir, "common/swagger/parameters.yml"))
    .add_spec(path.join(web_dir, "common/swagger/responses.yml"))
)

validator_map = {"body": BalrogRequestBodyValidator}

connexion_app = connexion.App(__name__, debug=False, options={"swagger_ui": False})
connexion_app.add_api(spec, validator_map=validator_map, strict_validation=True)
connexion_app.add_api(path.join(current_dir, "swagger", "api_v2.yml"), base_path="/v2", strict_validation=True, validate_responses=True)
app = connexion_app.app

create_dockerflow_endpoints(app)


@app.before_request
def setup_request():
    if request.full_path.startswith("/v2"):
        from auslib.global_state import dbo

        request.transaction = dbo.begin()

        if request.method in ("POST", "PUT", "DELETE"):
            username = verified_userinfo(request, app.config["AUTH_DOMAIN"], app.config["AUTH_AUDIENCE"])["email"]
            if not username:
                log.warning("Login Required")
                return problem(401, "Unauthenticated", "Login Required")
            # Machine to machine accounts are identified by uninformative clientIds
            # In order to keep Balrog permissions more readable, we map them to
            # more useful usernames, which are stored in the app config.
            if "@" not in username:
                username = app.config["M2M_ACCOUNT_MAPPING"].get(username, username)
            # Even if the user has provided a valid access token, we don't want to assume
            # that person should be able to access Balrog (in case auth0 is not configured
            # to be restrictive enough.
            elif not dbo.isKnownUser(username):
                log.warning("Authorization Required")
                return problem(403, "Forbidden", "Authorization Required")

            request.username = username


@app.after_request
def complete_request(response):
    if hasattr(request, "transaction"):
        try:
            if response.status_code >= 400:
                request.transaction.rollback()
            else:
                request.transaction.commit()
        finally:
            request.transaction.close()

    return response


@app.errorhandler(BlobValidationError)
def blob_validation_error(error):
    return problem(400, "Bad Request", "Invalid Blob", ext={"exception": error.errors})


@app.errorhandler(SignoffRequiredError)
def signoff_required_error(error):
    return problem(400, "Bad Request", "Signoff Required", ext={"exception": f"{error}"})


@app.errorhandler(ReadOnlyError)
def read_only_error(error):
    return problem(400, "Bad Request", "Read only", ext={"exception": f"{error}"})


@app.errorhandler(PermissionDeniedError)
def permission_denied_error(error):
    return problem(403, "Forbidden", "Permission Denied", ext={"exception": f"{error}"})


@app.errorhandler(ValueError)
def value_error(error):
    return problem(400, "Bad Request", "Unknown error", ext={"exception": f"{error}"})


# Connexion's error handling sometimes breaks when parameters contain
# unicode characters (https://github.com/zalando/connexion/issues/604).
# To work around, we catch them and return a 400 (which is what Connexion
# would do if it didn't hit this error).
@app.errorhandler(UnicodeEncodeError)
def unicode(error):
    return problem(400, "Unicode Error", "Connexion was unable to parse some unicode data correctly.")


@app.errorhandler(Exception)
def ise(error):
    capture_exception(error)
    log.exception("Caught ISE 500 error: %r", error)
    log.debug("Request path is: %s", request.path)
    log.debug("Request environment is: %s", request.environ)
    log.debug("Request headers are: %s", request.headers)
    return problem(500, "Internal Server Error", "Internal Server Error")


@app.after_request
def add_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = app.config.get("STRICT_TRANSPORT_SECURITY", "max-age=31536000;")
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST, PUT, DELETE"
    if "*" in app.config["CORS_ORIGINS"]:
        response.headers["Access-Control-Allow-Origin"] = "*"
    elif "Origin" in request.headers and request.headers["Origin"] in app.config["CORS_ORIGINS"]:
        response.headers["Access-Control-Allow-Origin"] = request.headers["Origin"]
    if re.match("^/ui/", request.path):
        # This enables swagger-ui to dynamically fetch and
        # load the swagger specification JSON file containing API definition and examples.
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
    else:
        response.headers["Content-Security-Policy"] = app.config.get("CONTENT_SECURITY_POLICY", "default-src 'none'; frame-ancestors 'none'")
    return response
