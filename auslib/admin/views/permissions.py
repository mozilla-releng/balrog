import simplejson as json

from flask import render_template, request, Response, jsonify, make_response

from auslib.admin.base import db
from auslib.admin.views.base import requirelogin, requirepermission, AdminView
from auslib.admin.views.forms import NewPermissionForm, ExistingPermissionForm

__all__ = ["UsersView", "PermissionsView", "SpecificPermissionView", "PermissionsPageView", "UserPermissionsPageView"]

def setpermission(f):
    def decorated(*args, **kwargs):
        if kwargs['permission'] != 'admin' and not kwargs['permission'].startswith('/'):
            kwargs['permission'] = '/%s' % kwargs['permission']
        return f(*args, **kwargs)
    return decorated

def permission2selector(permission):
    """Converts a permission to a valid CSS selector."""
    return permission.replace('/', '').replace(':', '')

class UsersView(AdminView):
    """/users"""
    def get(self):
        users = db.permissions.getAllUsers()
        self.log.debug("Found users: %s", users)
        fmt = request.args.get('format', 'html')
        if fmt == 'json':
            # We don't return a plain jsonify'ed list here because of:
            # http://flask.pocoo.org/docs/security/#json-security
            return jsonify(dict(users=users))
        else:
            return render_template('fragments/users.html', users=users)

class PermissionsView(AdminView):
    """/users/[user]/permissions"""
    def get(self, username):
        permissions = db.permissions.getUserPermissions(username)
        fmt = request.args.get('format', 'html')
        if fmt == 'json':
            return jsonify(permissions)
        else:
            forms = []
            for perm, values in permissions.items():
                prefix = permission2selector(perm)
                forms.append(ExistingPermissionForm(prefix=prefix, permission=perm, options=values['options'], data_version=values['data_version']))
            return render_template('fragments/user_permissions.html', username=username, permissions=forms)

class SpecificPermissionView(AdminView):
    """/users/[user]/permissions/[permission]"""
    @setpermission
    def get(self, username, permission):
        try:
            perm = db.permissions.getUserPermissions(username)[permission]
        except KeyError:
            return Response(status=404)
        fmt = request.args.get('format', 'html')
        if fmt == 'json':
            return jsonify(perm)
        else:
            prefix = permission2selector(permission)
            form = ExistingPermissionForm(prefix=prefix, permission=permission, options=perm['options'], data_version=perm['data_version'])
            return render_template('fragments/permission_row.html', username=username, form=form)

    @setpermission
    @requirelogin
    @requirepermission('/users/:id/permissions/:permission', options=[])
    def _put(self, username, permission, changed_by, transaction):
        try:
            if db.permissions.getUserPermissions(username, transaction).get(permission):
                form = ExistingPermissionForm()
                if not form.data_version.data:
                    raise ValueError("Must provide the data version when updating an existing permission.")
                db.permissions.updatePermission(changed_by, username, permission, form.data_version.data, form.options.data, transaction=transaction)
                new_data_version = db.permissions.getPermission(username=username, permission=permission, transaction=transaction)['data_version']
                return make_response(json.dumps(dict(new_data_version=new_data_version)), 200)
            else:
                form = NewPermissionForm()
                db.permissions.grantPermission(changed_by, username, permission, form.options.data, transaction=transaction)
                return make_response(json.dumps(dict(new_data_version=1)), 201)
        except ValueError, e:
            return Response(status=400, response=e.args)

    @setpermission
    @requirelogin
    @requirepermission('/users/:id/permissions/:permission', options=[])
    def _post(self, username, permission, changed_by, transaction):
        if not db.permissions.getUserPermissions(username, transaction=transaction).get(permission):
            return Response(status=404)
        try:
            form = ExistingPermissionForm()
            db.permissions.updatePermission(changed_by, username, permission, form.data_version.data, form.options.data, transaction=transaction)
            new_data_version = db.permissions.getPermission(username=username, permission=permission, transaction=transaction)['data_version']
            return make_response(json.dumps(dict(new_data_version=new_data_version)), 200)
        except ValueError, e:
            return Response(status=400, response=e.args)

    @setpermission
    @requirelogin
    @requirepermission('/users/:id/permissions/:permission', options=[])
    def _delete(self, username, permission, changed_by, transaction):
        if not db.permissions.getUserPermissions(username, transaction=transaction).get(permission):
            return Response(status=404)
        try:
            # For practical purposes, DELETE can't have a request body, which means the Form
            # won't find data where it's expecting it. Instead, we have to tell it to look at
            # the query string, which Flask puts in request.args.
            form = ExistingPermissionForm(request.args)
            db.permissions.revokePermission(changed_by, username, permission, form.data_version.data, transaction=transaction)
            return Response(status=200)
        except ValueError, e:
            return Response(status=400, response=e.args)

class PermissionsPageView(AdminView):
    """/permissions.html"""
    def get(self):
        users = db.permissions.getAllUsers()
        return render_template('permissions.html', users=users)

class UserPermissionsPageView(AdminView):
    """/user_permissions.html"""
    def get(self):
        username = request.args.get('username')
        if not username:
            return Response(status=404)
        permissions = db.permissions.getUserPermissions(username)
        forms = []
        for perm, values in permissions.items():
            prefix = permission2selector(perm)
            forms.append(ExistingPermissionForm(prefix=prefix, permission=perm, options=values['options'], data_version=values['data_version']))
        return render_template('user_permissions.html', username=username, permissions=forms, newPermission=NewPermissionForm())
