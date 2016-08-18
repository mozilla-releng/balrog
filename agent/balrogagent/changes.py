import logging


async def get_telemetry_uptake(*args):
    # TODO: implement this when https://bugzilla.mozilla.org/show_bug.cgi?id=1240522 is fixed
    return -1


def telemetry_is_ready(change, current_uptake):
    logging.debug("Comparing uptake for change %s (current: %s, required: %s", change["sc_id"], current_uptake, change["telemetry_uptake"])
    if current_uptake >= change["telemetry_uptake"]:
        return True
    else:
        return False


def time_is_ready(change, now):
    logging.debug("Comparing time for change %s (now: %s, scheduled time: %s", change["sc_id"], now, change["when"])
    if now >= change["when"]:
        return True
    else:
        return False
