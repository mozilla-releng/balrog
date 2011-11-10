import logging

log = logging.getLogger(__name__)

from auslib.client.base import app, AUS

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

    log_level = logging.INFO
    if options.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level, format="%(asctime)s: %(message)s")

    AUS.setDb(options.db)
    AUS.createTables()

    app.config['SECRET_KEY'] = 'abc123'
    app.config['DEBUG'] = True
    app.run(port=options.port)
