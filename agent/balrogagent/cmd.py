import aiohttp
import asyncio
import logging
import time
import traceback

from . import client


async def get_telemetry_uptake(*args):
    pass


def is_ready(change, current_uptake=None):
    if change.get("telemetry_uptake"):
        logging.debug("Comparing uptake for change %s (current: %s, required: %s", change["sc_id"], current_uptake, change["telemetry_uptake"])
        if current_uptake >= change["telemetry_uptake"]:
            return True
    elif change.get("when"):
        now = time.time()
        logging.debug("Comparing time for change %s (now: %s, scheduled time: %s", change["sc_id"], now, change["when"])
        if time.time() >= change["when"]:
            return True
    else:
        logging.warning("Unknown change type!")

    logging.debug("Change %s is not ready", change["sc_id"])
    return False


async def run_agent(loop, balrog_api_root, balrog_username, balrog_password, telemetry_api_root, sleeptime=30):
    auth = aiohttp.BasicAuth(balrog_username, balrog_password)

    while True:
        try:
            # TODO: switch this to a HEAD after https://github.com/KeepSafe/aiohttp/issues/852 is released
            resp = await client.request(balrog_api_root, "/csrf_token", method="GET", auth=auth, loop=loop)
            csrf_token = resp["csrf_token"]
            for change in (await client.request(balrog_api_root, "/scheduled_changes/rules", auth=auth, loop=loop))["scheduled_changes"]:
                logging.debug("Processing change %s", change["sc_id"])
                current_uptake = None
                if change["telemetry_uptake"]:
                    # TODO: probably replace this with a simple client.request()...
                    current_uptake = await get_telemetry_uptake(change["telemetry_product"], change["telemetry_channel"], loop=loop)
                if change["when"]:
                    change["when"] = change["when"] / 1000
                if is_ready(change, current_uptake):
                    logging.debug("Change %s is ready, enacting", change["sc_id"])
                    data = {"csrf_token": csrf_token}
                    endpoint = "/scheduled_changes/rules/{}/enact".format(change["sc_id"])
                    await client.request(balrog_api_root, endpoint, method="POST", data=data, auth=auth, loop=loop)

            await asyncio.sleep(sleeptime)
        except:
            logging.error(traceback.format_exc())
            await asyncio.sleep(sleeptime)


def main():
    import os

    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        run_agent(
            loop,
            os.environ["BALROG_API_ROOT"], os.environ["BALROG_USERNAME"], os.environ["BALROG_PASSWORD"],
            os.environ["TELEMETRY_API_ROOT"]
        )
    )


if __name__ == "__main__":
    main()
