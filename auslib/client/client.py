import asyncio
import aiohttp
import json
import logging


headers = {
    "Accept-Encoding": "application/json",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

def get_url(api_root, path):
    return api_root.rstrip("/") + path


async def request(session, api_root, path, method="GET", data=None, auth=None):
    url = get_url(api_root, path)
    if data:
        data = data.copy()

    if method not in ("GET", "HEAD"):
        resp = await session.request("HEAD", get_url(api_root, "/csrf_token"), auth=auth)
        if resp.status in range(200, 300):
            data["csrf_token"] = resp.headers["X-CSRF-Token"]
        else:
            raise Exception("fail!")

    resp = await session.request(method, url, data=json.dumps(data), headers=headers, auth=auth)
    if resp.status in range(200, 300):
        return await resp.json()
    else:
        raise Exception(resp.reason)


# get rule
# modify rule
# update rule

loop = asyncio.get_event_loop()
#with aiohttp.ClientSession(loop=loop) as session:
#    fut = asyncio.ensure_future(request(session, "http://localhost:8080/api", "/rules/69"))
#    fut.add_done_callback(lambda x: print("Here: {}", x.result()))
#
#    loop.run_until_complete(fut)


async def change_rule():
    with aiohttp.ClientSession(loop=loop) as session:
        res = await request(session, "http;//localhost:8080/api", "/rules/69")
        res["comment"] = "WTF"
        return await request(session, http://localhost:8080/api, "/rules/69", method="POST", data=res)

loop.run_until_complete(change_rule)
