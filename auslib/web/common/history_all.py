import json
import logging
from auslib.global_state import dbo
from connexion import problem, request
from flask import jsonify, Response
from auslib.web.common.csrf import get_csrf_headers
from auslib.web.common.history import HistoryHelper
from sqlalchemy.sql.expression import null
from auslib.web.common.rules import get_rules


log = logging.getLogger(__name__)

def _get_filters(rule, history_table):
    if history_table and rule:
        return [True, True]


def get_rules_histories():
    history_table = dbo.rules.history
    order_by = [history_table.timestamp.desc()]
    history_helper = HistoryHelper(hist_table=history_table,
                                   order_by=order_by,
                                   get_object_callback=lambda: get_rules,
                                   history_filters_callback=_get_filters,
                                   obj_not_found_msg='No history found for rules')
    try:
        return history_helper.get_history()
    except (ValueError, AssertionError) as msg:
        log.warning("Bad input: %s", msg)
        return problem(400, "Bad Request", "Error occurred when trying to fetch rules history",
                       ext={"exception": str(msg)})
