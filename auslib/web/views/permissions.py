import simplejson as json

from flask import render_template, request, Response, jsonify, make_response

from auslib.web.base import app, db
from auslib.web.views.base import requirelogin, requirepermission, AdminView
from auslib.web.views.forms import NewPermissionForm, ExistingPermissionForm

import logging
log = logging.getLogger(__name__)

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
        log.debug("UsersView.get: Found users: %s", users)
        fmt = request.args.get('format', 'html')
        log.debug("UsersView.get: format is '%s'", fmt)
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
        log.debug("PermissionsView.get: format is '%s':", fmt)
        if fmt == 'json':
            return jsonify(permissions)
        else:
            forms = []
            for perm, values in permissions.items():
                prefix = permission2selector(perm)
                forms.append(ExistingPermissionForm(prefix=prefix, permission=perm, options=values['options'], data_version=values['data_version']))
            return render_template('fragments/user_permissions.html', username=username, permissions=permissions)

class SpecificPermissionView(AdminView):
    """/users/[user]/permissions/[permission]"""
    @setpermission
    def get(self, username, permission):
        try:
            perm = db.permissions.getUserPermissions(username)[permission]
        except KeyError:
            return Response(status=404)
        fmt = request.args.get('format', 'html')
        log.debug("SpecificPermissionsView.get: format is '%s':", fmt)
        if fmt == 'json':
            return jsonify(perm)
        else:
            prefix = permission2selector(permission)
            form = ExistingPermissionForm(prefix=prefix, permission=permission, options=perm['options'], data_version=perm['data_version'])
            return render_template('fragments/permission.html', username=username, form=form)

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
        except Exception, e:
            return Response(status=500, response=e.args)

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
        except Exception, e:
            return Response(status=500, response=e.args)

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
            raise
            return Response(status=400, response=e.args)
        except Exception, e:
            raise
            return Response(status=500, response=e.args)

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

app.add_url_rule('/users', view_func=UsersView.as_view('users'))
app.add_url_rule('/users/<username>/permissions', view_func=PermissionsView.as_view('permissions'))
app.add_url_rule('/users/<username>/permissions/<path:permission>', view_func=SpecificPermissionView.as_view('specific_permission'))
# Some permissions may start with a slash, and the <path> converter won't match them, so we need an extra rule to cope.
app.add_url_rule('/users/<username>/permissions//<path:permission>', view_func=SpecificPermissionView.as_view('specific_permission'))
app.add_url_rule('/permissions.html', view_func=PermissionsPageView.as_view('permissions.html'))
app.add_url_rule('/user_permissions.html', view_func=UserPermissionsPageView.as_view('user_permissions.html'))
