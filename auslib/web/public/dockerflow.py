from flask import current_app

from auslib.dockerflow import get_version, heartbeat_response, lbheartbeat_response


def heartbeat():
    # web has only a read access to the database. That's why we don't use
    # the default database function.
    # Counting the rules should be a trivial enough operation that it won't
    # cause notable load, but will verify that the database works.
    return heartbeat_response(lambda dbo: dbo.rules.count())


def lbheartbeat():
    return lbheartbeat_response()


def version():
    version_file = current_app.config.get("VERSION_FILE")
    return get_version(version_file)
