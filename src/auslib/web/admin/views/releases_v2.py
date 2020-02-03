from flask import request

# TODO: shouldn't rely on db layer directly here
from ....db import SignoffRequiredError
from ....services import releases


def update_release(name, body):
    try:
        new_data_versions = releases.update_release(name, body["blob"], body["old_data_versions"], request.transaction)
        return new_data_versions, 200
    except SignoffRequiredError:
        return "Signoff is required, cannot update Release directly", 400


def overwrite_release(name, body):
    try:
        new_data_versions = releases.overwrite_release(name, body["blob"], body["old_data_versions"], request.transaction)
        return new_data_versions, 200
    except SignoffRequiredError:
        return "Signoff is required, cannot update Release directly", 400
