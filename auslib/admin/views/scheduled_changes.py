from flask import jsonify, request, Response

from auslib.admin.views.base import requirelogin, AdminView
from auslib.global_state import dbo


class ScheduledChangesView(AdminView):
    """/scheduled_changes/:namespace"""

    def __init__(self, namespace, table, forms, enact_permissions):
        self.namespace = namespace
        self.path = "/scheduled_changes/%s" % namespace
        self.table = table
        self.sc_table = table.scheduled_changes
        self.new_form, self.edit_form = forms
        self.new_permission, self.edit_permission = enact_permissions
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
            enact_permission = self.new_permission
        else:
            form = self.new_form()
            enact_permission = self.edit_permission

        permission_options = {"product": request.form.get("product")}
        if not dbo.permissions.hasUrlPermission(changed_by, self.path, "POST", urlOptions=permission_options):
            msg = "%s is not allowed to scheduled changes for %s" % (changed_by, self.namespace)
            self.log.warning("Unauthorized access attempt: %s", msg)
            return Response(status=401, response=msg)
        if not dbo.permissions.hasUrlPermission(changed_by, enact_permission, "POST", urlOptions=permission_options):
            msg = "%s does not have premission to enact requested change" % changed_by
            self.log.warning("Unauthorized access attempt: %s", msg)
            return Response(status=401, response=msg)

        try:
            sc_id = self.sc_table.insert(changed_by, transaction, **form.data)
        except ValueError as e:
            self.log.warning("Bad input: %s", e)
            return Response(status=400, response=str(e))

        return jsonify({"sc_id": sc_id})


class ScheduledChangeView(AdminView):
    """/scheduled_changes/:namespace/:sc_id"""

    def __init__(self, namespace, table, forms, enact_permissions):
        self.namespace = namespace
        self.path = "/scheduled_changes/%s/:sc_id" % namespace
        self.table = table
        self.sc_table = table.scheduled_changes
        self.new_form, self.edit_form = forms
        self.new_permission, self.edit_permission = enact_permissions
        super(ScheduledChangeView, self).__init__()
