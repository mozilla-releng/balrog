import json
from auslib.test.common.base import CommonTestBase


class TestPublicReleasesAPI(CommonTestBase):
    def test_get_releases(self):
        ret = self.public_client.get("/api/v1/releases")
        got = json.loads(ret.data)
        self.assertEquals(len(got["releases"]), 3)
        self.assertIsInstance(got["releases"][0], dict)
        self.assertEquals(got["releases"][0]["name"], "Fennec.55.0a1")
        self.assertEquals(got["releases"][0]["schema_version"], 1)
        self.assertIn("l", got["releases"][0]["locales"])

    # def test_get_releases_names(self):
    #     ret = self.public_client.get("/api/v1/releases?names_only=1")
    #     got = json.loads(ret.data)
    #     self.assertEquals(len(got["names"]), 3)

    # def test_get_releases_by_product(self):
    #     ret = self.public_client.get("/api/v1/releases?product=Fennec")
    #     got = json.loads(ret.data)
    #     self.assertEquals(len(got["releases"]), 1)

    # def test_get_releases_by_name_prefix(self):
    #     ret = self.public_client.get("/api/v1/releases?name_prefix=F")
    #     got = json.loads(ret.data)
    #     self.assertEquals(len(got["releases"]), 2)

    # def test_get_release(self):
    #     release = "Firefox.55.0a1"
    #     ret = self.public_client.get("/api/v1/releases/{}".format(release))
    #     self.assertTrue(ret.status_code, 200)
    #     got = json.loads(ret.data)
    #     self.assertEquals(got["name"], release)

    # def test_get_release_history(self):
    #     user = {'REMOTE_USER': 'bill'}
    #     data = dict(schema_version=1)
    #     body = dict(product="q", data_version=2, data=json.dumps(data))
    #     ret = self.admin_client.post("/releases/q", data=json.dumps(body),
    #                                  content_type="application/json", environ_base=user)
    #     self.assertEqual(ret.status_code, 200)

    #     ret = self.public_client.get("/api/v1/releases/q/revisions")
    #     self.assertEqual(ret.status_code, 200)
    #     got = json.loads(ret.data)
    #     self.assertEquals(got["count"], 2)
    #     self.assertEquals(len(got["revisions"]), 2)

    # def test_get_release_locale(self):
    #     ret = self.public_client.get("/api/v1/releases/Firefox.55.0a1/builds/p/l")
    #     self.assertEqual(ret.status_code, 200)
    #     self.assertEqual(ret.headers['X-Data-Version'], '1')

    # def test_get_release_locale_not_found(self):
    #     ret = self.public_client.get("/api/v1/releases/Firefox.55.0a1/builds/404/l")
    #     self.assertEqual(ret.status_code, 404)
    #     ret = self.public_client.get("/api/v1/releases/Firefox.55.0a1/builds/p/404")
    #     self.assertEqual(ret.status_code, 404)

    # def test_get_revisions_400(self):
    #     ret = self.public_client.get("/api/v1/releases/q/revisions?page=0")
    #     self.assertEqual(ret.status_code, 400)
