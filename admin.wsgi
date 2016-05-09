import logging
from os import path
import site
import sys

mydir = path.dirname(path.abspath(__file__))

site.addsitedir(mydir)
from auslib.util import thirdparty
thirdparty.extendsyspath()

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

from auslib.global_state import dbo, cache
from auslib.admin.base import app as application

cache.make_copies = True
for cache_name, cache_cfg in cfg.getCaches().iteritems():
    cache.make_cache(cache_name, *cache_cfg)

dbo.setDb(cfg.getDburi())
dbo.setDomainWhitelist(cfg.getDomainWhitelist())
application.config['WHITELISTED_DOMAINS'] = cfg.getDomainWhitelist()
application.config['PAGE_TITLE'] = cfg.getPageTitle()
application.config['SECRET_KEY'] = cfg.getSecretKey()
