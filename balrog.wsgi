import logging
from os import path
import site
import sys

mydir = path.dirname(path.abspath(__file__))
site.addsitedir(mydir)
site.addsitedir(path.join(mydir, 'vendor/lib/python'))

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

logging.basicConfig(filename=cfg.getLogfile(), level=cfg.getLogLevel(), format="%(asctime)s: %(message)s")
AUS.setDb(cfg.getDburi())
AUS.setSpecialHosts(cfg.getSpecialForceHosts())
