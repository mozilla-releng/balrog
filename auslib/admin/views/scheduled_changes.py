import json

from flask import jsonify, request, Response

from auslib.admin.views.base import AdminView


class ScheduledChangesView(AdminView):
    """/scheduled_changes/:namespace"""

    def __init__(self, namespace, table):
        self.namespace = namespace
        self.path = "/scheduled_changes/%s" % namespace
        self.table = table
        self.sc_table = table.scheduled_changes
        super(ScheduledChangesView, self).__init__()

    def get(self):
        rows = self.sc_table.select()
        return jsonify({
            "count": len(rows),
            "scheduled_changes": rows,
        })

    def _post(self, form, transaction, changed_by):
        if not form.validate():
            self.log.warning("Bad input: %s", form.errors)
            return Response(status=400, response=json.dumps(form.errors))

        try:
            sc_id = self.sc_table.insert(changed_by, transaction, **form.data)
        except ValueError as e:
            self.log.warning("Bad input: %s", e)
            return Response(status=400, response=str(e))

        return jsonify({"sc_id": sc_id})


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
        for k, v in form.data.iteritems():
            # sc_data_version is a "special" column, in that it's not part of the
            # primary data, and shouldn't be updatable by the user.
            if k == "sc_data_version":
                continue
            # We need to check for each column in both the JSON style post
            # and the regular multipart form data. If the key is not present in
            # either of these data structures. We treat this cases as no-op
            # and shouldn't modify the data for that key.
            # If the key is present we should modify the data as requested.
            # If a value is an empty string, we should remove that restriction
            # from the rule (aka, set as NULL in the db). The underlying Form
            # will have already converted it to None, so we can treat it the
            # same as a modification here.
            if (request.json and k in request.json) or k in request.form:
                what[k] = v

        try:
            self.sc_table.update({"sc_id": sc_id}, what, changed_by, form.sc_data_version.data, transaction)
        except ValueError as e:
            self.log.warning("Bad input: %s", e)
            return Response(status=400, response=str(e))

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
