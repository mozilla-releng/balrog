import json
import mock
from auslib.global_state import dbo
from auslib.test.admin.views.base import ViewTest


class TestEmergencyShutoff(ViewTest):
    def setUp(self):
        super(TestEmergencyShutoff, self).setUp()
        dbo.emergencyShutoffs.t.insert().execute(
            product='Firefox', channel='nightly', data_version=1)
        dbo.emergencyShutoffs.t.insert().execute(
            product='Fennec', channel='beta', data_version=1)
        dbo.emergencyShutoffs.t.insert().execute(
            product='Thunderbird', channel='nightly', data_version=1)
        dbo.emergencyShutoffs.scheduled_changes.t.insert().execute(
            sc_id=1, scheduled_by='bill', change_type='delete',
            data_version=1, base_product='Firefox', base_channel='nightly',
            base_data_version=1)
        dbo.emergencyShutoffs.scheduled_changes.t.insert().execute(
            sc_id=2, scheduled_by='bill', change_type='delete',
            data_version=1, base_product='Thunderbird', base_channel='nightly',
            base_data_version=1)
        dbo.emergencyShutoffs.scheduled_changes.conditions.t.insert().execute(
            sc_id=1, data_version=1, when=1000000)
        dbo.emergencyShutoffs.scheduled_changes.conditions.t.insert().execute(
            sc_id=2, data_version=1, when=1000000)
        dbo.emergencyShutoffs.scheduled_changes.signoffs.t.insert().execute(
            sc_id=1, username='bill', role='releng')
        dbo.productRequiredSignoffs.t.insert().execute(
            product='Firefox', channel='nightly', role='releng', signoffs_required=1, data_version=1)

    def test_get_emergency_shutoff_list(self):
        resp = self._get('/emergency_shutoff')
        self.assertStatusCode(resp, 200)
        data = json.loads(resp.data)
        self.assertEquals(data['count'], 3)
        self.assertIn('shutoffs', data)

    def test_get_by_id(self):
        resp = self._get('/emergency_shutoff/Fennec/beta')
        self.assertStatusCode(resp, 200)
        self.assertIn('X-Data-Version', resp.headers)
        data = json.loads(resp.data)
        self.assertIn('product', data)
        self.assertEquals(data['product'], 'Fennec')
        self.assertIn('channel', data)
        self.assertEquals(data['channel'], 'beta')

    def test_get_notfound(self):
        resp = self._get('/emergency_shutoff/foo/bar')
        self.assertStatusCode(resp, 404)

    def test_create(self):
        data = {'product': 'Thunderbird',
                'channel': 'release'}
        resp = self._post('/emergency_shutoff', data=data.copy())
        self.assertStatusCode(resp, 201)
        shutoffs = dbo.emergencyShutoffs.select(where=data)
        self.assertTrue(shutoffs)
        for key in data.keys():
            self.assertEquals(data[key], shutoffs[0][key])

    def test_try_create_for_existent_product_channel(self):
        data = {'product': 'Fennec',
                'channel': 'beta'}
        resp = self._post('/emergency_shutoff', data=data)
        self.assertStatusCode(resp, 400)

    def test_delete(self):
        resp = self._delete('/emergency_shutoff/Fennec/beta', qs=dict(data_version=1))
        self.assertStatusCode(resp, 200)

    def test_delete_notfound(self):
        resp = self._delete('/emergency_shutoff/Foo/bar', qs=dict(data_version=1))
        self.assertStatusCode(resp, 404)

    def test_delete_with_out_signoff(self):
        resp = self._delete('/emergency_shutoff/Firefox/nightly', qs=dict(data_version=1))
        self.assertStatusCode(resp, 400)

    def test_get_scheduled_changes(self):
        resp = self._get('/scheduled_changes/emergency_shutoff')
        self.assertStatusCode(resp, 200)
        resp_data = json.loads(resp.data)
        self.assertEquals(resp_data['count'], 2)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def test_schedule_deletion(self):
        data = {'when': 4200024, 'change_type': 'delete', 'data_version': 1,
                'product': 'Fennec', 'channel': 'beta'}
        ret = self._post("/scheduled_changes/emergency_shutoff", data=data)
        self.assertEquals(ret.status_code, 200)
        self.assertIn('sc_id', json.loads(ret.data))
        sc_table = dbo.emergencyShutoffs.scheduled_changes
        conditions_table = sc_table.conditions
        sc = sc_table.t.select().where(sc_table.base_product == data['product'])\
                                .where(sc_table.base_channel == data['channel'])\
                                .where(sc_table.base_data_version == data['data_version'])\
                                .where(sc_table.change_type == data['change_type'])\
                                .where(conditions_table.sc_id == sc_table.sc_id)\
                                .where(conditions_table.when == data['when'])\
                                .execute().fetchall()
        self.assertTrue(sc)

    def test_enact_updates_scheduled_for_reactivation(self):
        resp = self._post('/scheduled_changes/emergency_shutoff/1/enact')
        self.assertStatusCode(resp, 200)
        shutoffs = dbo.emergencyShutoffs.select(where=dict(product='Firefox', channel='nightly'))
        self.assertFalse(shutoffs)

    def test_enact_updates_scheduled_for_reactivation_without_signoff(self):
        resp = self._post('/scheduled_changes/emergency_shutoff/2/enact')
        self.assertStatusCode(resp, 200)
        shutoffs = dbo.emergencyShutoffs.select(where=dict(product='Thunderbird', channel='nightly'))
        self.assertFalse(shutoffs)
