from flask import Flask, request
from flask_compress import Compress

from raven.contrib.flask import Sentry

import auslib

import logging
log = logging.getLogger(__name__)

app = Flask(__name__)
sentry = Sentry()

from auslib.admin.views.csrf import CSRFView
from auslib.admin.views.permissions import UsersView, PermissionsView, \
  SpecificPermissionView, PermissionsPageView, UserPermissionsPageView
from auslib.admin.views.releases import SingleLocaleView, SingleBlobView, \
  SingleReleaseView, ReleasesPageView, ReleaseHistoryView, \
  ReleasesAPIView
from auslib.admin.views.rules import RulesPageView, RulesAPIView, \
  SingleRuleView, RuleHistoryView, RuleHistoryAPIView
from auslib.admin.views.history import DiffView, FieldView
from auslib.admin.views.index import IndexPageView, RecentChangesTableView

@app.errorhandler(500)
def isa(error):
    log.error("Caught ISE 500 error.")
    log.debug("Balrog version is: %s", auslib.version)
    log.debug("Request path is: %s", request.path)
    log.debug("Request environment is: %s", request.environ)
    log.debug("Request headers are: %s", request.headers)
    return error

# bug 887790: add necessary security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

Compress(app)

# Endpoints required for the Balrog 2.0 UI.
app.add_url_rule("/api/csrf_token", view_func=CSRFView.as_view("api_csrf"))
app.add_url_rule("/api/users", view_func=UsersView.as_view("api_users"))
app.add_url_rule("/api/users/<username>/permissions", view_func=PermissionsView.as_view("api_user_permissions"))
app.add_url_rule("/api/users/<username>/permissions/<path:permission>", view_func=SpecificPermissionView.as_view("api_specific_permission"))
# Some permissions may start with a slash, and the <path> converter won"t match them, so we need an extra rule to cope.
app.add_url_rule("/api/users/<username>/permissions//<path:permission>", view_func=SpecificPermissionView.as_view("api_specific_permission2"))
app.add_url_rule("/api/rules", view_func=RulesAPIView.as_view("api_rules"))
app.add_url_rule("/api/rules/<rule_id>", view_func=SingleRuleView.as_view("api_rule"))
app.add_url_rule("/api/rules/<rule_id>/revisions", view_func=RuleHistoryAPIView.as_view("api_rules_revisions"))
app.add_url_rule("/api/releases", view_func=ReleasesAPIView.as_view("api_releases"))
app.add_url_rule("/api/releases/<release>", view_func=SingleReleaseView.as_view("api_releases_revision"))
app.add_url_rule("/api/releases/<release>/builds/<platform>/<locale>", view_func=SingleLocaleView.as_view("api_single_locale"))
app.add_url_rule("/api/releases/<release>/revisions", view_func=ReleaseHistoryView.as_view("api_release_revisions"))
app.add_url_rule("/api/history/diff/<type_>/<change_id>/<field>", view_func=DiffView.as_view("api_diff"))
app.add_url_rule("/api/history/view/<type_>/<change_id>/<field>", view_func=FieldView.as_view("api_field"))


# Deprecated endpoints. These can be removed when the old UI is shut off _and_ submitter tools use the new "/api" endpoints.
app.add_url_rule('/csrf_token', view_func=CSRFView.as_view('csrf'))
app.add_url_rule('/users', view_func=UsersView.as_view('users'))
app.add_url_rule('/users/<username>/permissions', view_func=PermissionsView.as_view('permissions'))
app.add_url_rule('/users/<username>/permissions/<path:permission>', view_func=SpecificPermissionView.as_view('specific_permission'))
# Some permissions may start with a slash, and the <path> converter won't match them, so we need an extra rule to cope.
app.add_url_rule('/users/<username>/permissions//<path:permission>', view_func=SpecificPermissionView.as_view('specific_permission2'))
app.add_url_rule('/releases/<release>/builds/<platform>/<locale>', view_func=SingleLocaleView.as_view('single_locale'))
app.add_url_rule('/releases/<release>/data', view_func=SingleBlobView.as_view('release_data'))
app.add_url_rule('/releases/<release>/revisions/', view_func=ReleaseHistoryView.as_view('release_revisions'))
app.add_url_rule('/releases/<release>', view_func=SingleReleaseView.as_view('release'))
app.add_url_rule('/rules', view_func=RulesAPIView.as_view('rules'))
app.add_url_rule('/rules/<rule_id>', view_func=SingleRuleView.as_view('setrule'))
app.add_url_rule('/history/diff/<type_>/<change_id>/<field>', view_func=DiffView.as_view('diff'))
app.add_url_rule('/history/view/<type_>/<change_id>/<field>', view_func=FieldView.as_view('field'))


# TODO: Kill these endpoints + their classes when the old admin ui is shut off
app.add_url_rule('/permissions.html', view_func=PermissionsPageView.as_view('permissions.html'))
app.add_url_rule('/user_permissions.html', view_func=UserPermissionsPageView.as_view('user_permissions.html'))
app.add_url_rule('/releases.html', view_func=ReleasesPageView.as_view('releases.html'))
app.add_url_rule('/rules.html', view_func=RulesPageView.as_view('rules.html'))
app.add_url_rule('/recent_changes_table.html', view_func=RecentChangesTableView.as_view(''))
app.add_url_rule('/rules/<rule_id>/revisions/', view_func=RuleHistoryView.as_view('revisions.html'))
app.add_url_rule('/', view_func=IndexPageView.as_view('index.html'))
