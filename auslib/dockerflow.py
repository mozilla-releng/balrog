from os import path

from flask import Response, jsonify

from auslib.global_state import dbo


# Wrapper that creates the endpoints required by CloudOps' Dockerflow spec: https://github.com/mozilla-services/Dockerflow
# This gets used by both the admin and public apps.
def create_dockerflow_endpoints(app):
    @app.route("/__version__")
    def version():
        version_file = app.config.get("VERSION_FILE")
        if version_file and path.exists(version_file):
            with open(app.config["VERSION_FILE"]) as f:
                version_json = f.read()
            return Response(version_json, mimetype="application/json")
        else:
            return jsonify({
                "source": "https://github.com/mozilla/balrog",
                "version": "unknown",
                "commit": "unknown",
            })

    @app.route("/__heartbeat__")
    def heartbeat():
        """Per the Dockerflow spec:
        Respond to /__heartbeat__ with a HTTP 200 or 5xx on error. This should
        depend on services like the database to also ensure they are healthy."""
        # Counting the rules should be a trivial enough operation that it won't
        # cause notable load, but will verify that the database works.
        dbo.rules.countRules()
        return "OK!"

    @app.route("/__lbheartbeat__")
    def lbheartbeat():
        """Per the Dockerflow spec:
        Respond to /__lbheartbeat__ with an HTTP 200. This is for load balancer
        checks and should not check any dependent services."""
        return "OK!"
