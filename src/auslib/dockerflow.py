from os import path

from flask import Response, jsonify

from auslib.global_state import dbo


def _heartbeat_database_fn(dbo):
    return dbo.dockerflow.incrementWatchdogValue(changed_by="dockerflow")


def heartbeat_response(heartbeat_database_fn):
    """Per the Dockerflow spec:
    Respond to /__heartbeat__ with a HTTP 200 or 5xx on error. This should
    depend on services like the database to also ensure they are healthy."""
    try:
        database_entry_value = heartbeat_database_fn(dbo)
        return Response(str(database_entry_value), headers={"Cache-Control": "public, max-age=60"})
    except Exception:
        return Response(
            status=502,
            response="Can't connect to the database.",
            headers={"Cache-Control": "public, max-age=60"},
        )


def lbheartbeat_response():
    """Per the Dockerflow spec:
    Respond to /__lbheartbeat__ with an HTTP 200. This is for load balancer
    checks and should not check any dependent services."""
    return Response("OK!", headers={"Cache-Control": "no-cache"})


def get_version(version_file):
    if version_file and path.exists(version_file):
        with open(version_file) as f:
            version_json = f.read()
        return Response(
            version_json, mimetype="application/json", headers={"Cache-Control": "no-cache"}
        )
    else:
        return jsonify(
            {
                "source": "https://github.com/mozilla/balrog",
                "version": "unknown",
                "commit": "unknown",
            }
        )


# Keeping flask dockerflow endpoints here to maintain the admin api compatibility.
def create_dockerflow_endpoints(app, heartbeat_database_fn=_heartbeat_database_fn):
    """ Wrapper that creates the endpoints required by CloudOps' Dockerflow spec:
    https://github.com/mozilla-services/Dockerflow. This gets used by both the admin and public apps.
    :param heartbeat_database_fn: Function that calls the database when reponding to /__heartbeat__.
    A database object is passed to this function.

    If heartbeat_database_fn is None, a default function is be set. The default function writes in a
    dummy table. Even though we respond to GET, we do insert/update something in the database. This
    allows us to see if the connection to the database exists, is active, and if the credentials given
    are the correct ones. For more context see bug 1289178.
    """

    @app.route("/__heartbeat__")
    def heartbeat():
        return heartbeat_response(heartbeat_database_fn)

    @app.route("/__lbheartbeat__")
    def lbheartbeat():
        return lbheartbeat_response()

    @app.route("/__version__")
    def version():
        version_file = app.config.get("VERSION_FILE")
        return get_version(version_file)
