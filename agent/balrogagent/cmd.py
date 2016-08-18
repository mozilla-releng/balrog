import aiohttp
import asyncio
import logging
import time
import traceback

from . import client
from .changes import get_telemetry_uptake, telemetry_is_ready, time_is_ready
from .log import configure_logging


async def run_agent(loop, balrog_api_root, balrog_username, balrog_password, telemetry_api_root, sleeptime=30):
    auth = aiohttp.BasicAuth(balrog_username, balrog_password)

    while True:
        try:
            async with aiohttp.ClientSession(auth=auth, loop=loop) as session:
                logging.debug("Looking for active scheduled changes...")
                resp = await client.request(session, balrog_api_root, "/scheduled_changes/rules")
                sc = (await resp.json())["scheduled_changes"]
                logging.debug("Found %s", len(sc))
                for change in sc:
                    logging.debug("Processing change %s", change["sc_id"])
                    ready = False

                    if change["telemetry_uptake"]:
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

                    if ready:
                        logging.debug("Change %s is ready, enacting", change["sc_id"])
                        endpoint = "/scheduled_changes/rules/{}/enact".format(change["sc_id"])
                        await client.request(session, balrog_api_root, endpoint, method="POST")
                    else:
                        logging.debug("Change %s is not ready", change["sc_id"])

        except:
            logging.error(traceback.format_exc())
        finally:
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
