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
    query = get_input_dict()
    where = [False, False]
    where = [getattr(history_table, f) == query.get(f) for f in query]
    where.append(history_table.data_version != null())
    if hasattr(history_table, 'product'):
        where.append(history_table.product != null())
    if request.args.get('timestamp_from'):
        where.append(history_table.timestamp >= int(request.args.get('timestamp_from')))
    if request.args.get('timestamp_to'):
        where.append(history_table.timestamp <= int(request.args.get('timestamp_to')))
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
    return PermissionScheduledChangeHistoryView().get_all()


def get_rules_scheduled_change_history():
    return RuleScheduledChangeHistoryView().get_all()


def get_releases_scheduled_change_history():
    return ReleaseScheduledChangeHistoryView().get_all()


def get_product_required_signoffs_scheduled_change_history():
    return ProductRequiredSignoffScheduledChangeHistoryView().get_all()


def get_permission_required_signoffs_scheduled_change_history():
    return PermissionsRequiredSignoffScheduledChangeHistoryView().get_all()


def get_product_required_signoffs_history():
    return ProductRequiredSignoffsHistoryAPIView().get_all()


def get_permissions_required_signoffs_history():
    return PermissionsRequiredSignoffsHistoryAPIView().get_all()


def rules_history():
    methods = {
        'rules': get_rules_history(),
        'sc_rules': get_rules_scheduled_change_history()
    }
    history = {
        'rules': methods.get('rules'),
        'sc_rules': methods.get('sc_rules')
    }
    histories = {
        'Rules': json.loads(history['rules'].data),
        'Rules scheduled change': json.loads(history['sc_rules'].data)
    }
    return histories


def releases_history():
    releases_methods = {
        'releases': get_releases_history(),
        'sc_releases': get_releases_scheduled_change_history()
    }
    releases_history = {
        'releases': releases_methods.get('releases'),
        'sc_releases': releases_methods.get('sc_releases')
    }
    histories = {
        'Releases': json.loads(releases_history['releases'].data),
        'Releases scheduled change': json.loads(releases_history['sc_releases'].data)
    }
    return histories


def permissions_history():
    permissions_methods = {
        'permissions': get_permissions_history(),
        'sc_permissions': get_permissions_scheduled_change_history()
    }
    permissions_history = {
        'permissions': permissions_methods.get('permissions'),
        'sc_permissions': permissions_methods.get('sc_permissions')
    }
    histories = {
        'Permissions': json.loads(permissions_history['permissions'].data),
        'Permissions Scheduled Change': json.loads(permissions_history['sc_permissions'].data)
    }
    return histories


def product_required_signoffs_history():
    product_required_signoffs_methods = {
        'product_required_signoffs': get_product_required_signoffs_history(),
        'sc_product_required_signoffs': get_product_required_signoffs_scheduled_change_history()
    }
    product_required_signoffs_history = {
        'product_required_signoffs': product_required_signoffs_methods.get('product_required_signoffs'),
        'sc_product_required_signoffs': product_required_signoffs_methods.get('sc_product_required_signoffs')
    }
    histories = {
        'Product Required Signoffs': json.loads(product_required_signoffs_history['product_required_signoffs'].data),
        'Product Required Signoffs Scheduled Change': json.loads(product_required_signoffs_history['sc_product_required_signoffs'].data)
    }
    return histories


def permissions_required_signoffs_history():
    permissions_required_signoffs_methods = {
        'permissions_required_signoffs': get_permissions_required_signoffs_history(),
        'sc_permissions_required_signoffs': get_permission_required_signoffs_scheduled_change_history()
    }
    permissions_required_signoffs_history = {
        'permissions_required_signoffs': permissions_required_signoffs_methods.get('permissions_required_signoffs'),
        'sc_permissions_required_signoffs': permissions_required_signoffs_methods.get('sc_permissions_required_signoffs')
    }
    histories = {
        'Permissions Required Signoffs': json.loads(permissions_required_signoffs_history['permissions_required_signoffs'].data),
        'Permissions Required Signoffs Scheduled Change': json.loads(permissions_required_signoffs_history['sc_permissions_required_signoffs'].data)
    }
    return histories
