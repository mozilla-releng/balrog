from os import path

from flask import Flask, request, jsonify, Response
from flask_compress import Compress

import auslib

import logging
log = logging.getLogger(__name__)

app = Flask(__name__)

from auslib.admin.views.csrf import CSRFView
from auslib.admin.views.permissions import UsersView, PermissionsView, \
    SpecificPermissionView
from auslib.admin.views.releases import SingleLocaleView, \
    SingleReleaseView, ReleaseHistoryView, \
    ReleasesAPIView
from auslib.admin.views.rules import RulesAPIView, \
    SingleRuleView, RuleHistoryAPIView
from auslib.admin.views.history import DiffView, FieldView
from auslib.global_state import dbo


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
    return response

Compress(app)

# Endpoints required for the Balrog 2.0 UI.
# In the Mozilla deployments of Balrog, both the the admin API (these endpoints)
# and the static admin UI are hosted on the same domain. This API wsgi app is
# hosted at "/api", which is stripped away by the web server before we see
# these requests.
app.add_url_rule("/csrf_token", view_func=CSRFView.as_view("csrf"))
app.add_url_rule("/users", view_func=UsersView.as_view("users"))
app.add_url_rule("/users/<username>/permissions", view_func=PermissionsView.as_view("user_permissions"))
app.add_url_rule("/users/<username>/permissions/<path:permission>", view_func=SpecificPermissionView.as_view("specific_permission"))
# Some permissions may start with a slash, and the <path> converter won"t match them, so we need an extra rule to cope.
app.add_url_rule("/users/<username>/permissions//<path:permission>", view_func=SpecificPermissionView.as_view("specific_permission2"))
app.add_url_rule("/rules", view_func=RulesAPIView.as_view("rules"))
# Normal operations (get/update/delete) on rules can be done by id or alias...
app.add_url_rule("/rules/<id_or_alias>", view_func=SingleRuleView.as_view("rule"))
# ...but anything to do with history must be done by id, beacuse alias may change over time
app.add_url_rule("/rules/<int:rule_id>/revisions", view_func=RuleHistoryAPIView.as_view("rules_revisions"))
app.add_url_rule("/releases", view_func=ReleasesAPIView.as_view("releases"))
app.add_url_rule("/releases/<release>", view_func=SingleReleaseView.as_view("single_release"))
app.add_url_rule("/releases/<release>/builds/<platform>/<locale>", view_func=SingleLocaleView.as_view("single_locale"))
app.add_url_rule("/releases/<release>/revisions", view_func=ReleaseHistoryView.as_view("release_revisions"))
app.add_url_rule("/history/diff/<type_>/<change_id>/<field>", view_func=DiffView.as_view("diff"))
app.add_url_rule("/history/view/<type_>/<change_id>/<field>", view_func=FieldView.as_view("field"))


# Endpoints required by CloudOps as part of the Dockerflow spec: https://github.com/mozilla-services/Dockerflow


@app.route("/__version__")
def version():
    version_file = app.config.get("VERSION_FILE")
    if version_file and path.exists(version_file):
        with open(app.config["VERSION_FILE"]) as f:
            version_json = f.read()
        return Response(version_json, mimetype="application/json")
    else:
        return jsonify({
            "source": "https://github.com/mozilla/balrog",
            "version": "unknown",
            "commit": "unknown",
        })


@app.route("/__heartbeat__")
def heartbeat():
    """Per the Dockerflow spec:
    Respond to /__heartbeat__ with a HTTP 200 or 5xx on error. This should
    depend on services like the database to also ensure they are healthy."""
    # Counting the rules should be a trivial enough operation that it won't
    # cause notable load, but will verify that the database works.
    dbo.rules.countRules()
    return "OK!"


@app.route("/__lbheartbeat__")
def lbheartbeat():
    """Per the Dockerflow spec:
    Respond to /__lbheartbeat__ with an HTTP 200. This is for load balancer
    checks and should not check any dependent services."""
    return "OK!"
