from auslib.web.admin.views.csrf import CSRFView
from auslib.web.admin.views.rules import RulesAPIView, SingleRuleView, SingleRuleColumnView, \
RuleHistoryAPIView
from auslib.web.admin.views.permissions import UsersView


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


def users_get():
    """GET /users"""
    return UsersView().get()
