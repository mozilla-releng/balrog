from copy import deepcopy

from auslib.global_state import cache, dbo
from auslib.services import releases

from .base import CommonTestBase


class TestPublicReleasesAPI(CommonTestBase):
    def test_get_releases(self):
        ret = self.public_client.get("/api/v1/releases")
        got = ret.get_json()
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
        got = ret.get_json()
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
        got = ret.get_json()
        self.assertEqual(len(got["names"]), 3)

    def test_get_releases_by_product(self):
        ret = self.public_client.get("/api/v1/releases?product=Fennec")
        got = ret.get_json()
        self.assertEqual(len(got["releases"]), 1)
        self.assertEqual(got["releases"][0]["name"], "Fennec.55.0a1")

    def test_get_releases_by_name_prefix(self):
        ret = self.public_client.get("/api/v1/releases?name_prefix=F")
        got = ret.get_json()
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
        got = ret.get_json()
        self.assertEqual(got["name"], release)
        self.assertEqual(got["schema_version"], 1)
        self.assertIn("p", got["platforms"])
        platform = got["platforms"]["p"]
        self.assertIn("l", platform["locales"])

    def test_get_release_new_tables(self):
        release = "Firefox-56.0-build1"
        ret = self.public_client.get("/api/v1/releases/{}".format(release))
        self.assertTrue(ret.status_code, 200)
        got = ret.get_json()
        self.assertEqual(got["name"], release)
        self.assertEqual(got["schema_version"], 4)
        self.assertIn("WINNT_x86_64-msvc", got["platforms"])
        platform = got["platforms"]["WINNT_x86_64-msvc"]
        self.assertIn("en-US", platform["locales"])

    def test_get_release_does_not_mutate_cached_blob(self):
        # The public app runs the cache with make_copies=False, so the cached
        # base blob is a single object shared across every request (and, with
        # UWSGI_THREADS>1, across concurrent threads). get_release assembles the
        # full release by merging the separately-cached assets into the base, and
        # it must NOT do that merge in place on the shared cached object.
        # Reproduce the public-app caching setup and assert the cached row is
        # left untouched after a merge.
        release = "Firefox-56.0-build1"
        cache.reset()
        self.addCleanup(cache.reset)
        # make_copies is global state, ensure it's turned off for this test
        original_make_copies = cache.make_copies
        cache.make_copies = False
        self.addCleanup(setattr, cache, "make_copies", original_make_copies)
        for cache_name in ("releases", "releases_data_version", "release_assets", "release_assets_data_versions"):
            cache.make_cache(cache_name, 10, 10)

        with dbo.begin() as trans:
            base_only = deepcopy(releases.get_base_row(release, trans)["data"])
            blob = releases.get_release(release, trans, include_sc=False)["blob"]

        # Sanity check: the assembled blob carries per-locale asset data the base lacks
        self.assertIn("en-US", blob["platforms"]["WINNT_x86_64-msvc"]["locales"])
        self.assertNotEqual(blob, base_only)

        # The cached base row must be byte-for-byte the DB base row,
        # i.e. the asset merge did not write the locales into the shared cached object.
        cached = cache.get("releases", release)
        self.assertEqual(cached["data"], base_only)
        self.assertNotIn("locales", cached["data"].get("platforms", {}).get("WINNT_x86_64-msvc", {}))

    def test_get_release_locale(self):
        ret = self.public_client.get("/api/v1/releases/Firefox.55.0a1/builds/p/l")
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.headers["X-Data-Version"], "1")
        got = ret.get_json()
        self.assertEqual(got["buildID"], "5")

    def test_get_release_locale_new_tables(self):
        ret = self.public_client.get("/api/v1/releases/Firefox-56.0-build1/builds/WINNT_x86_64-msvc/en-US")
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.headers["X-Data-Version"], "1")
        got = ret.get_json()
        self.assertEqual(got["buildID"], "20170918210324")

    def test_get_release_locale_not_found(self):
        ret = self.public_client.get("/api/v1/releases/Firefox.55.0a1/builds/404/l")
        self.assertEqual(ret.status_code, 404)
        ret = self.public_client.get("/api/v1/releases/Firefox.55.0a1/builds/p/404")
        self.assertEqual(ret.status_code, 404)
