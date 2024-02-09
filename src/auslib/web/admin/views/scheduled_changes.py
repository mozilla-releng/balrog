import connexion
from flask import jsonify
from sqlalchemy.sql.expression import null

from auslib.util.signoffs import serialize_signoff_requirements
from auslib.web.admin.views.base import AdminView, requirelogin
from auslib.web.admin.views.history import HistoryView
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
    """/scheduled_changes/:namespace"""

    sc_table = table.scheduled_changes

    if where is None:
        where = {}

    if connexion.request.args.get("all") is None:
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
    """/scheduled_changes/:namespace/:sc_id"""

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


def delete_scheduled_change(sc_table, sc_id, data_version, transaction, changed_by):
    where = {"sc_id": sc_id}
    sc = sc_table.select(where, transaction, columns=["sc_id"])
    if not sc:
        return problem(404, "Bad Request", "Scheduled change does not exist")

    if not connexion.request.args.get("data_version", None):
        return problem(400, "Bad Request", "data_version is missing")

    sc_table.delete(where, changed_by, data_version, transaction)
    return jsonify({})


class EnactScheduledChangeView(AdminView):
    """/scheduled_changes/:namespace/:sc_id/enact"""

    def __init__(self, namespace, table):
        self.namespace = namespace
        self.path = "/scheduled_changes/%s/:sc_id/enact" % namespace
        self.table = table
        self.sc_table = table.scheduled_changes
        super(EnactScheduledChangeView, self).__init__()

    def _post(self, sc_id, transaction, changed_by):
        self.sc_table.enactChange(sc_id, changed_by, transaction)
        return jsonify({})


class SignoffsView(AdminView):
    """/scheduled_change/:namespace/:sc_id/signoffs"""

    def __init__(self, namespace, table):
        self.namespace = namespace
        self.path = "/scheduled_changes/%s/:sc_id/signoffs" % namespace
        self.signoffs_table = table.scheduled_changes.signoffs
        super(SignoffsView, self).__init__()

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        what = {"role": connexion.request.get_json().get("role")}
        self.signoffs_table.insert(changed_by, transaction, sc_id=sc_id, **what)
        return jsonify({})

    @requirelogin
    def _delete(self, sc_id, transaction, changed_by):
        username = connexion.request.args.get("username", changed_by)
        where = {"sc_id": sc_id, "username": username}
        signoff = self.signoffs_table.select(where, transaction)
        if not signoff:
            return jsonify({"error": "{} has no signoff to revoke".format(changed_by)})

        self.signoffs_table.delete(where, changed_by=changed_by, transaction=transaction)
        return jsonify({})


class ScheduledChangeHistoryView(HistoryView):
    """/scheduled_changes/:namespace/revisions"""

    def __init__(self, namespace, table, *args, **kwargs):
        self.namespace = namespace
        self.path = "/scheduled_changes/%s/revisions" % namespace
        super(ScheduledChangeHistoryView, self).__init__(table.scheduled_changes, *args, **kwargs)

    def _process_revisions(self, revisions):
        # Although Scheduled Changes are stored across two tables, we don't
        # expose that through the API. Because of this, we need to look up
        # history in both and return the combined version.
        # This is done by the database layer for non-history parts of Scheduled Changes, but
        # that's not feasible for History due to the inheritance structure of the tables,
        # so we do it here instead.

        # There's a big 'ol assumption here that the primary Scheduled Changes
        # table and the conditions table always keep their data version in sync.
        for r in revisions:
            cond = self.table.conditions.history.select(
                where=[self.table.conditions.history.sc_id == r["sc_id"], self.table.conditions.history.data_version == r["data_version"]]
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

    def _get_filters(self, sc):
        return [self.history_table.sc_id == sc["sc_id"], self.history_table.data_version != null()]

    def _get_filters_all(self, obj):
        query = get_input_dict()
        where = [False, False]
        where = [getattr(self.history_table, f) == query.get(f) for f in query]
        where.append(self.history_table.data_version != null())
        request = connexion.request
        if hasattr(self.history_table, "product" or " channel"):
            if request.args.get("product"):
                where.append(self.history_table.base_product == request.args.get("product"))
            if request.args.get("channel"):
                where.append(self.history_table.base_channel == request.args.get("channel"))
        if request.args.get("timestamp_from"):
            where.append(self.history_table.timestamp >= int(request.args.get("timestamp_from")))
        if request.args.get("timestamp_to"):
            where.append(self.history_table.timestamp <= int(request.args.get("timestamp_to")))
        return where

    def _get_what(self, change, changed_by, transaction):
        # There's a big 'ol assumption here that the primary Scheduled Changes
        # table and the conditions table always keep their data version in sync.
        cond_change = self.table.conditions.history.getChange(
            data_version=change["data_version"], column_values={"sc_id": change["sc_id"]}, transaction=transaction
        )
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
        for col in self.table.t.columns:
            if col.name.startswith("base_"):
                what[col.name] = change[col.name]

        return what

    def _get_sc(self, sc_id):
        sc = self.table.select(where=[self.table.sc_id == sc_id])
        return sc[0] if sc else None

    def get(self, sc_id):
        try:
            return self.get_revisions(
                get_object_callback=lambda: self._get_sc(sc_id),
                history_filters_callback=self._get_filters,
                process_revisions_callback=self._process_revisions,
                revisions_order_by=[self.history_table.timestamp.desc()],
                obj_not_found_msg="Scheduled change does not exist",
            )
        except (ValueError, AssertionError) as msg:
            self.log.warning("Bad input: %s", msg)
            return problem(400, "Bad Request", "Error in fetching revisions", ext={"exception": msg})

    def get_all(self):
        try:
            return self.get_revisions(
                get_object_callback=lambda: get_scheduled_changes,
                history_filters_callback=self._get_filters_all,
                process_revisions_callback=self._process_revisions,
                revisions_order_by=[self.history_table.timestamp.desc()],
                obj_not_found_msg="Scheduled change does not exist",
            )
        except (ValueError, AssertionError) as msg:
            self.log.warning("Bad input: %s", msg)
            return problem(400, "Bad Request", "Error in fetching revisions", ext={"exception": msg})

    def _post(self, sc_id, transaction, changed_by):
        return self.revert_to_revision(
            get_object_callback=lambda: self._get_sc(sc_id),
            change_field="sc_id",
            get_what_callback=lambda change: self._get_what(change, changed_by, transaction),
            changed_by=changed_by,
            response_message="Success",
            transaction=transaction,
            obj_not_found_msg="given sc_id was not found in the database",
        )
