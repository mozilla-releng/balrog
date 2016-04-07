import asyncio
import aiohttp
import logging


class APIClient(object):
    
    def __init__(self, event_loop, api_root="http://localhost:8080/api", auth=None, timeout=60):
        self.event_loop = event_loop
        self.api_root = api_root.rstrip("/")
        self.auth = auth
        self.timeout = timeout

    async def request(self, path, method="GET", data=None):
        url = self.api_root + path
        logging.debug("Preparing request to %s", url)
        if data:
            data = data.copy()

        with aiohttp.ClientSession(loop=self.event_loop) as session:
            if method not in ("GET", "HEAD"):
                resp = await self.do_request(session, url, "HEAD")
                if resp.status in range(200, 300):
                    if "data_version" not in data:
                        data["data_version"] = resp.headers["X-Data-Version"]
                    data["csrf_token"] = resp.headers["X-CSRF-Token"]
                elif resp.status == 404:
                    resp = await self.do_request(session, self.api_root + "/csrf_token", "HEAD")
                    data["csrf_token"] = resp.headers["X-CSRF_Token"]
                else:
                    raise Exception("fail")

            resp = await self.do_request(session, url, method, data)
            if resp.status in range(200, 300):
                return await resp.json()
            else:
                raise Exception("fail")

    async def do_request(self, session, url, method, data=None):
        headers = {
            "Accept-Encoding": "application/json",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        logging.debug("Making request to %s", url)
        with aiohttp.Timeout(self.timeout):
            return await session.request(method, url, data=data, headers=headers, auth=self.auth)
