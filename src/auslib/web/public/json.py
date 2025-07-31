import json

from flask import Response
from flask import current_app as app
from flask import g

from auslib.AUS import FORCE_FALLBACK_MAPPING, FORCE_MAIN_MAPPING
from auslib.web.public.helpers import AUS, get_aus_metadata_headers, get_content_signature_headers, with_transaction


@with_transaction
def get_update(transaction, **parameters):
    force = parameters.get("force")
    parameters["force"] = {FORCE_MAIN_MAPPING.query_value: FORCE_MAIN_MAPPING, FORCE_FALLBACK_MAPPING.query_value: FORCE_FALLBACK_MAPPING}.get(force)
    with g.statsd.timer("json.evaluate_rules"):
        release, _, eval_metadata = AUS.evaluateRules(parameters, transaction=transaction)

    if not release:
        return Response(status=404)

    with g.statsd.timer("json.make_response"):
        headers = get_aus_metadata_headers(eval_metadata)
        response = json.dumps(release.getResponse(parameters, app.config["ALLOWLISTED_DOMAINS"]))
        headers.update(get_content_signature_headers(response, ""))

    return Response(response=response, status=200, headers=headers, mimetype="application/json")


get_update_1 = get_update
get_update_2 = get_update
