import time

from flask import request, Response
from flask.views import MethodView

from auslib.admin.base import db
from auslib.util.timesince import timesince

import logging

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
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(self.__class__.__name__)
        MethodView.__init__(self, *args, **kwargs)

    def post(self, *args, **kwargs):
        self.log.debug("processing POST request to %s" % request.path)
        with db.begin() as trans:
            return self._post(*args, transaction=trans, **kwargs)

    def put(self, *args, **kwargs):
        self.log.debug("processing PUT request to %s" % request.path)
        with db.begin() as trans:
            return self._put(*args, transaction=trans, **kwargs)

    def delete(self, *args, **kwargs):
        self.log.debug("processing DELETE request to %s" % request.path)
        with db.begin() as trans:
            return self._delete(*args, transaction=trans, **kwargs)


class HistoryAdminView(AdminView):

    history_keys = ('timestamp', 'change_id', 'data_version', 'changed_by')

    def getAllRevisionKeys(self, revisions, primary_keys):
        try:
            all_keys = [
                x for x in revisions[0].keys()
                if x not in self.history_keys and x not in primary_keys
            ]
            all_keys.sort()
        except IndexError:
            all_keys = None
        return all_keys

    def annotateRevisionDifferences(self, revisions):
        _prev = {}
        for i, rev in enumerate(revisions):
            different = []
            for key, value in rev.items():
                if key in self.history_keys:
                    continue
                if key not in _prev:
                    _prev[key] = value
                else:
                    prev = _prev[key]
                    if prev != value:
                        different.append(key)
                # prep the value for being shown in revision_row.html
                if value is None:
                    value = 'NULL'
                elif not isinstance(value, basestring):
                    value = unicode(value)
                rev[key] = value

            rev['_different'] = different
            rev['_time_ago'] = getTimeAgo(rev['timestamp'])


def getTimeAgo(timestamp):
    # keeping this here amongst the view code because the use of the
    # timesince() function is specific to the view
    now, then = int(time.time()), int(timestamp / 1000.0)
    time_ago = timesince(
        then,
        now,
        afterword='ago',
        minute_granularity=True,
        max_no_sections=2
    )
    if not time_ago:
        time_ago = 'seconds ago'
    return time_ago
