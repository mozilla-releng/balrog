import json

import connexion
from flask import Response, jsonify, request
from sqlalchemy.sql.expression import null

from auslib.db import SignoffRequiredError
from auslib.global_state import dbo
from auslib.web.admin.views.base import debugPath, handleGeneralExceptions, log, requirelogin, transactionHandler
from auslib.web.admin.views.history import HistoryView
from auslib.web.admin.views.problem import problem
from auslib.web.admin.views.scheduled_changes import (
    ScheduledChangeHistoryView,
    SignoffsView,
    delete_scheduled_change,
    get_scheduled_changes,
    post_enact_scheduled_change,
    post_scheduled_change,
    post_scheduled_changes,
)
from auslib.web.common.history import get_input_dict


def get_required_signoffs(required_signoffs, where=None):
    rows = required_signoffs.select(where=where)
    return jsonify({"count": len(rows), "required_signoffs": [dict(rs) for rs in rows]})


def post_required_signoffs(required_signoffs, decisionFields, what, transaction, changed_by):
    where = {f: what.get(f) for f in decisionFields}
    if required_signoffs.select(where=where, transaction=transaction):
        raise SignoffRequiredError("Required Signoffs cannot be directly modified")
    else:
        try:
            required_signoffs.insert(changed_by=changed_by, transaction=transaction, **what)
            return Response(status=201, response=json.dumps({"new_data_version": 1}))
        except ValueError as e:
            log.warning("Bad input: %s", e.args)
            return problem(400, "Bad Request", str(e.args))


def delete_required_signoffs(*args, **kwargs):
    raise SignoffRequiredError("Required Signoffs cannot be directly deleted.")


class RequiredSignoffsHistoryAPIView(HistoryView):
    def __init__(self, table, decisionFields):
        self.decisionFields = decisionFields
        super(RequiredSignoffsHistoryAPIView, self).__init__(table=table)

    def _get_filters(self):
        query = get_input_dict()
        where = [getattr(self.table.history, f) == query.get(f) for f in query]
        where.append(self.table.history.data_version != null())
        request = connexion.request
        if hasattr(self.history_table, "channel"):
            if request.args.get("channel"):
                where.append(self.history_table.channel == request.args.get("channel"))
        if hasattr(self.history_table, "product"):
            where.append(self.history_table.product != null())
            if request.args.get("product"):
                where.append(self.history_table.product == request.args.get("product"))
        if request.args.get("timestamp_from"):
            where.append(self.history_table.timestamp >= int(request.args.get("timestamp_from")))
        if request.args.get("timestamp_to"):
            where.append(self.history_table.timestamp <= int(request.args.get("timestamp_to")))
        return where

    def get(self, input_dict):
        if not self.table.select({f: input_dict.get(f) for f in self.decisionFields}):
            return problem(404, "Not Found", "Requested Required Signoff does not exist")

        try:
            page = int(connexion.request.args.get("page", 1))
            limit = int(connexion.request.args.get("limit", 100))
        except ValueError as msg:
            self.log.warning("Bad input: %s", msg)
            return problem(400, "Bad Request", str(msg))
        offset = limit * (page - 1)

        where_count = [self.table.history.data_version != null()]
        for field in self.decisionFields:
            where_count.append(getattr(self.table.history, field) == input_dict.get(field))
        total_count = self.table.history.count(where=where_count)

        where = [getattr(self.table.history, f) == input_dict.get(f) for f in self.decisionFields]
        where.append(self.table.history.data_version != null())
        revisions = self.table.history.select(where=where, limit=limit, offset=offset, order_by=[self.table.history.timestamp.desc()])

        return jsonify(count=total_count, required_signoffs=revisions)

    def get_all(self):
        try:
            page = int(connexion.request.args.get("page", 1))
            limit = int(connexion.request.args.get("limit", 100))
        except ValueError as msg:
            self.log.warning("Bad input: %s", msg)
            return problem(400, "Bad Request", str(msg))
        offset = limit * (page - 1)

        where = self._get_filters()
        total_count = self.table.history.count(where=where)
        revisions = self.table.history.select(where=where, limit=limit, offset=offset, order_by=[self.table.history.timestamp.desc()])

        return jsonify(count=total_count, required_signoffs=revisions)


def get_product_required_signoffs():
    """/required_signoffs/product"""

    where = {param: request.args[param] for param in ("product", "channel") if param in request.args}
    return get_required_signoffs(required_signoffs=dbo.productRequiredSignoffs, where=where)


@requirelogin
@transactionHandler
@handleGeneralExceptions("POST")
@debugPath
def post_product_required_signoffs(signoff, transaction, changed_by):
    what = {
        "product": signoff.get("product"),
        "channel": signoff.get("channel"),
        "role": signoff.get("role"),
        "signoffs_required": int(signoff.get("signoffs_required")),
    }
    return post_required_signoffs(
        required_signoffs=dbo.productRequiredSignoffs, decisionFields=["product", "channel", "role"], what=what, transaction=transaction, changed_by=changed_by
    )


@handleGeneralExceptions("DELETE")
@debugPath
def delete_product_required_signoffs():
    return delete_required_signoffs()


class ProductRequiredSignoffsHistoryAPIView(RequiredSignoffsHistoryAPIView):
    """/required_signoffs/product/revisions"""

    def __init__(self):
        super(ProductRequiredSignoffsHistoryAPIView, self).__init__(dbo.productRequiredSignoffs, ["product", "channel", "role"])

    def get(self):
        input_dict = {
            "product": connexion.request.args.get("product"),
            "role": connexion.request.args.get("role"),
            "channel": connexion.request.args.get("channel"),
        }
        return super(ProductRequiredSignoffsHistoryAPIView, self).get(input_dict)


def get_product_rs_scheduled_changes():
    """/scheduled_changes/required_signoffs/product"""

    where = {f"base_{param}": request.args[param] for param in ("product", "channel") if param in request.args}
    return get_scheduled_changes(table=dbo.productRequiredSignoffs, where=where)


@requirelogin
@transactionHandler
@handleGeneralExceptions("POST")
@debugPath
def post_product_rs_scheduled_changes(sc_rs_product_body, transaction, changed_by):
    if sc_rs_product_body.get("when", None) is None:
        return problem(400, "Bad Request", "when cannot be set to null when scheduling a new change " "for a Product Required Signoff")
    change_type = sc_rs_product_body.get("change_type")

    what = {}
    for field in sc_rs_product_body:
        if change_type == "insert" and field == "data_version":
            continue
        what[field] = sc_rs_product_body[field]

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

    return post_scheduled_changes(
        sc_table=dbo.productRequiredSignoffs.scheduled_changes, what=what, transaction=transaction, changed_by=changed_by, change_type=change_type
    )


@requirelogin
@transactionHandler
@handleGeneralExceptions("POST")
@debugPath
def post_product_rs_scheduled_change(sc_id, sc_product_rs_body, transaction, changed_by):
    """/scheduled_changes/required_signoffs/product/<int:sc_id>"""

    # TODO: modify UI and clients to stop sending 'change_type' in request body
    sc_table = dbo.productRequiredSignoffs.scheduled_changes
    sc_rs_product = sc_table.select(where={"sc_id": sc_id}, transaction=transaction, columns=["change_type"])
    if sc_rs_product:
        change_type = sc_rs_product[0]["change_type"]
    else:
        return problem(404, "Not Found", "Unknown sc_id", ext={"exception": "No scheduled change for product required signoff found for given sc_id"})
    what = {}
    for field in sc_product_rs_body:
        if (
            (change_type == "insert" and field not in ["when", "product", "channel", "role", "signoffs_required"])
            or (change_type == "update" and field not in ["when", "signoffs_required", "data_version"])
            or (change_type == "delete" and field not in ["when", "data_version"])
        ):
            continue

        what[field] = sc_product_rs_body[field]

    if change_type in ["update", "delete"] and not what.get("data_version", None):
        return problem(400, "Bad Request", "Missing field", ext={"exception": "data_version is missing"})

    if what.get("signoffs_required", None):
        what["signoffs_required"] = int(what["signoffs_required"])

    return post_scheduled_change(
        sc_table=sc_table,
        sc_id=sc_id,
        what=what,
        transaction=transaction,
        changed_by=changed_by,
        old_sc_data_version=sc_product_rs_body.get("sc_data_version", None),
    )


@requirelogin
@transactionHandler
@handleGeneralExceptions("DELETE")
@debugPath
def delete_product_rs_scheduled_change(sc_id, data_version, transaction, changed_by):
    return delete_scheduled_change(
        sc_table=dbo.productRequiredSignoffs.scheduled_changes, sc_id=sc_id, data_version=data_version, transaction=transaction, changed_by=changed_by
    )


@requirelogin
@transactionHandler
@handleGeneralExceptions("POST")
@debugPath
def post_product_rs_enact_scheduled_change(sc_id, transaction, changed_by):
    """/scheduled_changes/required_signoffs/product/<int:sc_id>/enact"""

    return post_enact_scheduled_change(sc_table=dbo.productRequiredSignoffs.scheduled_changes, sc_id=sc_id, transaction=transaction, changed_by=changed_by)


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


def get_permissions_required_signoffs():
    """/required_signoffs/permissions"""

    where = {param: request.args[param] for param in ("product",) if param in request.args}
    return get_required_signoffs(required_signoffs=dbo.permissionsRequiredSignoffs, where=where)


@requirelogin
@transactionHandler
@handleGeneralExceptions("POST")
@debugPath
def post_permissions_required_signoffs(signoff, transaction, changed_by):
    what = {
        "product": signoff.get("product"),
        "role": signoff.get("role"),
        "signoffs_required": int(signoff.get("signoffs_required")),
    }
    return post_required_signoffs(
        required_signoffs=dbo.permissionsRequiredSignoffs, decisionFields=["product", "role"], what=what, transaction=transaction, changed_by=changed_by
    )


@handleGeneralExceptions("DELETE")
@debugPath
def delete_permissions_required_signoffs():
    return delete_required_signoffs()


class PermissionsRequiredSignoffsHistoryAPIView(RequiredSignoffsHistoryAPIView):
    """/required_signoffs/permissions/revisions"""

    def __init__(self):
        super(PermissionsRequiredSignoffsHistoryAPIView, self).__init__(dbo.permissionsRequiredSignoffs, ["product", "role"])

    def get(self):
        input_dict = {"product": connexion.request.args.get("product"), "role": connexion.request.args.get("role")}
        return super(PermissionsRequiredSignoffsHistoryAPIView, self).get(input_dict)


def get_permissions_rs_scheduled_changes():
    """/scheduled_changes/required_signoffs/permissions"""

    where = {f"base_{param}": request.args[param] for param in ("product",) if param in request.args}
    return get_scheduled_changes(table=dbo.permissionsRequiredSignoffs, where=where)


@requirelogin
@transactionHandler
@handleGeneralExceptions("POST")
@debugPath
def post_permissions_rs_scheduled_changes(sc_rs_permission_body, transaction, changed_by):
    if sc_rs_permission_body.get("when", None) is None:
        return problem(400, "Bad Request", "'when' cannot be set to null when scheduling a new change " "for a Permissions Required Signoff")
    change_type = sc_rs_permission_body.get("change_type")

    what = {}
    for field in sc_rs_permission_body:
        if change_type == "insert" and field == "data_version":
            continue
        what[field] = sc_rs_permission_body[field]

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

    return post_scheduled_changes(
        sc_table=dbo.permissionsRequiredSignoffs.scheduled_changes, what=what, transaction=transaction, changed_by=changed_by, change_type=change_type
    )


@requirelogin
@transactionHandler
@handleGeneralExceptions("POST")
@debugPath
def post_permissions_rs_scheduled_change(sc_id, sc_permission_rs_body, transaction, changed_by):
    """/scheduled_changes/required_signoffs/permissions/<int:sc_id>"""

    # TODO: modify UI and clients to stop sending 'change_type' in request body
    sc_table = dbo.permissionsRequiredSignoffs.scheduled_changes
    sc_rs_permission = sc_table.select(where={"sc_id": sc_id}, transaction=transaction, columns=["change_type"])
    if sc_rs_permission:
        change_type = sc_rs_permission[0]["change_type"]
    else:
        return problem(404, "Not Found", "Unknown sc_id", ext={"exception": "No scheduled change for permission required " "signoff found for given sc_id"})
    what = {}
    for field in sc_permission_rs_body:
        if (
            (change_type == "insert" and field not in ["when", "product", "role", "signoffs_required"])
            or (change_type == "update" and field not in ["when", "signoffs_required", "data_version"])
            or (change_type == "delete" and field not in ["when", "data_version"])
        ):
            continue
        what[field] = sc_permission_rs_body[field]

    if change_type in ["update", "delete"] and not what.get("data_version", None):
        return problem(400, "Bad Request", "Missing field", ext={"exception": "data_version is missing"})

    if what.get("signoffs_required", None):
        what["signoffs_required"] = int(what["signoffs_required"])

    return post_scheduled_change(
        sc_table=sc_table,
        sc_id=sc_id,
        what=what,
        transaction=transaction,
        changed_by=changed_by,
        old_sc_data_version=sc_permission_rs_body.get("sc_data_version", None),
    )


@requirelogin
@transactionHandler
@handleGeneralExceptions("DELETE")
@debugPath
def delete_permissions_rs_scheduled_change(sc_id, data_version, transaction, changed_by):
    return delete_scheduled_change(
        sc_table=dbo.permissionsRequiredSignoffs.scheduled_changes, sc_id=sc_id, data_version=data_version, transaction=transaction, changed_by=changed_by
    )


@requirelogin
@transactionHandler
@handleGeneralExceptions("POST")
@debugPath
def post_permissions_rs_enact_scheduled_change(sc_id, transaction, changed_by):
    """/scheduled_changes/required_signoffs/permissions/<int:sc_id>/enact"""

    return post_enact_scheduled_change(sc_table=dbo.permissionsRequiredSignoffs.scheduled_changes, sc_id=sc_id, transaction=transaction, changed_by=changed_by)


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
