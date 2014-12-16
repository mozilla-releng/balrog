import logging
from os import path
import site
import sys

mydir = path.dirname(path.abspath(__file__))

site.addsitedir(mydir)
from auslib.util import thirdparty
thirdparty.extendsyspath()

from auslib.config import ClientConfig
import auslib.log
from auslib.web.base import sentry

cfg = ClientConfig(path.join(mydir, 'balrog.ini'))
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
from auslib.web.base import app as application

for cache_name, cache_cfg in cfg.getCaches().iteritems():
    cache.make_cache(cache_name, *cache_cfg)

auslib.log.cef_config = auslib.log.get_cef_config(cfg.getCefLogfile())
dbo.setDb(cfg.getDburi())
dbo.setDomainWhitelist(cfg.getDomainWhitelist())
application.config['WHITELISTED_DOMAINS'] = cfg.getDomainWhitelist()
application.config['SPECIAL_FORCE_HOSTS'] = cfg.getSpecialForceHosts()
application.config['SENTRY_DSN'] = cfg.getSentryDsn()
application.config['SENTRY_PROCESSORS'] = ['auslib.util.sentry.SanitizeHeadersProcessor']

if application.config['SENTRY_DSN']:
    sentry.init_app(application)
