from flask import make_response, request
from flask.views import MethodView

from auslib.client.base import app, AUS

import logging
log = logging.getLogger(__name__)

class ClientRequestView(MethodView):
    def getHeaderArchitecture(self, buildTarget, ua):
        if buildTarget.startswith('Darwin'):
            if ua and 'PPC' in ua:
                return 'PPC'
            else:
                return 'Intel'
        else:
            return 'Intel'

    def getQueryFromURL(self, queryVersion, url):
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
                      'force': True,
                      'name': ''
                     }
        """
        # TODO support older URL versions. catlee suggests splitting on /, easy to use conditional assignment then
        query = url.copy()
        # TODO: Better way of dispatching different versions when we actually have to deal with them.
        if queryVersion == 3:
            query['name'] = AUS.identifyRequest(query)
            ua = request.headers.get('User-Agent')
            query['headerArchitecture'] = self.getHeaderArchitecture(query['buildTarget'], ua)
            query['force'] = (int(request.args.get('force', 0)) == 1)
            return query
        return {}

    """/update/3/<product>/<version>/<buildID>/<build target>/<locale>/<channel>/<os version>/<distribution>/<distribution version>"""
    def get(self, queryVersion, **url):
        query = self.getQueryFromURL(queryVersion, url)
        log.debug("ClientRequestView.get: Got query: %s", query)
        if query:
            rule = AUS.evaluateRules(query)
        else:
            rule = {}
        # passing {},{} returns empty xml
        log.debug("ClientRequestView.get: Got rule: %s", rule)
        xml = AUS.createXML(query, rule)
        log.debug("ClientRequestView.get: Sending XML: %s", xml)
        response = make_response(xml)
        response.mimetype = 'text/xml'
        return response

app.add_url_rule('/update/<int:queryVersion>/<product>/<version>/<buildID>/<buildTarget>/<locale>/<channel>/<osVersion>/<distribution>/<distVersion>/update.xml', view_func=ClientRequestView.as_view('clientrequest'))
