import logging
from os import path
import site
import sys

mydir = path.dirname(path.abspath(__file__))
site.addsitedir(mydir)
site.addsitedir(path.join(mydir, 'vendor/lib/python'))

from raven.contrib.flask import Sentry

from auslib import log_format
from auslib.admin.base import db, app as application
from auslib.config import AdminConfig

cfg = AdminConfig('/etc/aus/admin.ini')
errors = cfg.validate()
if errors:
    print >>sys.stderr, "Invalid configuration file:"
    for err in errors:
        print >>sys.stderr, err
    sys.exit(1)

logging.basicConfig(filename=cfg.getLogfile(), level=cfg.getLogLevel(), format=log_format)
db.setDburi(cfg.getDburi())
application.config['SECRET_KEY'] = cfg.getSecretKey()
application.config['SENTRY_DSN'] = cfg.getSentryDsn()
application.config['SENTRY_PROCESSORS'] = ['auslib.util.sentry.SanitizeHeadersProcessor']

if application.config['SENTRY_DSN']:
    sentry = Sentry(application)
