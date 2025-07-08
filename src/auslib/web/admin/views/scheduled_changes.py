import flask
from flask import jsonify
from sqlalchemy.sql.expression import null

from auslib.util.signoffs import serialize_signoff_requirements
from auslib.web.admin.views.base import log
from auslib.web.admin.views.history import get_revisions, revert_to_revision
from auslib.web.admin.views.problem import problem
from auslib.web.admin.views.validators import is_when_present_and_in_past_validator
from auslib.web.common.history import get_input_dict


def add_signoff_information(row, table, sc_table):
    scheduled_change = {"signoffs": {}, "required_signoffs": {}}
    base_row = {}
    base_pk = {}

    for k, v in row.items():
        if k == "data_version":
            scheduled_change["sc_data_version"] = v
        else:
            if k.startswith("base_"):
                k = k.replace("base_", "")
                base_row[k] = v
                if getattr(table, k).primary_key:
                    base_pk[k] = v
            scheduled_change[k] = v

    for signoff in sc_table.signoffs.select({"sc_id": row["sc_id"]}):
        scheduled_change["signoffs"][signoff["username"]] = signoff["role"]

    # No point in retrieving this for completed scheduled changes...
    if not row["complete"]:
        affected_rows = []
        # We don't need to consider the existing version of a row for
        # inserts, because it doesn't exist yet!
        if row["change_type"] != "insert":
            original_row = table.select(where=base_pk)[0]
            affected_rows.append(original_row)
        # We don't need to consider the future version of the row when
        # looking for required signoffs, because it won't exist when
        # enacted.
        if row["change_type"] != "delete":
            affected_rows.append(base_row)
        signoff_requirements = [obj for v in table.getPotentialRequiredSignoffs(affected_rows).values() for obj in v]
        scheduled_change["required_signoffs"] = serialize_signoff_requirements(signoff_requirements)

    return scheduled_change


def get_scheduled_changes(table, where=None):
    sc_table = table.scheduled_changes

    if where is None:
        where = {}

    if flask.request.args.get("all") is None:
        where["complete"] = False

    rows = sc_table.select(where=where)
    ret = {"count": len(rows), "scheduled_changes": []}
    for row in rows:
        ret["scheduled_changes"].append(add_signoff_information(row, table, sc_table))

    return jsonify(ret)


def post_scheduled_changes(sc_table, what, transaction, changed_by, change_type):
    if change_type not in ["insert", "update", "delete"]:
        return problem(400, "Bad Request", "Invalid or missing change_type")

    if is_when_present_and_in_past_validator(what):
        return problem(400, "Bad Request", "Changes may not be scheduled in the past")

    sc_id = sc_table.insert(changed_by, transaction, **what)
    signoffs = {}
    for signoff in sc_table.signoffs.select(where={"sc_id": sc_id}, transaction=transaction):
        signoffs[signoff["username"]] = signoff["role"]
    return jsonify(sc_id=sc_id, signoffs=signoffs)


def get_by_id_scheduled_change(table, sc_id):
    sc_table = table.scheduled_changes
    sc = sc_table.select(where={"sc_id": sc_id})
    if not sc:
        return problem(404, "Bad Request", "Scheduled change does not exist")

    scheduled_change = add_signoff_information(sc[0], table, sc_table)
    return jsonify({"scheduled_change": scheduled_change})


def post_scheduled_change(sc_table, sc_id, what, transaction, changed_by, old_sc_data_version):
    if is_when_present_and_in_past_validator(what):
        return problem(400, "Bad Request", "Changes may not be scheduled in the past")

    if what.get("data_version", None):
        what["data_version"] = int(what["data_version"])

    where = {"sc_id": sc_id}
    sc_table.update(where, what, changed_by, int(old_sc_data_version), transaction)
    sc = sc_table.select(where=where, transaction=transaction, columns=["data_version"])[0]
    signoffs = {}
    for signoff in sc_table.signoffs.select(where={"sc_id": sc_id}, transaction=transaction):
        signoffs[signoff["username"]] = signoff["role"]
    return jsonify(new_data_version=sc["data_version"], signoffs=signoffs)


def delete_scheduled_change(sc_table, sc_id, transaction, changed_by, data_version=None):
    where = {"sc_id": sc_id}
    sc = sc_table.select(where, transaction, columns=["sc_id"])
    if not sc:
        return problem(404, "Bad Request", "Scheduled change does not exist")

    if not data_version:
        return problem(400, "Bad Request", "data_version is missing")

    sc_table.delete(where, changed_by, data_version, transaction)
    return jsonify({})


def post_enact_scheduled_change(sc_table, sc_id, transaction, changed_by):
    sc_table.enactChange(sc_id, changed_by, transaction)
    return jsonify({})


def post_signoffs_scheduled_change(signoffs_table, sc_id, what, transaction, changed_by):
    signoffs_table.insert(changed_by, transaction, sc_id=sc_id, **what)
    return jsonify({})


def delete_signoffs_scheduled_change(sc_id, signoffs_table, transaction, changed_by):
    username = flask.request.args.get("username", changed_by)
    where = {"sc_id": sc_id, "username": username}
    signoff = signoffs_table.select(where, transaction)
    if not signoff:
        return jsonify({"error": "{} has no signoff to revoke".format(changed_by)})

    signoffs_table.delete(where, changed_by=changed_by, transaction=transaction)
    return jsonify({})


def _process_revisions_scheduled_change_history(sc_table, revisions):
    # Although Scheduled Changes are stored across two tables, we don't
    # expose that through the API. Because of this, we need to look up
    # history in both and return the combined version.
    # This is done by the database layer for non-history parts of Scheduled Changes, but
    # that's not feasible for History due to the inheritance structure of the tables,
    # so we do it here instead.

    # There's a big 'ol assumption here that the primary Scheduled Changes
    # table and the conditions table always keep their data version in sync.
    for r in revisions:
        cond = sc_table.conditions.history.select(
            where=[sc_table.conditions.history.sc_id == r["sc_id"], sc_table.conditions.history.data_version == r["data_version"]]
        )
        r.update(cond[0])

    _revisions = []

    for rev in revisions:
        r = {}
        for k, v in rev.items():
            if k == "data_version":
                r["sc_data_version"] = v
            else:
                r[k.replace("base_", "")] = v
        _revisions.append(r)

    return _revisions


def _get_filters_scheduled_change_history(sc_history_table, sc):
    return [sc_history_table.sc_id == sc["sc_id"], sc_history_table.data_version != null()]


def _get_filters_all_scheduled_change_history(sc_history_table, obj):
    query = get_input_dict()
    where = [False, False]
    where = [getattr(sc_history_table, f) == query.get(f) for f in query]
    where.append(sc_history_table.data_version != null())
    request = flask.request
    if hasattr(sc_history_table, "product" or " channel"):
        if request.args.get("product"):
            where.append(sc_history_table.base_product == request.args.get("product"))
        if request.args.get("channel"):
            where.append(sc_history_table.base_channel == request.args.get("channel"))
    if request.args.get("timestamp_from"):
        where.append(sc_history_table.timestamp >= int(request.args.get("timestamp_from")))
    if request.args.get("timestamp_to"):
        where.append(sc_history_table.timestamp <= int(request.args.get("timestamp_to")))
    return where


def _get_what_scheduled_change_history(sc_table, change, changed_by, transaction):
    # There's a big 'ol assumption here that the primary Scheduled Changes
    # table and the conditions table always keep their data version in sync.
    cond_change = sc_table.conditions.history.getChange(data_version=change["data_version"], column_values={"sc_id": change["sc_id"]}, transaction=transaction)
    what = dict(
        # One could argue that we should restore scheduled_by to its value from the change,
        # but since the person who is reverting could be different, it's probably best to
        # use that instead.
        scheduled_by=changed_by,
        complete=change["complete"],
        when=cond_change["when"],
        telemetry_product=cond_change["telemetry_product"],
        telemetry_channel=cond_change["telemetry_channel"],
        telemetry_uptake=cond_change["telemetry_uptake"],
    )
    # Copy in all the base table columns, too.
    for col in sc_table.t.columns:
        if col.name.startswith("base_"):
            what[col.name] = change[col.name]

    return what


def _get_sc_scheduled_change_history(sc_table, sc_id):
    sc = sc_table.select(where=[sc_table.sc_id == sc_id])
    return sc[0] if sc else None


def get_scheduled_change_history(sc_table, sc_id):
    try:
        return get_revisions(
            table=sc_table,
            get_object_callback=lambda: _get_sc_scheduled_change_history(sc_table, sc_id),
            history_filters_callback=_get_filters_scheduled_change_history,
            process_revisions_callback=_process_revisions_scheduled_change_history,
            revisions_order_by=[sc_table.history.timestamp.desc()],
            obj_not_found_msg="Scheduled change does not exist",
        )
    except (ValueError, AssertionError) as msg:
        log.warning("Bad input: %s", msg)
        return problem(400, "Bad Request", "Error in fetching revisions", ext={"exception": msg})


def get_all_scheduled_change_history(sc_table):
    try:
        return get_revisions(
            table=sc_table,
            get_object_callback=lambda: get_scheduled_changes,
            history_filters_callback=_get_filters_all_scheduled_change_history,
            process_revisions_callback=_process_revisions_scheduled_change_history,
            revisions_order_by=[sc_table.history.timestamp.desc()],
            obj_not_found_msg="Scheduled change does not exist",
        )
    except (ValueError, AssertionError) as msg:
        log.warning("Bad input: %s", msg)
        return problem(400, "Bad Request", "Error in fetching revisions", ext={"exception": msg})


def post_scheduled_change_history(sc_table, sc_id, transaction, changed_by):
    return revert_to_revision(
        table=sc_table,
        get_object_callback=lambda: _get_sc_scheduled_change_history(sc_table, sc_id),
        change_field="sc_id",
        get_what_callback=lambda change: _get_what_scheduled_change_history(sc_table, change, changed_by, transaction),
        changed_by=changed_by,
        response_message="Success",
        transaction=transaction,
        obj_not_found_msg="given sc_id was not found in the database",
    )
