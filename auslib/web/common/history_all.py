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
        return history_helper.get_unlimted_histories()
    except (ValueError, AssertionError) as msg:
        log.warning("Bad input: %s", msg)
        return problem(400, "Bad Request", "Error occurred when trying to fetch histories",
                       ext={"exception": str(msg)})


def get_rules_history():
    history_table = dbo.rules.history
    return _get_histories(history_table, get_rules)


def get_releases_history():
    history_table = dbo.releases.history
    return _get_histories(history_table, get_releases, process_release_revisions)


def get_permissions_history():
    history_table = dbo.permissions.history
    get_permissions = UsersView().get()
    return _get_histories(history_table, get_permissions)


def get_permissions_scheduled_change_history():
    """GET /history/scheduled_changes/permissions"""
    return PermissionScheduledChangeHistoryView().get_all()


def get_rules_scheduled_change_history():
    """GET /history/scheduled_changes/permissions"""
    return RuleScheduledChangeHistoryView().get_all()


def get_releases_scheduled_change_history():
    """GET /history/scheduled_changes/permissions"""
    return ReleaseScheduledChangeHistoryView().get_all()


def get_product_required_signoff_scheduled_change_history():
    return ProductRequiredSignoffScheduledChangeHistoryView().get_all()


def get_permission_required_signoff_scheduled_change_history():
    return PermissionsRequiredSignoffScheduledChangeHistoryView().get_all()


def get_product_required_signoffs_history():
    return ProductRequiredSignoffsHistoryAPIView().get_all()


def get_permissions_required_signoffs_history():
    return PermissionsRequiredSignoffsHistoryAPIView().get_all()


def history_methods():
    return {
        'rules': get_rules_history(),
        'releases': get_releases_history(),
        'permissions': get_permissions_history(),
        'permissions_required_signoffs': get_permissions_required_signoffs_history(),
        'product_required_signoffs': get_product_required_signoffs_history(),
        'releases_scheduled_change': get_releases_scheduled_change_history(),
        'rules_scheduled_change': get_rules_scheduled_change_history(),
        'permissions_scheduled_change': get_permissions_scheduled_change_history(),
        'permissions_required_signoff_scheduled_change': get_permission_required_signoff_scheduled_change_history(),
        'product_required_signoff_scheduled_change': get_product_required_signoff_scheduled_change_history(),
    }


def get_rrp_history():
    rrp_constants = ['rules', 'releases', 'permissions']
    methods = history_methods()
    histories = {}
    for constant in rrp_constants:
        if (request.args.get(constant)) == '1':
            history = methods.get(constant)
            histories[constant] = json.loads(history.data)
    return histories


def get_sc_history():
    sc_constants = [
        'rules_scheduled_change',
        'releases_scheduled_change',
        'permissions_scheduled_change',
        'permissions_required_signoff_scheduled_change',
        'product_required_signoff_scheduled_change',
    ]
    methods = history_methods()
    histories = {}
    for constant in sc_constants:
        if (request.args.get(constant)) == '1':
            history = methods.get(constant)
            histories[constant] = json.loads(history.data)
    return histories


def get_required_signoff_history():
    rrp_constants = [
        'permissions_required_signoffs',
        'product_required_signoffs',
    ]
    methods = history_methods()
    histories = {}
    print('request', request.args)
    for constant in rrp_constants:
        if (request.args.get(constant)) == '1':
            history = methods.get(constant)
            histories[constant] = json.loads(history.data)
    return histories
