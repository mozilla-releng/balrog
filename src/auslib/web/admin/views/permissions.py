import json

import connexion
from flask import Response, jsonify

from auslib.global_state import dbo
from auslib.web.admin.views.base import handleGeneralExceptions, requirelogin, transactionHandler, log
from auslib.web.admin.views.problem import problem
from auslib.web.admin.views.scheduled_changes import (
    EnactScheduledChangeView,
    ScheduledChangeHistoryView,
    ScheduledChangesView,
    ScheduledChangeView,
    SignoffsView,
)

__all__ = ["PermissionsView"]


def get_users():
    """/users"""

    users = dbo.permissions.getAllUsers()
    log.debug("Found users: %s", users)
    # We don't return a plain jsonify'ed list here because of:
    # http://flask.pocoo.org/docs/security/#json-security
    # return jsonify(dict(users=users))
    return jsonify(users)



@requirelogin
@handleGeneralExceptions("GET")
def get_specific_user(username, changed_by):
    """/users/:username
    Returns all of the details about the named user."""

    permissions = dbo.permissions.getUserPermissions(username, changed_by)

    if not permissions:
        return problem(status=404, title="Not Found", detail="No permission found for username %s" % username)
    roles = {r["role"]: {"data_version": r["data_version"]} for r in dbo.permissions.getUserRoles(username)}
    return jsonify({"username": username, "permissions": permissions, "roles": roles})



@requirelogin
@handleGeneralExceptions("GET")
def get_user_permissions(username, changed_by):
    """/users/:username/permissions"""

    permissions = dbo.permissions.getUserPermissions(username, changed_by)
    return jsonify(permissions)



@requirelogin
@handleGeneralExceptions("GET")
def get_specific_user_permission(username, permission, changed_by):
    """/users/:username/permissions/:permission"""

    try:
        perm = dbo.permissions.getUserPermissions(username, changed_by)[permission]
    except KeyError:
        return problem(404, "Not Found", "Requested user permission" " %s not found for %s" % (permission, username))
    return jsonify(perm)


@requirelogin
def put_specific_user_permission(username, permission, changed_by, transaction):
    try:
        if dbo.permissions.getUserPermissions(username, changed_by, transaction).get(permission):
            # Existing Permission
            if not connexion.request.get_json().get("data_version"):
                return problem(400, "Bad Request", "'data_version' is missing from request body")

            options_dict = None
            if connexion.request.get_json().get("options"):
                options_dict = json.loads(connexion.request.get_json().get("options"))
                if len(options_dict) == 0:
                    options_dict = None

            dbo.permissions.update(
                where={"username": username, "permission": permission},
                what={"options": options_dict},
                changed_by=changed_by,
                old_data_version=connexion.request.get_json().get("data_version"),
                transaction=transaction,
            )
            new_data_version = dbo.permissions.getPermission(username=username, permission=permission, transaction=transaction)["data_version"]
            return jsonify(new_data_version=new_data_version)
        else:
            # New Permission
            options_dict = None
            if connexion.request.get_json().get("options"):
                options_dict = json.loads(connexion.request.get_json().get("options"))
                if len(options_dict) == 0:
                    options_dict = None
            dbo.permissions.insert(changed_by, transaction=transaction, username=username, permission=permission, options=options_dict)
            return Response(status=201, response=json.dumps(dict(new_data_version=1)))
    except ValueError as e:
        log.warning("Bad input: %s", e.args)
        return problem(400, "Bad Request", str(e.args))


@requirelogin
def post_specific_user_permission(username, permission, changed_by, transaction):
    if not dbo.permissions.getUserPermissions(username, changed_by, transaction=transaction).get(permission):
        return problem(status=404, title="Not Found", detail="Requested user permission" " %s not found for %s" % (permission, username))
    try:
        # Existing Permission
        if not connexion.request.get_json().get("data_version"):
            return problem(400, "Bad Request", "'data_version' is missing from request body")
        options_dict = None
        if connexion.request.get_json().get("options"):
            options_dict = json.loads(connexion.request.get_json().get("options"))
            if len(options_dict) == 0:
                options_dict = None

        dbo.permissions.update(
            where={"username": username, "permission": permission},
            what={"options": options_dict},
            changed_by=changed_by,
            old_data_version=connexion.request.get_json().get("data_version"),
            transaction=transaction,
        )
        new_data_version = dbo.permissions.getPermission(username=username, permission=permission, transaction=transaction)["data_version"]
        return jsonify(new_data_version=new_data_version)
    except ValueError as e:
        log.warning("Bad input: %s", e.args)
        return problem(status=400, title="Bad Request", detail=str(e.args))


@requirelogin
def delete_specific_user_permission(username, permission, changed_by, transaction):
    if not dbo.permissions.getUserPermissions(username, changed_by, transaction=transaction).get(permission):
        return problem(404, "Not Found", "Requested user permission" " %s not found for %s" % (permission, username))
    try:
        # For practical purposes, DELETE can't have a request body, which means the Form
        # won't find data where it's expecting it. Instead, we have to tell it to look at
        # the query string, which Flask puts in request.args.

        old_data_version = int(connexion.request.args.get("data_version"))
        dbo.permissions.delete(
            where={"username": username, "permission": permission}, changed_by=changed_by, old_data_version=old_data_version, transaction=transaction
        )
        return Response(status=200)
    except ValueError as e:
        log.warning("Bad input: %s", e.args)
        return problem(400, "Bad Request", str(e.args))


class PermissionScheduledChangesView(ScheduledChangesView):
    """/scheduled_changes/permissions"""

    def __init__(self):
        super(PermissionScheduledChangesView, self).__init__("permissions", dbo.permissions)

    @requirelogin
    def _post(self, transaction, changed_by):
        if connexion.request.get_json().get("when", None) is None:
            return problem(400, "Bad Request", "'when' cannot be set to null when scheduling a new change " "for a Permission")
        change_type = connexion.request.get_json().get("change_type")

        what = connexion.request.get_json()
        if what.get("options", None):
            what["options"] = json.loads(what.get("options"))
            if len(what["options"]) == 0:
                what["options"] = None

        if change_type in ["update", "delete"]:
            if not what.get("data_version", None):
                return problem(400, "Bad Request", "Missing field", ext={"exception": "data_version is missing"})
            else:
                what["data_version"] = int(what["data_version"])

        return super(PermissionScheduledChangesView, self)._post(what, transaction, changed_by, change_type)


class PermissionScheduledChangeView(ScheduledChangeView):
    """/scheduled_changes/permissions/<int:sc_id>"""

    def __init__(self):
        super(PermissionScheduledChangeView, self).__init__("permissions", dbo.permissions)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        # TODO: modify UI and clients to stop sending 'change_type' in request body
        sc_permission = self.sc_table.select(where={"sc_id": sc_id}, transaction=transaction, columns=["change_type"])
        if sc_permission:
            change_type = sc_permission[0]["change_type"]
        else:
            return problem(404, "Not Found", "Unknown sc_id", ext={"exception": "No scheduled change for permission found for given sc_id"})

        # TODO: UI passes too many extra non-required fields apart from 'change_type' in request body
        # Only required fields must be passed to DB layer
        what = {}
        for field in connexion.request.get_json():
            # When editing an existing Scheduled Change for an for an existing Permission only options may be
            # provided. Because edits are identified by sc_id (in the URL), permission and username
            # are not required (nor allowed, because they are PK fields).
            # When editing an existing Scheduled Change for a new Permission, any field
            # may be changed.
            if (
                (change_type == "delete" and field not in ["when", "data_version"])
                or (change_type == "update" and field not in ["when", "options", "data_version"])
                or (change_type == "insert" and field not in ["when", "options", "permission", "username"])
            ):
                continue

            what[field] = connexion.request.get_json()[field]

        if change_type in ["update", "delete"] and not what.get("data_version", None):
            return problem(400, "Bad Request", "Missing field", ext={"exception": "data_version is missing"})

        if what.get("options", None):
            what["options"] = json.loads(what["options"])
            if len(what["options"]) == 0:
                what["options"] = None

        return super(PermissionScheduledChangeView, self)._post(sc_id, what, transaction, changed_by, connexion.request.get_json().get("sc_data_version"))

    @requirelogin
    def _delete(self, sc_id, transaction, changed_by):
        return super(PermissionScheduledChangeView, self)._delete(sc_id, transaction, changed_by)


class EnactPermissionScheduledChangeView(EnactScheduledChangeView):
    """/scheduled_changes/permissions/<int:sc_id>/enact"""

    def __init__(self):
        super(EnactPermissionScheduledChangeView, self).__init__("permissions", dbo.permissions)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(EnactPermissionScheduledChangeView, self)._post(sc_id, transaction, changed_by)


class PermissionScheduledChangeSignoffsView(SignoffsView):
    """/scheduled_changes/permissions/<int:sc_id>/signoffs"""

    def __init__(self):
        super(PermissionScheduledChangeSignoffsView, self).__init__("permissions", dbo.permissions)


class PermissionScheduledChangeHistoryView(ScheduledChangeHistoryView):
    """/scheduled_changes/permissions/<int:sc_id>/revisions"""

    def __init__(self):
        super(PermissionScheduledChangeHistoryView, self).__init__("permissions", dbo.permissions)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(PermissionScheduledChangeHistoryView, self)._post(sc_id, transaction, changed_by)


@requirelogin
@transactionHandler
def put_user_role(username, role, changed_by, transaction):
    """/users/:username/roles/:role"""

    # These requests are idempotent - if the user already has the desired role,
    # no change needs to be made. Because of this there's also no reason to
    # return an error.
    r = dbo.permissions.user_roles.select({"username": username, "role": role}, transaction=transaction)
    if r:
        return Response(status=200, response=json.dumps({"new_data_version": r[0]["data_version"]}))

    dbo.permissions.grantRole(username, role, changed_by, transaction)
    return Response(status=201, response=json.dumps({"new_data_version": 1}))


@requirelogin
@transactionHandler
def delete_user_role(username, role, data_version, changed_by, transaction):
    roles = [r["role"] for r in dbo.permissions.getUserRoles(username)]
    if role not in roles:
        return problem(404, "Not Found", "Role not found", ext={"exception": "No role '%s' found for " "username '%s'" % (role, username)})
    # query argument i.e. data_version  is also required.
    # All input value validations already defined in swagger specification and carried out by connexion
    dbo.permissions.revokeRole(username, role, changed_by=changed_by, old_data_version=data_version, transaction=transaction)
    return Response(status=200)
