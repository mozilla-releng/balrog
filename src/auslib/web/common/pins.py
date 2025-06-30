import json

from connexion import problem
from flask import Response, request

from auslib.global_state import dbo


def get_pin(product, channel, version):
    pin_row = dbo.pinnable_releases.getPinRow(product=product, channel=channel, version=version)
    if not pin_row:
        return problem(404, "Not Found", f"Pin for Product='{product}', Channel='{channel}', Version='{version}' not found")

    # getPinRow doesn't include the information that the caller necessarily already knows.
    # Add that back into the row data, for completeness
    pin_row["product"] = product
    pin_row["channel"] = channel
    pin_row["version"] = version

    headers = {"X-Data-Version": pin_row["data_version"]}
    if request.args.get("pretty"):
        indent = 4
        separators = (",", ": ")
    else:
        indent = None
        separators = None
    return Response(response=json.dumps(pin_row, indent=indent, separators=separators, sort_keys=True), mimetype="application/json", headers=headers)
