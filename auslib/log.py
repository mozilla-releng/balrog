from logging import Logger

from flask import request

log_format = "%(asctime)s - PID: %(process)s - Request: %(requestid)s - %(name)s.%(funcName)s#%(lineno)s: %(message)s"

class BalrogLogger(Logger):
    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None):
        if extra == None:
            extra = {}
        if 'requestid' not in extra:
            # Not all logging will be done from within a request
            # (eg, initial logging at start up). We need to be able to cope
            # with that.
            requestid = 'None'
            try:
                # "request" is a proxy object that passes along operations
                # to the real object. _get_current_object gives us the true
                # Request object, whose id is actually what we want.
                # Without this we end up with the id of the proxy object, which
                # is static for the life of the application.
                requestid = id(request._get_current_object())
            # RuntimeError will be raised if there's no active request.
            except RuntimeError:
                pass
            extra['requestid'] = requestid
        return Logger.makeRecord(self, name, level, fn, lno, msg, args, exc_info, func, extra)
