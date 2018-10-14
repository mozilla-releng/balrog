import connexion
import difflib
import six
import simplejson as json
from six import integer_types, text_type
from auslib.global_state import dbo
from flask import Response, jsonify, abort
from sqlalchemy import and_
from sqlalchemy.sql.expression import null
from auslib.web.admin.views.problem import problem
from auslib.web.admin.views.base import AdminView


def format_value(value):
   if isinstance(value, dict):
       try:
           value = json.dumps(value, indent=2, sort_keys=True)
       except ValueError:
           pass
   elif value is None:
       value = 'NULL'
   elif isinstance(value, integer_types):
       value = str(value)
   else:
       value = text_type(value, 'utf8') if six.PY2 else str(value)
   return value

class HistoryView(AdminView):
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
                      revisions_order_by,
                      process_revisions_callback=None,
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
            return problem(status=404, title="Not Found", detail=obj_not_found_msg)

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

        if process_revisions_callback:
            revisions = process_revisions_callback(revisions)

        ret = dict()
        ret[response_key] = revisions
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
            return problem(404, "Not Found", obj_not_found_msg)

        change_id = None
        if connexion.request.get_json():
            change_id = connexion.request.get_json().get('change_id')
        if not change_id:
            self.log.warning("Bad input: %s", "no change_id")
            return problem(400, "Bad Request", "No change_id passed in the request body")

        change = self.history_table.getChange(change_id=change_id)
        if change is None:
            return problem(400, "Bad Request", "Invalid change_id : {0} passed in the request body".format(change_id))

        obj_id = obj[change_field]

        if change[change_field] != obj_id:
            return problem(400, "Bad Request", "Bad {0} passed in the request".format(change_field))

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


class ScheduledReleaseDiffView(AdminView):
    """/history/diff/sc/release/:change_id"""

    def __init__(self):
        super(AdminView, self).__init__()
        self.table = dbo.releases.scheduled_changes.history

    def get_value(self, change_id):
        revision = self.table.getChange(change_id=change_id)
        if not revision:
            abort(400, 'Bad change_id')
        return revision

    def previous(self, value, change_id):
        sc_name, table = value['base_name'], self.table
        old_revision = table.select(
            where=[
                table.base_name == sc_name,
                table.change_id < change_id,
                table.data_version != null()
            ],
            limit=1,
            order_by=[table.timestamp.desc()],
        )
        if len(old_revision) > 0:
            return self.get_value(old_revision[0]['change_id'])

    def get(self, change_id):
       try:
           _curr = self.get_value(change_id)
           _prev = self.previous(_curr, change_id)

       except (KeyError, TypeError, IndexError) as msg:
           return problem(400, 'Bad Request', str(msg))
       except ValueError as msg:
           return problem(404, 'Not Found', str(msg))

       curr = format_value(_curr["base_data"]) if _curr else ''
       prev = format_value(_curr["base_data"]) if _prev else ''

       result = difflib.unified_diff(
           prev.splitlines(),
           curr.splitlines(),
           fromfile='Data Version {}'.format(_prev['data_version'] if _prev else ''),
           tofile='Data Version {}'.format(_curr['data_version'] if _curr else ''),
           lineterm=''
       )

       return Response('\n'.join(result), content_type='text/plain')
