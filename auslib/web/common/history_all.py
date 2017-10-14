import json
import connexion
import logging
from auslib.global_state import dbo
from connexion import problem, request
from flask import jsonify, Response
from auslib.web.common.csrf import get_csrf_headers
from auslib.web.common.history import HistoryHelper
from sqlalchemy.sql.expression import null
from auslib.web.common.rules import get_rules
from auslib.web.common.releases import get_releases, process_release_revisions
from auslib.web.admin.views.permissions import UsersView, PermissionScheduledChangeHistoryView
from auslib.web.admin.views.rules import RuleScheduledChangeHistoryView
from auslib.web.admin.views.releases import ReleaseScheduledChangeHistoryView
from auslib.web.admin.views.required_signoffs import ProductRequiredSignoffsHistoryAPIView
from auslib.web.admin.views.required_signoffs import PermissionsRequiredSignoffsHistoryAPIView


log = logging.getLogger(__name__)

def _get_filters(obj, history_table):
    input_dict = _get_input_dict()
    query = json.loads(input_dict.data)['query']
    where = [getattr(history_table, f) == query.get(f) for f in query]
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

def get_rules_histories():
    history_table = dbo.rules.history
    result = _get_histories(history_table, get_rules)
    # print ('NSGSHSNSNSHSHS', len(json.loads(result.data)['revisions']))
    return _get_histories(history_table, get_rules)


def get_releases_histories():
    history_table = dbo.releases.history
    return _get_histories(history_table, get_releases, process_release_revisions)

def get_permissions_histories():
    history_table = dbo.permissions.history
    get_permissions = UsersView().get()
    return _get_histories(history_table, get_permissions)


def get_scheduled_change_permissions_histories():
    """GET /history/scheduled_changes/permissions"""
    return PermissionScheduledChangeHistoryView().get_all()

def get_rules_scheduled_change_histories():
    """GET /history/scheduled_changes/permissions"""
    return RuleScheduledChangeHistoryView().get_all()

def get_releases_scheduled_change_histories():
    """GET /history/scheduled_changes/permissions"""
    return ReleaseScheduledChangeHistoryView().get_all()

def get_product_required_signoffs_histories():
    return ProductRequiredSignoffsHistoryAPIView().get_all()

def get_permissions_required_signoffs_histories():
    return PermissionsRequiredSignoffsHistoryAPIView().get_all()

def _get_input_dict():
    args = connexion.request.args
    obj_keys = []
    query_keys = []
    query = {}
    #use try to handle exceptions for cases where supplied parameter is not a key in histoyr_table
    for key in args:
        if args.get(key) == 'TRUE':
            obj_keys.append(key)
        else:
            query_keys.append(key)

    for key in query_keys:
        query[key] = connexion.request.args.get(key)
    return jsonify(query_keys=query_keys, obj_keys=obj_keys, query=query)

def filter_helper(obj):
    req = _get_input_dict()
    keys = req['keys']
    keys_values = req['values']
    for key in keys:
        if obj[key] != keys_values[key]:
            return False
    return True

def method_constants():
    return {
        'rules': get_rules_histories(),
        'releases': get_releases_histories(),
        'permissions': get_permissions_histories(),
    }

def get_filtered_history():
    requested_histories = json.loads(_get_input_dict().data)['obj_keys']
    methods = method_constants()
    histories = {}
    for requested_history in requested_histories:
        if methods.get(requested_history):
            history = methods.get(requested_history)
            histories[requested_history] = json.loads(history.data)
    return histories
