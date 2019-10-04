from flask import current_app as app, jsonify, Response

from auslib.AUS import FORCE_FALLBACK_MAPPING, FORCE_MAIN_MAPPING
from auslib.web.public.base import AUS, with_transaction


@with_transaction
def get_update(transaction, **parameters):
    force = parameters.get("force")
    parameters["force"] = {FORCE_MAIN_MAPPING.query_value: FORCE_MAIN_MAPPING, FORCE_FALLBACK_MAPPING.query_value: FORCE_FALLBACK_MAPPING}.get(force)
    release = AUS.evaluateRules(parameters, transaction=transaction)[0]
    if not release:
        return Response(status=404)

    response = release.getResponse(parameters, app.config["WHITELISTED_DOMAINS"])
    # TODO: sign with autograph here; cache in new in-memory cache
    return jsonify(response)
