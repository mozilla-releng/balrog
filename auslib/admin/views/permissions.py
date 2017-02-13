import simplejson as json

from flask import request, Response, jsonify

from auslib.global_state import dbo
from auslib.admin.views.base import requirelogin, AdminView
from auslib.admin.views.forms import NewPermissionForm, ExistingPermissionForm, DbEditableForm, \
    ScheduledChangeNewPermissionForm, ScheduledChangeExistingPermissionForm, \
    EditScheduledChangeNewPermissionForm, EditScheduledChangeExistingPermissionForm, \
    ScheduledChangeDeletePermissionForm
from auslib.admin.views.scheduled_changes import ScheduledChangesView, \
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


class CurrentUserView(AdminView):
    """Returns all of the details about the logged in user. The UI needs this
    method to know things about the current user because it does not have
    access to REMOTE_USER, so it cannot query directly by name."""

    def get(self, username):
        if username == "current":
            username = request.environ.get('REMOTE_USER', request.environ.get("HTTP_REMOTE_USER"))
        permissions = dbo.permissions.getUserPermissions(username)
        if not permissions:
            return Response(status=404)
        roles = {}
        for r in dbo.permissions.getUserRoles(username):
            roles[r["role"]] = {"data_version": r["data_version"]}
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
            return Response(status=404)
        return jsonify(perm)

    @requirelogin
    def _put(self, username, permission, changed_by, transaction):
        try:
            if dbo.permissions.getUserPermissions(username, transaction).get(permission):
                form = ExistingPermissionForm()
                if not form.validate():
                    self.log.warning("Bad input: %s", form.errors)
                    return Response(status=400, response=json.dumps(form.errors))
                dbo.permissions.update(where={"username": username, "permission": permission}, what={"options": form.options.data},
                                       changed_by=changed_by, old_data_version=form.data_version.data, transaction=transaction)
                new_data_version = dbo.permissions.getPermission(username=username, permission=permission, transaction=transaction)['data_version']
                return jsonify(new_data_version=new_data_version)
            else:
                form = NewPermissionForm()
                if not form.validate():
                    self.log.warning("Bad input: %s", form.errors)
                    return Response(status=400, response=json.dumps(form.errors))
                dbo.permissions.insert(changed_by, transaction=transaction, username=username, permission=permission, options=form.options.data)
                return Response(status=201, response=json.dumps(dict(new_data_version=1)))
        except ValueError as e:
            self.log.warning("Bad input: %s", e.args)
            return Response(status=400, response=e.args)

    @requirelogin
    def _post(self, username, permission, changed_by, transaction):
        if not dbo.permissions.getUserPermissions(username, transaction=transaction).get(permission):
            return Response(status=404)
        try:
            form = ExistingPermissionForm()
            if not form.validate():
                self.log.warning("Bad input: %s", form.errors)
                return Response(status=400, response=json.dumps(form.errors))
            dbo.permissions.update(where={"username": username, "permission": permission}, what={"options": form.options.data},
                                   changed_by=changed_by, old_data_version=form.data_version.data, transaction=transaction)
            new_data_version = dbo.permissions.getPermission(username=username, permission=permission, transaction=transaction)['data_version']
            return jsonify(new_data_version=new_data_version)
        except ValueError as e:
            self.log.warning("Bad input: %s", e.args)
            return Response(status=400, response=e.args)

    @requirelogin
    def _delete(self, username, permission, changed_by, transaction):
        if not dbo.permissions.getUserPermissions(username, transaction=transaction).get(permission):
            return Response(status=404)
        try:
            # For practical purposes, DELETE can't have a request body, which means the Form
            # won't find data where it's expecting it. Instead, we have to tell it to look at
            # the query string, which Flask puts in request.args.
            form = ExistingPermissionForm(request.args)
            if not form.validate():
                self.log.warning("Bad input: %s", form.errors)
                return Response(status=400, response=json.dumps(form.errors))
            dbo.permissions.delete(where={"username": username, "permission": permission}, changed_by=changed_by,
                                   old_data_version=form.data_version.data, transaction=transaction)
            return Response(status=200)
        except ValueError as e:
            self.log.warning("Bad input: %s", e.args)
            return Response(status=400, response=e.args)


class PermissionScheduledChangesView(ScheduledChangesView):
    def __init__(self):
        super(PermissionScheduledChangesView, self).__init__("permissions", dbo.permissions)

    @requirelogin
    def _post(self, transaction, changed_by):
        change_type = request.json.get("change_type")

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
        if request.json and request.json.get("data_version"):
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

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(PermissionScheduledChangeSignoffsView, self)._post(sc_id, transaction, changed_by)

    @requirelogin
    def _delete(self, sc_id, transaction, changed_by):
        return super(PermissionScheduledChangeSignoffsView, self)._delete(sc_id, transaction, changed_by)


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
            return Response(status=404)

        form = DbEditableForm(request.args)
        if not form.validate():
            self.log.warning("Bad input: %s", form.errors)
            return Response(status=400, response=json.dumps(form.errors))

        dbo.permissions.revokeRole(username, role, changed_by=changed_by, old_data_version=form.data_version.data, transaction=transaction)
        return Response(status=200)
