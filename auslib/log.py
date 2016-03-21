from logging import Logger

from flask import request

import cef

log_format = "%(asctime)s - %(levelname)s - PID: %(process)s - Request: %(requestid)s - %(name)s.%(funcName)s#%(lineno)s: %(message)s"

# Needs to be set by entry points.
cef_config = {}


class BalrogLogger(Logger):

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None):
        if extra is None:
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


# Standard CEF levels at Mozilla. More details here:
# https://mana.mozilla.org/wiki/display/SECURITY/CEF+Guidelines+for+Application+Development+at+Mozilla#CEFGuidelinesforApplicationDevelopmentatMozilla-apxaAppendixA-%C2%A0Severity%C2%A0IntegersSuggestions
CEF_INFO = 4
CEF_WARN = 6
CEF_ALERT = 8
CEF_EMERG = 10


def cef_event(name, severity, **custom_exts):
    # Extra values need to be in the format csNLabel=xxx, csN=yyy
    extra_exts = {}
    n = 2
    for k, v in custom_exts.iteritems():
        valueKey = 'cs%d' % n
        labelKey = '%sLabel' % valueKey
        extra_exts[labelKey] = k
        extra_exts[valueKey] = v
        n += 1

    username = request.environ.get('REMOTE_USER', 'Unknown User')
    cef.log_cef(name, severity, request.environ, cef_config, username=username, **extra_exts)


def get_cef_config(logfile):
    return {
        'cef.file': logfile,
        'cef.version': 0,  # This is the CEF format version
        'cef.product': 'Balrog',
        'cef.vendor': 'Mozilla',
        'cef.device_version': '1.0',
    }
