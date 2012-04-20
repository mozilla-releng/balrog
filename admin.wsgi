import logging
from os import path
import site
import sys

mydir = path.dirname(path.abspath(__file__))
site.addsitedir(mydir)
site.addsitedir(path.join(mydir, 'vendor/lib/python'))

from auslib.web.base import db, app as application
from auslib.config import AdminConfig

cfg = AdminConfig('/etc/aus/admin.ini')
errors = cfg.validate()
if errors:
    print >>sys.stderr, "Invalid configuration file:"
    for err in errors:
        print >>sys.stderr, err
    sys.exit(1)

logging.basicConfig(filename=cfg.getLogfile(), level=cfg.getLogLevel())
db.setDburi(cfg.getDburi())
application.config['SECRET_KEY'] = cfg.getSecretKey()
