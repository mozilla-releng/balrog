import connexion
from flask import Response, jsonify

from auslib.web.admin.views.base import log
from auslib.web.admin.views.problem import problem


def get_revisions(
    history_table,
    get_object_callback,
    history_filters_callback,
    revisions_order_by,
    process_revisions_callback=None,
    obj_not_found_msg="Requested object does not exist",
    response_key="revisions",
):
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
    page = int(connexion.request.args.get("page", 1))
    limit = int(connexion.request.args.get("limit", 10))

    obj = get_object_callback()
    if not obj:
        return problem(status=404, title="Not Found", detail=obj_not_found_msg)

    offset = limit * (page - 1)

    filters = history_filters_callback(obj)
    total_count = history_table.count(where=filters)

    revisions = history_table.select(where=filters, limit=limit, offset=offset, order_by=revisions_order_by)

    if process_revisions_callback:
        revisions = process_revisions_callback(revisions)

    ret = dict()
    ret[response_key] = revisions
    ret["count"] = total_count
    return jsonify(ret)


def revert_to_revision(
    table,
    get_object_callback,
    change_field,
    get_what_callback,
    changed_by,
    response_message,
    transaction,
    obj_not_found_msg="Requested object does not exist",
):
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
        change_id = connexion.request.get_json().get("change_id")
    if not change_id:
        log.warning("Bad input: %s", "no change_id")
        return problem(400, "Bad Request", "No change_id passed in the request body")

    change = table.history.getChange(change_id=change_id)
    if change is None:
        return problem(400, "Bad Request", "Invalid change_id : {0} passed in the request body".format(change_id))

    obj_id = obj[change_field]

    if change[change_field] != obj_id:
        return problem(400, "Bad Request", "Bad {0} passed in the request".format(change_field))

    old_data_version = obj["data_version"]

    # now we're going to make a new insert based on this
    what = get_what_callback(change)
    where = dict()
    where[change_field] = obj_id
    table.update(changed_by=changed_by, where=where, what=what, old_data_version=old_data_version, transaction=transaction)
    return Response(response_message)
