import logging
from os import path
import site
import sys

mydir = path.dirname(path.abspath(__file__))
site.addsitedir(mydir)
site.addsitedir(path.join(mydir, 'vendor/lib/python'))

from auslib.client.base import app as application
from auslib.client.base import AUS
from auslib.config import ClientConfig

cfg = ClientConfig('/etc/aus/client.ini')
errors = cfg.validate()
if errors:
    print >>sys.stderr, "Invalid configuration file:"
    for err in errors:
        print >>sys.stderr, err
    sys.exit(1)

logging.basicConfig(filename=cfg.getLogfile(), level=cfg.getLogLevel())
AUS.setDb(cfg.getDburi())
AUS.setSpecialHosts(cfg.getSpecialForceHosts())
