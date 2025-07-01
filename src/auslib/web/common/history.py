import json

import arrow
from flask import Response, jsonify, request


class HistoryHelper:
    def __init__(
        self,
        hist_table,
        order_by,
        get_object_callback,
        history_filters_callback,
        process_revisions_callback=None,
        obj_not_found_msg="Requested object does not exist",
    ):
        self.hist_table = hist_table
        self.order_by = order_by
        self.fn_history_filters = history_filters_callback
        self.fn_process_revisions = process_revisions_callback
        self.fn_get_object = get_object_callback
        self.obj_not_found_msg = obj_not_found_msg

    def get_history(self, response_key="revisions"):
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        assert page >= 1

        obj = self.fn_get_object()
        if not obj:
            return Response(status=404, response=self.obj_not_found_msg)

        offset = limit * (page - 1)

        filters = self.fn_history_filters(obj, self.hist_table)
        total_count = self.hist_table.count(where=filters)

        revisions = self.hist_table.select(where=filters, limit=limit, offset=offset, order_by=self.order_by)

        if self.fn_process_revisions:
            revisions = self.fn_process_revisions(revisions)

        ret = {}
        ret[response_key] = revisions
        ret["count"] = total_count
        return jsonify(ret)


def get_input_dict():
    reserved_filter_params = ["limit", "product", "channel", "page", "timestamp_from", "timestamp_to"]
    args = request.args
    query_keys = []
    query = {}
    for key in args:
        if key not in reserved_filter_params:
            query_keys.append(key)

    for key in query_keys:
        query[key] = request.args.get(key)
    return query


history_keys = ("timestamp", "change_id", "data_version", "changed_by")


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
                value = "NULL"
            elif isinstance(value, dict):
                try:
                    value = json.dumps(value, indent=2, sort_keys=True)
                except ValueError:
                    pass
            elif isinstance(value, int):
                value = str(value)
            elif not isinstance(value, str):
                value = str(value)
            rev[key] = value

        rev["_different"] = different
        # Divide by 1000 because the timestamp from the database is to the millisecond,
        # but stored as an integer
        rev["_time_ago"] = arrow.get(rev["timestamp"] / 1000).humanize()
