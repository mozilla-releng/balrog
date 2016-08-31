import aiohttp
import asyncio
import logging
import time

from . import client
from .changes import get_telemetry_uptake, telemetry_is_ready, time_is_ready
from .log import configure_logging


async def run_agent(loop, balrog_api_root, balrog_username, balrog_password, telemetry_api_root, sleeptime=30,
                    once=False, raise_exceptions=False):
    auth = aiohttp.BasicAuth(balrog_username, balrog_password)

    while True:
        try:
            logging.debug("Looking for active scheduled changes...")
            resp = await client.request(balrog_api_root, "/scheduled_changes/rules", auth=auth, loop=loop)
            sc = (await resp.json())["scheduled_changes"]
            resp.close()
            logging.debug("Found %s", len(sc))
            for change in sc:
                logging.debug("Processing change %s", change["sc_id"])
                ready = False

                # Figure out if the change is ready, which is type-specific.
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

                # If it *is* ready, enact it!
                if ready:
                    logging.debug("Change %s is ready, enacting", change["sc_id"])
                    endpoint = "/scheduled_changes/rules/{}/enact".format(change["sc_id"])
                    resp = await client.request(balrog_api_root, endpoint, method="POST", auth=auth, loop=loop)
                    resp.close()
                else:
                    logging.debug("Change %s is not ready", change["sc_id"])

        except:
            logging.error("Encountered exception:", exc_info=True)
            if raise_exceptions:
                raise
        finally:
            if not once:
                await asyncio.sleep(sleeptime)

        if once:
            return


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
