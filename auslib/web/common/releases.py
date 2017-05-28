import json
import logging
from auslib.global_state import dbo
from connexion import request
from flask import jsonify, Response
from sqlalchemy.sql.expression import null
from auslib.web.common.history import (
    annotateRevisionDifferences, HistoryHelper)


log = logging.getLogger(__name__)


def get_releases():
    kwargs = {}
    if request.args.get('product'):
        kwargs['product'] = request.args.get('product')
    if request.args.get('name_prefix'):
        kwargs['name_prefix'] = request.args.get('name_prefix')
    if request.args.get('names_only'):
        kwargs['nameOnly'] = True
    releases = dbo.releases.getReleaseInfo(**kwargs)
    if request.args.get('names_only'):
        names = []
        for release in releases:
            names.append(release['name'])
        data = {'names': names}
    else:
        _releases = []
        _mapping = {
            # return : db name
            'name': 'name',
            'product': 'product',
            'data_version': 'data_version',
            'read_only': 'read_only',
            'rule_ids': 'rule_ids',
        }
        for release in releases:
            _releases.append(dict(
                (key, release[db_key])
                for key, db_key in _mapping.items()
            ))
        data = {
            'releases': _releases,
        }
    return jsonify(data)


def _get_release(release):
    releases = dbo.releases.getReleases(name=release, limit=1)
    return releases[0] if releases else None


def get_release(release):
    release = _get_release(release)
    if not release:
        return Response(status=404, mimetype="application/json")
    headers = {'X-Data-Version': release['data_version']}
    if request.args.get("pretty"):
        indent = 4
    else:
        indent = None
    return Response(response=json.dumps(release['data'], indent=indent, sort_keys=True), mimetype='application/json', headers=headers)


def _get_filters(release, history_table):
    return [history_table.name == release['name'],
            history_table.data_version != null()]


def _process_revisions(revisions):
    annotateRevisionDifferences(revisions)

    _mapping = [
        'data_version',
        'name',
        'product',
        'read_only',
        '_different',
        '_time_ago',
        'change_id',
        'changed_by',
        "timestamp"]

    _revisions = []
    for r in revisions:
        _revisions.append(dict(
            (item, r[item])
            for item in _mapping
        ))

    return _revisions


def get_release_history(release):
    history_table = dbo.releases.history
    order_by = [history_table.timestamp.desc()]
    history_helper = HistoryHelper(history_table, order_by)\
        .with_get_object_callback(lambda: _get_release(release),
                                  'Requested release does not exist')\
        .with_history_filters_callback(_get_filters)\
        .with_process_revisions_callback(_process_revisions)
    try:
        return history_helper.get_history()
    except (ValueError, AssertionError) as e:
        log.warning("Bad input: %s", json.dumps(e.args))
        return Response(status=400, response=json.dumps({"data": e.args}))
