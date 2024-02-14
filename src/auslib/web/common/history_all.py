import json
import logging

from connexion import problem, request
from sqlalchemy.sql.expression import null

from auslib.global_state import dbo
from auslib.web.admin.views.permissions import PermissionScheduledChangeHistoryView, get_users
from auslib.web.admin.views.required_signoffs import (
    PermissionsRequiredSignoffScheduledChangeHistoryView,
    ProductRequiredSignoffScheduledChangeHistoryView,
    get_all_permissions_rs_revisions,
    get_all_product_rs_revisions,
)
from auslib.web.admin.views.rules import RuleScheduledChangeHistoryView
from auslib.web.common.history import HistoryHelper, get_input_dict
from auslib.web.common.rules import get_rules

log = logging.getLogger(__name__)


def _get_filters(obj, history_table):
    query = get_input_dict()
    where = [False, False]
    where = [getattr(history_table, f) == query.get(f) for f in query]
    where.append(history_table.data_version != null())
    if hasattr(history_table, "product"):
        where.append(history_table.product != null())
        if request.args.get("product"):
            where.append(history_table.product == request.args.get("product"))
    if hasattr(history_table, "channel"):
        where.append(history_table.channel != null())
        if request.args.get("channel"):
            where.append(history_table.channel == request.args.get("channel"))
    if request.args.get("timestamp_from"):
        where.append(history_table.timestamp >= int(request.args.get("timestamp_from")))
    if request.args.get("timestamp_to"):
        where.append(history_table.timestamp <= int(request.args.get("timestamp_to")))
    return where


def _get_histories(table, obj, process_revisions_callback=None):
    history_table = table
    order_by = [history_table.timestamp.desc()]
    history_helper = HistoryHelper(
        hist_table=history_table,
        order_by=order_by,
        get_object_callback=lambda: obj,
        history_filters_callback=_get_filters,
        obj_not_found_msg="No history found",
        process_revisions_callback=process_revisions_callback,
    )
    try:
        return history_helper.get_history()
    except (ValueError, AssertionError) as msg:
        log.warning("Bad input: %s", msg)
        return problem(400, "Bad Request", "Error occurred when trying to fetch histories", ext={"exception": str(msg)})


def rules_history():
    """GET /rules/history"""
    history_table = dbo.rules.history
    rules = _get_histories(history_table, get_rules)
    history = {"rules": rules, "sc_rules": RuleScheduledChangeHistoryView().get_all()}
    histories = {"Rules": json.loads(history["rules"].data), "Rules scheduled change": json.loads(history["sc_rules"].data)}
    return histories


def permissions_history():
    """GET /permissions/history"""
    history_table = dbo.permissions.history
    get_permissions = get_users()
    permissions = _get_histories(history_table, get_permissions)
    permissions_history = {"permissions": permissions, "sc_permissions": PermissionScheduledChangeHistoryView().get_all()}
    histories = {
        "Permissions": json.loads(permissions_history["permissions"].data),
        "Permissions Scheduled Change": json.loads(permissions_history["sc_permissions"].data),
    }
    return histories


def product_required_signoffs_history():
    """GET /required_signoffs/product/history"""
    product_required_signoffs_history = {
        "sc_product_required_signoffs": ProductRequiredSignoffScheduledChangeHistoryView().get_all(),
        "product_required_signoffs": get_all_product_rs_revisions(),
    }
    histories = {
        "Product Required Signoffs": json.loads(product_required_signoffs_history["product_required_signoffs"].data),
        "Product Required Signoffs Scheduled Change": json.loads(product_required_signoffs_history["sc_product_required_signoffs"].data),
    }
    return histories


def permissions_required_signoffs_history():
    """GET /permissions_required_signoffs/history"""
    permissions_required_signoffs_history = {
        "sc_permissions_required_signoffs": PermissionsRequiredSignoffScheduledChangeHistoryView().get_all(),
        "permissions_required_signoffs": get_all_permissions_rs_revisions(),
    }
    histories = {
        "Permissions Required Signoffs": json.loads(permissions_required_signoffs_history["permissions_required_signoffs"].data),
        "Permissions Required Signoffs Scheduled Change": json.loads(permissions_required_signoffs_history["sc_permissions_required_signoffs"].data),
    }
    return histories
