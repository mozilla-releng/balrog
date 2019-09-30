from flask import jsonify

from auslib.web.public.base import with_transaction


@with_transaction
def get_update(transaction, **parameters):
    release = AUS.evaluateRules(query, transaction=transaction)[0]
    if not release:
        return Response(status=404)

    response = release.makeResponse(updateQuery, app.config["WHITELISTED_DOMAINS"])
    return jsonify(response)
