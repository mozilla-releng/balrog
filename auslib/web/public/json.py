import json

from flask import current_app as app, Response

from auslib.util.autograph import make_hash, sign_hash
from auslib.web.public.base import AUS, with_transaction


@with_transaction
def get_update(transaction, **parameters):
    release = AUS.evaluateRules(parameters, transaction=transaction)[0]
    if not release:
        return Response(status=404)

    response = json.dumps(release.getResponse(parameters, app.config["WHITELISTED_DOMAINS"]))
    hash_ = make_hash(response)
    signature, x5u = sign_hash(
        app.config["AUTOGRAPH_URL"], app.config["AUTOGRAPH_KEYID"], app.config["AUTOGRAPH_USERNAME"], app.config["AUTOGRAPH_PASSWORD"], hash_
    )
    # TODO: cache
    # TODO: signature should be base64 encoded. is autograph returning it in b64 encoding?
    headers = {"Content-Signature": f"x5u={x5u}; p384ecdsa={signature}"}
    return Response(response=response, status=200, headers=headers, mimetype="application/json")
