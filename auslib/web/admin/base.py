import urllib
import re

from flask import request
from flask_compress import Compress
from auslib.web.admin.views.validators import BalrogRequestBodyValidator
from raven.contrib.flask import Sentry

import connexion
import logging
log = logging.getLogger(__name__)

validator_map = {
    'body': BalrogRequestBodyValidator
}

# TODO set debug=False after fully migrating all the admin APIs
connexion_app = connexion.App(__name__, specification_dir='swagger/', validator_map=validator_map, debug=True)
connexion_app.add_api("api.yaml", validate_responses=True, strict_validation=True)
app = connexion_app.app
sentry = Sentry()

from auslib.web.admin.views.permissions import PermissionScheduledChangeHistoryView
from auslib.web.admin.views.releases import ReleaseScheduledChangeHistoryView
from auslib.web.admin.views.required_signoffs import \
    ProductRequiredSignoffScheduledChangeHistoryView, \
    PermissionsRequiredSignoffScheduledChangeHistoryView
from auslib.web.admin.views.rules import RuleScheduledChangeHistoryView
from auslib.dockerflow import create_dockerflow_endpoints


create_dockerflow_endpoints(app)


# When running under uwsgi, paths will not get decoded before hitting the app.
# We need to handle this ourselves in certain fields, and adding converters
# for them is the best way to do this.
class UnquotingMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ["PATH_INFO"] = urllib.unquote(environ["PATH_INFO"])
        return self.app(environ, start_response)


app.wsgi_app = UnquotingMiddleware(app.wsgi_app)


@app.errorhandler(500)
def ise(error):
    log.error("Caught ISE 500 error.")
    log.debug("Request path is: %s", request.path)
    log.debug("Request environment is: %s", request.environ)
    log.debug("Request headers are: %s", request.headers)
    return error


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


# Endpoints required for the Balrog 2.0 UI.
# In the Mozilla deployments of Balrog, both the the admin API (these endpoints)
# and the static admin UI are hosted on the same domain. This API wsgi app is
# hosted at "/api", which is stripped away by the web server before we see
# these requests.
app.add_url_rule("/scheduled_changes/rules/<int:sc_id>/revisions", view_func=RuleScheduledChangeHistoryView.as_view("scheduled_change_rules_history"))

app.add_url_rule("/scheduled_changes/permissions/<int:sc_id>/revisions",
                 view_func=PermissionScheduledChangeHistoryView.as_view("scheduled_change_permissions_history"))

app.add_url_rule("/scheduled_changes/releases/<int:sc_id>/revisions",
                 view_func=ReleaseScheduledChangeHistoryView.as_view("scheduled_change_releases_history"))

app.add_url_rule("/scheduled_changes/required_signoffs/product/<int:sc_id>/revisions",
                 view_func=ProductRequiredSignoffScheduledChangeHistoryView.as_view("scheduled_change_product_rs_history"))

app.add_url_rule("/scheduled_changes/required_signoffs/permissions/<int:sc_id>/revisions",
                 view_func=PermissionsRequiredSignoffScheduledChangeHistoryView.as_view("scheduled_change_permissions_rs_history"))
