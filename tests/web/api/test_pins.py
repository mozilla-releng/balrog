from auslib.global_state import dbo

from .base import CommonTestBase


class TestPinsPublicAPI(CommonTestBase):
    def setUp(self):
        super(TestPinsPublicAPI, self).setUp()
        dbo.pinnable_releases.t.insert().execute(
            product="test_product",
            version="1.",
            channel="test_channel",
            mapping="test_mapping",
            data_version=1,
        )

    def test_get_pin(self):
        resp = self.public_client.get("/api/v1/pins/test_product/test_channel/1.")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("X-Data-Version", resp.headers)
        data = resp.get_json()
        self.assertIn("product", data)
        self.assertEqual(data["product"], "test_product")
        self.assertIn("channel", data)
        self.assertEqual(data["channel"], "test_channel")
        self.assertIn("version", data)
        self.assertEqual(data["version"], "1.")
        self.assertIn("mapping", data)
        self.assertEqual(data["mapping"], "test_mapping")

    def test_get_pin_notfound(self):
        resp = self.public_client.get("/api/v1/pins/test_product/test_channel/2.")
        self.assertEqual(resp.status_code, 404)
