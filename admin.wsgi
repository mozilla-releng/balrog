import logging
from os import path
import site
import sys

mydir = path.dirname(path.abspath(__file__))
site.addsitedir(mydir)
site.addsitedir(path.join(mydir, 'vendor/lib/python'))

from raven.contrib.flask import Sentry

from auslib.config import AdminConfig
import auslib.log

cfg = AdminConfig(path.join(mydir, 'admin.ini'))
errors = cfg.validate()
if errors:
    print >>sys.stderr, "Invalid configuration file:"
    for err in errors:
        print >>sys.stderr, err
    sys.exit(1)

# Logging needs to get set-up before importing the application
# to make sure that logging done from other modules uses our Logger.
logging.setLoggerClass(auslib.log.BalrogLogger)
logging.basicConfig(filename=cfg.getLogfile(), level=cfg.getLogLevel(), format=auslib.log.log_format)

from auslib.admin.base import db, app as application

auslib.log.cef_config = auslib.log.get_cef_config(cfg.getCefLogfile())
db.setDburi(cfg.getDburi())
db.setupChangeMonitors(cfg.getSystemAccounts())
db.setDomainWhitelist(cfg.getDomainWhitelist())
application.config['SECRET_KEY'] = cfg.getSecretKey()
application.config['SENTRY_DSN'] = cfg.getSentryDsn()
application.config['SENTRY_PROCESSORS'] = ['auslib.util.sentry.SanitizeHeadersProcessor']

if application.config['SENTRY_DSN']:
    sentry = Sentry(application)
