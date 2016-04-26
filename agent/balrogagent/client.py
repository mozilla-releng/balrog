import aiohttp
import json


headers = {
    "Accept-Encoding": "application/json",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def get_url(api_root, path):
    return api_root.rstrip("/") + path


async def request(api_root, path, method="GET", data=None, auth=None, loop=None):
    if auth:
        auth = aiohttp.BasicAuth(*auth)
    url = get_url(api_root, path)
    if data:
        data = data.copy()

    async with aiohttp.request(method, url, data=json.dumps(data), headers=headers, auth=auth, loop=loop) as resp:
        if resp.status in range(200, 300):
            return await resp.json()
        else:
            raise Exception(resp.reason)
