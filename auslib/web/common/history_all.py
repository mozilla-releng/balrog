import json
import logging
from auslib.global_state import dbo
from connexion import problem, request
from flask import jsonify, Response
from auslib.web.common.csrf import get_csrf_headers
from auslib.web.common.history import HistoryHelper
from sqlalchemy.sql.expression import null
from auslib.web.common.rules import get_rules
from auslib.web.common.releases import get_releases, process_release_revisions


log = logging.getLogger(__name__)

def _get_filters(obj, history_table):
    if history_table and obj:
        return [True, True]

def _get_histories(table, obj, process_revisions_callback=None):
    history_table = table
    order_by = [history_table.timestamp.desc()]
    history_helper = HistoryHelper(hist_table=history_table,
                                   order_by=order_by,
                                   get_object_callback=lambda: get_rules,
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
    return _get_histories(history_table, get_rules)


def get_releases_histories():
    history_table = dbo.releases.history
    return _get_histories(history_table, get_releases, process_release_revisions)

