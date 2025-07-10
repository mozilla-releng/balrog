import logging
import re
import sys

from flask import current_app as app
from flask import make_response, request
from statsd.defaults.env import statsd

from auslib.AUS import FORCE_FALLBACK_MAPPING, FORCE_MAIN_MAPPING
from auslib.blobs.base import XMLBlob, createBlob
from auslib.errors import BadDataError
from auslib.global_state import dbo
from auslib.services import releases
from auslib.web.public.helpers import AUS, get_aus_metadata_headers, get_content_signature_headers, with_transaction

LOG = logging.getLogger(__name__)


def getHeaderArchitecture(buildTarget, ua):
    if buildTarget.startswith("Darwin"):
        if ua and "PPC" in ua:
            return "PPC"
        else:
            return "Intel"
    else:
        return "Intel"


def getSystemCapabilities(systemCapabilities):
    # Set defaults for the broken-down fields, because not all query versions
    # will have all values.
    caps = {"instructionSet": None, "memory": None, "jaws": None}
    # New-style SYSTEM_CAPABILITIES, as implemented in https://bugzilla.mozilla.org/show_bug.cgi?id=1373367
    if systemCapabilities.startswith("ISET:"):
        for part in systemCapabilities.split(","):
            # Skip fields with an unparseable format, which we see often. Eg:
            # ISET:SSE4_2,MEM:32768,(select*from(select(sleep(20)))a)
            if ":" not in part:
                continue
            key, value = part.split(":", 1)
            if key == "ISET":
                caps["instructionSet"] = value
            elif key == "MEM":
                try:
                    caps["memory"] = int(value)
                except ValueError:
                    caps["memory"] = None
            elif key == "JAWS":
                try:
                    caps["jaws"] = bool(int(value))
                except ValueError:
                    caps["jaws"] = None
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
            try:
                caps["memory"] = int(parts[1])
            except ValueError:
                caps["memory"] = None

    return caps


def getCleanQueryFromURL(url):
    query = url.copy()
    # Any of the fields (except queryVersion, which is hardcoded) could contain Unicode data.
    # The lower level of Balrog is not ready to support Unicode yet, and any valid data will
    # not contain Unicode characters - so for now, we simply encode to ascii and replace the
    # Unicode characters.
    # Until the lower level of Balrog supports Unicode better, the simplest thing to do
    # is simply pretend these strings are ascii (which is the case for any valid query).
    for field in query:
        if field == "queryVersion":
            continue
        query[field] = query[field].encode("ascii", "replace").decode()
    # Some versions of Avast make requests and blindly append "?avast=1" to
    # them, which breaks query string parsing if ?force=1 is already
    # there. Because we're nice people we'll fix it up.
    if "force" in query and "avast" in query["force"]:
        try:
            force_value = query["force"]
            force_split = force_value.split("?", 1)

            if len(force_split) < 2:
                force_split = force_value.split("%3F", 1)

            query["force"] = force_split[0]

            avast_parameter = force_split[1]
            avast_split = avast_parameter.split("=")
            query[avast_split[0]] = int(avast_split[1])
        except (IndexError, ValueError):
            pass

    # Some versions of Avast have a bug in them that prepends "x86 "
    if "locale" in query:
        query["locale"] = query["locale"].replace("x86 ", "")

    return query


def getQueryFromURL(url):
    query = getCleanQueryFromURL(url)
    if "systemCapabilities" in query:
        query.update(getSystemCapabilities(url["systemCapabilities"]))
        del query["systemCapabilities"]
    ua = request.headers.get("User-Agent")
    query["headerArchitecture"] = getHeaderArchitecture(query["buildTarget"], ua)
    force = query.get("force")
    query["force"] = {FORCE_MAIN_MAPPING.query_value: FORCE_MAIN_MAPPING, FORCE_FALLBACK_MAPPING.query_value: FORCE_FALLBACK_MAPPING}.get(force)
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
    pattern = r"^.*/update/(\d+)/.*\.xml.*$"
    match = re.match(pattern, request_url)
    if match:
        version = int(match.group(1))
    return version


@with_transaction
def get_update_blob(transaction, **url):
    with statsd.timer("client.parse_query"):
        url["queryVersion"] = extract_query_version(request.url)
        # Underlying code depends on osVersion being set. Since this route only
        # exists to support ancient queries, and all newer versions have osVersion
        # in them it's easier to set this here than make the all of the underlying
        # code support queries without it.
        if url["queryVersion"] == 1:
            url["osVersion"] = ""
        # Bug 1517743 - two Firefox nightlies can't parse update.xml when it contains the usual newlines or indentations
        squash_response = False

        query = getQueryFromURL(url)
        LOG.debug("Got query: %s", query)

    with statsd.timer("client.evaluate_rules"):
        release, update_type, eval_metadata = AUS.evaluateRules(query, transaction=transaction)

    response_blobs = []
    if release:
        if not isinstance(release, XMLBlob):
            raise BadDataError("Wrong blob type")
        response_products = release.getResponseProducts()
        response_blob_names = release.getResponseBlobs()
        if response_products:
            with statsd.timer("client.process_response_products"):
                # if we have a SuperBlob of gmp, we process the response products and
                # concatenate their inner XMLs
                response_blobs.extend(evaluate_response_products(response_products, query, transaction))
        elif response_blob_names:
            with statsd.timer("client.process_response_blobs"):
                # if we have a SuperBlob of systemaddons, we process the response products and
                # concatenate their inner XMLs
                response_blobs.extend(evaluate_response_blobs(response_blob_names, update_type, query, transaction))
        else:
            # if we just have a plain old single blob, just add it
            response_blobs.append({"product_query": query, "response_release": release, "response_update_type": update_type})
            # Bug 1517743 - we want a cheap test because this will be run on each request
            if release["name"] == "Firefox-mozilla-central-nightly-latest" and query["buildID"] in ("20190103220533", "20190104093221"):
                squash_response = True
                LOG.debug("Busted nightly detected, will squash xml response")

    with statsd.timer("client.make_response"):
        return construct_response(release, query, update_type, response_blobs, squash_response, eval_metadata)


def evaluate_response_products(response_products, query, transaction):
    response_blobs = []
    for product in response_products:
        product_query = query.copy()
        product_query["product"] = product
        response_release, response_update_type, _ = AUS.evaluateRules(product_query, transaction=transaction)
        if not response_release:
            continue

        response_blobs.append({"product_query": product_query, "response_release": response_release, "response_update_type": response_update_type})

    return response_blobs


def evaluate_response_blobs(response_blob_names, update_type, query, transaction):
    response_blobs = []
    for blob_name in response_blob_names:
        product_query = query.copy()
        release_row = releases.get_release(blob_name, transaction, include_sc=False)
        response_release = None
        if release_row:
            product_query["product"] = releases.get_product(blob_name, transaction)
            response_release = createBlob(release_row["blob"])
        # TODO: remove me when old releases table dies
        else:
            product = dbo.releases.getReleases(name=blob_name, limit=1, transaction=transaction)[0]["product"]
            product_query["product"] = product
            response_release = dbo.releases.getReleaseBlob(name=blob_name, transaction=transaction)
        if not response_release:
            LOG.warning("No release found with name: %s", blob_name)
            continue

        response_blobs.append({"product_query": product_query, "response_release": response_release, "response_update_type": update_type})

    return response_blobs


def construct_response(release, query, update_type, response_blobs, squash_response, eval_metadata):
    if release:
        # getHeaderXML() returns outermost header for an update which
        # is same for all release type
        xml = release.getHeaderXML()
        # we assume that all blobs will have similar ones. We might want to
        # verify that all of them are indeed the same in the future.

        # Appending Header
        # In case of superblob Extracting Header form parent release
        xml.append(release.getInnerHeaderXML(query, update_type, app.config["ALLOWLISTED_DOMAINS"], app.config["SPECIAL_FORCE_HOSTS"]))
        for response_blob in response_blobs:
            xml.extend(
                response_blob["response_release"].getInnerXML(
                    response_blob["product_query"], response_blob["response_update_type"], app.config["ALLOWLISTED_DOMAINS"], app.config["SPECIAL_FORCE_HOSTS"]
                )
            )
        # Appending Footer
        # In case of superblob Extracting Header form parent release
        xml.append(release.getInnerFooterXML(query, update_type, app.config["ALLOWLISTED_DOMAINS"], app.config["SPECIAL_FORCE_HOSTS"]))
        xml.append(release.getFooterXML())
        # ensure valid xml by using the right entity for ampersand
        xml = re.sub("&(?!amp;)", "&amp;", "\n".join(xml))
    else:
        xml = ['<?xml version="1.0"?>']
        xml.append("<updates>")
        xml.append("</updates>")
        xml = "\n".join(xml)

    # Bug 1517743 - remove newlines and 4 space indents
    if squash_response:
        xml = xml.replace("\n", "").replace("    ", "")

    LOG.debug("Sending XML: %s", xml)
    response = make_response(xml)
    response.headers["Cache-Control"] = app.cacheControl
    response.headers.extend(get_aus_metadata_headers(eval_metadata))
    if query["product"] in app.config.get("CONTENT_SIGNATURE_PRODUCTS", []):
        response.headers.extend(get_content_signature_headers(xml, query["product"]))
    response.mimetype = "text/xml"
    return response


def _set_functions(function_names, function):
    module = sys.modules[__name__]
    for function_name in function_names:
        setattr(module, function_name, function)


update_blob_functions = [
    "get_update_blob_1",
    "get_update_blob_2",
    "get_update_blob_3",
    "get_update_blob_3_esrpre",
    "get_update_blob_4",
    "get_update_blob_5",
    "get_update_blob_6",
]

_set_functions(update_blob_functions, get_update_blob)
