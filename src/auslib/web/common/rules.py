import json
import logging

from connexion import problem
from flask import Response, jsonify, request
from sqlalchemy.sql.expression import null

from auslib.global_state import dbo
from auslib.web.common.history import HistoryHelper

log = logging.getLogger(__name__)


def get():
    # TODO: When we switch to Swagger 3, this can move to the Swagger spec
    if request.args.get("timestamp") and request.args.get("product"):
        return problem(status=400, title="Bad Request", detail="Cannot query with a timestamp and a product at the same time")

    if request.args.get("timestamp"):
        rules = dbo.rules.history.getPointInTime(request.args.get("timestamp"))
    else:
        where = {}
        for field in ("product",):
            if request.args.get(field):
                where[field] = request.args[field]

        rules = dbo.rules.getOrderedRules(where=where)
    return jsonify(count=len(rules), rules=rules)


def get_rule(id_or_alias):
    rule = dbo.rules.getRule(id_or_alias)
    if not rule:
        return problem(status=404, title="Not Found", detail="Requested rule wasn't found", ext={"exception": "Requested rule does not exist"})

    headers = {"X-Data-Version": rule["data_version"]}
    return Response(response=json.dumps(rule), mimetype="application/json", headers=headers)


def _get_filters(rule, history_table):
    return [history_table.rule_id == rule["rule_id"], history_table.data_version != null()]


def get_history(rule_id):
    history_table = dbo.rules.history
    order_by = [history_table.timestamp.desc()]
    history_helper = HistoryHelper(
        hist_table=history_table,
        order_by=order_by,
        get_object_callback=lambda: dbo.rules.getRule(rule_id),
        history_filters_callback=_get_filters,
        obj_not_found_msg="Requested rule does not exist",
    )
    try:
        return history_helper.get_history(response_key="rules")
    except (ValueError, AssertionError) as msg:
        log.warning("Bad input: %s", msg)
        return problem(
            400, "Bad Request", "Error occurred when trying to fetch" " Rule's revisions having rule_id {0}".format(rule_id), ext={"exception": str(msg)}
        )
