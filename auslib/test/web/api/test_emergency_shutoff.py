import json
from auslib.global_state import dbo
from auslib.test.web.api.base import CommonTestBase


class TestEmergencyShutoff(CommonTestBase):
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

    def test_get_emergency_shutoff_list(self):
        resp = self.public_client.get('/api/v1/emergency_shutoff')
        self.assertEquals(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEquals(data['count'], 3)
        self.assertIn('shutoffs', data)

    def test_get_emergency_shutoff(self):
        resp = self.public_client.get('/api/v1/emergency_shutoff/1')
        self.assertEquals(resp.status_code, 200)
        self.assertIn('X-Data-Version', resp.headers)
        data = json.loads(resp.data)
        self.assertIn('product', data)
        self.assertEquals(data['product'], 'Firefox')
        self.assertIn('channel', data)
        self.assertEquals(data['channel'], 'nightly')

    def test_get_emergency_shutoff_notfound(self):
        resp = self.public_client.get('/api/v1/emergency_shutoff/404')
        self.assertEquals(resp.status_code, 404)

    def test_get_filtered_emergency_shutoffs(self):
        resp = self.public_client.get('/api/v1/emergency_shutoff?product=Fennec')
        self.assertEquals(resp.status_code, 200)
        data = json.loads(resp.data)
        for shutoff in data['shutoffs']:
            self.assertEquals('Fennec', shutoff['product'])

        resp = self.public_client.get('/api/v1/emergency_shutoff?channel=nightly')
        self.assertEquals(resp.status_code, 200)
        data = json.loads(resp.data)
        for shutoff in data['shutoffs']:
            self.assertEquals('nightly', shutoff['channel'])

        resp = self.public_client.get('/api/v1/emergency_shutoff?channel=test&product=Firefox')
        self.assertEquals(resp.status_code, 200)
        data = json.loads(resp.data)
        for shutoff in data['shutoffs']:
            self.assertEquals('Firefox', shutoff['product'])
            self.assertEquals('test', shutoff['channel'])
