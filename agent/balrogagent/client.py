import aiohttp
import json


headers = {
    "Accept-Encoding": "application/json",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def get_url(api_root, path):
    return api_root.rstrip("/") + path


async def request(session, api_root, path, method="GET", data=None, auth=None):
    if auth:
        auth = aiohttp.BasicAuth(*auth)
    url = get_url(api_root, path)
    if data:
        data = data.copy()

    if method not in ("GET", "HEAD"):
        # TODO: switch this to a HEAD after https://github.com/KeepSafe/aiohttp/issues/852 is released
        async with session.request("GET", get_url(api_root, "/csrf_token"), headers=headers, auth=auth) as resp:
            if resp.status in range(200, 300):
                data["csrf_token"] = resp.headers["X-CSRF-Token"]

    async with session.request(method, url, data=json.dumps(data), headers=headers, auth=auth) as resp:
        if resp.status in range(200, 300):
            return await resp.json()
        else:
            raise Exception(resp.reason)
