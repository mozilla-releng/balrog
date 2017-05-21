from auslib.web.admin.views.rules import (
    RulesAPIView, SingleRuleView, RuleHistoryAPIView)


def get():
    view = RulesAPIView()
    return view.get()


def get_by_id_or_alias(id_or_alias):
    view = SingleRuleView()
    return view.get(id_or_alias, False)


def get_revisions(rule_id):
    view = RuleHistoryAPIView()
    return view.get(rule_id)
