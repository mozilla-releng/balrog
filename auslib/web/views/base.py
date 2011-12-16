from flask import request, Response

from auslib.web.base import db

def requirelogin(f):
    def decorated(*args, **kwargs):
        username = request.environ.get('REMOTE_USER')
        if not username:
            return Response(status=401)
        return f(*args, changed_by=username, **kwargs)
    return decorated

def requirepermission(options=['product']):
    def wrap(f):
        def decorated(*args, **kwargs):
            try:
                username = request.environ.get('REMOTE_USER')
                url = request.path
                method = request.method
                extra = dict()
                for opt in options:
                    extra[opt] = request.form[opt]
                if not db.permissions.hasUrlPermission(username, url, method, urlOptions=extra):
                    return Response(status=401,
                        response="%s is not allowed to access %s by %s" % (username, url, method))
                return f(*args, **kwargs)
            except KeyError:
                return Response(status=400, response="Couldn't find 'product' in form")
        return decorated
    return wrap
