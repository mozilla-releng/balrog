from flask import jsonify, Response
import json

from auslib.admin.views.base import requirelogin, AdminView
from auslib.admin.views.forms import ProductRequiredSignoffsForm
from auslib.db import SignoffRequiredError
from auslib.global_state import dbo


class RequiredSignoffsView(AdminView):

    def __init__(self, table):
        self.table = table
        super(RequiredSignoffsView, self).__init__()

    def get(self):
        rows = self.table.select()
        return jsonify({"count": len(rows), "required_signoffs": [dict(rs) for rs in rows]})

    def _post(self, form, transaction, changed_by):
        if not form.validate():
            self.log.warning("Bad input: %s", form.errors)
            return Response(status=400, response=json.dumps(form.errors))

        where = {"product": form.product.data, "channel": form.channel.data, "role": form.role.data}
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
        super(ProductRequiredSignoffsView, self).__init__(dbo.productRequiredSignoffs)

    @requirelogin
    def _post(self, transaction, changed_by):
        form = ProductRequiredSignoffsForm()
        return super(ProductRequiredSignoffsView, self)._post(form, transaction, changed_by)
