import aiohttp
import asyncio
import logging
import time

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


async def run_agent(balrog_api_root, balrog_username, balrog_password, telemetry_api_root, sleeptime=30):
    auth = asyncio.BasicAuth(balrog_username, balrog_password)
    loop = asyncio.get_loop()

    while True:
        with aiohttp.ClientSession(loop=loop) as session:
            for change in await client.request(session, balrog_api_root, "/scheduled_changes/rules", auth=auth):
                current_uptake = None
                if change["type"] == "uptake":
                    current_uptake = await get_telemetry_uptake(change["telemetry_product"], change["telemetry_channel"])
                if is_ready(change, current_uptake):
                    await client.request(session, balrog_api_root, "/scheduled_changes/rules/{}".format(change["sc_id"]), method="POST", auth=auth)

        time.sleep(sleeptime)


def main():
    import os

    run_agent(
        os.environ["BALROG_API_ROOT"], os.environ["BALROG_USERNAME"], os.environ["BALROG_PASSWORD"],
        os.environ["TELEMETRY_API_ROOT"]
    )


if __name__ == "__main__":
    main()
