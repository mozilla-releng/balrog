import logging

log = logging.getLogger(__name__)

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.set_defaults(
        db='sqlite:///update.db',
        port=8000,
    )
    parser.add_option("-d", "--db", dest="db", help="database to use, relative to inputdir")
    parser.add_option("-p", "--port", dest="port", type="int", help="port for server")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
        help="Verbose output")
    options, args = parser.parse_args()

    from auslib import log_format
    from auslib.client.base import app, AUS

    log_level = logging.INFO
    if options.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level, format=log_format)

    AUS.setDb(options.db)
    AUS.createTables()

    app.config['SECRET_KEY'] = 'abc123'
    app.config['DEBUG'] = True
    app.run(port=options.port)
