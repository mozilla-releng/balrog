import json
import logging
from auslib.global_state import dbo
from connexion import problem, request
from sqlalchemy.sql.expression import null
from auslib.web.common.history import HistoryHelper, get_input_dict
from auslib.web.common.rules import get_rules
from auslib.web.common.releases import get_releases, process_release_revisions
from auslib.web.admin.views.permissions import UsersView, PermissionScheduledChangeHistoryView
from auslib.web.admin.views.rules import RuleScheduledChangeHistoryView
from auslib.web.admin.views.releases import ReleaseScheduledChangeHistoryView
from auslib.web.admin.views.required_signoffs import ProductRequiredSignoffsHistoryAPIView, \
    PermissionsRequiredSignoffsHistoryAPIView, ProductRequiredSignoffScheduledChangeHistoryView, \
    PermissionsRequiredSignoffScheduledChangeHistoryView


log = logging.getLogger(__name__)


def _get_filters(obj, history_table):
    input_dict = get_input_dict()
    query = json.loads(input_dict.data)['query']
    where = [False, False]
    try:
        where = [getattr(history_table, f) == query.get(f) for f in query]
        where.append(history_table.product != null())
        where.append(history_table.data_version != null())
        if request.args.get('timestamp_from'):
            where.append(history_table.timestamp >= int(request.args.get('timestamp_from')))
        if request.args.get('timestamp_to'):
            where.append(history_table.timestamp <= int(request.args.get('timestamp_to')))
        return where
    except AttributeError:
        return where


def _get_histories(table, obj, process_revisions_callback=None):
    history_table = table
    order_by = [history_table.timestamp.desc()]
    history_helper = HistoryHelper(hist_table=history_table,
                                   order_by=order_by,
                                   get_object_callback=lambda: obj,
                                   history_filters_callback=_get_filters,
                                   obj_not_found_msg='No history found',
                                   process_revisions_callback=process_revisions_callback)
    try:
        return history_helper.get_history()
    except (ValueError, AssertionError) as msg:
        log.warning("Bad input: %s", msg)
        return problem(400, "Bad Request", "Error occurred when trying to fetch histories",
                       ext={"exception": str(msg)})


def get_rules_history():
    """GET /rules/history"""
    history_table = dbo.rules.history
    return _get_histories(history_table, get_rules)


def get_releases_history():
    """GET /releases/history"""
    history_table = dbo.releases.history
    return _get_histories(history_table, get_releases, process_release_revisions)


def get_permissions_history():
    """GET /permissions/history"""
    history_table = dbo.permissions.history
    get_permissions = UsersView().get()
    return _get_histories(history_table, get_permissions)


def get_permissions_scheduled_change_history():
    """GET /permissions_scheduled_change/history"""
    return PermissionScheduledChangeHistoryView().get_all()


def get_rules_scheduled_change_history():
    """GET /rules_scheduled_change/history"""
    return RuleScheduledChangeHistoryView().get_all()


def get_releases_scheduled_change_history():
    """GET /releases_scheduled_change/history"""
    return ReleaseScheduledChangeHistoryView().get_all()


def get_product_required_signoffs_scheduled_change_history():
    """GET /product_required_signoffs_scheduled_change/history"""
    return ProductRequiredSignoffScheduledChangeHistoryView().get_all()


def get_permission_required_signoffs_scheduled_change_history():
    """GET /permissions_required_signoff_scheduled_change/history"""
    return PermissionsRequiredSignoffScheduledChangeHistoryView().get_all()


def get_product_required_signoffs_history():
    """GET /product_required_signoffs/history"""
    return ProductRequiredSignoffsHistoryAPIView().get_all()


def get_permission_required_signoffs_history():
    """GET /permission_required_signoffs/history"""
    return PermissionsRequiredSignoffsHistoryAPIView().get_all()
