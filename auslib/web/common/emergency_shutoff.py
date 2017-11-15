import json
from auslib.global_state import dbo
from connexion import problem
from flask import jsonify, Response


def get(product=None, channel=None):
    where = {
        k: v for k, v in [('product', product), ('channel', channel)] if v}
    shutoffs = dbo.emergencyShutoff.getEmergencyShutoffs(where)
    shutoffs_count = len(shutoffs)
    return jsonify(count=shutoffs_count, shutoffs=shutoffs)


def get_by_id(shutoff_id):
    shutoff = dbo.emergencyShutoff.getEmergencyShutoff(shutoff_id)
    if not shutoff:
        return problem(status=404,
                       title="Not Found",
                       detail="Requested emergency shutoff wasn't found",
                       ext={"exception": "Requested shutoff does not exist"})

    headers = {'X-Data-Version': shutoff['data_version']}

    return Response(response=json.dumps(shutoff),
                    headers=headers,
                    mimetype="application/json")
