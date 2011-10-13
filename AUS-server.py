import BaseHTTPServer, SocketServer
import re
import logging

log = logging.getLogger(__name__)

from AUS import *

class AUS3HTTPServer(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve a GET request to AUS3."""
        self.send_response(200)
        self.send_header("Content-type", "text/xml;")

        # resolve update
        query = self.getQueryFromURL()
        if query:
            rule = AUS.evaluateRules(query)
        else:
            rule = {}
        # passing {},{} returns empty xml
        xml = AUS.createXML(query, rule)
        self.send_response(200)
        self.send_header("Content-Length", len(xml))
        self.end_headers()
        self.wfile.write(xml)

    def getQueryFromURL(self):
        """ Use regexp to turn
                "update/3/Firefox/4.0b13pre/20110303122430/Darwin_x86_64-gcc-u-i386-x86_64/en-US/nightly/Darwin%2010.6.0/default/default/update.xml?force=1"
            into
                testUpdate = {
                      'product': 'Firefox',
                      'version': '4.0b13pre',
                      'buildID': '20110303122430',
                      'buildTarget': 'Darwin_x86_64-gcc-u-i386-x86_64',
                      'locale': 'en-US',
                      'channel': 'nightly',
                      'osVersion': 'Darwin%2010.6.0',
                      'distribution': 'default',
                      'distVersion': 'default',
                      'headerArchitecture': 'Intel',
                      'name': ''
                     }
        """
        # TODO support older URL versions. catlee suggests splitting on /, easy to use conditional assignment then
        # TODO support force queries to void throttling, and pass through to downloads
        m = re.match("/update/3/(?P<product>.*?)/(?P<version>.*?)/(?P<buildID>.*?)/(?P<buildTarget>.*?)/(?P<locale>.*?)/(?P<channel>.*?)/(?P<osVersion>.*?)/(?P<distribution>.*?)/(?P<distVersion>.*?)/update.xml", self.path)
        if m:
            query = m.groupdict()
            query['name'] = AUS.identifyRequest(query)
            if query['buildTarget'].startswith('Darwin'):
                ua = self.headers.getfirstmatchingheader('User-Agent')
                if ua and 'PPC' in ua[0]:
                    query['headerArchitecture'] = 'PPC'
                else:
                    query['headerArchitecture'] = 'Intel'
            else:
                query['headerArchitecture'] = 'Intel'
            return query
        else:
            return {}

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

    AUS = AUS3(dbname=options.db)

    Handler = AUS3HTTPServer
    httpd = SocketServer.TCPServer(("", options.port), Handler)

    log.info("Serving on port %s", options.port)
    httpd.serve_forever()
