import json
import time
from connexion import request
from flask import Response, jsonify
from sqlalchemy import and_
from auslib.util.timesince import timesince


class HistoryHelper():
    def __init__(self, hist_table, order_by):
        self.hist_table = hist_table
        self.order_by = order_by
        self.fn_get_object = None
        self.fn_history_filters = None
        self.fn_process_revisions = None
        self.obj_not_found_msg = 'Requested object does not exist'

    def with_get_object_callback(self, get_object_callback, obj_not_found_msg=None):
        self.fn_get_object = get_object_callback
        if obj_not_found_msg:
            self.obj_not_found_msg = obj_not_found_msg
        return self

    def with_history_filters_callback(self, history_filters_callback):
        self.fn_history_filters = history_filters_callback
        return self

    def with_process_revisions_callback(self, process_revisions_callback):
        self.fn_process_revisions = process_revisions_callback
        return self

    def get_history(self, response_key='revisions'):
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        assert page >= 1

        obj = self.fn_get_object()
        if not obj:
            return Response(status=404,
                            response=self.obj_not_found_msg)

        offset = limit * (page - 1)

        filters = self.fn_history_filters(obj, self.hist_table)
        total_count = self.hist_table.t.count()\
                                       .where(and_(*filters))\
                                       .execute().fetchone()[0]

        revisions = self.hist_table.select(
            where=filters,
            limit=limit,
            offset=offset,
            order_by=self.order_by)

        _revisions = self.fn_process_revisions(revisions)

        ret = {}
        ret[response_key] = _revisions
        ret['count'] = total_count
        return jsonify(ret)


history_keys = ('timestamp', 'change_id', 'data_version', 'changed_by')


def annotateRevisionDifferences(revisions):
    _prev = {}
    for i, rev in enumerate(revisions):
        different = []
        for key, value in rev.items():
            if key in history_keys:
                continue
            if key not in _prev:
                _prev[key] = value
            else:
                prev = _prev[key]
                if prev != value:
                    different.append(key)
            # prep the value for being shown in revision_row.html
            if value is None:
                value = 'NULL'
            elif isinstance(value, dict):
                try:
                    value = json.dumps(value, indent=2, sort_keys=True)
                except ValueError:
                    pass
            elif isinstance(value, int):
                value = unicode(str(value), 'utf8')
            elif not isinstance(value, basestring):
                value = unicode(value, 'utf8')
            rev[key] = value

        rev['_different'] = different
        rev['_time_ago'] = getTimeAgo(rev['timestamp'])


def getTimeAgo(timestamp):
    now, then = int(time.time()), int(timestamp / 1000.0)
    time_ago = timesince(
        then,
        now,
        afterword='ago',
        minute_granularity=True,
        max_no_sections=2)
    if not time_ago:
        time_ago = 'seconds ago'
    return time_ago
