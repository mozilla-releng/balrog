from flask import current_app as app, jsonify, Response

from auslib.web.public.base import AUS, with_transaction


@with_transaction
def get_update(transaction, **parameters):
    release = AUS.evaluateRules(parameters, transaction=transaction)[0]
    if not release:
        return Response(status=404)

    response = release.getResponse(parameters, app.config["WHITELISTED_DOMAINS"])
    # TODO: sign with autograph here; cache in new in-memory cache
    return jsonify(response)
