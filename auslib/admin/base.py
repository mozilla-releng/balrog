from flask import Flask, request

from auslib import version
from auslib.db import AUSDatabase

import logging
log = logging.getLogger(__name__)

app = Flask(__name__)
db = AUSDatabase()

from auslib.admin.views.csrf import CSRFView
from auslib.admin.views.permissions import UsersView, PermissionsView, \
  SpecificPermissionView, PermissionsPageView, UserPermissionsPageView
from auslib.admin.views.releases import SingleLocaleView, SingleBlobView, \
  SingleReleaseView, ReleasesPageView, ReleaseHistoryView
from auslib.admin.views.rules import RulesPageView, RulesAPIView, \
  SingleRuleView, RuleHistoryView
from auslib.admin.views.history import DiffView, FieldView
from auslib.admin.views.index import IndexPageView, RecentChangesTableView

@app.errorhandler(500)
def isa(error):
    log.error("Caught ISE 500 error.")
    log.debug("Balrog version is: %s", version)
    log.debug("Request path is: %s", request.path)
    log.debug("Request environment is: %s", request.environ)
    log.debug("Request headers are: %s", request.headers)
    return error

app.add_url_rule('/csrf_token', view_func=CSRFView.as_view('csrf'))
app.add_url_rule('/users', view_func=UsersView.as_view('users'))
app.add_url_rule('/users/<username>/permissions', view_func=PermissionsView.as_view('permissions'))
app.add_url_rule('/users/<username>/permissions/<path:permission>', view_func=SpecificPermissionView.as_view('specific_permission'))
# Some permissions may start with a slash, and the <path> converter won't match them, so we need an extra rule to cope.
app.add_url_rule('/users/<username>/permissions//<path:permission>', view_func=SpecificPermissionView.as_view('specific_permission'))
app.add_url_rule('/permissions.html', view_func=PermissionsPageView.as_view('permissions.html'))
app.add_url_rule('/user_permissions.html', view_func=UserPermissionsPageView.as_view('user_permissions.html'))
app.add_url_rule('/releases/<release>/builds/<platform>/<locale>', view_func=SingleLocaleView.as_view('single_locale'))
app.add_url_rule('/releases/<release>/data', view_func=SingleBlobView.as_view('release_data'))
app.add_url_rule('/releases/<release>/revisions/', view_func=ReleaseHistoryView.as_view('release_revisions'))
app.add_url_rule('/releases/<release>', view_func=SingleReleaseView.as_view('release'))
app.add_url_rule('/releases.html', view_func=ReleasesPageView.as_view('releases.html'))
app.add_url_rule('/rules.html', view_func=RulesPageView.as_view('rules.html'))
app.add_url_rule('/rules', view_func=RulesAPIView.as_view('rules'))
app.add_url_rule('/rules/<rule_id>/revisions/', view_func=RuleHistoryView.as_view('revisions.html'))
app.add_url_rule('/rules/<rule_id>', view_func=SingleRuleView.as_view('setrule'))
app.add_url_rule('/history/diff/<type_>/<change_id>/<field>', view_func=DiffView.as_view('diff'))
app.add_url_rule('/history/view/<type_>/<change_id>/<field>', view_func=FieldView.as_view('field'))
app.add_url_rule('/recent_changes_table.html', view_func=RecentChangesTableView.as_view(''))
app.add_url_rule('/', view_func=IndexPageView.as_view('index.html'))
