import json
import logging
import socket
import sys
import traceback

from flask import request

log_format = "%(asctime)s - %(levelname)s - PID: %(process)s - Request: %(requestid)s - %(name)s.%(funcName)s#%(lineno)s: %(message)s"


class BalrogLogger(logging.Logger):
    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        if extra is None:
            extra = {}
        if "requestid" not in extra:
            # Not all logging will be done from within a request
            # (eg, initial logging at start up). We need to be able to cope
            # with that.
            requestid = "None"
            try:
                # "request" is a proxy object that passes along operations
                # to the real object. _get_current_object gives us the true
                # Request object, whose id is actually what we want.
                # Without this we end up with the id of the proxy object, which
                # is static for the life of the application.
                # TODO: this doesn't seem to be 100% unique.
                # Sometimes requests that happen around the same time will
                # end up with the same value here. Possibly only when the
                # query strings are the same, or srcip?
                requestid = str(id(request._get_current_object()))
            # RuntimeError will be raised if there's no active request.
            except RuntimeError:
                pass
            extra["requestid"] = requestid
        return logging.Logger.makeRecord(self, name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)  # pragma: no cover


class JsonLogFormatter(logging.Formatter):
    """Log formatter that outputs machine-readable json.

    This log formatter outputs JSON format messages that are compatible with
    Mozilla's standard heka-based log aggregation infrastructure.

    See also:
    https://mana.mozilla.org/wiki/display/CLOUDSERVICES/Logging+Standard
    https://mana.mozilla.org/wiki/pages/viewpage.action?pageId=42895640

    Adapted from:
    https://github.com/mozilla-services/mozservices/blob/master/mozsvc/util.py#L106
    """

    LOGGING_FORMAT_VERSION = "2.0"

    # Map from Python logging to GCP severity levels
    # From https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry#LogSeverity
    SYSLOG_LEVEL_MAP = {
        logging.CRITICAL: 600,
        logging.ERROR: 500,
        logging.WARNING: 400,
        logging.INFO: 200,
        logging.DEBUG: 100,
    }

    # Syslog level to use when/if python level isn't found in map
    DEFAULT_SYSLOG_LEVEL = 200

    EXCLUDED_LOGRECORD_ATTRS = set(
        (
            "args",
            "asctime",
            "created",
            "exc_info",
            "exc_text",
            "filename",
            "funcName",
            "levelname",
            "levelno",
            "lineno",
            "module",
            "msecs",
            "message",
            "msg",
            "name",
            "pathname",
            "process",
            "processName",
            "relativeCreated",
            "stack_info",
            "thread",
            "threadName",
        )
    )

    def __init__(self, fmt=None, datefmt=None, logger_name="Balrog"):
        self.logger_name = logger_name
        self.hostname = socket.gethostname()
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        """
        Map from Python LogRecord attributes to JSON log format fields

        * from - https://docs.python.org/3/library/logging.html#logrecord-attributes
        * to - https://mana.mozilla.org/wiki/pages/viewpage.action?pageId=42895640
        """
        out = dict(
            Timestamp=int(record.created * 1e9),
            Type=record.name,
            Logger=self.logger_name,
            Hostname=self.hostname,
            EnvVersion=self.LOGGING_FORMAT_VERSION,
            Severity=self.SYSLOG_LEVEL_MAP.get(record.levelno, self.DEFAULT_SYSLOG_LEVEL),
            Pid=record.process,
        )

        # Include any custom attributes set on the record.
        # These would usually be collected metrics data.
        fields = dict()
        for key, value in record.__dict__.items():
            if key not in self.EXCLUDED_LOGRECORD_ATTRS:
                fields[key] = value

        # Only include the 'message' key if it has useful content
        # and is not already a JSON blob.
        message = record.getMessage()
        if message:
            if not message.startswith("{") or not message.endswith("}"):
                fields["message"] = message

        # If there is an error, format it for nice output.
        if record.exc_info is not None:
            fields["error"] = repr(record.exc_info[1])
            fields["traceback"] = safer_format_traceback(*record.exc_info)

        out["Fields"] = fields

        return json.dumps(out, default=str)


def safer_format_traceback(exc_typ, exc_val, exc_tb):
    """Format an exception traceback into safer string.
    We don't want to let users write arbitrary data into our logfiles,
    which could happen if they e.g. managed to trigger a ValueError with
    a carefully-crafted payload.  This function formats the traceback
    using "%r" for the actual exception data, which passes it through repr()
    so that any special chars are safely escaped.
    """
    lines = ["Uncaught exception:\n"]
    lines.extend(traceback.format_tb(exc_tb))
    lines.append("%r\n" % (exc_typ,))
    lines.append("%r\n" % (exc_val,))
    return "".join(lines)


def configure_logging(stream=sys.stdout, formatter=JsonLogFormatter, format_=log_format, level=logging.DEBUG):
    logging.setLoggerClass(BalrogLogger)
    handler = logging.StreamHandler(stream)
    formatter = formatter(fmt=format_)
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)
    logging.root.setLevel(level)
