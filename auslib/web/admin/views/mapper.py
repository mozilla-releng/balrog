from auslib.web.admin.views.csrf import CSRFView
from auslib.web.admin.views.rules import RulesAPIView, SingleRuleView, SingleRuleColumnView, \
    RuleHistoryAPIView
from auslib.web.admin.views.permissions import UsersView, AllRolesView, SpecificUserView,\
    PermissionsView, UserRolesView, UserRoleView, SpecificPermissionView
from releases import ReleaseDiffView, ReleaseFieldView


def csrf_get():
    """GET /csrf_token"""
    return CSRFView().get()


def rules_get():
    """GET /rules"""
    return RulesAPIView().get()


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


def rules_revisions_get(rule_id):
    """GET /rules/:id/revisions"""
    return RuleHistoryAPIView().get(rule_id)


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
