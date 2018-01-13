import json
import connexion

from sqlalchemy.sql.expression import null

from flask import jsonify, Response

from auslib.web.admin.views.base import requirelogin, AdminView
from auslib.web.admin.views.history import HistoryView
from auslib.web.admin.views.problem import problem
from auslib.web.admin.views.scheduled_changes import ScheduledChangesView, \
    ScheduledChangeView, EnactScheduledChangeView, SignoffsView, \
    ScheduledChangeHistoryView
from auslib.db import SignoffRequiredError
from auslib.global_state import dbo
from auslib.web.common.history import get_input_dict
from sqlalchemy import and_


class RequiredSignoffsView(AdminView):

    def __init__(self, table, decisionFields):
        self.table = table
        self.decisionFields = decisionFields
        super(RequiredSignoffsView, self).__init__()

    def get(self):
        rows = self.table.select()
        return jsonify({"count": len(rows), "required_signoffs": [dict(rs) for rs in rows]})

    def _post(self, what, transaction, changed_by):
        where = {f: what.get(f) for f in self.decisionFields}
        if self.table.select(where=where, transaction=transaction):
            raise SignoffRequiredError("Required Signoffs cannot be directly modified")
        else:
            try:
                self.table.insert(changed_by=changed_by, transaction=transaction, **what)
                return Response(status=201, response=json.dumps({"new_data_version": 1}))
            except ValueError as e:
                self.log.warning("Bad input: %s", e.args)
                return problem(400, "Bad Request", str(e.args))

    def _delete(self, *args, **kwargs):
        raise SignoffRequiredError("Required Signoffs cannot be directly deleted.")


class RequiredSignoffsHistoryAPIView(HistoryView):

    def __init__(self, table, decisionFields):
        self.decisionFields = decisionFields
        super(RequiredSignoffsHistoryAPIView, self).__init__(table=table)

    def _get_filters(self):
        query = get_input_dict()
        where = [getattr(self.table.history, f) == query.get(f) for f in query]
        where.append(self.table.history.data_version != null())
        if hasattr(self.history_table, 'product'):
            where.append(self.history_table.product != null())
        request = connexion.request
        if request.args.get('timestamp_from'):
            where.append(self.history_table.timestamp >= int(request.args.get('timestamp_from')))
        if request.args.get('timestamp_to'):
            where.append(self.history_table.timestamp <= int(request.args.get('timestamp_to')))
        return where

    def get(self, input_dict):
        if not self.table.select({f: input_dict.get(f) for f in self.decisionFields}):
            return problem(404, "Not Found", "Requested Required Signoff does not exist")

        try:
            page = int(connexion.request.args.get('page', 1))
            limit = int(connexion.request.args.get('limit', 100))
        except ValueError as msg:
            self.log.warning("Bad input: %s", msg)
            return problem(400, "Bad Request", str(msg))
        offset = limit * (page - 1)

        query = self.table.history.t.count().where(self.table.history.data_version != null())
        for field in self.decisionFields:
            query = query.where(getattr(self.table.history, field) == input_dict.get(field))
        total_count = query.execute().fetchone()[0]

        where = [getattr(self.table.history, f) == input_dict.get(f) for f in self.decisionFields]
        where.append(self.table.history.data_version != null())
        revisions = self.table.history.select(
            where=where, limit=limit, offset=offset,
            order_by=[self.table.history.timestamp.desc()]
        )

        return jsonify(count=total_count, required_signoffs=revisions)

    def get_all(self):
        try:
            page = int(connexion.request.args.get('page', 1))
            limit = int(connexion.request.args.get('limit', 100))
        except ValueError as msg:
            self.log.warning("Bad input: %s", msg)
            return problem(400, "Bad Request", str(msg))
        offset = limit * (page - 1)

        where = self._get_filters()
        total_count = self.table.history.t.count()\
                                        .where(and_(*where))\
                                        .execute().fetchone()[0]

        revisions = self.table.history.select(
            where=where, limit=limit, offset=offset,
            order_by=[self.table.history.timestamp.desc()]
        )

        return jsonify(count=total_count, required_signoffs=revisions)


class ProductRequiredSignoffsView(RequiredSignoffsView):
    """/required_signoffs/product"""

    def __init__(self):
        super(ProductRequiredSignoffsView, self).__init__(dbo.productRequiredSignoffs, ["product", "channel", "role"])

    @requirelogin
    def _post(self, transaction, changed_by):
        what = {"product": connexion.request.get_json().get("product"),
                "channel": connexion.request.get_json().get("channel"),
                "role": connexion.request.get_json().get("role"),
                "signoffs_required": int(connexion.request.get_json().get("signoffs_required")),
                }
        return super(ProductRequiredSignoffsView, self)._post(what, transaction, changed_by)


class ProductRequiredSignoffsHistoryAPIView(RequiredSignoffsHistoryAPIView):
    """/required_signoffs/product/revisions"""

    def __init__(self):
        super(ProductRequiredSignoffsHistoryAPIView, self).__init__(dbo.productRequiredSignoffs, ["product", "channel", "role"])

    def get(self):
        input_dict = {'product': connexion.request.args.get('product'),
                      'role': connexion.request.args.get('role'),
                      'channel': connexion.request.args.get('channel')}
        return super(ProductRequiredSignoffsHistoryAPIView, self).get(input_dict)


class ProductRequiredSignoffsScheduledChangesView(ScheduledChangesView):
    """/scheduled_changes/required_signoffs/product"""

    def __init__(self):
        super(ProductRequiredSignoffsScheduledChangesView, self).__init__("product_req_signoffs", dbo.productRequiredSignoffs)

    @requirelogin
    def _post(self, transaction, changed_by):
        if connexion.request.get_json().get("when", None) is None:
            return problem(400, "Bad Request", "when cannot be set to null when scheduling a new change "
                                               "for a Product Required Signoff")
        change_type = connexion.request.get_json().get("change_type")

        what = {}
        for field in connexion.request.get_json():
            if field == "csrf_token" or change_type == "insert" and field == "data_version":
                continue
            what[field] = connexion.request.get_json()[field]

        if change_type == "update":
            for field in ["signoffs_required", "data_version"]:
                if not what.get(field, None):
                    return problem(400, "Bad Request", "Missing field", ext={"exception": "%s is missing" % field})
                else:
                    what[field] = int(what[field])

        elif change_type == "insert":
            if not what.get("signoffs_required", None):
                return problem(400, "Bad Request", "Missing field", ext={"exception": "signoffs_required is missing"})
            else:
                what["signoffs_required"] = int(what["signoffs_required"])

        elif change_type == "delete":
            if not what.get("data_version", None):
                return problem(400, "Bad Request", "Missing field", ext={"exception": "data_version is missing"})
            else:
                what["data_version"] = int(what["data_version"])

        return super(ProductRequiredSignoffsScheduledChangesView, self)._post(what, transaction, changed_by,
                                                                              change_type)


class ProductRequiredSignoffScheduledChangeView(ScheduledChangeView):
    """/scheduled_changes/required_signoffs/product/<int:sc_id>"""

    def __init__(self):
        super(ProductRequiredSignoffScheduledChangeView, self).__init__("product_req_signoffs", dbo.productRequiredSignoffs)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        # TODO: modify UI and clients to stop sending 'change_type' in request body
        sc_rs_product = self.sc_table.select(where={"sc_id": sc_id}, transaction=transaction, columns=["change_type"])
        if sc_rs_product:
            change_type = sc_rs_product[0]["change_type"]
        else:
            return problem(404, "Not Found", "Unknown sc_id",
                           ext={"exception": "No scheduled change for product required signoff found for given sc_id"})
        what = {}
        for field in connexion.request.get_json():
            if ((change_type == "insert" and field not in
                ["when", "product", "channel", "role", "signoffs_required"]) or
                (change_type == "update" and field not in ["when", "signoffs_required", "data_version"]) or
                    (change_type == "delete" and field not in ["when", "data_version"])):
                continue

            what[field] = connexion.request.get_json()[field]

        if change_type in ["update", "delete"] and not what.get("data_version", None):
            return problem(400, "Bad Request", "Missing field", ext={"exception": "data_version is missing"})

        if what.get("signoffs_required", None):
            what["signoffs_required"] = int(what["signoffs_required"])

        return super(ProductRequiredSignoffScheduledChangeView, self)._post(sc_id, what, transaction, changed_by,
                                                                            connexion.request.get_json().
                                                                            get("sc_data_version", None))

    @requirelogin
    def _delete(self, sc_id, transaction, changed_by):
        return super(ProductRequiredSignoffScheduledChangeView, self)._delete(sc_id, transaction, changed_by)


class EnactProductRequiredSignoffScheduledChangeView(EnactScheduledChangeView):
    """/scheduled_changes/required_signoffs/product/<int:sc_id>/enact"""

    def __init__(self):
        super(EnactProductRequiredSignoffScheduledChangeView, self).__init__("product_req_signoffs", dbo.productRequiredSignoffs)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(EnactProductRequiredSignoffScheduledChangeView, self)._post(sc_id, transaction, changed_by)


class ProductRequiredSignoffScheduledChangeSignoffsView(SignoffsView):
    """/scheduled_changes/required_signoffs/product/<int:sc_id>/signoffs"""

    def __init__(self):
        super(ProductRequiredSignoffScheduledChangeSignoffsView, self).__init__("product_req_signoffs", dbo.productRequiredSignoffs)


class ProductRequiredSignoffScheduledChangeHistoryView(ScheduledChangeHistoryView):
    """/scheduled_changes/required_signoffs/product/<int:sc_id>/revisions"""

    def __init__(self):
        super(ProductRequiredSignoffScheduledChangeHistoryView, self).__init__("product_req_signoffs", dbo.productRequiredSignoffs)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(ProductRequiredSignoffScheduledChangeHistoryView, self)._post(sc_id, transaction, changed_by)


class PermissionsRequiredSignoffsView(RequiredSignoffsView):
    """/required_signoffs/permissions"""

    def __init__(self):
        super(PermissionsRequiredSignoffsView, self).__init__(dbo.permissionsRequiredSignoffs, ["product", "role"])

    @requirelogin
    def _post(self, transaction, changed_by):
        what = {"product": connexion.request.get_json().get("product"),
                "role": connexion.request.get_json().get("role"),
                "signoffs_required": int(connexion.request.get_json().get("signoffs_required")),
                }
        return super(PermissionsRequiredSignoffsView, self)._post(what, transaction, changed_by)


class PermissionsRequiredSignoffsHistoryAPIView(RequiredSignoffsHistoryAPIView):
    """/required_signoffs/permissions/revisions"""

    def __init__(self):
        super(PermissionsRequiredSignoffsHistoryAPIView, self).__init__(dbo.permissionsRequiredSignoffs, ["product", "role"])

    def get(self):
        input_dict = {'product': connexion.request.args.get('product'), 'role': connexion.request.args.get('role')}
        return super(PermissionsRequiredSignoffsHistoryAPIView, self).get(input_dict)


class PermissionsRequiredSignoffsScheduledChangesView(ScheduledChangesView):
    """/scheduled_changes/required_signoffs/permissions"""

    def __init__(self):
        super(PermissionsRequiredSignoffsScheduledChangesView, self).__init__("permissions_req_signoffs", dbo.permissionsRequiredSignoffs)

    @requirelogin
    def _post(self, transaction, changed_by):
        if connexion.request.get_json().get("when", None) is None:
            return problem(400, "Bad Request", "'when' cannot be set to null when scheduling a new change "
                                               "for a Permissions Required Signoff")
        change_type = connexion.request.get_json().get("change_type")

        what = {}
        for field in connexion.request.get_json():
            if field == "csrf_token" or change_type == "insert" and field == "data_version":
                continue
            what[field] = connexion.request.get_json()[field]

        if change_type == "update":
            for field in ["signoffs_required", "data_version"]:
                if not what.get(field, None):
                    return problem(400, "Bad Request", "Missing field", ext={"exception": "%s is missing" % field})
                else:
                    what[field] = int(what[field])

        elif change_type == "insert":
            if not what.get("signoffs_required", None):
                return problem(400, "Bad Request", "Missing field", ext={"exception": "signoffs_required is missing"})
            else:
                what["signoffs_required"] = int(what["signoffs_required"])

        elif change_type == "delete":
            if not what.get("data_version", None):
                return problem(400, "Bad Request", "Missing field", ext={"exception": "data_version is missing"})
            else:
                what["data_version"] = int(what["data_version"])

        return super(PermissionsRequiredSignoffsScheduledChangesView, self)._post(what, transaction, changed_by,
                                                                                  change_type)


class PermissionsRequiredSignoffScheduledChangeView(ScheduledChangeView):
    """/scheduled_changes/required_signoffs/permissions/<int:sc_id>"""

    def __init__(self):
        super(PermissionsRequiredSignoffScheduledChangeView, self).__init__("permissions_req_signoffs", dbo.permissionsRequiredSignoffs)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        # TODO: modify UI and clients to stop sending 'change_type' in request body
        sc_rs_permission = self.sc_table.select(where={"sc_id": sc_id},
                                                transaction=transaction, columns=["change_type"])
        if sc_rs_permission:
            change_type = sc_rs_permission[0]["change_type"]
        else:
            return problem(404, "Not Found", "Unknown sc_id",
                           ext={"exception": "No scheduled change for permission required "
                                             "signoff found for given sc_id"})
        what = {}
        for field in connexion.request.get_json():
            if ((change_type == "insert" and field not in ["when", "product", "role", "signoffs_required"]) or
                    (change_type == "update" and field not in ["when", "signoffs_required", "data_version"]) or
                    (change_type == "delete" and field not in ["when", "data_version"])):
                continue
            what[field] = connexion.request.get_json()[field]

        if change_type in ["update", "delete"] and not what.get("data_version", None):
            return problem(400, "Bad Request", "Missing field", ext={"exception": "data_version is missing"})

        if what.get("signoffs_required", None):
            what["signoffs_required"] = int(what["signoffs_required"])

        return super(PermissionsRequiredSignoffScheduledChangeView, self)._post(sc_id, what, transaction, changed_by,
                                                                                connexion.request.get_json().
                                                                                get("sc_data_version", None))

    @requirelogin
    def _delete(self, sc_id, transaction, changed_by):
        return super(PermissionsRequiredSignoffScheduledChangeView, self)._delete(sc_id, transaction, changed_by)


class EnactPermissionsRequiredSignoffScheduledChangeView(EnactScheduledChangeView):
    """/scheduled_changes/required_signoffs/permissions/<int:sc_id>/enact"""

    def __init__(self):
        super(EnactPermissionsRequiredSignoffScheduledChangeView, self).__init__("permissions_req_signoffs", dbo.permissionsRequiredSignoffs)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(EnactPermissionsRequiredSignoffScheduledChangeView, self)._post(sc_id, transaction, changed_by)


class PermissionsRequiredSignoffScheduledChangeSignoffsView(SignoffsView):
    """/scheduled_changes/required_signoffs/permissions/<int:sc_id>/signoffs"""

    def __init__(self):
        super(PermissionsRequiredSignoffScheduledChangeSignoffsView, self).__init__("permissions_req_signoffs", dbo.permissionsRequiredSignoffs)


class PermissionsRequiredSignoffScheduledChangeHistoryView(ScheduledChangeHistoryView):
    """/scheduled_changes/required_signoffs/permissions/<int:sc_id>/revisions"""

    def __init__(self):
        super(PermissionsRequiredSignoffScheduledChangeHistoryView, self).__init__("permissions_req_signoffs", dbo.permissionsRequiredSignoffs)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(PermissionsRequiredSignoffScheduledChangeHistoryView, self)._post(sc_id, transaction, changed_by)
