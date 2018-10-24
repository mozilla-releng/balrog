import json
import mock

from auslib.test.web.api.base import CommonTestBase


class TestPublicReleasesAPI(CommonTestBase):
    def test_get_releases(self):
        ret = self.public_client.get("/api/v1/releases")
        got = ret.get_json()
        self.assertEquals(len(got["releases"]), 3)
        self.assertIsInstance(got["releases"][0], dict)
        releases = [(release["name"], release["product"]) for release in got["releases"]]
        self.assertIn(("Fennec.55.0a1", "Fennec"), releases)
        self.assertIn(("Firefox.55.0a1", "Firefox"), releases)
        self.assertIn(("q", "q"), releases)

    def test_get_releases_names(self):
        ret = self.public_client.get("/api/v1/releases?names_only=1")
        got = ret.get_json()
        self.assertEquals(len(got["names"]), 3)
        self.assertIn("Fennec.55.0a1", got["names"])
        self.assertIn("Firefox.55.0a1", got["names"])
        self.assertIn("q", got["names"])

    def test_get_releases_by_product(self):
        ret = self.public_client.get("/api/v1/releases?product=Fennec")
        got = ret.get_json()
        self.assertEquals(len(got["releases"]), 1)
        self.assertEquals(got["releases"][0]["name"], "Fennec.55.0a1")

    def test_get_releases_by_name_prefix(self):
        ret = self.public_client.get("/api/v1/releases?name_prefix=F")
        got = ret.get_json()
        self.assertEquals(len(got["releases"]), 2)
        releases = [(release["name"], release["product"]) for release in got["releases"]]
        self.assertIn(("Firefox.55.0a1", "Firefox"), releases)
        self.assertIn(("Fennec.55.0a1", "Fennec"), releases)

    def test_get_release(self):
        release = "Firefox.55.0a1"
        ret = self.public_client.get("/api/v1/releases/{}".format(release))
        self.assertTrue(ret.status_code, 200)
        got = ret.get_json()
        self.assertNotIn('X-CSRF-Token', ret.headers)
        self.assertEquals(got["name"], release)
        self.assertEquals(got["schema_version"], 1)
        self.assertIn("p", got["platforms"])
        platform = got["platforms"]["p"]
        self.assertIn("l", platform["locales"])

    @mock.patch("time.time", mock.MagicMock(return_value=300000))
    def test_get_release_history(self):
        ret = self.public_client.get("/api/v1/releases/q/revisions")
        self.assertEqual(ret.status_code, 200)
        got = ret.get_json()
        self.assertEquals(got["count"], 1)
        self.assertEquals(len(got["revisions"]), 1)
        revision = got["revisions"][0]
        self.assertEquals(revision["name"], "q")
        self.assertEquals(revision["data_version"], 1)

    def test_get_release_locale(self):
        ret = self.public_client.get("/api/v1/releases/Firefox.55.0a1/builds/p/l")
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.headers['X-Data-Version'], '1')
        got = ret.get_json()
        self.assertEqual(got["buildID"], "5")

    def test_get_release_locale_not_found(self):
        ret = self.public_client.get("/api/v1/releases/Firefox.55.0a1/builds/404/l")
        self.assertEqual(ret.status_code, 404)
        ret = self.public_client.get("/api/v1/releases/Firefox.55.0a1/builds/p/404")
        self.assertEqual(ret.status_code, 404)

    @mock.patch("time.time", mock.MagicMock(return_value=300000))
    def test_get_revisions_400(self):
        ret = self.public_client.get("/api/v1/releases/q/revisions?page=0")
        self.assertEqual(ret.status_code, 400)
