import aiohttp
import asyncio
import asynctest
import json

from ..cmd import run_agent


@asynctest.patch("balrogagent.client.request")
@asynctest.patch("balrogagent.cmd.telemetry_is_ready")
@asynctest.patch("balrogagent.cmd.time_is_ready")
class TestRunAgent(asynctest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    async def _runAgent(self, scheduled_changes, request):
        def side_effect(balrog_api_root, endpoint, auth, loop, method='GET'):
            if 'required_signoffs' in endpoint:
                endpoint = '/'.join(endpoint.split('/')[-2:])
            else:
                endpoint = endpoint.split('/')[-1]
            response = aiohttp.client.ClientResponse("GET",
                                                     "http://balrog.fake/scheduled_changes/%s" % endpoint)
            response.headers = {"Content-Type": "application/json"}
            changes = scheduled_changes.get(endpoint) or []
            if method != 'GET':
                body = ""
            else:
                body = {"count": len(changes), "scheduled_changes": changes}
            response._content = bytes(json.dumps(body), "utf-8")
            return response

        request.side_effect = side_effect

        return await run_agent(self.loop, "http://balrog.fake", "balrog", "balrog", "telemetry", once=True, raise_exceptions=True)

    @asynctest.patch("time.time")
    async def testSignoffsAbsent(self, time, time_is_ready, telemetry_is_ready, request):
        time.return_value = 999999999
        time_is_ready.return_value = True
        sc = {'permissions': [{"priority": None, "sc_id": 4,
                               "when": 234,
                               "telemetry_uptake": None,
                               "telemetry_product": None,
                               "telemetry_channel": None,
                               "signoffs": {"mary": "relman"},
                               "required_signoffs": {"releng": 1, "relman": 1}},
                              {"priority": None, "sc_id": 5,
                               "when": 234,
                               "telemetry_uptake": None,
                               "telemetry_product": None,
                               "telemetry_channel": None,
                               "signoffs": {"bill": "releng", "mary": "relman"},
                               "required_signoffs": {"releng": 1, "relman": 1}}]}
        await self._runAgent(sc, request)
