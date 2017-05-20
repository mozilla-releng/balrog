import json
import time
import connexion
from flask import Response, jsonify
from sqlalchemy import and_
from auslib.web.admin.views.problem import problem
from auslib.web.admin.views.base import AdminView
from auslib.util.timesince import timesince


class HistoryAdminView(AdminView):

    history_keys = ('timestamp', 'change_id', 'data_version', 'changed_by')

    def annotateRevisionDifferences(self, revisions):
        _prev = {}
        for i, rev in enumerate(revisions):
            different = []
            for key, value in rev.items():
                if key in self.history_keys:
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
            rev['_time_ago'] = self.getTimeAgo(rev['timestamp'])

    def getTimeAgo(self, timestamp):
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


class HistoryView(HistoryAdminView):
    """Base class for history views. Provides basics operations to get all
    object revisions and revert object to specific revision.

    @param table: Table.
    @type table: auslib.db.AUSTable
    """

    def __init__(self, table, *args, **kwargs):
        self.table = table
        self.history_table = table.history
        super(HistoryView, self).__init__(*args, **kwargs)

    def get_revisions(self,
                      get_object_callback,
                      history_filters_callback,
                      process_revisions_callback,
                      revisions_order_by,
                      obj_not_found_msg='Requested object does not exist',
                      response_key='revisions'):
        """Get revisions for Releases, Rules or ScheduledChanges.
        Uses callable parameters to handle specific AUS object data.

        @param get_object_callback: A callback to get requested AUS object.
        @type get_object_callback: callable

        @param history_filters_callback: A callback that get the filters list
        to query the history.
        @type history_filters_callback: callable

        @param process_revisions_callback: A callback that process revisions
        according to the requested AUS object.
        @type process_revisions_callback: callable

        @param revisions_order_by: Fields list to sort history.
        @type revisions_order_by: list

        @param obj_not_found_msg: Error message for not found AUS object.
        @type obj_not_found_msg: string

        @param response_key: Dictionary key to wrap returned revisions.
        @type response_key: string
        """
        page = int(connexion.request.args.get('page', 1))
        limit = int(connexion.request.args.get('limit', 10))

        obj = get_object_callback()
        if not obj:
            return problem(status=404, title="Not Found", detail="History object not found",
                           ext={"exception": self.not_found_msg})

        offset = limit * (page - 1)

        filters = history_filters_callback(obj)
        total_count = self.history_table.t.count()\
                                          .where(and_(*filters))\
                                          .execute().fetchone()[0]

        revisions = self.history_table.select(
            where=filters,
            limit=limit,
            offset=offset,
            order_by=revisions_order_by)

        _revisions = process_revisions_callback(revisions)

        ret = dict()
        ret[response_key] = _revisions
        ret['count'] = total_count
        return jsonify(ret)

    def revert_to_revision(self,
                           get_object_callback,
                           change_field,
                           get_what_callback,
                           changed_by,
                           response_message,
                           transaction,
                           obj_not_found_msg='Requested object does not exist'):
        """Reverts Releases, Rules or ScheduledChanges object to specific
        revision. Uses callable parameters to handle specific AUS object data.

        @param get_object_callback: A callback to get requested AUS object.
        @type get_object_callback: callable

        @param change_field: Specific table field to match revision.
        @type change_field: string

        @param get_what_callback: Criteria to revert revision.
        @type get_what_callback: callable

        @param changed_by: User.
        @type changed_by: string

        @param response_message: Success message.
        @type response_message: string

        @param transaction: Transaction
        @type transaction: auslib.db.AUSTransaction

        @param obj_not_found_msg: Error message for not found AUS object.
        @type obj_not_found_msg: string
        """

        obj = get_object_callback()
        if not obj:
            return problem(404, "Not Found", obj_not_found_msg,
                           ext={"exception": "Requested object wasn't found"})

        change_id = None
        if connexion.request.json:
            change_id = connexion.request.json.get('change_id')
        if not change_id:
            self.log.warning("Bad input: %s", "no change_id")
            return problem(400, "Bad Request", "No change_id passed in the request body")

        change = self.history_table.getChange(change_id=change_id)
        if change is None:
            return problem(400, "Bad Request", "Invalid change_id : {0} passed in the request body".format(change_id))

        obj_id = obj[change_field]

        if change[change_field] != obj_id:
            return problem(400, "Bad Request", detail="Bad {0} passed in the request".format(change_field))

        old_data_version = obj['data_version']

        # now we're going to make a new insert based on this
        what = get_what_callback(change)
        where = dict()
        where[change_field] = obj_id
        self.table.update(changed_by=changed_by,
                          where=where,
                          what=what,
                          old_data_version=old_data_version,
                          transaction=transaction)
        return Response(response_message)
