# TODO: shouldn't rely on db layer directly here
from ....db import SignoffRequiredError
from ....global_state import dbo
from ....services import releases


def update_release(name, body):
    with dbo.begin() as trans:
        try:
            new_data_versions = releases.update_release(name, body["blob"], body["old_data_versions"], trans)
            return new_data_versions, 200
        except SignoffRequiredError:
            return "Signoff is required, cannot update Release directly", 400


def overwrite_release(name, body):
    with dbo.begin() as trans:
        try:
            new_data_versions = releases.overwrite_release(name, body["blob"], body["old_data_versions"], trans)
            return new_data_versions, 200
        except SignoffRequiredError:
            return "Signoff is required, cannot update Release directly", 400
