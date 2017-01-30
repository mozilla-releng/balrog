import json

from sqlalchemy.sql.expression import null

from flask import jsonify, request, Response
from flask_wtf import Form

from auslib.admin.views.base import AdminView, HistoryAdminView
from auslib.admin.views.forms import DbEditableForm, SignoffForm


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
            # TODO: Probably need to return signoffs still required after
            # that's been implemented. That + existing signoffs may end up
            # in the same data structure.
            r = {"signoffs": {}}
            for signoff in self.sc_table.signoffs.select({"sc_id": row["sc_id"]}):
                r["signoffs"][signoff["username"]] = signoff["role"]

            for k, v in row.iteritems():
                if k == "data_version":
                    r["sc_data_version"] = v
                else:
                    r[k.replace("base_", "")] = v
            ret["scheduled_changes"].append(r)
        return jsonify(ret)

    def _post(self, form, transaction, changed_by):
        if not form.validate():
            self.log.warning("Bad input: %s", form.errors)
            return Response(status=400, response=json.dumps(form.errors))

        try:
            # Forms can normally be accessed as a dict through form.data,
            # but because some of the Forms we end up using have a Field
            # called "data", this gets overridden, so we need to construct
            # a dict ourselves.
            columns = {k: v.data for k, v in form._fields.iteritems()}
            sc_id = self.sc_table.insert(changed_by, transaction, **columns)
        except ValueError as e:
            self.log.warning("Bad input: %s", e)
            return Response(status=400, response=json.dumps({"exception": e.args}))

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
            if (request.json and k in request.json):
                what[k] = v.data

        where = {"sc_id": sc_id}
        try:
            self.sc_table.update(where, what, changed_by, form.sc_data_version.data, transaction)
            signOffs = self.sc_table.signoffs.select(where=where, transaction=transaction, columns=["sc_id", "username"])
            for signOff in signOffs:
                self.sc_table.signoffs.delete(where={"sc_id": sc_id, "username": signOff["username"]},
                                              changed_by=changed_by, transaction=transaction)
        except ValueError as e:
            self.log.warning("Bad input: %s", e)
            return Response(status=400, response=json.dumps({"exception": e.args}))

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

        try:
            self.signoffs_table.insert(changed_by, transaction, sc_id=sc_id, **form.data)
        except ValueError as e:
            self.log.warning("Bad input: %s", e)
            return Response(status=400, response=json.dumps({"exception": e.args}))

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


class ScheduledChangeHistoryView(HistoryAdminView):
    """/scheduled_changes/:namespace/revisions"""

    def __init__(self, namespace, table, *args, **kwargs):
        self.namespace = namespace
        self.path = "/scheduled_changes/%s/revisions" % namespace
        self.table = table
        super(ScheduledChangeHistoryView, self).__init__(*args, **kwargs)

    def get(self, sc_id):
        if not self.table.scheduled_changes.select({"sc_id": sc_id}):
            return Response(status=404, response="Scheduled change does not exist")

        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 100))
            assert page >= 1
        except (ValueError, AssertionError) as msg:
            self.log.warning("Bad input: %s", msg)
            return Response(status=400, response=json.dumps({"exception": msg}))

        offset = limit * (page - 1)
        total_count = self.table.scheduled_changes.history.t.count()\
            .where(self.table.scheduled_changes.history.sc_id == sc_id)\
            .where(self.table.scheduled_changes.history.data_version != null())\
            .execute()\
            .fetchone()[0]

        # Although Scheduled Changes are stored across two tables, we don't
        # expose that through the API. Because of this, we need to look up
        # history in both and return the combined version.
        # This is done by the database layer for non-history parts of Scheduled Changes, but
        # that's not feasible for History due to the inheritance structure of the tables,
        # so we do it here instead.
        revisions = self.table.scheduled_changes.history.select(
            where=[self.table.scheduled_changes.history.sc_id == sc_id,
                   self.table.scheduled_changes.history.data_version != null()],
            limit=limit,
            offset=offset,
            order_by=[self.table.scheduled_changes.history.timestamp.desc()],
        )
        # There's a big 'ol assumption here that the primary Scheduled Changes
        # table and the conditions table always keep their data version in sync.
        for r in revisions:
            cond = self.table.scheduled_changes.conditions.history.select(
                where=[self.table.scheduled_changes.conditions.history.sc_id == r["sc_id"],
                       self.table.scheduled_changes.conditions.history.data_version == r["data_version"]],
            )
            r.update(cond[0])

        ret = {
            "count": total_count,
            "revisions": [],
        }

        for rev in revisions:
            r = {}
            for k, v in rev.iteritems():
                if k == "data_version":
                    r["sc_data_version"] = v
                else:
                    r[k.replace("base_", "")] = v
            ret["revisions"].append(r)

        return jsonify(ret)

    def _post(self, sc_id, transaction, changed_by):
        change_id = None
        if request.json:
            change_id = request.json.get('change_id')
        if not change_id:
            self.log.warning("Bad input: %s", "no change_id")
            return Response(status=400, response=json.dumps({"exception": "no change_id"}))
        change = self.table.scheduled_changes.history.getChange(change_id=change_id, transaction=transaction)
        if change is None:
            return Response(status=400, response=json.dumps({"exception": "bad change_id"}))
        if change['sc_id'] != sc_id:
            return Response(status=400, response=json.dumps({"exception": "bad sc_id"}))
        sc = self.table.scheduled_changes.select({"sc_id": sc_id}, transaction=transaction)[0]
        if sc is None:
            return Response(status=400, response=json.dumps({"exception": "bad sc_id"}))
        old_data_version = sc['data_version']

        # There's a big 'ol assumption here that the primary Scheduled Changes
        # table and the conditions table always keep their data version in sync.
        cond_change = self.table.scheduled_changes.conditions.history.getChange(
            data_version=change["data_version"],
            column_values={"sc_id": change["sc_id"]},
            transaction=transaction,
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
        for col in self.table.scheduled_changes.t.get_children():
            if col.name.startswith("base_"):
                what[col.name] = change[col.name]

        self.table.scheduled_changes.update(changed_by=changed_by, where={"sc_id": sc_id}, what=what,
                                            old_data_version=old_data_version, transaction=transaction)
        return Response("Success")
