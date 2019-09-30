from flask import current_app as app, jsonify, Response

from auslib.web.public.base import AUS, with_transaction


@with_transaction
def get_update(transaction, **parameters):
    # TODO: should these be required, or make them optional at db layer?
    parameters["headerArchitecture"] = "TODO"
    parameters["force"] = 1 # TODO
    parameters["buildID"] = 1
    parameters["osVersion"] = "TODO"
    parameters["locale"] = "TODO"
    release = AUS.evaluateRules(parameters, transaction=transaction)[0]
    if not release:
        return Response(status=404)

    response = release.getResponse(parameters, app.config["WHITELISTED_DOMAINS"])
    # TODO: should the blob return raw json instead of making us do this?
    return jsonify(response)
