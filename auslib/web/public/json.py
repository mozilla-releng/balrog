import json

from flask import current_app as app, Response

from auslib.AUS import FORCE_FALLBACK_MAPPING, FORCE_MAIN_MAPPING
from auslib.global_state import cache
from auslib.util.autograph import make_hash, sign_hash
from auslib.web.public.base import AUS, with_transaction


@with_transaction
def get_update(transaction, **parameters):
    force = parameters.get("force")
    parameters["force"] = {FORCE_MAIN_MAPPING.query_value: FORCE_MAIN_MAPPING, FORCE_FALLBACK_MAPPING.query_value: FORCE_FALLBACK_MAPPING}.get(force)
    release = AUS.evaluateRules(parameters, transaction=transaction)[0]
    if not release:
        return Response(status=404)

    response = json.dumps(release.getResponse(parameters, app.config["WHITELISTED_DOMAINS"]))
    hash_ = make_hash(response)

    def sign():
        return sign_hash(app.config["AUTOGRAPH_URL"], app.config["AUTOGRAPH_KEYID"], app.config["AUTOGRAPH_USERNAME"], app.config["AUTOGRAPH_PASSWORD"], hash_)

    signature, x5u = cache.get("content_signatures", hash_, sign)
    headers = {"Content-Signature": f"x5u={x5u}; p384ecdsa={signature}"}
    return Response(response=response, status=200, headers=headers, mimetype="application/json")
