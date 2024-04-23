import json

from flask import Response
from flask import current_app as app
from mozilla_version.errors import PatternNotMatchedError
from mozilla_version.version import BaseVersion

from auslib.AUS import FORCE_FALLBACK_MAPPING, FORCE_MAIN_MAPPING
from auslib.web.public.helpers import AUS, get_aus_metadata_headers, get_content_signature_headers, with_transaction

# Map of products and version.
# Uses legacy key if requested version is < value set here.
LEGACY_PRODUCT_VERSION_MAPPING = {"FirefoxVPN": "2.22.0"}


def use_legacy_key(product=None, version=None):
    # Skip if product is not in the mapping or version is not provided
    if product not in LEGACY_PRODUCT_VERSION_MAPPING or not version:
        return False

    try:
        limit_version = BaseVersion.parse(LEGACY_PRODUCT_VERSION_MAPPING[product])
        if BaseVersion.parse(version) < limit_version:
            return True
    except (PatternNotMatchedError, ValueError):
        # Likely a malformed version string - ignore legacy key and sign with latest available
        pass
    return False


@with_transaction
def get_update(transaction, **parameters):
    force = parameters.get("force")
    parameters["force"] = {FORCE_MAIN_MAPPING.query_value: FORCE_MAIN_MAPPING, FORCE_FALLBACK_MAPPING.query_value: FORCE_FALLBACK_MAPPING}.get(force)
    release, _, eval_metadata = AUS.evaluateRules(parameters, transaction=transaction)
    if not release:
        return Response(status=404)

    headers = get_aus_metadata_headers(eval_metadata)

    response = json.dumps(release.getResponse(parameters, app.config["ALLOWLISTED_DOMAINS"]))

    headers.update(get_content_signature_headers(response, "", use_legacy_key(parameters.get("product"), parameters.get("version"))))

    return Response(response=response, status=200, headers=headers, mimetype="application/json")


get_update_1 = get_update
get_update_2 = get_update
