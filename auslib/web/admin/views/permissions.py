import simplejson as json
import connexion
from flask import Response, jsonify
from auslib.web.admin.views.problem import problem
from auslib.global_state import dbo
from auslib.web.admin.views.base import requirelogin, AdminView
from auslib.web.admin.views.forms import ScheduledChangeNewPermissionForm, ScheduledChangeExistingPermissionForm, \
    EditScheduledChangeNewPermissionForm, EditScheduledChangeExistingPermissionForm, \
    ScheduledChangeDeletePermissionForm
from auslib.web.admin.views.scheduled_changes import ScheduledChangesView, \
    ScheduledChangeView, EnactScheduledChangeView, ScheduledChangeHistoryView,\
    SignoffsView

__all__ = ["UsersView", "PermissionsView", "SpecificPermissionView"]


class UsersView(AdminView):
    """/users"""

    def get(self):
        users = dbo.permissions.getAllUsers()
        self.log.debug("Found users: %s", users)
        # We don't return a plain jsonify'ed list here because of:
        # http://flask.pocoo.org/docs/security/#json-security
        return jsonify(dict(users=users))


class SpecificUserView(AdminView):
    """Returns all of the details about the logged in user. The UI needs this
    method to know things about the current user because it does not have
    access to REMOTE_USER, so it cannot query directly by name."""

    def get(self, username):
        current_user = connexion.request.environ.get('REMOTE_USER', connexion.request.environ.get("HTTP_REMOTE_USER"))
        if username == "current":
            username = current_user
        # If the user is retrieving permissions other than their own, we need
        # to make sure they have enough access to do so. If any user is able
        # to retrieve permissions of anyone, it may make privilege escalation
        # attacks easier.
        # TODO: do this at the database layer
        else:
            if username != current_user and not dbo.hasPermission(current_user, "permission", "view"):
                return problem(status=403, title="Forbidden",
                               detail="You are not authorized to view permissions of other users.")

        permissions = dbo.permissions.getUserPermissions(username)
        if not permissions:
            return problem(status=404, title="Not Found", detail="No permission found for username %s" % username)
        roles = {r["role"]: {"data_version": r["data_version"]} for r in dbo.permissions.getUserRoles(username)}
        return jsonify({"username": username, "permissions": permissions, "roles": roles})


class PermissionsView(AdminView):
    """/users/:username/permissions"""

    def get(self, username):
        permissions = dbo.permissions.getUserPermissions(username)
        return jsonify(permissions)


class SpecificPermissionView(AdminView):
    """/users/:username/permissions/:permission"""
    def get(self, username, permission):
        try:
            perm = dbo.permissions.getUserPermissions(username)[permission]
        except KeyError:
            return problem(404, "Not Found", "Requested user permission"
                                             " %s not found for %s" % (permission, username))
        return jsonify(perm)

    @requirelogin
    def _put(self, username, permission, changed_by, transaction):
        try:
            if dbo.permissions.getUserPermissions(username, transaction).get(permission):
                # Existing Permission
                if not connexion.request.json.get("data_version"):
                    return problem(400, "Bad Request", "'data_version' is missing from request body")

                options_dict = None
                if connexion.request.json.get("options"):
                    options_dict = json.loads(connexion.request.json.get("options"))

                dbo.permissions.update(where={"username": username, "permission": permission},
                                       what={"options": options_dict}, changed_by=changed_by,
                                       old_data_version=connexion.request.json.get("data_version"),
                                       transaction=transaction)
                new_data_version = dbo.permissions.getPermission(username=username, permission=permission,
                                                                 transaction=transaction)['data_version']
                return jsonify(new_data_version=new_data_version)
            else:
                # New Permission
                options_dict = None
                if connexion.request.json.get("options"):
                    options_dict = json.loads(connexion.request.json.get("options"))
                dbo.permissions.insert(changed_by, transaction=transaction, username=username, permission=permission,
                                       options=options_dict)
                return Response(status=201, response=json.dumps(dict(new_data_version=1)))
        except ValueError as e:
            self.log.warning("Bad input: %s", e.args)
            return problem(400, "Bad Request", str(e.args))

    @requirelogin
    def _post(self, username, permission, changed_by, transaction):
        if not dbo.permissions.getUserPermissions(username, transaction=transaction).get(permission):
            return problem(status=404, title="Not Found", detail="Requested user permission"
                                                                 " %s not found for %s" % (permission, username))
        try:
            # Existing Permission
            if not connexion.request.json.get("data_version"):
                return problem(400, "Bad Request", "'data_version' is missing from request body")
            options_dict = None
            if connexion.request.json.get("options"):
                options_dict = json.loads(connexion.request.json.get("options"))

            dbo.permissions.update(where={"username": username, "permission": permission},
                                   what={"options": options_dict}, changed_by=changed_by,
                                   old_data_version=connexion.request.json.get("data_version"),
                                   transaction=transaction)
            new_data_version = dbo.permissions.getPermission(username=username, permission=permission,
                                                             transaction=transaction)['data_version']
            return jsonify(new_data_version=new_data_version)
        except ValueError as e:
            self.log.warning("Bad input: %s", e.args)
            return problem(status=400, title="Bad Request", detail=str(e.args))

    @requirelogin
    def _delete(self, username, permission, changed_by, transaction):
        if not dbo.permissions.getUserPermissions(username, transaction=transaction).get(permission):
            return problem(404, "Not Found", "Requested user permission"
                                             " %s not found for %s" % (permission, username))
        try:
            # For practical purposes, DELETE can't have a request body, which means the Form
            # won't find data where it's expecting it. Instead, we have to tell it to look at
            # the query string, which Flask puts in request.args.

            old_data_version = int(connexion.request.args.get("data_version"))
            dbo.permissions.delete(where={"username": username, "permission": permission},
                                   changed_by=changed_by, old_data_version=old_data_version, transaction=transaction)
            return Response(status=200)
        except ValueError as e:
            self.log.warning("Bad input: %s", e.args)
            return problem(400, "Bad Request", str(e.args))


class PermissionScheduledChangesView(ScheduledChangesView):
    def __init__(self):
        super(PermissionScheduledChangesView, self).__init__("permissions", dbo.permissions)

    @requirelogin
    def _post(self, transaction, changed_by):
        change_type = connexion.request.json.get("change_type")

        if change_type == "update":
            form = ScheduledChangeExistingPermissionForm()
        elif change_type == "insert":
            form = ScheduledChangeNewPermissionForm()
        elif change_type == "delete":
            form = ScheduledChangeDeletePermissionForm()
        else:
            return Response(status=400, response="Invalid or missing change_type")

        return super(PermissionScheduledChangesView, self)._post(form, transaction, changed_by)


class PermissionScheduledChangeView(ScheduledChangeView):
    def __init__(self):
        super(PermissionScheduledChangeView, self).__init__("permissions", dbo.permissions)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        if connexion.request.json and connexion.request.json.get("data_version"):
            form = EditScheduledChangeExistingPermissionForm()
        else:
            form = EditScheduledChangeNewPermissionForm()

        return super(PermissionScheduledChangeView, self)._post(sc_id, form, transaction, changed_by)

    @requirelogin
    def _delete(self, sc_id, transaction, changed_by):
        return super(PermissionScheduledChangeView, self)._delete(sc_id, transaction, changed_by)


class EnactPermissionScheduledChangeView(EnactScheduledChangeView):
    def __init__(self):
        super(EnactPermissionScheduledChangeView, self).__init__("permissions", dbo.permissions)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(EnactPermissionScheduledChangeView, self)._post(sc_id, transaction, changed_by)


class PermissionScheduledChangeSignoffsView(SignoffsView):
    def __init__(self):
        super(PermissionScheduledChangeSignoffsView, self).__init__("permissions", dbo.permissions)


class PermissionScheduledChangeHistoryView(ScheduledChangeHistoryView):
    def __init__(self):
        super(PermissionScheduledChangeHistoryView, self).__init__("permissions", dbo.permissions)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(PermissionScheduledChangeHistoryView, self)._post(sc_id, transaction, changed_by)


class UserRolesView(AdminView):
    """/users/:username/roles"""

    def get(self, username):
        roles = dbo.permissions.getUserRoles(username)
        return jsonify({"roles": roles})


class AllRolesView(AdminView):
    """/users/roles"""

    def get(self):
        roles = dbo.permissions.getAllRoles()
        return jsonify({"roles": roles})


class UserRoleView(AdminView):
    """/users/:username/roles/:role"""

    @requirelogin
    def _put(self, username, role, changed_by, transaction):
        # These requests are idempotent - if the user already has the desired role,
        # no change needs to be made. Because of this there's also no reason to
        # return an error.
        r = dbo.permissions.user_roles.select({"username": username, "role": role}, transaction=transaction)
        if r:
            return Response(status=200, response=json.dumps({"new_data_version": r[0]["data_version"]}))

        dbo.permissions.grantRole(username, role, changed_by, transaction)
        return Response(status=201, response=json.dumps({"new_data_version": 1}))

    @requirelogin
    def _delete(self, username, role, changed_by, transaction):
        roles = [r['role'] for r in dbo.permissions.getUserRoles(username)]
        if role not in roles:
            return problem(404, "Not Found", "Role not found", ext={"exception": "No role '%s' found for "
                                                                                 "username '%s'" % (role, username)})
        # query argument i.e. data_version  is also required.
        # All input value validations already defined in swagger specification and carried out by connexion.
        old_data_version = int(connexion.request.args.get("data_version"))
        dbo.permissions.revokeRole(username, role, changed_by=changed_by,
                                   old_data_version=old_data_version, transaction=transaction)
        return Response(status=200)
