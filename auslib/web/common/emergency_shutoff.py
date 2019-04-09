import json

from connexion import problem
from flask import Response, jsonify

from auslib.global_state import dbo


def get():
    shutoffs = dbo.emergencyShutoffs.select()
    shutoffs_count = len(shutoffs)
    return jsonify(count=shutoffs_count, shutoffs=shutoffs)


def get_by_id(product, channel):
    shutoffs = dbo.emergencyShutoffs.select(where=dict(product=product, channel=channel))
    if not shutoffs:
        return problem(status=404,
                       title="Not Found",
                       detail="Requested emergency shutoff wasn't found",
                       ext={"exception": "Requested shutoff does not exist"})

    headers = {'X-Data-Version': shutoffs[0]['data_version']}

    return Response(response=json.dumps(shutoffs[0]),
                    headers=headers,
                    mimetype="application/json")
