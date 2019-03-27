import re
import connexion
import logging
import auslib

from os import path
from flask import request
from flask_compress import Compress
from auslib.web.admin.views.problem import problem
from auslib.web.admin.views.validators import BalrogRequestBodyValidator
from raven.contrib.flask import Sentry
from specsynthase.specbuilder import SpecBuilder

try:
    from urllib import unquote
except ImportError:  # pragma: no cover
    from urllib.parse import unquote


log = logging.getLogger(__name__)

current_dir = path.dirname(__file__)
web_dir = path.dirname(auslib.web.__file__)

spec = SpecBuilder().add_spec(path.join(current_dir, 'swagger/api.yaml'))\
                    .add_spec(path.join(web_dir, 'common/swagger/definitions.yml'))\
                    .add_spec(path.join(web_dir, 'common/swagger/parameters.yml'))\
                    .add_spec(path.join(web_dir, 'common/swagger/responses.yml'))

validator_map = {
    'body': BalrogRequestBodyValidator
}

connexion_app = connexion.App(__name__, validator_map=validator_map, debug=False)
connexion_app.add_api(spec, strict_validation=True)
app = connexion_app.app
sentry = Sentry()

from auslib.dockerflow import create_dockerflow_endpoints

create_dockerflow_endpoints(app)


# When running under uwsgi, paths will not get decoded before hitting the app.
# We need to handle this ourselves in certain fields, and adding converters
# for them is the best way to do this.
class UnquotingMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ["PATH_INFO"] = unquote(environ["PATH_INFO"])
        return self.app(environ, start_response)


app.wsgi_app = UnquotingMiddleware(app.wsgi_app)


@app.errorhandler(500)
def ise(error):
    log.error("Caught ISE 500 error.")
    log.debug("Request path is: %s", request.path)
    log.debug("Request environment is: %s", request.environ)
    log.debug("Request headers are: %s", request.headers)
    return problem(500, "Internal Server Error", "Internal Server Error")


# Connexion's error handling sometimes breaks when parameters contain
# unicode characters (https://github.com/zalando/connexion/issues/604).
# To work around, we catch them and return a 400 (which is what Connexion
# would do if it didn't hit this error).
@app.errorhandler(UnicodeEncodeError)
def unicode(error):
    return problem(400, "Unicode Error", "Connexion was unable to parse some unicode data correctly.")


@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers["Strict-Transport-Security"] = app.config.get("STRICT_TRANSPORT_SECURITY", "max-age=31536000;")
    if re.match("^/ui/", request.path):
        # This enables swagger-ui to dynamically fetch and
        # load the swagger specification JSON file containing API definition and examples.
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    else:
        response.headers["Content-Security-Policy"] = \
            app.config.get("CONTENT_SECURITY_POLICY", "default-src 'none'; frame-ancestors 'none'")
    return response


Compress(app)
