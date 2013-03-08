import logging
from os import path
import site
import sys

mydir = path.dirname(path.abspath(__file__))
site.addsitedir(mydir)
site.addsitedir(path.join(mydir, 'vendor/lib/python'))

from raven.contrib.flask import Sentry

from auslib import log_format
from auslib.web.base import app as application
from auslib.web.base import AUS
from auslib.config import ClientConfig

cfg = ClientConfig('/etc/aus/balrog.ini')
errors = cfg.validate()
if errors:
    print >>sys.stderr, "Invalid configuration file:"
    for err in errors:
        print >>sys.stderr, err
    sys.exit(1)

logging.basicConfig(filename=cfg.getLogfile(), level=cfg.getLogLevel(), format=log_format)
AUS.setDb(cfg.getDburi())
AUS.setSpecialHosts(cfg.getSpecialForceHosts())
application.config['SENTRY_DSN'] = cfg.getSentryDsn()
application.config['SENTRY_PROCESSORS'] = ['auslib.util.sentry.SanitizeHeadersProcessor']

if application.config['SENTRY_DSN']:
    sentry = Sentry(application)
