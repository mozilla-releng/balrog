import urllib

from flask import Flask, request
from flask_compress import Compress

from raven.contrib.flask import Sentry

import logging
log = logging.getLogger(__name__)

app = Flask(__name__)
sentry = Sentry()

from auslib.web.admin.views.csrf import CSRFView
from auslib.web.admin.views.permissions import UsersView, PermissionsView, \
    SpecificPermissionView, UserRolesView, UserRoleView, AllRolesView, \
    PermissionScheduledChangesView, PermissionScheduledChangeView, \
    EnactPermissionScheduledChangeView, PermissionScheduledChangeHistoryView, \
    PermissionScheduledChangeSignoffsView, SpecificUserView
from auslib.web.admin.views.releases import SingleLocaleView, \
    SingleReleaseView, ReleaseHistoryView, \
    ReleasesAPIView, SingleReleaseColumnView, ReleaseReadOnlyView, \
    ReleaseScheduledChangesView, ReleaseScheduledChangeView, \
    EnactReleaseScheduledChangeView, ReleaseScheduledChangeHistoryView, \
    ReleaseScheduledChangeSignoffsView, ReleaseFieldView, ReleaseDiffView
from auslib.web.admin.views.required_signoffs import ProductRequiredSignoffsView, \
    ProductRequiredSignoffsHistoryAPIView, \
    ProductRequiredSignoffsScheduledChangesView, \
    ProductRequiredSignoffScheduledChangeView, \
    EnactProductRequiredSignoffScheduledChangeView, \
    ProductRequiredSignoffScheduledChangeSignoffsView, \
    ProductRequiredSignoffScheduledChangeHistoryView, \
    PermissionsRequiredSignoffsView, \
    PermissionsRequiredSignoffsHistoryAPIView, \
    PermissionsRequiredSignoffsScheduledChangesView, \
    PermissionsRequiredSignoffScheduledChangeView, \
    EnactPermissionsRequiredSignoffScheduledChangeView, \
    PermissionsRequiredSignoffScheduledChangeSignoffsView, \
    PermissionsRequiredSignoffScheduledChangeHistoryView
from auslib.web.admin.views.rules import RulesAPIView, \
    SingleRuleView, RuleHistoryAPIView, SingleRuleColumnView, \
    RuleScheduledChangesView, RuleScheduledChangeView, \
    EnactRuleScheduledChangeView, RuleScheduledChangeHistoryView, \
    RuleScheduledChangeSignoffsView
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
    response.headers["Content-Security-Policy"] = app.config.get("CONTENT_SECURITY_POLICY", "default-src 'none'; frame-ancestors 'none'")
    return response


Compress(app)


# Endpoints required for the Balrog 2.0 UI.
# In the Mozilla deployments of Balrog, both the the admin API (these endpoints)
# and the static admin UI are hosted on the same domain. This API wsgi app is
# hosted at "/api", which is stripped away by the web server before we see
# these requests.
app.add_url_rule("/csrf_token", view_func=CSRFView.as_view("csrf"))
app.add_url_rule("/users", view_func=UsersView.as_view("users"))
app.add_url_rule("/users/roles", view_func=AllRolesView.as_view("all_users_roles"))
app.add_url_rule("/users/<username>", view_func=SpecificUserView.as_view("specific_user"))
app.add_url_rule("/users/<username>/permissions", view_func=PermissionsView.as_view("user_permissions"))
app.add_url_rule("/users/<username>/permissions/<permission>", view_func=SpecificPermissionView.as_view("specific_permission"))
app.add_url_rule("/users/<username>/roles", view_func=UserRolesView.as_view("user_roles"))
app.add_url_rule("/users/<username>/roles/<role>", view_func=UserRoleView.as_view("user_role"))
app.add_url_rule("/rules", view_func=RulesAPIView.as_view("rules"))
# Normal operations (get/update/delete) on rules can be done by id or alias...
app.add_url_rule("/rules/<id_or_alias>", view_func=SingleRuleView.as_view("rule"))
app.add_url_rule("/rules/columns/<column>", view_func=SingleRuleColumnView.as_view("rule_columns"))
# ...but anything to do with history must be done by id, beacuse alias may change over time
app.add_url_rule("/rules/<int:rule_id>/revisions", view_func=RuleHistoryAPIView.as_view("rules_revisions"))
app.add_url_rule("/releases", view_func=ReleasesAPIView.as_view("releases"))
app.add_url_rule("/releases/<release>", view_func=SingleReleaseView.as_view("single_release"))
app.add_url_rule("/releases/<release>/read_only", view_func=ReleaseReadOnlyView.as_view("read_only"))
app.add_url_rule("/releases/<release>/builds/<platform>/<locale>", view_func=SingleLocaleView.as_view("single_locale"))
app.add_url_rule("/releases/<release>/revisions", view_func=ReleaseHistoryView.as_view("release_revisions"))
app.add_url_rule("/releases/columns/<column>", view_func=SingleReleaseColumnView.as_view("release_columns"))
app.add_url_rule("/required_signoffs/product", view_func=ProductRequiredSignoffsView.as_view("product_required_signoffs"))
app.add_url_rule("/required_signoffs/product/revisions", view_func=ProductRequiredSignoffsHistoryAPIView.as_view("product_required_signoffs_revisions"))
app.add_url_rule("/required_signoffs/permissions", view_func=PermissionsRequiredSignoffsView.as_view("permissions_required_signoffs"))
app.add_url_rule("/required_signoffs/permissions/revisions",
                 view_func=PermissionsRequiredSignoffsHistoryAPIView.as_view("permissions_required_signoffs_revisions"))
app.add_url_rule("/history/diff/release/<change_id>/<field>", view_func=ReleaseDiffView.as_view("release_diff"))
app.add_url_rule("/history/view/release/<change_id>/<field>", view_func=ReleaseFieldView.as_view("release_field"))
app.add_url_rule("/scheduled_changes/rules", view_func=RuleScheduledChangesView.as_view("scheduled_changes_rules"))
app.add_url_rule("/scheduled_changes/rules/<int:sc_id>", view_func=RuleScheduledChangeView.as_view("scheduled_change_rules"))
app.add_url_rule("/scheduled_changes/rules/<int:sc_id>/enact", view_func=EnactRuleScheduledChangeView.as_view("enact_scheduled_change_rules"))
app.add_url_rule("/scheduled_changes/rules/<int:sc_id>/signoffs", view_func=RuleScheduledChangeSignoffsView.as_view("scheduled_change_rules_signoffs"))
app.add_url_rule("/scheduled_changes/rules/<int:sc_id>/revisions", view_func=RuleScheduledChangeHistoryView.as_view("scheduled_change_rules_history"))
app.add_url_rule("/scheduled_changes/permissions", view_func=PermissionScheduledChangesView.as_view("scheduled_changes_permissions"))
app.add_url_rule("/scheduled_changes/permissions/<int:sc_id>", view_func=PermissionScheduledChangeView.as_view("scheduled_change_permissions"))
app.add_url_rule("/scheduled_changes/permissions/<int:sc_id>/enact", view_func=EnactPermissionScheduledChangeView.as_view("enact_scheduled_change_permissions"))
app.add_url_rule("/scheduled_changes/permissions/<int:sc_id>/signoffs",
                 view_func=PermissionScheduledChangeSignoffsView.as_view("scheduled_change_permissions_signoffs"))
app.add_url_rule("/scheduled_changes/permissions/<int:sc_id>/revisions",
                 view_func=PermissionScheduledChangeHistoryView.as_view("scheduled_change_permissions_history"))
app.add_url_rule("/scheduled_changes/releases", view_func=ReleaseScheduledChangesView.as_view("scheduled_changes_releases"))
app.add_url_rule("/scheduled_changes/releases/<int:sc_id>", view_func=ReleaseScheduledChangeView.as_view("scheduled_change_releases"))
app.add_url_rule("/scheduled_changes/releases/<int:sc_id>/enact", view_func=EnactReleaseScheduledChangeView.as_view("enact_scheduled_change_releases"))
app.add_url_rule("/scheduled_changes/releases/<int:sc_id>/signoffs", view_func=ReleaseScheduledChangeSignoffsView.as_view("scheduled_change_release_signoffs"))
app.add_url_rule("/scheduled_changes/releases/<int:sc_id>/revisions",
                 view_func=ReleaseScheduledChangeHistoryView.as_view("scheduled_change_releases_history"))
app.add_url_rule("/scheduled_changes/required_signoffs/product", view_func=ProductRequiredSignoffsScheduledChangesView.as_view("scheduled_changes_product_rs"))
app.add_url_rule("/scheduled_changes/required_signoffs/product/<int:sc_id>",
                 view_func=ProductRequiredSignoffScheduledChangeView.as_view("scheduled_change_product_rs"))
app.add_url_rule("/scheduled_changes/required_signoffs/product/<int:sc_id>/enact",
                 view_func=EnactProductRequiredSignoffScheduledChangeView.as_view("enact_scheduled_change_product_rs"))
app.add_url_rule("/scheduled_changes/required_signoffs/product/<int:sc_id>/signoffs",
                 view_func=ProductRequiredSignoffScheduledChangeSignoffsView.as_view("scheduled_change_product_rs_signoffs"))
app.add_url_rule("/scheduled_changes/required_signoffs/product/<int:sc_id>/revisions",
                 view_func=ProductRequiredSignoffScheduledChangeHistoryView.as_view("scheduled_change_product_rs_history"))
app.add_url_rule("/scheduled_changes/required_signoffs/permissions",
                 view_func=PermissionsRequiredSignoffsScheduledChangesView.as_view("scheduled_changes_permissions_rs"))
app.add_url_rule("/scheduled_changes/required_signoffs/permissions/<int:sc_id>",
                 view_func=PermissionsRequiredSignoffScheduledChangeView.as_view("scheduled_change_permissions_rs"))
app.add_url_rule("/scheduled_changes/required_signoffs/permissions/<int:sc_id>/enact",
                 view_func=EnactPermissionsRequiredSignoffScheduledChangeView.as_view("enact_scheduled_change_permissions_rs"))
app.add_url_rule("/scheduled_changes/required_signoffs/permissions/<int:sc_id>/signoffs",
                 view_func=PermissionsRequiredSignoffScheduledChangeSignoffsView.as_view("scheduled_change_permissions_rs_signoffs"))
app.add_url_rule("/scheduled_changes/required_signoffs/permissions/<int:sc_id>/revisions",
                 view_func=PermissionsRequiredSignoffScheduledChangeHistoryView.as_view("scheduled_change_permissions_rs_history"))
