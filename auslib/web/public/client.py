import re
import sys

from connexion import request

from flask import make_response, current_app as app

import six

from auslib.AUS import AUS, SUCCEED, FAIL
from auslib.global_state import dbo

import logging

try:
    from urllib import unquote
except ImportError: # pragma: no cover
    from urllib.parse import unquote


AUS = AUS()
LOG = logging.getLogger(__name__)


def getHeaderArchitecture(buildTarget, ua):
    if buildTarget.startswith('Darwin'):
        if ua and 'PPC' in ua:
            return 'PPC'
        else:
            return 'Intel'
    else:
        return 'Intel'


def getSystemCapabilities(systemCapabilities):
    # Set defaults for the broken-down fields, because not all query versions
    # will have all values.
    caps = {"instructionSet": None, "memory": None, "jaws": None}
    # New-style SYSTEM_CAPABILITIES, as implemented in https://bugzilla.mozilla.org/show_bug.cgi?id=1373367
    if systemCapabilities.startswith("ISET:"):
        for part in systemCapabilities.split(","):
            key, value = part.split(":", 1)
            if key == "ISET":
                caps["instructionSet"] = value
            elif key == "MEM":
                caps["memory"] = int(value)
            elif key == "JAWS":
                caps["jaws"] = bool(int(value))
    # Old-style, unprefixed SYSTEM_CAPABILITIES. Only supports instructionSet and memory.
    else:
        parts = systemCapabilities.split(",")
        # The only known valid formats for this field are either a single part,
        # or two parts separated by a comma. Anything else is unparsable, so we
        # we cannot safely assign any fields.
        if len(parts) == 1:
            caps["instructionSet"] = parts[0]
        elif len(parts) == 2:
            caps["instructionSet"] = parts[0]
            caps["memory"] = int(parts[1])

    return caps


def getCleanQueryFromURL(url):
    query = url.copy()
    # Any of the fields (except queryVersion, which is hardcoded) could contain Unicode data.
    # The lower level of Balrog is not ready to support Unicode yet, and any valid data will
    # not contain Unicode characters - so for now, we simply encode to ascii and replace the
    # Unicode characters.
    # This is something that we should revisit when we upgrade to Python 3, as it will be as
    # easy to pretend Unicode doesn't exist. (Which is why this block is only for Python 2 --
    # encoding to ascii in Python 3 gives us "bytes", which causes a whole mess of problems
    # later.)
    if six.PY2:
        for field in query:
            if field == "queryVersion":
                continue
            query[field] = query[field].encode("ascii", "replace")
    # Some versions of Avast make requests and blindly append "?avast=1" to
    # them, which breaks query string parsing if ?force=1 is already
    # there. Because we're nice people we'll fix it up.
    if 'force' in query and 'avast' in query['force']:
        force_value = query['force']
        force_split = force_value.split('?', 1)

        if len(force_split) < 2:
            force_split = force_value.split('%3F', 1)

        query['force'] = force_split[0]

        avast_parameter = force_split[1]
        avast_split = avast_parameter.split('=')
        query[avast_split[0]] = int(avast_split[1])

    # Some versions of Avast have a bug in them that prepends "x86 "
    if 'locale' in query:
        query['locale'] = query['locale'].replace('x86 ', '')

    return query


def getQueryFromURL(url):
    query = getCleanQueryFromURL(url)
    if "systemCapabilities" in query:
        query.update(getSystemCapabilities(url["systemCapabilities"]))
        del query["systemCapabilities"]
    query['osVersion'] = unquote(query['osVersion'])
    ua = request.headers.get('User-Agent')
    query['headerArchitecture'] = getHeaderArchitecture(query['buildTarget'], ua)
    force = query.get('force')
    query['force'] = {
        SUCCEED.query_value: SUCCEED,
        FAIL.query_value: FAIL
    }.get(force)
    if "mig64" in query:
        # "1" is the only value that official clients send. We ignore any other values
        # by setting mig64 to None.
        if query.get("mig64") == "1":
            query["mig64"] = True
        else:
            query["mig64"] = False
    else:
        query["mig64"] = None
    return query


def extract_query_version(request_url):
    version = 0
    pattern = '^.*/update/(\d+)/.*\.xml.*$'
    match = re.match(pattern, request_url)
    if match:
        version = int(match.group(1))
    return version


def get_update_blob(**url):
    url['queryVersion'] = extract_query_version(request.url)
    # Underlying code depends on osVersion being set. Since this route only
    # exists to support ancient queries, and all newer versions have osVersion
    # in them it's easier to set this here than make the all of the underlying
    # code support queries without it.
    if url['queryVersion'] == 1:
        url['osVersion'] = ''

    query = getQueryFromURL(url)
    LOG.debug("Got query: %s", query)
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
                    LOG.warning("No release found with name: %s", blob_name)
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

        # Appending Header
        # In case of superblob Extracting Header form parent release
        xml.append(release.getInnerHeaderXML(query,
                                             update_type,
                                             app.config["WHITELISTED_DOMAINS"],
                                             app.config["SPECIAL_FORCE_HOSTS"]))
        for response_blob in response_blobs:
            xml.extend(response_blob['response_release']
                       .getInnerXML(response_blob['product_query'],
                                    response_blob['response_update_type'],
                                    app.config["WHITELISTED_DOMAINS"],
                                    app.config["SPECIAL_FORCE_HOSTS"]))
        # Appending Footer
        # In case of superblob Extracting Header form parent release
        xml.append(release.getInnerFooterXML(query,
                                             update_type,
                                             app.config["WHITELISTED_DOMAINS"],
                                             app.config["SPECIAL_FORCE_HOSTS"]))
        xml.append(release.getFooterXML())
        # ensure valid xml by using the right entity for ampersand
        xml = re.sub('&(?!amp;)', '&amp;', '\n'.join(xml))
    else:
        xml = ['<?xml version="1.0"?>']
        xml.append('<updates>')
        xml.append('</updates>')
        xml = "\n".join(xml)
    LOG.debug("Sending XML: %s", xml)
    response = make_response(xml)
    response.headers["Cache-Control"] = app.cacheControl
    response.mimetype = "text/xml"
    return response


def _set_functions(function_names, function):
    module = sys.modules[__name__]
    for function_name in function_names:
        setattr(module, function_name, function)


update_blob_functions = ["get_update_blob_1",
                         "get_update_blob_2",
                         "get_update_blob_3",
                         "get_update_blob_3_esrpre",
                         "get_update_blob_4",
                         "get_update_blob_5",
                         "get_update_blob_6"]

_set_functions(update_blob_functions, get_update_blob)
