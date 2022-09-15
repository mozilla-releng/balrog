from flask import request

from auslib.global_state import dbo

from .problem import problem


def get_pin(product, channel, version):
    pin_row = dbo.pinnable_releases.getPinRow(product=product, channel=channel, version=version, transaction=request.transaction)
    if pin_row:
        # getPinRow doesn't include the information that the caller necessarily already knows.
        # Add that back into the row data, for completeness
        pin_row["product"] = product
        pin_row["channel"] = channel
        pin_row["version"] = version

        return pin_row, 200
    else:
        return problem(404, "Not Found", "Pin does not exist")
