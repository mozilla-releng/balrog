import json

from flask import request, Response
from flask.views import MethodView

from auslib.global_state import dbo
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
                msg = "Bad input: {}".format(e.message)
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
