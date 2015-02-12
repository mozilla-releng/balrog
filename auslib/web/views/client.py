import urllib

from flask import make_response, request
from flask.views import MethodView

from auslib.web.base import AUS, app

import logging

class ClientRequestView(MethodView):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(self.__class__.__name__)
        MethodView.__init__(self, *args, **kwargs)

    def getHeaderArchitecture(self, buildTarget, ua):
        if buildTarget.startswith('Darwin'):
            if ua and 'PPC' in ua:
                return 'PPC'
            else:
                return 'Intel'
        else:
            return 'Intel'

    def removeAvastBrokenness(self, locale):
        # Some versions of Avast have a bug in them that prepends "x86 "
        # to the locale. We need to make sure we handle this case correctly
        # so that these people can keep up to date.
        return locale.replace("x86 ", "")

    def getQueryFromURL(self, url):
        query = url.copy()
        query["locale"] = self.removeAvastBrokenness(query["locale"])
        query['osVersion'] = urllib.unquote(query['osVersion'])
        ua = request.headers.get('User-Agent')
        query['headerArchitecture'] = self.getHeaderArchitecture(query['buildTarget'], ua)
        query['force'] = (int(request.args.get('force', 0)) == 1)
        return query

    def get(self, **url):
        query = self.getQueryFromURL(url)
        self.log.debug("Got query: %s", query)
        release, update_type = AUS.evaluateRules(query)
        # passing {},None returns empty xml
        if release:
            xml = release.createXML(query, update_type, app.config["WHITELISTED_DOMAINS"], app.config["SPECIAL_FORCE_HOSTS"])
        else:
            xml = ['<?xml version="1.0"?>']
            xml.append('<updates>')
            xml.append('</updates>')
            xml = "\n".join(xml)
        self.log.debug("Sending XML: %s", xml)
        response = make_response(xml)
        response.mimetype = 'text/xml'
        return response
