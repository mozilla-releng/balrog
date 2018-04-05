import aiohttp
import json
import logging


default_headers = {
    "Accept-Encoding": "application/json",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def get_url(api_root, path):
    return api_root.rstrip("/") + path


async def request(api_root, path, method="GET", data={}, headers=default_headers, auth=None, loop=None):
    headers = headers.copy()
    url = get_url(api_root, path)
    csrf_url = get_url(api_root, "/csrf_token")
    data = data.copy()

    # CSRF tokens are only required for POST/PUT/DELETE.
    if method not in ("HEAD", "GET"):
        logging.debug("Sending %s request to %s", "HEAD", csrf_url)
        async with aiohttp.request("HEAD", csrf_url, auth=auth, loop=loop) as resp:
            resp.raise_for_status()
            data["csrf_token"] = resp.headers["X-CSRF-Token"]

    logging.debug("Sending %s request to %s", method, url)
    async with aiohttp.request(method, url, data=json.dumps(data), headers=headers, auth=auth, loop=loop) as resp:
        # Raises on 400 code or higher, we can assume things are good if we make it past this.
        resp.raise_for_status()
        return (await resp.json())
