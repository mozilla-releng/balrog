import aiohttp
import asyncio
import logging
import time
import traceback

from . import client


__version__ = 0.1


async def get_telemetry_uptake(*args):
    pass


def is_ready(change, current_uptake=None):
    if change["type"] == "uptake":
        if current_uptake >= change["telemetry_uptake"]:
            return True
    elif change["type"] == "time":
        if time.now() > change["when"]:
            return True
    else:
        logging.warning("Unknown change type!")

    return False


async def run_agent(loop, balrog_api_root, balrog_username, balrog_password, telemetry_api_root, sleeptime=30):
    auth = aiohttp.BasicAuth(balrog_username, balrog_password)

    while True:
        try:
            with aiohttp.ClientSession(loop=loop) as session:
                for change in await client.request(session, balrog_api_root, "/scheduled_changes/rules", auth=auth):
                    current_uptake = None
                    if change["type"] == "uptake":
                        current_uptake = await get_telemetry_uptake(change["telemetry_product"], change["telemetry_channel"])
                    if is_ready(change, current_uptake):
                        # TODO: switch this to a HEAD after https://github.com/KeepSafe/aiohttp/issues/852 is released
                        resp = await client.request(session, balrog_api_root, "/csrf_token", method="GET", auth=auth)
                        data = {"csrf_token": resp["csrf_token"]}
                        await client.request(session, balrog_api_root, "/scheduled_changes/rules/{}".format(change["sc_id"]), method="POST", data=data, auth=auth)

            time.sleep(sleeptime)
        except:
            logging.error(traceback.format_exc())
            time.sleep(sleeptime)


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
