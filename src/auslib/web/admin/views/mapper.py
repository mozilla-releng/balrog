from auslib.web.admin.views.permissions import PermissionScheduledChangeHistoryView, PermissionScheduledChangeSignoffsView
from auslib.web.admin.views.releases import ReleaseScheduledChangeHistoryView, ReleaseScheduledChangeSignoffsView
from auslib.web.admin.views.required_signoffs import (
    PermissionsRequiredSignoffScheduledChangeHistoryView,
    PermissionsRequiredSignoffScheduledChangeSignoffsView,
    PermissionsRequiredSignoffsHistoryAPIView,
    ProductRequiredSignoffScheduledChangeHistoryView,
    ProductRequiredSignoffScheduledChangeSignoffsView,
    ProductRequiredSignoffsHistoryAPIView,
)
from auslib.web.admin.views.rules import RuleHistoryAPIView, RuleScheduledChangeHistoryView, RuleScheduledChangeSignoffsView


def rules_revisions_post(rule_id):
    """POST /rules/:id/revisions"""
    return RuleHistoryAPIView().post(rule_id)


def required_signoffs_product_revisions_get():
    """GET /required_signoffs/product/revisions"""
    return ProductRequiredSignoffsHistoryAPIView().get()


def required_signoffs_permissions_revisions_get():
    """GET /required_signoffs/permissions/revisions"""
    return PermissionsRequiredSignoffsHistoryAPIView().get()


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
