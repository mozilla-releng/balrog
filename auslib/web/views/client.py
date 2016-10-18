import urllib
import re

from flask import make_response, request
from flask.views import MethodView

from auslib.web.base import AUS, app
from auslib.global_state import dbo

import logging


class ClientRequestView(MethodView):
    def __init__(self, *args, **kwargs):
        # By default, we want a cache that can be shared across requests from different users ("public")
        # and a maximum age of 60 seconds, to keep our TTL low.
        self.cacheControl = app.config.get("CACHE_CONTROL", "public, max-age=60")
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
        # Some versions of Avast make requests and blindly append "?avast=1" to
        # them, which breaks query string parsing if ?force=1 is already
        # there. Because we're nice people we'll fix it up.
        qs = request.environ.get("QUERY_STRING", "")
        if "force" in qs and "avast" in qs:
            qs = qs.replace("?avast=1", "&avast=1")
            qs = qs.replace("%3Favast=1", "&avast=1")
            request.environ["QUERY_STRING"] = qs
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
            response_products = release.getResponseProducts()
            response_blobs = []
            response_blob_names = release.getResponseBlobs()
            if response_products:
                # if we have a SuperBlob of gmp, we process the response products and
                # concatenate their inner XMLs
                for product in response_products:
                    product_query = query.copy()
                    product_query["product"] = product
                    response_release, response_update_type = AUS.evaluateRules(product_query)
                    if not response_release:
                        continue

                    response_blobs.append({'product_query': product_query,
                                           'response_release': response_release,
                                           'response_update_type': response_update_type})
            elif response_blob_names:
                for blob_name in response_blob_names:
                    # if we have a SuperBlob of systemaddons, we process the response products and
                    # concatenate their inner XMLs
                    product_query = query.copy()
                    product = dbo.releases.getReleases(name=blob_name, limit=1)[0]['product']
                    product_query["product"] = product
                    response_release = dbo.releases.getReleaseBlob(name=blob_name)
                    if not response_release:
                        self.log.warning("No release found with name: %s", blob_name)
                        continue

                    response_blobs.append({'product_query': product_query,
                                           'response_release': response_release,
                                           'response_update_type': update_type})
            else:
                response_blobs.append({'product_query': query,
                                       'response_release': release,
                                       'response_update_type': update_type})

            # getHeaderXML() returns outermost header for an update which
            # is same for all release type
            xml = release.getHeaderXML()
            # we assume that all blobs will have similar ones. We might want to
            # verify that all of them are indeed the same in the future.

            # Extracting Header
            # In case of superblob Extracting Header form parent release
            innerHeaderXML = release.getInnerHeaderXML(query,
                                                       update_type,
                                                       app.config["WHITELISTED_DOMAINS"],
                                                       app.config["SPECIAL_FORCE_HOSTS"])
            # Extracting Footer
            # In case of superblob Extracting Header form parent release
            innerFooterXML = release.getInnerFooterXML(query,
                                                       update_type,
                                                       app.config["WHITELISTED_DOMAINS"],
                                                       app.config["SPECIAL_FORCE_HOSTS"])
            xml.append(innerHeaderXML)
            for response_blob in response_blobs:
                xml.extend(response_blob['response_release']
                           .getInnerXML(response_blob['product_query'],
                                        response_blob['response_update_type'],
                                        app.config["WHITELISTED_DOMAINS"],
                                        app.config["SPECIAL_FORCE_HOSTS"]))

            xml.append(innerFooterXML)
            xml.append(release.getFooterXML())
            # ensure valid xml by using the right entity for ampersand
            xml = re.sub('&(?!amp;)', '&amp;', '\n'.join(xml))
        else:
            xml = ['<?xml version="1.0"?>']
            xml.append('<updates>')
            xml.append('</updates>')
            xml = "\n".join(xml)
        self.log.debug("Sending XML: %s", xml)
        response = make_response(xml)
        response.headers["Cache-Control"] = self.cacheControl
        response.mimetype = "text/xml"
        return response
