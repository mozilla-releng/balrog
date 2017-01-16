import json

from flask import jsonify, Response, request

from auslib.admin.views.base import requirelogin, AdminView
from auslib.admin.views.forms import ProductRequiredSignoffForm, \
    ScheduledChangeExistingProductRequiredSignoffForm, \
    ScheduledChangeNewProductRequiredSignoffForm, \
    ScheduledChangeDeleteProductRequiredSignoffForm, \
    EditScheduledChangeNewProductRequiredSignoffForm, \
    EditScheduledChangeExistingProductRequiredSignoffForm, \
    PermissionsRequiredSignoffForm, \
    ScheduledChangeExistingPermissionsRequiredSignoffForm, \
    ScheduledChangeNewPermissionsRequiredSignoffForm, \
    ScheduledChangeDeletePermissionsRequiredSignoffForm, \
    EditScheduledChangeNewPermissionsRequiredSignoffForm, \
    EditScheduledChangeExistingPermissionsRequiredSignoffForm
from auslib.admin.views.scheduled_changes import ScheduledChangesView, \
    ScheduledChangeView, EnactScheduledChangeView, SignoffsView, \
    ScheduledChangeHistoryView
from auslib.db import SignoffRequiredError
from auslib.global_state import dbo


class RequiredSignoffsView(AdminView):

    def __init__(self, table, decisionFields):
        self.table = table
        self.decisionFields = decisionFields
        super(RequiredSignoffsView, self).__init__()

    def get(self):
        rows = self.table.select()
        return jsonify({"count": len(rows), "required_signoffs": [dict(rs) for rs in rows]})

    def _post(self, form, transaction, changed_by):
        if not form.validate():
            self.log.warning("Bad input: %s", form.errors)
            return Response(status=400, response=json.dumps(form.errors))

        where = {}
        for f in self.decisionFields:
            where[f] = form[f].data
        if self.table.select(where=where, transaction=transaction):
            raise SignoffRequiredError("Required Signoffs cannot be directly modified")
        else:
            try:
                self.table.insert(changed_by=changed_by, transaction=transaction, **form.data)
                return Response(status=201, response=json.dumps({"new_data_version": 1}))
            except ValueError as e:
                self.log.warning("Bad input: %s", e.args)
                return Response(status=400, response=e.args)

    def _delete(self, *args, **kwargs):
        raise SignoffRequiredError("Required Signoffs cannot be directly deleted.")


class ProductRequiredSignoffsView(RequiredSignoffsView):

    def __init__(self):
        super(ProductRequiredSignoffsView, self).__init__(dbo.productRequiredSignoffs, ["product", "channel", "role"])

    @requirelogin
    def _post(self, transaction, changed_by):
        form = ProductRequiredSignoffForm()
        return super(ProductRequiredSignoffsView, self)._post(form, transaction, changed_by)


class ProductRequiredSignoffsScheduledChangesView(ScheduledChangesView):
    def __init__(self):
        super(ProductRequiredSignoffsScheduledChangesView, self).__init__("product_req_signoffs", dbo.productRequiredSignoffs)

    @requirelogin
    def _post(self, transaction, changed_by):
        change_type = request.json.get("change_type")

        if change_type == "update":
            form = ScheduledChangeExistingProductRequiredSignoffForm()
        elif change_type == "insert":
            form = ScheduledChangeNewProductRequiredSignoffForm()
        elif change_type == "delete":
            form = ScheduledChangeDeleteProductRequiredSignoffForm()
        else:
            return Response(status=400, response="Invalid or missing change_type")

        return super(ProductRequiredSignoffsScheduledChangesView, self)._post(form, transaction, changed_by)


class ProductRequiredSignoffScheduledChangeView(ScheduledChangeView):
    def __init__(self):
        super(ProductRequiredSignoffScheduledChangeView, self).__init__("product_req_signoffs", dbo.productRequiredSignoffs)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        if request.json and request.json.get("data_version"):
            form = EditScheduledChangeExistingProductRequiredSignoffForm()
        else:
            form = EditScheduledChangeNewProductRequiredSignoffForm()

        return super(ProductRequiredSignoffScheduledChangeView, self)._post(sc_id, form, transaction, changed_by)

    @requirelogin
    def _delete(self, sc_id, transaction, changed_by):
        return super(ProductRequiredSignoffScheduledChangeView, self)._delete(sc_id, transaction, changed_by)


class EnactProductRequiredSignoffScheduledChangeView(EnactScheduledChangeView):
    def __init__(self):
        super(EnactProductRequiredSignoffScheduledChangeView, self).__init__("product_req_signoffs", dbo.productRequiredSignoffs)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(EnactProductRequiredSignoffScheduledChangeView, self)._post(sc_id, transaction, changed_by)


class ProductRequiredSignoffScheduledChangeSignoffsView(SignoffsView):
    def __init__(self):
        super(ProductRequiredSignoffScheduledChangeSignoffsView, self).__init__("product_req_signoffs", dbo.productRequiredSignoffs)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(ProductRequiredSignoffScheduledChangeSignoffsView, self)._post(sc_id, transaction, changed_by)

    @requirelogin
    def _delete(self, sc_id, transaction, changed_by):
        return super(ProductRequiredSignoffScheduledChangeSignoffsView, self)._delete(sc_id, transaction, changed_by)


class ProductRequiredSignoffScheduledChangeHistoryView(ScheduledChangeHistoryView):
    def __init__(self):
        super(ProductRequiredSignoffScheduledChangeHistoryView, self).__init__("product_req_signoffs", dbo.productRequiredSignoffs)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(ProductRequiredSignoffScheduledChangeHistoryView, self)._post(sc_id, transaction, changed_by)


class PermissionsRequiredSignoffsView(RequiredSignoffsView):

    def __init__(self):
        super(PermissionsRequiredSignoffsView, self).__init__(dbo.permissionsRequiredSignoffs, ["product", "role"])

    @requirelogin
    def _post(self, transaction, changed_by):
        form = PermissionsRequiredSignoffForm()
        return super(PermissionsRequiredSignoffsView, self)._post(form, transaction, changed_by)


class PermissionsRequiredSignoffsScheduledChangesView(ScheduledChangesView):
    def __init__(self):
        super(PermissionsRequiredSignoffsScheduledChangesView, self).__init__("permissions_req_signoffs", dbo.permissionsRequiredSignoffs)

    @requirelogin
    def _post(self, transaction, changed_by):
        change_type = request.json.get("change_type")

        if change_type == "update":
            form = ScheduledChangeExistingPermissionsRequiredSignoffForm()
        elif change_type == "insert":
            form = ScheduledChangeNewPermissionsRequiredSignoffForm()
        elif change_type == "delete":
            form = ScheduledChangeDeletePermissionsRequiredSignoffForm()
        else:
            return Response(status=400, response="Invalid or missing change_type")

        return super(PermissionsRequiredSignoffsScheduledChangesView, self)._post(form, transaction, changed_by)


class PermissionsRequiredSignoffScheduledChangeView(ScheduledChangeView):
    def __init__(self):
        super(PermissionsRequiredSignoffScheduledChangeView, self).__init__("permissions_req_signoffs", dbo.permissionsRequiredSignoffs)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        if request.json and request.json.get("data_version"):
            form = EditScheduledChangeExistingPermissionsRequiredSignoffForm()
        else:
            form = EditScheduledChangeNewPermissionsRequiredSignoffForm()

        return super(PermissionsRequiredSignoffScheduledChangeView, self)._post(sc_id, form, transaction, changed_by)

    @requirelogin
    def _delete(self, sc_id, transaction, changed_by):
        return super(PermissionsRequiredSignoffScheduledChangeView, self)._delete(sc_id, transaction, changed_by)


class EnactPermissionsRequiredSignoffScheduledChangeView(EnactScheduledChangeView):
    def __init__(self):
        super(EnactPermissionsRequiredSignoffScheduledChangeView, self).__init__("permissions_req_signoffs", dbo.permissionsRequiredSignoffs)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(EnactPermissionsRequiredSignoffScheduledChangeView, self)._post(sc_id, transaction, changed_by)


class PermissionsRequiredSignoffScheduledChangeSignoffsView(SignoffsView):
    def __init__(self):
        super(PermissionsRequiredSignoffScheduledChangeSignoffsView, self).__init__("permissions_req_signoffs", dbo.permissionsRequiredSignoffs)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(PermissionsRequiredSignoffScheduledChangeSignoffsView, self)._post(sc_id, transaction, changed_by)

    @requirelogin
    def _delete(self, sc_id, transaction, changed_by):
        return super(PermissionsRequiredSignoffScheduledChangeSignoffsView, self)._delete(sc_id, transaction, changed_by)


class PermissionsRequiredSignoffScheduledChangeHistoryView(ScheduledChangeHistoryView):
    def __init__(self):
        super(PermissionsRequiredSignoffScheduledChangeHistoryView, self).__init__("permissions_req_signoffs", dbo.permissionsRequiredSignoffs)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(PermissionsRequiredSignoffScheduledChangeHistoryView, self)._post(sc_id, transaction, changed_by)
