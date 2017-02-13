import json

from sqlalchemy.sql.expression import null

from flask import jsonify, Response, request

from auslib.admin.views.base import requirelogin, AdminView
from auslib.admin.views.forms import ProductRequiredSignoffForm, \
    ProductRequiredSignoffHistoryForm, \
    ScheduledChangeExistingProductRequiredSignoffForm, \
    ScheduledChangeNewProductRequiredSignoffForm, \
    ScheduledChangeDeleteProductRequiredSignoffForm, \
    EditScheduledChangeNewProductRequiredSignoffForm, \
    EditScheduledChangeExistingProductRequiredSignoffForm, \
    PermissionsRequiredSignoffForm, \
    PermissionsRequiredSignoffHistoryForm, \
    ScheduledChangeExistingPermissionsRequiredSignoffForm, \
    ScheduledChangeNewPermissionsRequiredSignoffForm, \
    ScheduledChangeDeletePermissionsRequiredSignoffForm, \
    EditScheduledChangeNewPermissionsRequiredSignoffForm, \
    EditScheduledChangeExistingPermissionsRequiredSignoffForm
from auslib.admin.views.history import HistoryView
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

        where = {f: form[f].data for f in self.decisionFields}
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


class RequiredSignoffsHistoryAPIView(HistoryView):

    def __init__(self, table, decisionFields):
        self.decisionFields = decisionFields
        super(RequiredSignoffsHistoryAPIView, self).__init__(table=table)

    def get(self, form):
        if not self.table.select({f: getattr(form, f).data for f in self.decisionFields}):
            return Response(status=404, response="Requested Required Signoff does not exist")

        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 100))
            assert page >= 1
        except (ValueError, AssertionError) as msg:
            self.log.warning("Bad input: %s", msg)
            return Response(status=400, response=str(msg))
        offset = limit * (page - 1)

        query = self.table.history.t.count().where(self.table.history.data_version != null())
        for field in self.decisionFields:
            query = query.where(getattr(self.table.history, field) == getattr(form, field).data)
        total_count = query.execute().fetchone()[0]

        where = [getattr(self.table.history, f) == getattr(form, f).data for f in self.decisionFields]
        where.append(self.table.history.data_version != null())
        revisions = self.table.history.select(
            where=where, limit=limit, offset=offset,
            order_by=[self.table.history.timestamp.desc()]
        )

        return jsonify(count=total_count, required_signoffs=revisions)


class ProductRequiredSignoffsView(RequiredSignoffsView):

    def __init__(self):
        super(ProductRequiredSignoffsView, self).__init__(dbo.productRequiredSignoffs, ["product", "channel", "role"])

    @requirelogin
    def _post(self, transaction, changed_by):
        form = ProductRequiredSignoffForm()
        return super(ProductRequiredSignoffsView, self)._post(form, transaction, changed_by)


class ProductRequiredSignoffsHistoryAPIView(RequiredSignoffsHistoryAPIView):

    def __init__(self):
        super(ProductRequiredSignoffsHistoryAPIView, self).__init__(dbo.productRequiredSignoffs, ["product", "channel", "role"])

    def get(self):
        form = ProductRequiredSignoffHistoryForm(request.args)
        return super(ProductRequiredSignoffsHistoryAPIView, self).get(form)


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
            self.log.warning("Bad input: %s", msg)
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


class PermissionsRequiredSignoffsHistoryAPIView(RequiredSignoffsHistoryAPIView):

    def __init__(self):
        super(PermissionsRequiredSignoffsHistoryAPIView, self).__init__(dbo.permissionsRequiredSignoffs, ["product", "role"])

    def get(self):
        form = PermissionsRequiredSignoffHistoryForm(request.args)
        return super(PermissionsRequiredSignoffsHistoryAPIView, self).get(form)


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
            self.log.warning("Bad input: %s", msg)
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


class PermissionsRequiredSignoffScheduledChangeHistoryView(ScheduledChangeHistoryView):
    def __init__(self):
        super(PermissionsRequiredSignoffScheduledChangeHistoryView, self).__init__("permissions_req_signoffs", dbo.permissionsRequiredSignoffs)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(PermissionsRequiredSignoffScheduledChangeHistoryView, self)._post(sc_id, transaction, changed_by)
