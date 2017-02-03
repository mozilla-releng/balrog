import json
import time

from flask import request, Response
from flask.views import MethodView

from auslib.global_state import dbo
from auslib.util.timesince import timesince
from auslib.db import OutdatedDataError, PermissionDeniedError, UpdateMergeError, ChangeScheduledError, \
    SignoffRequiredError
import logging


def requirelogin(f):
    def decorated(*args, **kwargs):
        username = request.environ.get('REMOTE_USER', request.environ.get("HTTP_REMOTE_USER"))
        if not username:
            logging.warning("Login Required")
            return Response(status=401)
        return f(*args, changed_by=username, **kwargs)
    return decorated


def handleGeneralExceptions(messages):
    def wrap(f):
        def decorated(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except OutdatedDataError as e:
                msg = "Couldn't perform the request %s. Outdated Data Version. old_data_version doesn't match current data_version" % messages
                logging.warning("Bad input: %s", msg)
                logging.warning(e)
                return Response(status=400, response=json.dumps({"exception": msg}), mimetype="application/json")
            except UpdateMergeError as e:
                msg = "Couldn't perform the request %s due to merge error. Is there a scheduled change that conflicts with yours?" % messages
                logging.warning("Bad input: %s", msg)
                logging.warning(e)
                return Response(status=400, response=json.dumps({"exception": msg}), mimetype="application/json")
            except ChangeScheduledError as e:
                msg = "Couldn't perform the request %s due a conflict with a scheduled change. " % messages
                msg += e.message
                logging.warning("Bad input: %s", msg)
                logging.warning(e)
                return Response(status=400, response=json.dumps({"exception": msg}), mimetype="application/json")
            except SignoffRequiredError as e:
                msg = "This change requires signoff, it cannot be done directly."
                logging.warning(msg)
                logging.warning(e)
                return Response(status=400, response=json.dumps({"exception": msg}), mimetype="application/json")
            except PermissionDeniedError as e:
                msg = "Permission denied to perform the request. {}".format(e.message)
                logging.warning(msg)
                return Response(status=403, response=json.dumps({"exception": msg}), mimetype="application/json")
            except ValueError as e:
                msg = "Error. {}".format(e.message)
                logging.warning(msg)
                return Response(status=400, response=json.dumps({"exception": msg}), mimetype="application/json")
        return decorated
    return wrap


class AdminView(MethodView):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(self.__class__.__name__)
        MethodView.__init__(self, *args, **kwargs)

    @handleGeneralExceptions("POST")
    def post(self, *args, **kwargs):
        self.log.debug("processing POST request to %s" % request.path)
        with dbo.begin() as trans:
            return self._post(*args, transaction=trans, **kwargs)

    @handleGeneralExceptions("PUT")
    def put(self, *args, **kwargs):
        self.log.debug("processing PUT request to %s" % request.path)
        with dbo.begin() as trans:
            return self._put(*args, transaction=trans, **kwargs)

    @handleGeneralExceptions("DELETE")
    def delete(self, *args, **kwargs):
        self.log.debug("processing DELETE request to %s" % request.path)
        with dbo.begin() as trans:
            return self._delete(*args, transaction=trans, **kwargs)


class HistoryAdminView(AdminView):

    history_keys = ('timestamp', 'change_id', 'data_version', 'changed_by')

    def getAllRevisionKeys(self, revisions, primary_keys):
        try:
            all_keys = sorted([
                x for x in revisions[0].keys()
                if x not in self.history_keys and x not in primary_keys
            ])
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
                elif isinstance(value, dict):
                    try:
                        value = json.dumps(value, indent=2, sort_keys=True)
                    except ValueError:
                        pass
                elif isinstance(value, int):
                    value = unicode(str(value), 'utf8')
                elif not isinstance(value, basestring):
                    value = unicode(value, 'utf8')
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
