from flask import request, Response
from flask.views import MethodView
from auslib.global_state import dbo
from auslib.web.admin.views.problem import problem
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
                msg = "Couldn't perform the request %s. Outdated Data Version. " \
                      "old_data_version doesn't match current data_version" % messages
                logging.warning("Bad input: %s", msg)
                logging.warning(e)
                # using connexion.problem results in TypeError: 'ConnexionResponse' object is not callable
                # hence using flask.Response but modifying response's json data into connexion.problem format
                # for validation purpose
                return problem(400, "Bad Request", "OutdatedDataError", ext={"exception": msg})
            except UpdateMergeError as e:
                msg = "Couldn't perform the request %s due to merge error. " \
                      "Is there a scheduled change that conflicts with yours?" % messages
                logging.warning("Bad input: %s", msg)
                logging.warning(e)
                return problem(400, "Bad Request", "UpdateMergeError", ext={"exception": msg})
            except ChangeScheduledError as e:
                msg = "Couldn't perform the request %s due a conflict with a scheduled change. " % messages
                msg += e.message
                logging.warning("Bad input: %s", msg)
                logging.warning(e)
                return problem(400, "Bad Request", "ChangeScheduledError", ext={"exception": msg})
            except SignoffRequiredError as e:
                msg = "This change requires signoff, it cannot be done directly. {}".format(e.message)
                logging.warning(msg)
                logging.warning(e)
                return problem(400, "Bad Request", "SignoffRequiredError", ext={"exception": msg})
            except PermissionDeniedError as e:
                msg = "Permission denied to perform the request. {}".format(e.message)
                logging.warning(msg)
                return problem(403, "Forbidden", "PermissionDeniedError", ext={"exception": msg})
            except ValueError as e:
                msg = "Bad input: {}".format(e.message)
                logging.warning(msg)
                return problem(400, "Bad Request", "ValueError", ext={"exception": msg})
        return decorated
    return wrap


def transactionHandler(request_handler):
    def decorated(*args, **kwargs):
        trans = dbo.begin()
        # Transactions are automatically rolled back by the context manager if
        # _post raises an Exception, but we need to make sure they are also
        # rolled back if the View returns any sort of error.
        try:
            ret = request_handler(*args, transaction=trans, **kwargs)
            if ret.status_code >= 400:
                trans.rollback()
            else:
                trans.commit()
            return ret
        except:
            trans.rollback()
            raise
        finally:
            trans.close()

    return decorated


class AdminView(MethodView):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(self.__class__.__name__)
        MethodView.__init__(self, *args, **kwargs)

    @transactionHandler
    @handleGeneralExceptions("POST")
    def post(self, *args, **kwargs):
        self.log.debug("processing POST request to %s" % request.path)
        return self._post(*args, **kwargs)

    @transactionHandler
    @handleGeneralExceptions("PUT")
    def put(self, *args, **kwargs):
        self.log.debug("processing PUT request to %s" % request.path)
        return self._put(*args, **kwargs)

    @transactionHandler
    @handleGeneralExceptions("DELETE")
    def delete(self, *args, **kwargs):
        self.log.debug("processing DELETE request to %s" % request.path)
        return self._delete(*args, **kwargs)


def serialize_signoff_requirements(requirements):
    dct = {}
    for rs in requirements:
        signoffs_required = max(dct.get(rs["role"], 0), rs["signoffs_required"])
        dct[rs["role"]] = signoffs_required

    return dct
