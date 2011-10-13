import simplejson as json

from flask import render_template, request, Response, jsonify
from flask.views import MethodView

from auslib.web.base import app, db
from auslib.web.views.base import requirelogin

def setpermission(f):
    def decorated(*args, **kwargs):
        if kwargs['permission'] != 'admin' and not kwargs['permission'].startswith('/'):
            kwargs['permission'] = '/%s' % kwargs['permission']
        return f(*args, **kwargs)
    return decorated
        
class UsersView(MethodView):
    """/users"""
    def get(self):
        users = db.permissions.getAllUsers()
        # We don't return a plain jsonify'ed list here because of:
        # http://flask.pocoo.org/docs/security/#json-security
        return jsonify(dict(users=users))

class PermissionsView(MethodView):
    """/users/[user]/permissions"""
    def get(self, username):
        permissions = db.permissions.getUserPermissions(username)
        return jsonify(permissions)

class SpecificPermissionView(MethodView):
    """/users/[user]/permissions/[permission]"""
    def _getOptions(self):
            if 'options' in request.form and request.form['options']:
                return json.loads(request.form['options'])
            else:
                return None

    def get(self, username, permission):
        return jsonify(db.permissions.getUserPermissions(username)[permission])

    @setpermission
    @requirelogin
    def put(self, username, permission, changed_by):
        try:
            options = self._getOptions()
            if db.permissions.getUserPermissions(username).get(permission):
                # Raises ValueError if it can't convert the data, which (properly)
                # causes us to return 400 below.
                data_version = int(request.form['data_version'])
                db.permissions.updatePermission(changed_by, username, permission, data_version, options)
                return Response(status=200)
            else:
                db.permissions.grantPermission(changed_by, username, permission, options)
                return Response(status=201)
        except ValueError, e:
            return Response(status=400, response=e.message)
        except Exception, e:
            return Response(status=500, response=e.message)

    @setpermission
    @requirelogin
    def post(self, username, permission, changed_by):
        if not db.permissions.getUserPermissions(username).get(permission):
            return Response(status=404)
        try:
            options = self._getOptions()
            data_version = int(request.form['data_version'])
            db.permissions.updatePermission(changed_by, username, permission, data_version, options)
            return Response(status=200)
        except ValueError, e:
            import sys
            return Response(status=400, response=e.message)
        except Exception, e:
            return Response(status=500, response=e.message)

    @setpermission
    @requirelogin
    def delete(self, username, permission, changed_by):
        if not db.permissions.getUserPermissions(username).get(permission):
            return Response(status=404)
        try:
            data_version = int(request.args['data_version'])
            db.permissions.revokePermission(changed_by, username, permission, data_version)
            return Response(status=200)
        except ValueError, e:
            return Response(status=400, response=e.message)
        except Exception, e:
            return Response(status=500, response=e.message)

class PermissionsPageView(MethodView):
    """/permissions.html"""
    def get(self):
        users = db.permissions.getAllUsers()
        return render_template('permissions.html', users=users)

class UserPermissionsPageView(MethodView):
    """/user_permissions.html"""
    def get(self):
        username = request.args.get('username')
        permissions = db.permissions.getUserPermissions(username)
        if not username:
            return Response(status=404)
        return render_template('user_permissions.html', username=username, permissions=permissions)

app.add_url_rule('/users', view_func=UsersView.as_view('users'))
app.add_url_rule('/users/<username>/permissions', view_func=PermissionsView.as_view('permissions'))
app.add_url_rule('/users/<username>/permissions/<path:permission>', view_func=SpecificPermissionView.as_view('specific_permission'))
app.add_url_rule('/permissions.html', view_func=PermissionsPageView.as_view('permissions.html'))
app.add_url_rule('/user_permissions.html', view_func=UserPermissionsPageView.as_view('user_permissions.html'))
