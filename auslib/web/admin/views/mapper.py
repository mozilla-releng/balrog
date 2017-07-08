from auslib.web.admin.views.csrf import CSRFView

from auslib.web.admin.views.rules import RulesAPIView, SingleRuleView, SingleRuleColumnView, \
    RuleHistoryAPIView

from auslib.web.admin.views.permissions import UsersView, AllRolesView, SpecificUserView,\
    PermissionsView, UserRolesView, UserRoleView, SpecificPermissionView

from auslib.web.admin.views.releases import ReleaseDiffView, ReleaseFieldView, ReleasesAPIView, SingleReleaseView,\
    ReleaseReadOnlyView, SingleReleaseColumnView, SingleLocaleView, ReleaseHistoryView

from auslib.web.admin.views.required_signoffs import ProductRequiredSignoffsHistoryAPIView, \
    PermissionsRequiredSignoffsHistoryAPIView, ProductRequiredSignoffsView, PermissionsRequiredSignoffsView


def csrf_get():
    """GET /csrf_token"""
    return CSRFView().get()


def rules_post():
    """POST /rules"""
    return RulesAPIView().post()


def rules_id_or_alias_get(id_or_alias):
    """GET /rules/:id"""
    return SingleRuleView().get(id_or_alias)


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


def rules_revisions_post(id_or_alias):
    """POST /rules/:id/revisions"""
    return RuleHistoryAPIView().post(id_or_alias)


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
