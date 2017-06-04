import json
import logging
from auslib.global_state import dbo
from connexion import request
from flask import jsonify, Response
from auslib.web.common.history import HistoryHelper
from sqlalchemy.sql.expression import null


log = logging.getLogger(__name__)


def get_rules():
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


def get_rule(id_or_alias):
    rule = dbo.rules.getRule(id_or_alias)
    if not rule:
        return Response(status=404, response="Requested rule does not exist")

    headers = {'X-Data-Version': rule['data_version']}
    return Response(response=json.dumps(rule),
                    mimetype="application/json", headers=headers)


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
        'systemCapabilities': 'systemCapabilities',
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


def get_rule_history(id_or_alias):
    history_table = dbo.rules.history
    order_by = [history_table.timestamp.desc()]
    history_helper = HistoryHelper(history_table, order_by)\
        .with_get_object_callback(lambda: dbo.rules.getRule(id_or_alias),
                                  'Requested rule does not exist')\
        .with_history_filters_callback(_get_filters)\
        .with_process_revisions_callback(_process_revisions)
    try:
        return history_helper.get_history(response_key='rules')
    except (ValueError, AssertionError) as msg:
        log.warning("Bad input: %s", msg)
        return Response(status=400, response=str(msg))
