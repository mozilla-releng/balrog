import json

import aiohttp
import asynctest
from yarl import URL

from .. import client


class fake_request:
    def __init__(self, response_body, response_code):
        self.response_body = response_body
        self.response_code = response_code
        self.csrf_resp = None
        self.request_data = None

    async def __call__(self, method, url, loop=None, data={}, **kwargs):
        if url.endswith("csrf_token"):
            self.csrf_resp = aiohttp.client.ClientResponse(
                "HEAD",
                URL("http://balrog.fake/api/csrf_token"),
                writer=None,
                continue100=None,
                timer=None,
                request_info=None,
                auto_decompress=None,
                traces=None,
                loop=loop,
                session=None,
            )
            self.csrf_resp.headers = {"X-CSRF-Token": "foo"}
            self.csrf_resp.status = 200
            return self.csrf_resp
        else:
            self.request_data = data
            resp = aiohttp.client.ClientResponse(
                method, URL(url), writer=None, continue100=None, timer=None, request_info=None, auto_decompress=None, traces=None, loop=loop, session=None
            )
            resp.headers = {"Content-Type": "application/json"}
            resp._body = bytes(json.dumps(self.response_body), "utf-8")
            resp.status = self.response_code
            return resp


class TestBalrogClient(asynctest.TestCase):
    async def testGET(self):
        mocked_resp = {
            "count": 2,
            "scheduled_changes": [
                {"sc_id": 1, "when": 123456789},
                {"sc_id": 2, "telemetry_product": "Firefox", "telemetry_channel": "release", "telemetry_uptake": 3000},
            ],
        }
        with asynctest.patch("aiohttp.request", fake_request(mocked_resp, 200)) as r:
            resp = await client.request("http://balrog.fake", "/api/scheduled_changes", loop=self.loop)
            # GET requests shouldn't retrieve a CSRF token
            self.assertEqual(r.csrf_resp, None)
            self.assertEqual(json.loads(r.request_data), {})
            self.assertEqual(mocked_resp, await resp.json())

    async def testPOST(self):
        mocked_resp = {"new_data_version": 2}
        with asynctest.patch("aiohttp.request", fake_request(mocked_resp, 200)) as r:
            resp = await client.request("http://balrog.fake", "/api/scheduled_changes/1", method="POST", data={"when": 987654321}, loop=self.loop)
            self.assertEqual(r.csrf_resp.headers, {"X-CSRF-Token": "foo"})
            self.assertEqual(json.loads(r.request_data), {"csrf_token": "foo", "when": 987654321})
            self.assertEqual(mocked_resp, await resp.json())
