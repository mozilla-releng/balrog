import aiohttp
import asyncio
import asynctest
import json

from ..cmd import run_agent


@asynctest.patch("balrogagent.client.request")
# TODO: why do we have to mock the versions of these imported into cmd isntead
# of mocking balrogagent.changes.*?
@asynctest.patch("balrogagent.cmd.telemetry_is_ready")
@asynctest.patch("balrogagent.cmd.time_is_ready")
class TestRunAgent(asynctest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    async def _runAgent(self, scheduled_changes, request):
        request.return_value = aiohttp.client.ClientResponse("GET", "http://balrog.fake/api/scheduled_changes")
        request.return_value.headers = {"Content-Type": "application/json"}
        body = {"count": len(scheduled_changes), "scheduled_changes": scheduled_changes}
        request.return_value._content = bytes(json.dumps(body), "utf-8")

        return await run_agent(self.loop, "http://balrog.fake", "balrog", "balrog", "telemetry", once=True, raise_exceptions=True)

    async def testNoChanges(self, request, telemetry_is_ready, time_is_ready):
        sc = []
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 0)
        self.assertEquals(request.call_count, 1)

    @asynctest.patch("time.time")
    async def testTimeBasedNotReady(self, request, telemetry_is_ready, time_is_ready, time):
        time.return_value = 0
        time_is_ready.return_value = False
        sc = [{"sc_id": 4, "when": 23456789, "telemetry_uptake": None, "telemetry_product": None, "telemetry_channel": None}]
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 1)
        self.assertEquals(request.call_count, 1)

    @asynctest.patch("time.time")
    async def testTimeBasedIsReady(self, request, telemetry_is_ready, time_is_ready, time):
        time.return_value = 999999999
        time_is_ready.return_value = True
        sc = [{"sc_id": 4, "when": 23456789, "telemetry_uptake": None, "telemetry_product": None, "telemetry_channel": None}]
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 1)
        self.assertEquals(request.call_count, 2)

    @asynctest.patch("balrogagent.cmd.get_telemetry_uptake")
    async def testTelemetryBasedNotReady(self, request, telemetry_is_ready, time_is_ready, get_telemetry_uptake):
        telemetry_is_ready.return_value = False
        get_telemetry_uptake.return_value = 0
        sc = [{"sc_id": 4, "when": None, "telemetry_uptake": 1000, "telemetry_product": "foo", "telemetry_channel": "bar"}]
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 1)
        self.assertEquals(time_is_ready.call_count, 0)
        self.assertEquals(request.call_count, 1)

    @asynctest.patch("balrogagent.cmd.get_telemetry_uptake")
    async def testTelemetryBasedIsReady(self, request, telemetry_is_ready, time_is_ready, get_telemetry_uptake):
        telemetry_is_ready.return_value = True
        get_telemetry_uptake.return_value = 20000
        sc = [{"sc_id": 4, "when": None, "telemetry_uptake": 1000, "telemetry_product": "foo", "telemetry_channel": "bar"}]
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 1)
        self.assertEquals(time_is_ready.call_count, 0)
        self.assertEquals(request.call_count, 2)
