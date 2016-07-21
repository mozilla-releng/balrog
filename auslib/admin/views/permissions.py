import simplejson as json

from flask import request, Response, jsonify, make_response

from auslib.global_state import dbo
from auslib.admin.views.base import requirelogin, requirepermission, AdminView
from auslib.admin.views.forms import NewPermissionForm, ExistingPermissionForm

__all__ = ["UsersView", "PermissionsView", "SpecificPermissionView"]


def setpermission(f):
    def decorated(*args, **kwargs):
        if kwargs['permission'] not in ('admin', 'release', 'release_locale', 'release_read_only', 'rule', 'permission') \
           and not kwargs['permission'].startswith('/'):
            kwargs['permission'] = '/%s' % kwargs['permission']
        return f(*args, **kwargs)
    return decorated


def permission2selector(permission):
    """Converts a permission to a valid CSS selector."""
    return permission.replace('/', '').replace(':', '')


class UsersView(AdminView):
    """/users"""

    def get(self):
        users = dbo.permissions.getAllUsers()
        self.log.debug("Found users: %s", users)
        # We don't return a plain jsonify'ed list here because of:
        # http://flask.pocoo.org/docs/security/#json-security
        return jsonify(dict(users=users))


class PermissionsView(AdminView):
    """/users/:username/permissions"""

    def get(self, username):
        permissions = dbo.permissions.getUserPermissions(username)
        return jsonify(permissions)


class SpecificPermissionView(AdminView):
    """/users/:username/permissions/:permission"""
    @setpermission
    def get(self, username, permission):
        try:
            perm = dbo.permissions.getUserPermissions(username)[permission]
        except KeyError:
            return Response(status=404)
        return jsonify(perm)

    @setpermission
    @requirelogin
    @requirepermission('/users/:id/permissions/:permission', options=[])
    def _put(self, username, permission, changed_by, transaction):
        try:
            if dbo.permissions.getUserPermissions(username, transaction).get(permission):
                form = ExistingPermissionForm()
                if not form.validate():
                    self.log.warning("Bad input: %s", form.errors)
                    return Response(status=400, response=json.dumps(form.errors))
                dbo.permissions.updatePermission(changed_by, username, permission, form.data_version.data, form.options.data, transaction=transaction)
                new_data_version = dbo.permissions.getPermission(username=username, permission=permission, transaction=transaction)['data_version']
                return make_response(json.dumps(dict(new_data_version=new_data_version)), 200)
            else:
                form = NewPermissionForm()
                if not form.validate():
                    self.log.warning("Bad input: %s", form.errors)
                    return Response(status=400, response=json.dumps(form.errors))
                dbo.permissions.grantPermission(changed_by, username, permission, form.options.data, transaction=transaction)
                return make_response(json.dumps(dict(new_data_version=1)), 201)
        except ValueError as e:
            self.log.warning("Bad input: %s", e.args)
            return Response(status=400, response=e.args)

    @setpermission
    @requirelogin
    @requirepermission('/users/:id/permissions/:permission', options=[])
    def _post(self, username, permission, changed_by, transaction):
        if not dbo.permissions.getUserPermissions(username, transaction=transaction).get(permission):
            return Response(status=404)
        try:
            form = ExistingPermissionForm()
            if not form.validate():
                self.log.warning("Bad input: %s", form.errors)
                return Response(status=400, response=json.dumps(form.errors))
            dbo.permissions.updatePermission(changed_by, username, permission, form.data_version.data, form.options.data, transaction=transaction)
            new_data_version = dbo.permissions.getPermission(username=username, permission=permission, transaction=transaction)['data_version']
            return make_response(json.dumps(dict(new_data_version=new_data_version)), 200)
        except ValueError as e:
            self.log.warning("Bad input: %s", e.args)
            return Response(status=400, response=e.args)

    @setpermission
    @requirelogin
    @requirepermission('/users/:id/permissions/:permission', options=[])
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
            dbo.permissions.revokePermission(changed_by, username, permission, form.data_version.data, transaction=transaction)
            return Response(status=200)
        except ValueError as e:
            self.log.warning("Bad input: %s", e.args)
            return Response(status=400, response=e.args)
