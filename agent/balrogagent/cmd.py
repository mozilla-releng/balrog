import aiohttp
import asyncio
import logging
import time
import traceback

from . import client
from .changes import get_telemetry_uptake, is_ready
from .log import configure_logging


async def run_agent(loop, balrog_api_root, balrog_username, balrog_password, telemetry_api_root, sleeptime=30):
    auth = aiohttp.BasicAuth(balrog_username, balrog_password)

    while True:
        try:
            async with aiohttp.ClientSession(auth=auth, loop=loop) as session:
                logging.debug("Looking for active scheduled changes...")
                # TODO: sometimes getting "unclosed response" and "unclosed connection" errors.
                resp = await client.request(session, balrog_api_root, "/csrf_token", method="HEAD")
                csrf_token = resp.headers["X-CSRF-Token"]
                resp = await client.request(session, balrog_api_root, "/scheduled_changes/rules")
                sc = (await resp.json())["scheduled_changes"]
                logging.debug("Found %s", len(sc))
                for change in sc:
                    logging.debug("Processing change %s", change["sc_id"])
                    ready_kwargs = {}
                    if change["telemetry_uptake"]:
                        # TODO: maybe replace this with a simple client.request()...
                        ready_kwargs["current_uptake"] = await get_telemetry_uptake(change["telemetry_product"], change["telemetry_channel"], loop=loop)
                    if change["when"]:
                        # "when" is to-the-millisecond timestamp that gets stored as an int.
                        # It needs to be converted back to a float before it can be compared
                        # against other timestamps.
                        change["when"] = change["when"] / 1000
                        ready_kwargs["now"] = time.time()
                    if is_ready(change, **ready_kwargs):
                        logging.debug("Change %s is ready, enacting", change["sc_id"])
                        data = {"csrf_token": csrf_token}
                        endpoint = "/scheduled_changes/rules/{}/enact".format(change["sc_id"])
                        await client.request(session, balrog_api_root, endpoint, method="POST", data=data)

            await asyncio.sleep(sleeptime)
        except:
            logging.error(traceback.format_exc())
            await asyncio.sleep(sleeptime)


def main():
    import os

    logging_kwargs = {
        "level": os.environ.get("LOG_LEVEL", logging.INFO)
    }
    if os.environ.get("LOG_FORMAT") == "plain":
        logging_kwargs["formatter"] = logging.Formatter
    configure_logging(**logging_kwargs)

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
