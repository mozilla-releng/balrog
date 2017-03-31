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

    async def testNoChanges(self, time_is_ready, telemetry_is_ready, request):
        sc = {}
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 0)
        self.assertEquals(request.call_count, 5)

    @asynctest.patch("time.time")
    async def testTimeBasedNotReadyRules(self, time, time_is_ready, telemetry_is_ready, request):
        time.return_value = 0
        time_is_ready.return_value = False
        sc = {'rules': [{"priority": None, "sc_id": 4, "when": 23456789, "telemetry_uptake": None, "telemetry_product": None, "telemetry_channel": None}]}
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 1)
        self.assertEquals(request.call_count, 5)

    @asynctest.patch("time.time")
    async def testTimeBasedNotReadyReleases(self, time, time_is_ready, telemetry_is_ready, request):
        time.return_value = 0
        time_is_ready.return_value = False
        sc = {'releases': [{"priority": None, "sc_id": 4, "when": 23456789, "telemetry_uptake": None, "telemetry_product": None, "telemetry_channel": None}]}
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 1)
        self.assertEquals(request.call_count, 5)

    @asynctest.patch("time.time")
    async def testTimeBasedNotReadyPermissions(self, time, time_is_ready, telemetry_is_ready, request):
        time.return_value = 0
        time_is_ready.return_value = False
        sc = {'permissions': [{"priority": None, "sc_id": 4, "when": 23456789, "telemetry_uptake": None, "telemetry_product": None, "telemetry_channel": None}]}
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 1)
        self.assertEquals(request.call_count, 5)

    @asynctest.patch("time.time")
    async def testTimeBasedIsNotReadyRequiredSignoffs(self, time, time_is_ready, telemetry_is_ready, request):
        time.return_value = 0
        time_is_ready.return_value = False
        sc = {'required_signoffs/product': [{"priority": None, "sc_id": 4, "when": 23456789,
                                             "telemetry_uptake": None,
                                             "telemetry_product": None,
                                             "telemetry_channel": None}],
              'required_signoffs/permissions': [{"priority": None, "sc_id": 4, "when": 23456789,
                                                 "telemetry_uptake": None,
                                                 "telemetry_product": None,
                                                 "telemetry_channel": None}]}
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 2)
        self.assertEquals(request.call_count, 5)

    @asynctest.patch("time.time")
    async def testTimeBasedIsReadyRules(self, time, time_is_ready, telemetry_is_ready, request):
        time.return_value = 999999999
        time_is_ready.return_value = True
        sc = {'rules': [{"priority": None, "sc_id": 4, "when": 234, "telemetry_uptake": None, "telemetry_product": None, "telemetry_channel": None}]}
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 1)
        self.assertEquals(request.call_count, 6)

    @asynctest.patch("time.time")
    async def testTimeBasedIsReadyReleases(self, time, time_is_ready, telemetry_is_ready, request):
        time.return_value = 999999999
        time_is_ready.return_value = True
        sc = {'releases': [{"priority": None, "sc_id": 4, "when": 234, "telemetry_uptake": None, "telemetry_product": None, "telemetry_channel": None}]}
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 1)
        self.assertEquals(request.call_count, 6)

    @asynctest.patch("time.time")
    async def testTimeBasedIsReadyPermissions(self, time, time_is_ready, telemetry_is_ready, request):
        time.return_value = 999999999
        time_is_ready.return_value = True
        sc = {'permissions': [{"priority": None, "sc_id": 4, "when": 234, "telemetry_uptake": None, "telemetry_product": None, "telemetry_channel": None}]}
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 1)
        self.assertEquals(request.call_count, 6)

    @asynctest.patch("time.time")
    async def testTimeBasedIsReadyRequiredSignoffs(self, time, time_is_ready, telemetry_is_ready, request):
        time.return_value = 999999999
        time_is_ready.return_value = True
        sc = {'required_signoffs/product': [{"priority": None, "sc_id": 4, "when": 234,
                                             "telemetry_uptake": None,
                                             "telemetry_product": None,
                                             "telemetry_channel": None}],
              'required_signoffs/permissions': [{"priority": None, "sc_id": 4, "when": 234,
                                                 "telemetry_uptake": None,
                                                 "telemetry_product": None,
                                                 "telemetry_channel": None}]}
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 2)
        self.assertEquals(request.call_count, 7)

    @asynctest.patch("balrogagent.cmd.get_telemetry_uptake")
    async def testTelemetryBasedNotReady(self, get_telemetry_uptake, time_is_ready, telemetry_is_ready, request):
        telemetry_is_ready.return_value = False
        get_telemetry_uptake.return_value = 0
        sc = {'rules': [{"priority": None, "sc_id": 4, "when": None, "telemetry_uptake": 1000, "telemetry_product": "foo", "telemetry_channel": "bar"}]}
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 1)
        self.assertEquals(time_is_ready.call_count, 0)
        self.assertEquals(request.call_count, 5)

    @asynctest.patch("balrogagent.cmd.get_telemetry_uptake")
    async def testTelemetryBasedIsReady(self, get_telemetry_uptake, time_is_ready, telemetry_is_ready, request):
        telemetry_is_ready.return_value = True
        get_telemetry_uptake.return_value = 20000
        sc = {'rules': [{"priority": None, "sc_id": 4, "when": None, "telemetry_uptake": 1000, "telemetry_product": "foo", "telemetry_channel": "bar"}]}
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 1)
        self.assertEquals(time_is_ready.call_count, 0)
        self.assertEquals(request.call_count, 6)

    @asynctest.patch("time.time")
    async def testMultipleEndpointsAtOnce(self, time, time_is_ready, telemetry_is_ready, request):
        time.return_value = 999999999
        time_is_ready.return_value = True
        sc = {'releases': [{"priority": None, "sc_id": 4, "when": 234, "telemetry_uptake": None, "telemetry_product": None, "telemetry_channel": None}],
              'rules': [{"priority": None, "sc_id": 5, "when": 234, "telemetry_uptake": None, "telemetry_product": None, "telemetry_channel": None}],
              'permissions': [{"priority": None, "sc_id": 6, "when": 234, "telemetry_uptake": None, "telemetry_product": None, "telemetry_channel": None}]}
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 3)
        self.assertEquals(request.call_count, 8)

    @asynctest.patch("time.time")
    async def testMultipleChangesOneEndpoint(self, time, time_is_ready, telemetry_is_ready, request):
        time.return_value = 999999999
        time_is_ready.return_value = True
        sc = {'releases': [{"priority": None, "sc_id": 4, "when": 234, "telemetry_uptake": None,
                            "telemetry_product": None, "telemetry_channel": None},
                           {"priority": None, "sc_id": 5, "when": 234, "telemetry_uptake": None,
                            "telemetry_product": None, "telemetry_channel": None},
                           {"priority": None, "sc_id": 6, "when": 234, "telemetry_uptake": None,
                            "telemetry_product": None, "telemetry_channel": None}]}
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 3)
        self.assertEquals(request.call_count, 8)
        called_endpoints = [call[0][1] for call in request.call_args_list]
        self.assertIn('/scheduled_changes/releases', called_endpoints)
        self.assertIn('/scheduled_changes/permissions', called_endpoints)
        self.assertIn('/scheduled_changes/rules', called_endpoints)
        self.assertIn('/scheduled_changes/releases/4/enact', called_endpoints)
        self.assertIn('/scheduled_changes/releases/5/enact', called_endpoints)
        self.assertIn('/scheduled_changes/releases/6/enact', called_endpoints)

    @asynctest.patch("time.time")
    async def testSignoffsPresent(self, time, time_is_ready, telemetry_is_ready, request):
        time.return_value = 999999999
        time_is_ready.return_value = True
        sc = {'permissions': [{"priority": None, "sc_id": 4,
                               "when": 234,
                               "telemetry_uptake": None,
                               "telemetry_product": None,
                               "telemetry_channel": None,
                               "signoffs": {"bill": "releng", "mary": "relman"},
                               "required_signoffs": {"releng": 1, "relman": 1}}]}
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 1)
        self.assertEquals(request.call_count, 6)

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
                               "required_signoffs": {"releng": 1, "relman": 1}}]}
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 1)
        self.assertEquals(request.call_count, 5)

    @asynctest.patch("time.time")
    async def testRightEnactOrderForMultipleChangesOneEndpoint(self, time, time_is_ready, telemetry_is_ready, request):
        time.return_value = 999999999
        time_is_ready.return_value = True
        sc = {'releases': [{"priority": 1, "sc_id": 4, "when": 234, "telemetry_uptake": None,
                            "telemetry_product": None, "telemetry_channel": None},
                           {"priority": 2, "sc_id": 5, "when": 234, "telemetry_uptake": None,
                            "telemetry_product": None, "telemetry_channel": None},
                           {"priority": 1, "sc_id": 6, "when": 378, "telemetry_uptake": None,
                            "telemetry_product": None, "telemetry_channel": None},
                           {"priority": 2, "sc_id": 7, "when": 187, "telemetry_uptake": None,
                            "telemetry_product": None, "telemetry_channel": None},
                           {"priority": 2, "sc_id": 8, "when": 1000, "telemetry_uptake": None,
                            "telemetry_product": None, "telemetry_channel": None},
                           {"priority": 4, "sc_id": 9, "when": 74, "telemetry_uptake": None,
                            "telemetry_product": None, "telemetry_channel": None},
                           {"priority": 3, "sc_id": 10, "when": 543, "telemetry_uptake": None,
                            "telemetry_product": None, "telemetry_channel": None}
                           ]}
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 7)
        self.assertEquals(request.call_count, 12)
        called_endpoints = [call[0][1] for call in request.call_args_list]
        called_endpoints = called_endpoints[2:9]  # the list slice returns only the enacted endpoints
        self.assertEquals(called_endpoints.index('/scheduled_changes/releases/4/enact'), 6)
        self.assertEquals(called_endpoints.index('/scheduled_changes/releases/5/enact'), 3)
        self.assertEquals(called_endpoints.index('/scheduled_changes/releases/6/enact'), 5)
        self.assertEquals(called_endpoints.index('/scheduled_changes/releases/7/enact'), 4)
        self.assertEquals(called_endpoints.index('/scheduled_changes/releases/8/enact'), 2)
        self.assertEquals(called_endpoints.index('/scheduled_changes/releases/9/enact'), 0)
        self.assertEquals(called_endpoints.index('/scheduled_changes/releases/10/enact'), 1)

    @asynctest.patch("time.time")
    async def testRightEnactOrderForMultipleEndpointsAtOnce(self, time, time_is_ready, telemetry_is_ready, request):
        time.return_value = 999999999
        time_is_ready.return_value = True
        sc = {'releases': [{"priority": 1, "sc_id": 4, "when": 234, "telemetry_uptake": None,
                            "telemetry_product": None, "telemetry_channel": None},
                           {"priority": 2, "sc_id": 5, "when": 234, "telemetry_uptake": None,
                            "telemetry_product": None, "telemetry_channel": None},
                           {"priority": 1, "sc_id": 6, "when": 378, "telemetry_uptake": None,
                            "telemetry_product": None, "telemetry_channel": None},
                           {"priority": 2, "sc_id": 7, "when": 187, "telemetry_uptake": None,
                            "telemetry_product": None, "telemetry_channel": None}],
              'rules': [{"priority": 100, "sc_id": 1, "when": 23400, "telemetry_uptake": None,
                         "telemetry_product": None, "telemetry_channel": None},
                        {"priority": 300, "sc_id": 2, "when": 7000, "telemetry_uptake": None,
                         "telemetry_product": None, "telemetry_channel": None},
                        {"priority": 50, "sc_id": 3, "when": 329, "telemetry_uptake": None,
                         "telemetry_product": None, "telemetry_channel": None}],
              'permissions': [{"priority": 600, "sc_id": 8, "when": 45400, "telemetry_uptake": None,
                               "telemetry_product": None, "telemetry_channel": None},
                              {"priority": 600, "sc_id": 9, "when": 98000, "telemetry_uptake": None,
                               "telemetry_product": None, "telemetry_channel": None},
                              {"priority": 600, "sc_id": 10, "when": 5000, "telemetry_uptake": None,
                               "telemetry_product": None, "telemetry_channel": None}]

              }
        await self._runAgent(sc, request)
        self.assertEquals(telemetry_is_ready.call_count, 0)
        self.assertEquals(time_is_ready.call_count, 10)
        self.assertEquals(request.call_count, 15)
        called_endpoints = [call[0][1] for call in request.call_args_list]
        self.assertLess(called_endpoints.index('/scheduled_changes/rules'), called_endpoints.index('/scheduled_changes/releases'))
        self.assertLess(called_endpoints.index('/scheduled_changes/releases'), called_endpoints.index('/scheduled_changes/permissions'))
        self.assertLess(called_endpoints.index('/scheduled_changes/releases/5/enact'), called_endpoints.index('/scheduled_changes/releases/7/enact'))
        self.assertLess(called_endpoints.index('/scheduled_changes/releases/7/enact'), called_endpoints.index('/scheduled_changes/releases/6/enact'))
        self.assertLess(called_endpoints.index('/scheduled_changes/releases/6/enact'), called_endpoints.index('/scheduled_changes/releases/4/enact'))
        self.assertLess(called_endpoints.index('/scheduled_changes/rules/2/enact'), called_endpoints.index('/scheduled_changes/rules/1/enact'))
        self.assertLess(called_endpoints.index('/scheduled_changes/rules/1/enact'), called_endpoints.index('/scheduled_changes/rules/3/enact'))
        self.assertLess(called_endpoints.index('/scheduled_changes/permissions/9/enact'), called_endpoints.index('/scheduled_changes/permissions/8/enact'))
        self.assertLess(called_endpoints.index('/scheduled_changes/permissions/8/enact'), called_endpoints.index('/scheduled_changes/permissions/10/enact'))
