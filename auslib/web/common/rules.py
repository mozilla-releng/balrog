import json
import logging
from auslib.global_state import dbo
from connexion import problem, request
from flask import jsonify, Response
from auslib.web.common.csrf import get_csrf_headers
from auslib.web.common.history import HistoryHelper
from sqlalchemy.sql.expression import null


log = logging.getLogger(__name__)


def get_rules():
    # We can't use a form here because it will enforce "csrf_token" needing
    # to exist, which doesn't make sense for GET requests.
    where = {}
    for field in ("product",):
        if request.args.get(field):
            where[field] = request.args[field]

    rules = dbo.rules.getOrderedRules(where=where)
    count = 0
    _rules = []
    for rule in rules:
        _rules.append(dict(
            (key, value)
            for key, value in rule.items()
        ))
        count += 1
    return jsonify(count=count, rules=_rules)


def get_rule(id_or_alias, with_csrf_headers=False):
    rule = dbo.rules.getRule(id_or_alias)
    if not rule:
        return problem(status=404, title="Not Found", detail="Requested rule wasn't found",
                       ext={"exception": "Requested rule does not exist"})

    headers = {'X-Data-Version': rule['data_version']}
    if with_csrf_headers:
        headers.update(get_csrf_headers())
    return Response(response=json.dumps(rule),
                    mimetype="application/json", headers=headers)


def get_rule_with_csrf_headers(id_or_alias):
    return get_rule(id_or_alias, with_csrf_headers=True)


def _process_revisions(revisions):
    _mapping = {
        # return : db name
        'rule_id': 'rule_id',
        'mapping': 'mapping',
        'fallbackMapping': 'fallbackMapping',
        'priority': 'priority',
        'alias': 'alias',
        'product': 'product',
        'version': 'version',
        'backgroundRate': 'backgroundRate',
        'buildID': 'buildID',
        'channel': 'channel',
        'locale': 'locale',
        'distribution': 'distribution',
        'buildTarget': 'buildTarget',
        'osVersion': 'osVersion',
        'instructionSet': 'instructionSet',
        'memory': 'memory',
        'mig64': 'mig64',
        'distVersion': 'distVersion',
        'comment': 'comment',
        'update_type': 'update_type',
        'headerArchitecture': 'headerArchitecture',
        'data_version': 'data_version',
        # specific to revisions
        'change_id': 'change_id',
        'timestamp': 'timestamp',
        'changed_by': 'changed_by',
    }

    _rules = []

    for rule in revisions:
        _rules.append(dict(
            (key, rule[db_key])
            for key, db_key in _mapping.items()
        ))

    return _rules


def _get_filters(rule, history_table):
    return [history_table.rule_id == rule['rule_id'],
            history_table.data_version != null()]


def get_rule_history(rule_id):
    history_table = dbo.rules.history
    order_by = [history_table.timestamp.desc()]
    history_helper = HistoryHelper(hist_table=history_table,
                                   order_by=order_by,
                                   get_object_callback=lambda: dbo.rules.getRule(rule_id),
                                   history_filters_callback=_get_filters,
                                   process_revisions_callback=_process_revisions,
                                   obj_not_found_msg='Requested rule does not exist')
    try:
        return history_helper.get_history(response_key='rules')
    except (ValueError, AssertionError) as msg:
        log.warning("Bad input: %s", msg)
        return problem(400, "Bad Request", "Error occurred when trying to fetch"
                                           " Rule's revisions having rule_id {0}".format(rule_id),
                       ext={"exception": str(msg)})
