from auslib.web.admin.views.permissions import (
    EnactPermissionScheduledChangeView,
    PermissionScheduledChangeHistoryView,
    PermissionScheduledChangeSignoffsView,
    PermissionScheduledChangesView,
    PermissionScheduledChangeView,
)
from auslib.web.admin.views.pinnable_releases import EnactPinnableReleaseScheduledChangeView, PinnableReleaseScheduledChangesView
from auslib.web.admin.views.releases import (
    EnactReleaseScheduledChangeView,
    ReleaseScheduledChangeHistoryView,
    ReleaseScheduledChangeSignoffsView,
    ReleaseScheduledChangesView,
    ReleaseScheduledChangeView,
    ScheduledReleaseDiffView,
)
from auslib.web.admin.views.required_signoffs import (
    EnactPermissionsRequiredSignoffScheduledChangeView,
    EnactProductRequiredSignoffScheduledChangeView,
    PermissionsRequiredSignoffScheduledChangeHistoryView,
    PermissionsRequiredSignoffScheduledChangeSignoffsView,
    PermissionsRequiredSignoffScheduledChangeView,
    PermissionsRequiredSignoffsHistoryAPIView,
    PermissionsRequiredSignoffsScheduledChangesView,
    ProductRequiredSignoffScheduledChangeHistoryView,
    ProductRequiredSignoffScheduledChangeSignoffsView,
    ProductRequiredSignoffScheduledChangeView,
    ProductRequiredSignoffsHistoryAPIView,
    ProductRequiredSignoffsScheduledChangesView,
)
from auslib.web.admin.views.rules import (
    EnactRuleScheduledChangeView,
    RuleHistoryAPIView,
    RuleScheduledChangeHistoryView,
    RuleScheduledChangeSignoffsView,
    RuleScheduledChangesView,
    RuleScheduledChangeView,
)


def rules_revisions_post(rule_id):
    """POST /rules/:id/revisions"""
    return RuleHistoryAPIView().post(rule_id)


def scheduled_release_diff_get(sc_id):
    """GET /scheduled_changes/diff/release/:sc_id"""
    return ScheduledReleaseDiffView().get(sc_id)


def required_signoffs_product_revisions_get():
    """GET /required_signoffs/product/revisions"""
    return ProductRequiredSignoffsHistoryAPIView().get()


def required_signoffs_permissions_revisions_get():
    """GET /required_signoffs/permissions/revisions"""
    return PermissionsRequiredSignoffsHistoryAPIView().get()


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


def scheduled_change_rules_get_by_id(sc_id):
    return RuleScheduledChangeView().get(sc_id)


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


def scheduled_change_releases_get_by_id(sc_id):
    return ReleaseScheduledChangeView().get(sc_id)


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


def scheduled_changes_pinnable_releases_get():
    """GET /scheduled_changes/pinnable_releases"""
    return PinnableReleaseScheduledChangesView().get()


def enact_scheduled_change_pinnable_releases_post(sc_id):
    """POST /scheduled_changes/rules/<int:sc_id>/enact"""
    return EnactPinnableReleaseScheduledChangeView().post(sc_id)
