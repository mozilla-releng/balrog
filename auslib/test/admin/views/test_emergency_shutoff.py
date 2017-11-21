import json
from auslib.global_state import dbo
from auslib.test.admin.views.base import ViewTest


class TestEmergencyShutoff(ViewTest):
    def setUp(self):
        super(TestEmergencyShutoff, self).setUp()
        dbo.emergencyShutoff.t.insert().execute(
            shutoff_id=1, product='Firefox', channel='nightly',
            updates_disabled=False, data_version=1,
            additional_notification_list='foo@bar.org')
        dbo.emergencyShutoff.t.insert().execute(
            shutoff_id=2, product='Fennec', channel='nightly',
            updates_disabled=False, data_version=1)
        dbo.emergencyShutoff.t.insert().execute(
            shutoff_id=3, product='Firefox', channel='test',
            updates_disabled=True, data_version=1)
        dbo.emergencyShutoff.scheduled_changes.t.insert().execute(
            sc_id=1, scheduled_by="bill", change_type="update",
            data_version=1, base_shutoff_id=3, base_product='Firefox',
            base_channel='test', base_updates_disabled=False,
            base_data_version=1)
        dbo.emergencyShutoff.scheduled_changes.conditions.t.insert().execute(
            sc_id=1, data_version=1, when=1000000)
        dbo.productRequiredSignoffs.t.insert().execute(
            product="Thunderbird", channel="release", role="releng", signoffs_required=1, data_version=1)
        dbo.productRequiredSignoffs.t.insert().execute(
            product="Firefox", channel="release", role="releng", signoffs_required=1, data_version=1)

    def test_get_emergency_shutoff_list(self):
        resp = self._get('/emergency_shutoff')
        self.assertStatusCode(resp, 200)
        data = json.loads(resp.data)
        self.assertEquals(data['count'], 3)
        self.assertIn('shutoffs', data)

    def test_get_emergency_shutoff(self):
        resp = self._get('/emergency_shutoff/1')
        self.assertStatusCode(resp, 200)
        self.assertIn('X-Data-Version', resp.headers)
        data = json.loads(resp.data)
        self.assertIn('product', data)
        self.assertEquals(data['product'], 'Firefox')
        self.assertIn('channel', data)
        self.assertEquals(data['channel'], 'nightly')

    def test_get_emergency_shutoff_notfound(self):
        resp = self._get('/emergency_shutoff/404')
        self.assertStatusCode(resp, 404)

    def test_get_filtered_emergency_shutoffs(self):
        qs = {'product': 'Fennec'}
        resp = self._get('/emergency_shutoff', qs=qs)
        self.assertStatusCode(resp, 200)
        data = json.loads(resp.data)
        for shutoff in data['shutoffs']:
            self.assertEquals('Fennec', shutoff['product'])

        qs = {'channel': 'nightly'}
        resp = self._get('/emergency_shutoff', qs=qs)
        self.assertStatusCode(resp, 200)
        data = json.loads(resp.data)
        for shutoff in data['shutoffs']:
            self.assertEquals('nightly', shutoff['channel'])

        qs = {'channel': 'test', 'product': 'Firefox'}
        resp = self._get('/emergency_shutoff', qs=qs)
        self.assertStatusCode(resp, 200)
        data = json.loads(resp.data)
        for shutoff in data['shutoffs']:
            self.assertEquals('Firefox', shutoff['product'])
            self.assertEquals('test', shutoff['channel'])

    def test_create_emergency_shutoff(self):
        data = {'product': 'Thunderbird',
                'channel': 'release',
                'additional_notification_list': 'm@m.org'}
        resp = self._post('/emergency_shutoff', data=data.copy())
        self.assertStatusCode(resp, 201)

        qs = {'channel': 'release', 'product': 'Thunderbird'}
        resp = self._get('/emergency_shutoff', qs=qs)
        self.assertStatusCode(resp, 200)
        resp_data = json.loads(resp.data)

        shutoff = resp_data['shutoffs'][0]
        for k, v in data.items():
            self.assertIn(k, shutoff)
            self.assertEquals(v, shutoff[k])

    def test_try_create_for_existent_product_channel_shutoff(self):
        data = {'product': 'Fennec',
                'channel': 'nightly'}
        resp = self._post('/emergency_shutoff', data=data)
        self.assertStatusCode(resp, 400)

    def test_try_create_for_product_with_no_required_signoff(self):
        data = {'product': 'Test',
                'channel': 'nightly'}
        resp = self._post('/emergency_shutoff', data=data)
        self.assertStatusCode(resp, 400)

    def test_change_emergency_shutoff(self):
        data = {'product': 'Firefox',
                'channel': 'release',
                'additional_notification_list': 'foo@bar.com', 'data_version': 1}
        resp = self._put('/emergency_shutoff/1', data=data.copy())
        self.assertStatusCode(resp, 200)
        resp = self._get('/emergency_shutoff/1')
        self.assertStatusCode(resp, 200)
        shutoff = json.loads(resp.data)
        del data['data_version']
        for k, v in data.items():
            if k == 'data_version':
                v += 1
            self.assertIn(k, shutoff)
            self.assertEquals(v, shutoff[k])

    def test_change_to_existent_emergency_shutoff(self):
        data = {'product': 'Firefox',
                'channel': 'test', 'data_version': 1}
        resp = self._put('/emergency_shutoff/1', data=data)
        self.assertStatusCode(resp, 400)

    def test_change_emergency_shutoff_not_found(self):
        data = {'product': 'Firefox',
                'channel': 'test', 'data_version': 1}
        resp = self._put('/emergency_shutoff/404', data=data)
        self.assertStatusCode(resp, 404)

    def test_delete_emergency_shutoff(self):
        resp = self._delete('/emergency_shutoff/2', qs=dict(data_version=1))
        self.assertStatusCode(resp, 200)

    def test_delete_emergency_shutoff_not_found(self):
        resp = self._delete('/emergency_shutoff/404', qs=dict(data_version=1))
        self.assertStatusCode(resp, 404)

    def test_delete_emergency_shutoff_with_sc(self):
        resp = self._delete('/emergency_shutoff/3', qs=dict(data_version=1))
        self.assertStatusCode(resp, 400)

    def test_disable_updates(self):
        resp = self._put('/emergency_shutoff/2/disable_updates')
        self.assertStatusCode(resp, 200)
        resp = self._get('/emergency_shutoff/2')
        self.assertStatusCode(resp, 200)
        shutoff = json.loads(resp.data)
        self.assertEquals(shutoff['updates_disabled'], True)
        resp = self._get('/scheduled_changes/emergency_shutoff')
        resp_data = json.loads(resp.data)
        self.assertTrue(
            [sc for sc in resp_data['scheduled_changes'] if sc['shutoff_id'] == 2])

    def test_disable_updates_not_found(self):
        resp = self._put('/emergency_shutoff/404/disable_updates')
        self.assertStatusCode(resp, 404)

    def test_try_disable_already_disabled_updates(self):
        resp = self._put('/emergency_shutoff/3/disable_updates')
        self.assertStatusCode(resp, 400)

    def test_get_emergency_shutoff_scheduled_changes(self):
        resp = self._get('/scheduled_changes/emergency_shutoff')
        self.assertStatusCode(resp, 200)
        resp_data = json.loads(resp.data)
        self.assertEquals(resp_data['count'], 1)

    def test_enact_updates_scheduled_for_reactivation(self):
        resp = self._post('/scheduled_changes/emergency_shutoff/1/enact')
        self.assertStatusCode(resp, 200)
        resp = self._get('/emergency_shutoff/2')
        self.assertStatusCode(resp, 200)
        shutoff = json.loads(resp.data)
        self.assertEquals(shutoff['updates_disabled'], False)
