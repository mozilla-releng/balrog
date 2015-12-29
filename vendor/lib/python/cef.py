# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Sync Server
#
# The Initial Developer of the Original Code is the Mozilla Foundation.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Tarek Ziade (tarek@mozilla.com)
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****
import sys
import threading
try:
    import syslog
    _SYSLOG_OPTIONS = {'PID': syslog.LOG_PID,
                       'CONS': syslog.LOG_CONS,
                       'NDELAY': syslog.LOG_NDELAY,
                       'NOWAIT': syslog.LOG_NOWAIT}

    # LOG_PERROR is undefined on some platforms, e.g. solaris
    if hasattr(syslog, 'LOG_PERROR'):
        _SYSLOG_OPTIONS['PERROR'] = syslog.LOG_PERROR

    _SYSLOG_PRIORITY = {'EMERG': syslog.LOG_EMERG,
                        'ALERT': syslog.LOG_ALERT,
                        'CRIT': syslog.LOG_CRIT,
                        'ERR': syslog.LOG_ERR,
                        'WARNING': syslog.LOG_WARNING,
                        'NOTICE': syslog.LOG_NOTICE,
                        'INFO': syslog.LOG_INFO,
                        'DEBUG': syslog.LOG_DEBUG}

    _SYSLOG_FACILITY = {'KERN': syslog.LOG_KERN,
                        'USER': syslog.LOG_USER,
                        'MAIL': syslog.LOG_MAIL,
                        'DAEMON': syslog.LOG_DAEMON,
                        'AUTH': syslog.LOG_AUTH,
                        'LPR': syslog.LOG_LPR,
                        'NEWS': syslog.LOG_NEWS,
                        'UUCP': syslog.LOG_UUCP,
                        'CRON': syslog.LOG_CRON,
                        'LOCAL0': syslog.LOG_LOCAL0,
                        'LOCAL1': syslog.LOG_LOCAL1,
                        'LOCAL2': syslog.LOG_LOCAL2,
                        'LOCAL3': syslog.LOG_LOCAL3,
                        'LOCAL4': syslog.LOG_LOCAL4,
                        'LOCAL5': syslog.LOG_LOCAL5,
                        'LOCAL6': syslog.LOG_LOCAL6,
                        'LOCAL7': syslog.LOG_LOCAL7}
    SYSLOG = True
except ImportError:
    _SYSLOG_OPTIONS = _SYSLOG_PRIORITY = _SYSLOG_FACILITY = None
    SYSLOG = False

import logging
import socket
from time import strftime
import re
try:
    from services import logger
except ImportError:
    logger = logging.getLogger('CEF')  # NOQA

_HOST = socket.gethostname()
_MAXLEN = 1024

# pre-defined signatures
AUTH_FAILURE = 'AuthFail'
CAPTCHA_FAILURE = 'CaptchaFail'
OVERRIDE_FAILURE = 'InvalidAdmin'
ACCOUNT_LOCKED = 'AccountLockout'
PASSWD_RESET_CLR = 'PasswordResetCleared'

_CEF_FORMAT = ('%(date)s %(host)s CEF:%(version)s|%(vendor)s|%(product)s|'
               '%(device_version)s|%(signature)s|%(name)s|%(severity)s|'
               'cs1Label=requestClientApplication cs1=%(user_agent)s '
               'requestMethod=%(method)s request=%(url)s '
               'src=%(source)s dhost=%(dest)s suser=%(suser)s')

_EXTENSIONS = ['cs1Label', 'cs1', 'requestMethod', 'request', 'src', 'dhost',
               'suser']
_PREFIX = re.compile(r'([|\\\r\n])')
_EXTENSION = re.compile(r'([\\=])')
_KEY = re.compile(r'^[a-zA-Z0-9_\-.]+$')


def _get_source_ip(environ):
    """Extracts the source IP from the environ."""
    if 'HTTP_X_FORWARDED_FOR' in environ:
        return environ['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
    elif 'REMOTE_ADDR' in environ:
        return environ['REMOTE_ADDR']
    return None


def _to_str(data):
    """Converts to str, encoding unicode strings with utf8"""
    if isinstance(data, unicode):
        return data.encode('utf8')
    return str(data)


def _convert_prefix(data):
    """Escapes | and = and convert to utf8 string"""
    data = _to_str(data)
    return _PREFIX.sub(r'\\\1', data)


def _convert_ext(data):
    """Escapes | and = and convert to utf8 string"""
    data = _to_str(data)
    return _EXTENSION.sub(r'\\\1', data)


_LOG_OPENED = None

# will make log writing atomic per-process
# unfortunately this will not work when several process uses it
# so lines might get mixed on high loads.
# we would need a dedicated per-server log service for this
# to serialize all logs
_log_lock = threading.RLock()


def _syslog(msg, config):
    """Opens the log with configured options and logs."""
    logopt = _str2logopt(config.get('syslog_options'))
    facility = _str2facility(config.get('syslog_facility'))
    ident = config.get('syslog_ident', sys.argv[0])
    priority = _str2priority(config.get('syslog.priority'))
    with _log_lock:
        global _LOG_OPENED
        if _LOG_OPENED != (ident, logopt, facility):
            syslog.openlog(ident, logopt, facility)
            _LOG_OPENED = ident, logopt, facility
        if isinstance(msg, unicode):
            msg = msg.encode('utf-8')
        syslog.syslog(priority, msg)


def _str2logopt(value):
    if value is None:
        return 0
    res = 0
    for option in value.split(','):
        res = res | _SYSLOG_OPTIONS[option.strip()]
    return res


def _str2priority(value):
    if value is None:
        return syslog.LOG_INFO
    return _SYSLOG_PRIORITY[value.strip()]


def _str2facility(value):
    if value is None:
        return syslog.LOG_LOCAL4
    return _SYSLOG_FACILITY[value.strip()]


def _check_key(key):
    if _KEY.match(key) is not None:
        return key
    msg = 'The "%s" key contains illegal characters' % key
    logger.warning(msg)

    # replacing illegal characters with a '?'
    return _KEY.sub('?', key)


def _filter_params(namespace, data, replace_dot='_', splitchar='.'):
    """Keeps only params that starts with the namespace.
    """
    params = {}
    for key, value in data.items():
        if splitchar not in key:
            continue
        skey = key.split(splitchar)
        if skey[0] != namespace:
            continue
        params[replace_dot.join(skey[1:])] = _to_str(value)
    return params


def _get_fields(name, severity, environ, config, username=None,
               signature=None, **kw):
    name = _convert_prefix(name)
    if signature is None:
        signature = name
    else:
        signature = _convert_prefix(signature)

    severity = _convert_prefix(severity)
    source = _get_source_ip(environ)

    fields = {'severity': severity,
              'source': source,
              'method': _convert_ext(environ.get('REQUEST_METHOD', '')),
              'url': _convert_ext(environ.get('PATH_INFO', '')),
              'dest': _convert_ext(environ.get('HTTP_HOST', u'none')),
              'user_agent': _convert_ext(environ.get('HTTP_USER_AGENT',
                                                     u'none')),
              'signature': signature,
              'name': name,
              'version': config['version'],
              'vendor': config['vendor'],
              'device_version': config['device_version'],
              'product': config['product'],
              'host': _to_str(_HOST),
              'suser': _to_str(username),
              'date': strftime("%b %d %H:%M:%S")}

    # make sure we don't have a | anymore in regular fields
    for key, value in list(kw.items()):
        new_key = _check_key(key)
        if new_key == key:
            continue
        kw[new_key] = _to_str(value)
        del kw[key]

    # overriding with provided datas
    fields.update(kw)
    return fields


def _len(data):
    if isinstance(data, str):
        return len(data)
    elif isinstance(data, unicode):
        return len(data.encode('utf8'))
    return len(str(data))


def _format_msg(fields, kw, maxlen=_MAXLEN):
    # adding custom extensions
    # sorting by size
    msg = _CEF_FORMAT % fields

    extensions = [(_len(value), len(key), key, value)
                    for key, value in kw.items()
                  if key not in _EXTENSIONS]
    extensions.sort()

    msg_len = len(msg)

    for value_len, key_len, key, value in extensions:
        added_len = value_len + key_len + 2
        value = _convert_ext(value)
        key = _check_key(key)

        if maxlen and msg_len + added_len > maxlen:
            # msg is too big.
            warn = 'CEF Message too big. %s %s' % (msg, str(kw.items()))
            logger.warning(warn)
            break

        msg += ' %s=%s' % (key, value)
        msg_len += added_len

    return msg


def log_cef(name, severity, environ, config, username='none',
            signature=None, **kw):
    """Creates a CEF record, and emit it in syslog or another file.

    Args:
        - name: name to log
        - severity: integer from 0 to 10
        - environ: the WSGI environ object
        - config: configuration dict
        - signature: CEF signature code - defaults to name value
        - username: user name - defaults to 'none'
        - extra keywords: extra keys used in the CEF extension
    """
    config = _filter_params('cef', config)
    fields = _get_fields(name, severity, environ, config, username=username,
                        signature=signature, **kw)
    msg = _format_msg(fields, kw)

    if config['file'] == 'syslog':
        if not SYSLOG:
            raise ValueError('syslog not supported on this platform')
        _syslog(msg, config)
    else:
        with _log_lock:
            with open(config['file'], 'a') as f:
                f.write('%s\n' % msg)


LEVEL_MAP = {
    logging.DEBUG: syslog.LOG_DEBUG,
    logging.WARNING: syslog.LOG_WARNING,
    logging.INFO: syslog.LOG_INFO,
    logging.ERROR: syslog.LOG_ERR,
    logging.CRITICAL: syslog.LOG_CRIT,
}


class _Formatter(logging.Formatter):
    def format(self, record):
        kw = record.args
        fields = _get_fields(record.msg, kw['severity'], kw['environ'],
                             {'version': kw.get('version', 0),
                              'vendor': kw.get('vendor', 'Mozilla'),
                              'device_version': kw.get('device_version', '1'),
                              'product': kw.get('product', 'Mozilla')},
                             username=kw.get('username'),
                             signature=kw.get('signature'))

        datefmt = getattr(self, 'datefmt', None)
        if not datefmt:
            datefmt = '%H:%M:%s'
        fields['date'] = strftime(datefmt)
        return _format_msg(fields, kw['data'], maxlen=kw.get('maxlen'))


class SysLogFormatter(_Formatter):
    def format(self, record):
        record.args['severity'] = LEVEL_MAP[record.levelno]
        return _Formatter.format(self, record)
