from connexion import NoContent
from flask import request

from ....services import releases
from .problem import problem


def get_all():
    return releases.get_releases(request.transaction, request.args), 200


def get(name):
    ret = releases.get_release(name, request.transaction)
    if ret:
        return ret, 200
    else:
        return problem(404, "Not Found", "Release does not exist")


def get_data_versions(name):
    ret = releases.get_data_versions(name, request.transaction)
    if ret:
        return ret, 200
    else:
        return problem(404, "Not Found", "Release does not exist")


def get_data_version(name, path):
    ret = releases.get_data_version(name, path, request.transaction)
    if ret:
        return ret, 200
    else:
        return problem(404, "Not Found", "Release does not exist")


def update(name, body):
    if not releases.exists(name, request.transaction):
        return problem(404, "Missing", "Release does not exist")
    new_data_versions = releases.update_release(name, body["blob"], body["old_data_versions"], body.get("when"), request.username, request.transaction)
    return new_data_versions, 200


def ensure(name, body):
    new_data_versions = releases.set_release(
        name, body["blob"], body.get("product"), body.get("old_data_versions"), body.get("when"), request.username, request.transaction
    )
    return new_data_versions, 200


def delete(name):
    if releases.exists(name, request.transaction) or releases.sc_exists(name, request.transaction):
        releases.delete_release(name, request.username, request.transaction)
        return NoContent, 200
    else:
        return problem(404, "Not Found", "Release does not exist")


def set_read_only(name, body):
    if not releases.exists(name, request.transaction):
        return problem(404, "Missing", "Release does not exist")
    ret = releases.set_read_only(name, body["read_only"], body["old_data_version"], request.username, request.transaction)
    return ret, 200


def signoff_scheduled_change(name, body):
    if not releases.sc_exists(name, request.transaction):
        return problem(404, "Missing", "Release has no scheduled changes")
    ret = releases.signoff(name, body["role"], request.username, request.transaction)
    return ret, 200


def revoke_signoff_scheduled_change(name):
    if not releases.sc_exists(name, request.transaction):
        return problem(404, "Missing", "Release has no scheduled changes")
    ret = releases.revoke_signoff(name, request.username, request.transaction)
    return ret, 200


def enact_scheduled_changes(name):
    if not releases.sc_exists(name, request.transaction):
        return problem(404, "Missing", "Release has no scheduled changes")
    ret = releases.enact_scheduled_changes(name, request.username, request.transaction)
    return ret, 200


def set_pinnable(name, body):
    if not releases.exists(name, request.transaction):
        return problem(404, "Not Found", "Release does not exist")
    ret = releases.set_pinnable(name, body["product"], body["channel"], body["version"], body.get("when"), request.username, request.transaction)
    return ret, 200
