import json

from sqlalchemy.sql.expression import null

from flask import jsonify, request, Response
from flask_wtf import Form

from auslib.admin.views.base import AdminView
from auslib.admin.views.forms import DbEditableForm, SignoffForm
from auslib.admin.views.history import HistoryView


class ScheduledChangesView(AdminView):
    """/scheduled_changes/:namespace"""

    def __init__(self, namespace, table):
        self.namespace = namespace
        self.path = "/scheduled_changes/%s" % namespace
        self.table = table
        self.sc_table = table.scheduled_changes
        super(ScheduledChangesView, self).__init__()

    def get(self):
        if request.args.get("all"):
            rows = self.sc_table.select()
        else:
            rows = self.sc_table.select(where={"complete": False})
        ret = {"count": len(rows), "scheduled_changes": []}
        for row in rows:
            r = {"signoffs": {}, "required_signoffs": {}}
            base_row = {}

            for k, v in row.iteritems():
                if k == "data_version":
                    r["sc_data_version"] = v
                else:
                    if k.startswith("base_"):
                        k = k.replace("base_", "")
                        base_row[k] = v
                    r[k] = v

            for signoff in self.sc_table.signoffs.select({"sc_id": row["sc_id"]}):
                r["signoffs"][signoff["username"]] = signoff["role"]

            # No point in retrieving this for completed scheduled changes...
            if not row["complete"]:
                for rs in self.table.getPotentialRequiredSignoffs([base_row]):
                    r["required_signoffs"][rs["role"]] = max(r["required_signoffs"].get(rs["role"], 0), rs["signoffs_required"])

            ret["scheduled_changes"].append(r)
        return jsonify(ret)

    def _post(self, form, transaction, changed_by):
        if not form.validate():
            self.log.warning("Bad input: %s", form.errors)
            return Response(status=400, response=json.dumps(form.errors))

        # Forms can normally be accessed as a dict through form.data,
        # but because some of the Forms we end up using have a Field
        # called "data", this gets overridden, so we need to construct
        # a dict ourselves.
        columns = {k: v.data for k, v in form._fields.iteritems()}
        sc_id = self.sc_table.insert(changed_by, transaction, **columns)
        return jsonify(sc_id=sc_id)


class ScheduledChangeView(AdminView):
    """/scheduled_changes/:namespace/:sc_id"""

    def __init__(self, namespace, table):
        self.namespace = namespace
        self.path = "/scheduled_changes/%s/:sc_id" % namespace
        self.table = table
        self.sc_table = table.scheduled_changes
        super(ScheduledChangeView, self).__init__()

    def _post(self, sc_id, form, transaction, changed_by):
        if not form.validate():
            self.log.warning("Bad input: %s", form.errors)
            return Response(status=400, response=json.dumps(form.errors))

        what = dict()
        # We need to be able to support changing AND removing things
        # and because of how Flask's request object and WTForm's defaults work
        # this gets a little hairy.
        for k, v in form._fields.iteritems():
            # sc_data_version is a "special" column, in that it's not part of the
            # primary data, and shouldn't be updatable by the user.
            if k == "sc_data_version":
                continue
            # If the key is not present in the request we treat it as a no-op
            # and shouldn't modify the data for that key.
            # If the key is present we should modify the data as requested.
            # If a value is an empty string, we should remove that restriction
            # from the rule (aka, set as NULL in the db). The underlying Form
            # will have already converted it to None, so we can treat it the
            # same as a modification here.
            if request.json and k in request.json:
                what[k] = v.data

        where = {"sc_id": sc_id}
        self.sc_table.update(where, what, changed_by, form.sc_data_version.data, transaction)
        sc = self.sc_table.select(where=where, transaction=transaction, columns=["data_version"])[0]
        return jsonify(new_data_version=sc["data_version"])

    def _delete(self, sc_id, transaction, changed_by):
        where = {"sc_id": sc_id}
        sc = self.sc_table.select(where, transaction, columns=["sc_id"])
        if not sc:
            return Response(status=404, response="Scheduled change does not exist")

        form = DbEditableForm(request.args)
        self.sc_table.delete(where, changed_by, form.data_version.data, transaction)
        return Response(status=200)


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
        return Response(status=200)


class SignoffsView(AdminView):
    """/scheduled_change/:namespace/:sc_id/signoffs"""

    def __init__(self, namespace, table):
        self.namespace = namespace
        self.path = "/scheduled_changes/%s/:sc_id/signoffs" % namespace
        self.signoffs_table = table.scheduled_changes.signoffs
        super(SignoffsView, self).__init__()

    def _post(self, sc_id, transaction, changed_by):
        form = SignoffForm()
        if not form.validate():
            self.log.warning("Bad input: %s", form.errors)
            return Response(status=400, response=json.dumps(form.errors))

        self.signoffs_table.insert(changed_by, transaction, sc_id=sc_id, **form.data)
        return Response(status=200)

    def _delete(self, sc_id, transaction, changed_by):
        where = {"sc_id": sc_id}
        signoff = self.signoffs_table.select(where, transaction)
        if not signoff:
            return Response(status=404, response="{} has no signoff to revoke".format(changed_by))

        form = Form(request.args)
        if not form.validate():
            self.log.warning("Bad input: %s", form.errors)
            return Response(status=400, response=json.dumps(form.errors))

        self.signoffs_table.delete(where, changed_by=changed_by, transaction=transaction)
        return Response(status=200)


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
                where=[self.table.conditions.history.sc_id == r["sc_id"],
                       self.table.conditions.history.data_version == r["data_version"]],
            )
            r.update(cond[0])

        _revisions = []

        for rev in revisions:
            r = {}
            for k, v in rev.iteritems():
                if k == "data_version":
                    r["sc_data_version"] = v
                else:
                    r[k.replace("base_", "")] = v
            _revisions.append(r)

        return _revisions

    def _get_filters(self, sc):
        return [self.history_table.sc_id == sc['sc_id'],
                self.history_table.data_version != null()]

    def _get_what(self, change, changed_by, transaction):
        # There's a big 'ol assumption here that the primary Scheduled Changes
        # table and the conditions table always keep their data version in sync.
        cond_change = self.table.conditions.history.getChange(
            data_version=change["data_version"],
            column_values={"sc_id": change["sc_id"]},
            transaction=transaction)
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
        for col in self.table.t.get_children():
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
                obj_not_found_msg='Scheduled change does not exist')
        except (ValueError, AssertionError) as msg:
            self.log.warning("Bad input: %s", msg)
            return Response(status=400,
                            response=json.dumps({"exception": msg}))

    def _post(self, sc_id, transaction, changed_by):
        return self.revert_to_revision(
            get_object_callback=lambda: self._get_sc(sc_id),
            change_field='sc_id',
            get_what_callback=lambda change: self._get_what(change,
                                                            changed_by,
                                                            transaction),
            changed_by=changed_by,
            response_message='Success',
            transaction=transaction,
            obj_not_found_msg=json.dumps({"exception": "bad sc_id"}))
