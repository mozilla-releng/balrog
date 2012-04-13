from flask import request, Response
from flask.views import MethodView

from auslib.web.base import db

import logging
log = logging.getLogger(__name__)

def requirelogin(f):
    def decorated(*args, **kwargs):
        username = request.environ.get('REMOTE_USER')
        if not username:
            return Response(status=401)
        return f(*args, changed_by=username, **kwargs)
    return decorated

def requirepermission(url, options=['product']):
    def wrap(f):
        def decorated(*args, **kwargs):
            username = request.environ.get('REMOTE_USER')
            method = request.method
            extra = dict()
            for opt in options:
                if opt not in request.form:
                    return Response(status=400, response="Couldn't find required option %s in form" % opt)
                extra[opt] = request.form[opt]
            if not db.permissions.hasUrlPermission(username, url, method, urlOptions=extra):
                return Response(status=401,
                    response="%s is not allowed to access %s by %s" % (username, url, method))
            return f(*args, **kwargs)
        return decorated
    return wrap

class AdminView(MethodView):
    def post(self, *args, **kwargs):
        log.debug("AdminView.post: processing POST request to %s" % request.path)
        with db.begin() as trans:
            return self._post(*args, transaction=trans, **kwargs)
        log.debug("AdminView.post: finished processing POST request to %s" % request.path)

    def put(self, *args, **kwargs):
        log.debug("AdminView.post: processing PUT request to %s" % request.path)
        with db.begin() as trans:
            return self._put(*args, transaction=trans, **kwargs)
        log.debug("AdminView.post: finished processing PUT request to %s" % request.path)

    def delete(self, *args, **kwargs):
        log.debug("AdminView.post: processing DELETE request to %s" % request.path)
        with db.begin() as trans:
            return self._delete(*args, transaction=trans, **kwargs)
        log.debug("AdminView.post: finished processing DELETE request to %s" % request.path)
