import os
from os import path
import site

site.addsitedir(path.dirname(path.abspath(__file__)))
from auslib.util import thirdparty
thirdparty.extendsyspath()

from migrate import DatabaseAlreadyControlledError

import logging

log = logging.getLogger(__name__)

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.set_defaults(
        db='sqlite:///update.db',
        port=8000,
        whitelistedDomains=[
            "download.mozilla.org",
            "stage.mozilla.org",
            "ftp.mozilla.org",
            "ciscobinary.openh264.org",
        ],
        specialForceHosts=["http://download.mozilla.org"],
    )
    parser.add_option("-d", "--db", dest="db", help="database to use, relative to inputdir")
    parser.add_option("-p", "--port", dest="port", type="int", help="port for server")
    parser.add_option("--host", dest="host", default='127.0.0.1', help="host to listen on. for example, 0.0.0.0 binds on all interfaces.")
    parser.add_option("--whitelist-domain", dest="whitelistedDomains", action="append")
    parser.add_option("--special-force-host", dest="specialForceHosts", action="append",
                      help="Hosts to forward force=1 on to, use a protocol prefix like http://")
    parser.add_option("--cef-log", dest="cefLog", default="cef.log")
    parser.add_option("--profile-dir", dest="profile_dir", default=None,
                      help="Enables profiling and logs to the specified file."),
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
        help="Verbose output")
    options, args = parser.parse_args()

    # Logging needs to get set-up before importing the application
    # to make sure that logging done from other modules uses our Logger.
    import auslib.log

    logging.setLoggerClass(auslib.log.BalrogLogger)
    log_level = logging.INFO
    if options.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level, format=auslib.log.log_format)

    from auslib.global_state import dbo, cache
    from auslib.web.base import app

    cache.make_cache("blob", 500, 3600)
    cache.make_cache("blob_version", 500, 60)

    auslib.log.cef_config = auslib.log.get_cef_config(options.cefLog)
    dbo.setDb(options.db)
    dbo.setDomainWhitelist(options.whitelistedDomains)
    try:
        dbo.create()
    except DatabaseAlreadyControlledError:
        pass

    if options.profile_dir:
        from werkzeug.contrib.profiler import ProfilerMiddleware
        if not path.exists(options.profile_dir):
            os.makedirs(options.profile_dir)
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir=options.profile_dir)

    app.config['WHITELISTED_DOMAINS'] = options.whitelistedDomains
    app.config['SPECIAL_FORCE_HOSTS'] = options.specialForceHosts
    app.config['SECRET_KEY'] = 'abc123'
    app.config['DEBUG'] = True

    app.run(port=options.port, host=options.host)
