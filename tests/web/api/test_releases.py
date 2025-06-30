from .base import CommonTestBase


class TestPublicReleasesAPI(CommonTestBase):
    def test_get_releases(self):
        ret = self.public_client.get("/api/v1/releases")
        got = ret.json()
        self.assertEqual(len(got["releases"]), 8)
        self.assertIsInstance(got["releases"][0], dict)
        releases = [(release["name"], release["product"]) for release in got["releases"]]
        self.assertIn(("Fennec.55.0a1", "Fennec"), releases)
        self.assertIn(("Firefox.55.0a1", "Firefox"), releases)
        self.assertIn(("q", "q"), releases)
        self.assertIn(("Firefox-54.0.1-build1", "Firefox"), releases)
        self.assertIn(("Firefox-56.0-build1", "Firefox"), releases)
        self.assertIn(("Superblob-e8f4a19cfd695bf0eb66a2115313c31cc23a2369c0dc7b736d2f66d9075d7c66", "SystemAddons"), releases)
        self.assertIn(("hotfix-bug-1548973@mozilla.org-1.1.4", "SystemAddons"), releases)
        self.assertIn(("timecop@mozilla.com-1.0", "SystemAddons"), releases)

    def test_get_releases_names(self):
        ret = self.public_client.get("/api/v1/releases?names_only=1")
        got = ret.json()
        self.assertEqual(len(got["names"]), 8)
        self.assertIn("Fennec.55.0a1", got["names"])
        self.assertIn("Firefox.55.0a1", got["names"])
        self.assertIn("q", got["names"])
        self.assertIn("Firefox-54.0.1-build1", got["names"])
        self.assertIn("Firefox-56.0-build1", got["names"])
        self.assertIn("Superblob-e8f4a19cfd695bf0eb66a2115313c31cc23a2369c0dc7b736d2f66d9075d7c66", got["names"])
        self.assertIn("hotfix-bug-1548973@mozilla.org-1.1.4", got["names"])
        self.assertIn("timecop@mozilla.com-1.0", got["names"])
        ret = self.public_client.get("/api/v1/releases?names_only=1&product=Firefox")
        got = ret.json()
        self.assertEqual(len(got["names"]), 3)

    def test_get_releases_by_product(self):
        ret = self.public_client.get("/api/v1/releases?product=Fennec")
        got = ret.json()
        self.assertEqual(len(got["releases"]), 1)
        self.assertEqual(got["releases"][0]["name"], "Fennec.55.0a1")

    def test_get_releases_by_name_prefix(self):
        ret = self.public_client.get("/api/v1/releases?name_prefix=F")
        got = ret.json()
        self.assertEqual(len(got["releases"]), 4)
        releases = [(release["name"], release["product"]) for release in got["releases"]]
        self.assertIn(("Firefox.55.0a1", "Firefox"), releases)
        self.assertIn(("Fennec.55.0a1", "Fennec"), releases)
        self.assertIn(("Firefox-54.0.1-build1", "Firefox"), releases)
        self.assertIn(("Firefox-56.0-build1", "Firefox"), releases)
        self.assertNotIn(("q", "q"), releases)
        self.assertNotIn(("Superblob-e8f4a19cfd695bf0eb66a2115313c31cc23a2369c0dc7b736d2f66d9075d7c66", "SystemAddons"), releases)

    def test_get_release(self):
        release = "Firefox.55.0a1"
        ret = self.public_client.get("/api/v1/releases/{}".format(release))
        self.assertTrue(ret.status_code, 200)
        got = ret.json()
        self.assertEqual(got["name"], release)
        self.assertEqual(got["schema_version"], 1)
        self.assertIn("p", got["platforms"])
        platform = got["platforms"]["p"]
        self.assertIn("l", platform["locales"])

    def test_get_release_new_tables(self):
        release = "Firefox-56.0-build1"
        ret = self.public_client.get("/api/v1/releases/{}".format(release))
        self.assertTrue(ret.status_code, 200)
        got = ret.json()
        self.assertEqual(got["name"], release)
        self.assertEqual(got["schema_version"], 4)
        self.assertIn("WINNT_x86_64-msvc", got["platforms"])
        platform = got["platforms"]["WINNT_x86_64-msvc"]
        self.assertIn("en-US", platform["locales"])

    def test_get_release_locale(self):
        ret = self.public_client.get("/api/v1/releases/Firefox.55.0a1/builds/p/l")
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.headers["X-Data-Version"], "1")
        got = ret.json()
        self.assertEqual(got["buildID"], "5")

    def test_get_release_locale_new_tables(self):
        ret = self.public_client.get("/api/v1/releases/Firefox-56.0-build1/builds/WINNT_x86_64-msvc/en-US")
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.headers["X-Data-Version"], "1")
        got = ret.json()
        self.assertEqual(got["buildID"], "20170918210324")

    def test_get_release_locale_not_found(self):
        ret = self.public_client.get("/api/v1/releases/Firefox.55.0a1/builds/404/l")
        self.assertEqual(ret.status_code, 404)
        ret = self.public_client.get("/api/v1/releases/Firefox.55.0a1/builds/p/404")
        self.assertEqual(ret.status_code, 404)
