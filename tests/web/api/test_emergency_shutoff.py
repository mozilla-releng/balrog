from auslib.global_state import dbo

from .base import CommonTestBase


class TestEmergencyShutoff(CommonTestBase):
    def setUp(self):
        super(TestEmergencyShutoff, self).setUp()
        dbo.emergencyShutoffs.t.insert().execute(product="Firefox", channel="nightly", data_version=1)
        dbo.emergencyShutoffs.t.insert().execute(product="Fennec", channel="nightly", data_version=1)
        dbo.emergencyShutoffs.t.insert().execute(product="Firefox", channel="test", data_version=1)

    def test_get_emergency_shutoff_list(self):
        resp = self.public_client.get("/api/v1/emergency_shutoff")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["count"], 3)
        self.assertIn("shutoffs", data)

    def test_get_emergency_shutoff(self):
        resp = self.public_client.get("/api/v1/emergency_shutoff/Firefox/nightly")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("X-Data-Version", resp.headers)
        data = resp.json()
        self.assertIn("product", data)
        self.assertEqual(data["product"], "Firefox")
        self.assertIn("channel", data)
        self.assertEqual(data["channel"], "nightly")

    def test_get_emergency_shutoff_notfound(self):
        resp = self.public_client.get("/api/v1/emergency_shutoff/Thunderbird/beta")
        self.assertEqual(resp.status_code, 404)
