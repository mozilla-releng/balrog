import asyncio
import logging
import time
from collections import defaultdict

from . import client
from .changes import get_telemetry_uptake, telemetry_is_ready, time_is_ready
from .log import configure_logging

V1_SCHEDULED_CHANGE_ENDPOINTS = [
    "rules",
    "releases",
    "permissions",
    "emergency_shutoff",
    "required_signoffs/product",
    "required_signoffs/permissions",
    "pinnable_releases",
]
V2_SCHEDULED_CHANGE_ENDPOINTS = ["/v2/releases"]


async def process_v1_scheduled_changes(loop, balrog_api_root, auth0_secrets):
    for endpoint in V1_SCHEDULED_CHANGE_ENDPOINTS:
        logging.debug("Looking for active scheduled changes for endpoint %s..." % endpoint)
        resp = await client.request(balrog_api_root, "/scheduled_changes/%s" % endpoint, loop=loop, auth0_secrets=auth0_secrets)
        sc = resp["scheduled_changes"]
        if endpoint == "rules":
            # Rules are sorted by priority, when available. Deletions will not have
            # a priority set, so we treat them as the lowest priority possible.
            sc = sorted(sc, key=lambda k: (k["when"], k["priority"] or 0), reverse=True)
        logging.debug("Found %s", len(sc))
        for change in sc:
            logging.debug("Processing change %s", change["sc_id"])
            ready = False

            # Figure out if the change is ready, which is type-specific.
            if change.get("telemetry_uptake"):
                # TODO: maybe replace this with a simple client.request()...
                current_uptake = await get_telemetry_uptake(change["telemetry_product"], change["telemetry_channel"], loop=loop)
                ready = telemetry_is_ready(change, current_uptake)
            elif change["when"]:
                # "when" is to-the-millisecond timestamp that gets stored as an int.
                # It needs to be converted back to a float before it can be compared
                # against other timestamps.
                ready = time_is_ready(change, time.time())
            else:
                logging.debug("Unknown change type!")

            # Check if all the required signoffs have been obtained
            required_signoffs = change.get("required_signoffs") or {}
            signoffs = change.get("signoffs") or {}
            if not verify_signoffs(required_signoffs, signoffs):
                logging.debug("Signoff requirements unmet, marking as not ready")
                ready = False

            # If we have all required signoffs, go ahead
            if ready:
                logging.debug("Change %s is ready, enacting", change["sc_id"])
                url = "/scheduled_changes/{}/{}/enact".format(endpoint, change["sc_id"])
                await client.request(balrog_api_root, url, method="POST", auth0_secrets=auth0_secrets, loop=loop)
            else:
                logging.debug("Change %s is not ready", change["sc_id"])


async def process_v2_scheduled_changes(loop, balrog_api_root, auth0_secrets):
    for endpoint in V2_SCHEDULED_CHANGE_ENDPOINTS:
        logging.debug(f"Looking for active scheduled changes for endpoint {endpoint}...")
        resp = await client.request(balrog_api_root, endpoint, loop=loop, auth0_secrets=auth0_secrets)
        for r in filter(lambda r: len(r["scheduled_changes"]) > 0, resp.get("releases", [])):
            t = time.time()
            required_signoffs = r.get("required_signoffs", {})
            if all([time_is_ready(sc, t) and verify_signoffs(required_signoffs, sc.get("signoffs", {})) for sc in r["scheduled_changes"]]):
                logging.debug(f"Change for {r['name']} is ready, enacting")
                await client.request(balrog_api_root, f"{endpoint}/{r['name']}/enact", method="POST", auth0_secrets=auth0_secrets, loop=loop)


async def run_agent(loop, balrog_api_root, telemetry_api_root, auth0_secrets, sleeptime=30, once=False, raise_exceptions=False):
    while True:
        try:
            await process_v1_scheduled_changes(loop, balrog_api_root, auth0_secrets)
            await process_v2_scheduled_changes(loop, balrog_api_root, auth0_secrets)

        except Exception:
            logging.error("Encountered exception:", exc_info=True)
            if raise_exceptions:
                raise
        finally:
            if not once:
                await asyncio.sleep(sleeptime)

        if once:
            return


def verify_signoffs(required_signoffs, signoffs):
    obtained_signoffs = defaultdict(int)
    for user, role in signoffs.items():
        obtained_signoffs[role] += 1
    for role, number in required_signoffs.items():
        if required_signoffs.get(role, 0) > obtained_signoffs[role]:
            return False
    return True


def main():
    import os

    logging_kwargs = {"level": os.environ.get("LOG_LEVEL", logging.INFO)}
    if os.environ.get("LOG_FORMAT") == "plain":
        logging_kwargs["formatter"] = logging.Formatter
    if os.environ.get("SENTRY_DSN"):
        logging_kwargs["sentry_dsn"] = os.environ["SENTRY_DSN"]
    configure_logging(**logging_kwargs)
    auth0_secrets = dict(
        domain=os.environ["AUTH0_DOMAIN"],
        audience=os.environ["AUTH0_AUDIENCE"],
        client_id=os.environ["AUTH0_M2M_CLIENT_ID"],
        client_secret=os.environ["AUTH0_M2M_CLIENT_SECRET"],
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_agent(loop, os.environ["BALROG_API_ROOT"], os.environ["TELEMETRY_API_ROOT"], auth0_secrets=auth0_secrets))


if __name__ == "__main__":
    main()
