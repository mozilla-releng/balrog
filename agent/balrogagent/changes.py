import logging


async def get_telemetry_uptake(*args):
    # TODO: implement this when https://bugzilla.mozilla.org/show_bug.cgi?id=1240522 is fixed
    pass


def is_ready(change, now=None, current_uptake=None):
    if change.get("telemetry_uptake"):
        logging.debug("Comparing uptake for change %s (current: %s, required: %s", change["sc_id"], current_uptake, change["telemetry_uptake"])
        if current_uptake >= change["telemetry_uptake"]:
            return True
    elif change.get("when"):
        logging.debug("Comparing time for change %s (now: %s, scheduled time: %s", change["sc_id"], now, change["when"])
        if now >= change["when"]:
            return True
    else:
        logging.warning("Unknown change type!")

    logging.debug("Change %s is not ready", change["sc_id"])
    return False
