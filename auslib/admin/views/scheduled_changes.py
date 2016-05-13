from flask import jsonify, request, Response

from auslib.admin.views.base import requirelogin, AdminView


class ScheduledChangesView(AdminView):
    """/scheduled_changes/:namespace"""

    def __init__(self, namespace, table, forms):
        self.namespace = namespace
        self.path = "/scheduled_changes/%s" % namespace
        self.table = table
        self.sc_table = table.scheduled_changes
        self.new_form, self.edit_form = forms
        super(ScheduledChangesView, self).__init__()

    def get(self):
        rows = self.sc_table.select()
        return jsonify({
            "count": len(rows),
            "scheduled_changes": rows,
        })

    @requirelogin
    def _post(self, transaction, changed_by):
        if request.form.get("data_version"):
            form = self.edit_form()
        else:
            form = self.new_form()

        try:
            sc_id = self.sc_table.insert(changed_by, transaction, **form.data)
        except ValueError as e:
            self.log.warning("Bad input: %s", e)
            return Response(status=400, response=str(e))

        return jsonify({"sc_id": sc_id})


class ScheduledChangeView(AdminView):
    """/scheduled_changes/:namespace/:sc_id"""

    def __init__(self, namespace, table, forms):
        self.namespace = namespace
        self.path = "/scheduled_changes/%s/:sc_id" % namespace
        self.table = table
        self.sc_table = table.scheduled_changes
        self.new_form, self.edit_form = forms
        super(ScheduledChangeView, self).__init__()

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        if request.form.get("data_version"):
            form = self.edit_form()
        else:
            form = self.new_form()

        rule_data = form.data.copy()
        del rule_data["sc_data_version"]
        old_data_version = form.data["sc_data_version"]

        try:
            self.sc_table.update({"sc_id": sc_id}, form.data, changed_by, old_data_version, transaction)
        except ValueError as e:
            self.log.warning("Bad input: %s", e)
            return Response(status=400, response=str(e))

        return Response(status=200)
