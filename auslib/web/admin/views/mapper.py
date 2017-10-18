from auslib.web.admin.views.csrf import CSRFView

from auslib.web.admin.views.rules import RulesAPIView, SingleRuleView, SingleRuleColumnView, \
    RuleHistoryAPIView, RuleScheduledChangesView, EnactRuleScheduledChangeView, RuleScheduledChangeSignoffsView, \
    RuleScheduledChangeView, RuleScheduledChangeHistoryView

from auslib.web.admin.views.permissions import UsersView, AllRolesView, SpecificUserView,\
    PermissionsView, UserRolesView, UserRoleView, SpecificPermissionView, PermissionScheduledChangesView, \
    EnactPermissionScheduledChangeView, PermissionScheduledChangeSignoffsView, PermissionScheduledChangeView, \
    PermissionScheduledChangeHistoryView

from auslib.web.admin.views.releases import ReleaseDiffView, ReleaseFieldView, ReleasesAPIView, SingleReleaseView,\
    ReleaseReadOnlyView, SingleReleaseColumnView, SingleLocaleView, ReleaseHistoryView, ReleaseScheduledChangesView, \
    EnactReleaseScheduledChangeView, ReleaseScheduledChangeSignoffsView, ReleaseScheduledChangeView, \
    ReleaseScheduledChangeHistoryView

from auslib.web.admin.views.required_signoffs import ProductRequiredSignoffsHistoryAPIView, \
    PermissionsRequiredSignoffsHistoryAPIView, ProductRequiredSignoffsView, PermissionsRequiredSignoffsView,\
    ProductRequiredSignoffsScheduledChangesView, PermissionsRequiredSignoffsScheduledChangesView, \
    EnactProductRequiredSignoffScheduledChangeView, EnactPermissionsRequiredSignoffScheduledChangeView, \
    ProductRequiredSignoffScheduledChangeSignoffsView, PermissionsRequiredSignoffScheduledChangeSignoffsView, \
    ProductRequiredSignoffScheduledChangeView, PermissionsRequiredSignoffScheduledChangeView, \
    ProductRequiredSignoffScheduledChangeHistoryView, PermissionsRequiredSignoffScheduledChangeHistoryView


def csrf_get():
    """GET /csrf_token"""
    return CSRFView().get()


def rules_post():
    """POST /rules"""
    return RulesAPIView().post()


def rules_id_or_alias_post(id_or_alias):
    """POST /rules/:id"""
    return SingleRuleView().post(id_or_alias)


def rules_id_or_alias_put(id_or_alias):
    """PUT /rules/:id"""
    return SingleRuleView().put(id_or_alias)


def rules_id_or_alias_delete(id_or_alias):
    """DELETE /rules/:id"""
    return SingleRuleView().delete(id_or_alias)


def single_rule_column_get(column):
    """GET /rules/columns/:column"""
    return SingleRuleColumnView().get(column)


def rules_revisions_post(rule_id):
    """POST /rules/:id/revisions"""
    return RuleHistoryAPIView().post(rule_id)


def users_get():
    """GET /users"""
    return UsersView().get()


def all_users_roles_get():
    """GET /users/roles"""
    return AllRolesView().get()


def specific_user_get(username):
    """GET /users/:username"""
    return SpecificUserView().get(username)


def user_permissions_get(username):
    """GET /users/:username/permissions"""
    return PermissionsView().get(username)


def user_get_roles(username):
    """GET /users/:username/roles"""
    return UserRolesView().get(username)


def user_role_put(username, role):
    """PUT /users/:username/roles/:role"""
    return UserRoleView().put(username, role)


def user_role_delete(username, role):
    """DELETE /users/:username/roles/:role"""
    return UserRoleView().delete(username, role)


def user_specific_permission_get(username, permission):
    """GET /users/:username/permissions/:permission"""
    return SpecificPermissionView().get(username, permission)


def user_specific_permission_put(username, permission):
    """PUT /users/:username/permissions/:permission"""
    return SpecificPermissionView().put(username, permission)


def user_specific_permission_post(username, permission):
    """POST /users/:username/permissions/:permission"""
    return SpecificPermissionView().post(username, permission)


def user_specific_permission_delete(username, permission):
    """DELETE /users/:username/permissions/:permission"""
    return SpecificPermissionView().delete(username, permission)


def release_diff_history_get(change_id, field):
    """GET /history/diff/release/:id/:field"""
    return ReleaseDiffView().get(change_id, field)


def release_view_history_get(change_id, field):
    """GET /history/view/release/:id/:field"""
    return ReleaseFieldView().get(change_id, field)


def release_get():
    """GET /releases"""
    return ReleasesAPIView().get()


def release_post():
    """POST /releases"""
    return ReleasesAPIView().post()


def single_release_post(release):
    """POST /releases/:release"""
    return SingleReleaseView().post(release)


def single_release_put(release):
    """PUT /releases/:release"""
    return SingleReleaseView().put(release)


def single_release_delete(release):
    """DELETE /releases/:release"""
    return SingleReleaseView().delete(release)


def release_read_only_get(release):
    """GET /releases/:release/read_only"""
    return ReleaseReadOnlyView().get(release)


def release_read_only_put(release):
    """PUT /releases/:release/read_only"""
    return ReleaseReadOnlyView().put(release)


def release_single_column_get(column):
    """GET /releases/columns/:column"""
    return SingleReleaseColumnView().get(column)


def release_single_locale_view_put(release, platform, locale):
    """PUT /releases/[release]/builds/[platform]/[locale]"""
    return SingleLocaleView().put(release, platform, locale)


def release_history_view_post(release):
    """POST /releases/:release/revisions"""
    return ReleaseHistoryView().post(release)


def required_signoffs_product_revisions_get():
    """GET /required_signoffs/product/revisions"""
    return ProductRequiredSignoffsHistoryAPIView().get()


def required_signoffs_permissions_revisions_get():
    """GET /required_signoffs/permissions/revisions"""
    return PermissionsRequiredSignoffsHistoryAPIView().get()


def required_signoffs_product_get():
    """GET /required_signoffs/product"""
    return ProductRequiredSignoffsView().get()


def required_signoffs_product_post():
    """POST /required_signoffs/product"""
    return ProductRequiredSignoffsView().post()


def required_signoffs_product_delete():
    """DELETE /required_signoffs/product"""
    return ProductRequiredSignoffsView().delete()


def required_signoffs_permissions_get():
    """GET /required_signoffs/permissions"""
    return PermissionsRequiredSignoffsView().get()


def required_signoffs_permissions_post():
    """POST /required_signoffs/permissions"""
    return PermissionsRequiredSignoffsView().post()


def required_signoffs_permissions_delete():
    """DELETE /required_signoffs/permissions"""
    return PermissionsRequiredSignoffsView().delete()


def scheduled_changes_rules_get():
    """GET /scheduled_changes/rules"""
    return RuleScheduledChangesView().get()


def scheduled_changes_rules_post():
    """POST /scheduled_changes/rules"""
    return RuleScheduledChangesView().post()


def scheduled_changes_permissions_get():
    """GET /scheduled_changes/permissions"""
    return PermissionScheduledChangesView().get()


def scheduled_changes_permissions_post():
    """POST /scheduled_changes/permissions"""
    return PermissionScheduledChangesView().post()


def scheduled_changes_releases_get():
    """GET /scheduled_changes/releases"""
    return ReleaseScheduledChangesView().get()


def scheduled_changes_releases_post():
    """POST /scheduled_changes/releases"""
    return ReleaseScheduledChangesView().post()


def scheduled_changes_rs_product_get():
    """GET /scheduled_changes/required_signoffs/product"""
    return ProductRequiredSignoffsScheduledChangesView().get()


def scheduled_changes_rs_product_post():
    """POST /scheduled_changes/required_signoffs/product"""
    return ProductRequiredSignoffsScheduledChangesView().post()


def scheduled_changes_rs_permissions_get():
    """GET /scheduled_changes/required_signoffs/permissions"""
    return PermissionsRequiredSignoffsScheduledChangesView().get()


def scheduled_changes_rs_permissions_post():
    """POST /scheduled_changes/required_signoffs/permissions"""
    return PermissionsRequiredSignoffsScheduledChangesView().post()


def enact_scheduled_change_rules_post(sc_id):
    """POST /scheduled_changes/rules/<int:sc_id>/enact"""
    return EnactRuleScheduledChangeView().post(sc_id)


def enact_scheduled_change_permissions_post(sc_id):
    """POST /scheduled_changes/permissions/<int:sc_id>/enact"""
    return EnactPermissionScheduledChangeView().post(sc_id)


def enact_scheduled_change_releases_post(sc_id):
    """POST /scheduled_changes/releases/<int:sc_id>/enact"""
    return EnactReleaseScheduledChangeView().post(sc_id)


def enact_scheduled_change_product_rs_post(sc_id):
    """POST /scheduled_changes/required_signoffs/product/<int:sc_id>/enact"""
    return EnactProductRequiredSignoffScheduledChangeView().post(sc_id)


def enact_scheduled_change_permissions_rs_post(sc_id):
    """POST /scheduled_changes/required_signoffs/permissions/<int:sc_id>/enact"""
    return EnactPermissionsRequiredSignoffScheduledChangeView().post(sc_id)


def scheduled_change_rules_signoffs_post(sc_id):
    """POST /scheduled_changes/rules/<int:sc_id>/signoffs"""
    return RuleScheduledChangeSignoffsView().post(sc_id)


def scheduled_change_rules_signoffs_delete(sc_id):
    """DELETE /scheduled_changes/rules/<int:sc_id>/signoffs"""
    return RuleScheduledChangeSignoffsView().delete(sc_id)


def scheduled_change_permissions_signoffs_post(sc_id):
    """POST /scheduled_changes/permissions/<int:sc_id>/signoffs"""
    return PermissionScheduledChangeSignoffsView().post(sc_id)


def scheduled_change_permissions_signoffs_delete(sc_id):
    """DELETE /scheduled_changes/permissions/<int:sc_id>/signoffs"""
    return PermissionScheduledChangeSignoffsView().delete(sc_id)


def scheduled_change_release_signoffs_post(sc_id):
    """POST /scheduled_changes/releases/<int:sc_id>/signoffs"""
    return ReleaseScheduledChangeSignoffsView().post(sc_id)


def scheduled_change_release_signoffs_delete(sc_id):
    """DELETE /scheduled_changes/releases/<int:sc_id>/signoffs"""
    return ReleaseScheduledChangeSignoffsView().delete(sc_id)


def scheduled_change_product_rs_signoffs_post(sc_id):
    """POST /scheduled_changes/required_signoffs/product/<int:sc_id>/signoffs"""
    return ProductRequiredSignoffScheduledChangeSignoffsView().post(sc_id)


def scheduled_change_product_rs_signoffs_delete(sc_id):
    """DELETE /scheduled_changes/required_signoffs/product/<int:sc_id>/signoffs"""
    return ProductRequiredSignoffScheduledChangeSignoffsView().delete(sc_id)


def scheduled_change_permissions_rs_signoffs_post(sc_id):
    """POST /scheduled_changes/required_signoffs/permissions/<int:sc_id>/signoffs"""
    return PermissionsRequiredSignoffScheduledChangeSignoffsView().post(sc_id)


def scheduled_change_permissions_rs_signoffs_delete(sc_id):
    """DELETE /scheduled_changes/required_signoffs/permissions/<int:sc_id>/signoffs"""
    return PermissionsRequiredSignoffScheduledChangeSignoffsView().delete(sc_id)


def scheduled_change_rules_post(sc_id):
    """POST /scheduled_changes/rules/<int:sc_id>"""
    return RuleScheduledChangeView().post(sc_id)


def scheduled_change_rules_delete(sc_id):
    """DELETE /scheduled_changes/rules/<int:sc_id>"""
    return RuleScheduledChangeView().delete(sc_id)


def scheduled_change_permissions_post(sc_id):
    """POST /scheduled_changes/permissions/<int:sc_id>"""
    return PermissionScheduledChangeView().post(sc_id)


def scheduled_change_permissions_delete(sc_id):
    """DELETE /scheduled_changes/permissions/<int:sc_id>"""
    return PermissionScheduledChangeView().delete(sc_id)


def scheduled_change_releases_post(sc_id):
    """POST /scheduled_changes/releases/<int:sc_id>"""
    return ReleaseScheduledChangeView().post(sc_id)


def scheduled_change_releases_delete(sc_id):
    """DELETE /scheduled_changes/releases/<int:sc_id>"""
    return ReleaseScheduledChangeView().delete(sc_id)


def scheduled_change_product_rs_post(sc_id):
    """POST /scheduled_changes/required_signoffs/product/<int:sc_id>"""
    return ProductRequiredSignoffScheduledChangeView().post(sc_id)


def scheduled_change_product_rs_delete(sc_id):
    """DELETE /scheduled_changes/required_signoffs/product/<int:sc_id>"""
    return ProductRequiredSignoffScheduledChangeView().delete(sc_id)


def scheduled_change_permissions_rs_post(sc_id):
    """POST /scheduled_changes/required_signoffs/permissions/<int:sc_id>"""
    return PermissionsRequiredSignoffScheduledChangeView().post(sc_id)


def scheduled_change_permissions_rs_delete(sc_id):
    """DELETE /scheduled_changes/required_signoffs/permissions/<int:sc_id>"""
    return PermissionsRequiredSignoffScheduledChangeView().delete(sc_id)


def scheduled_change_rules_history_get(sc_id):
    """GET /scheduled_changes/rules/<int:sc_id>/revisions"""
    return RuleScheduledChangeHistoryView().get(sc_id)


def scheduled_change_rules_history_post(sc_id):
    """POST /scheduled_changes/rules/<int:sc_id>/revisions"""
    return RuleScheduledChangeHistoryView().post(sc_id)


def scheduled_change_permissions_history_get(sc_id):
    """GET /scheduled_changes/permissions/<int:sc_id>/revisions"""
    return PermissionScheduledChangeHistoryView().get(sc_id)


def scheduled_change_permissions_history_post(sc_id):
    """POST /scheduled_changes/permissions/<int:sc_id>/revisions"""
    return PermissionScheduledChangeHistoryView().post(sc_id)


def scheduled_change_releases_history_get(sc_id):
    """GET /scheduled_changes/releases/<int:sc_id>/revisions"""
    return ReleaseScheduledChangeHistoryView().get(sc_id)


def scheduled_change_releases_history_post(sc_id):
    """POST /scheduled_changes/releases/<int:sc_id>/revisions"""
    return ReleaseScheduledChangeHistoryView().post(sc_id)


def scheduled_change_product_rs_history_get(sc_id):
    """GET /scheduled_changes/required_signoffs/product/<int:sc_id>/revisions"""
    return ProductRequiredSignoffScheduledChangeHistoryView().get(sc_id)


def scheduled_change_product_rs_history_post(sc_id):
    """POST /scheduled_changes/required_signoffs/product/<int:sc_id>/revisions"""
    return ProductRequiredSignoffScheduledChangeHistoryView().post(sc_id)


def scheduled_change_permissions_rs_history_get(sc_id):
    """GET /scheduled_changes/required_signoffs/permissions/<int:sc_id>/revisions"""
    return PermissionsRequiredSignoffScheduledChangeHistoryView().get(sc_id)


def scheduled_change_permissions_rs_history_post(sc_id):
    """POST /scheduled_changes/required_signoffs/permissions/<int:sc_id>/revisions"""
    return PermissionsRequiredSignoffScheduledChangeHistoryView().post(sc_id)
