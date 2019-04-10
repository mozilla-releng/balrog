import mock

from auslib.test.admin.views.base import ViewTest
from auslib.web.admin.base import app


class TestCSRFEndpoint(ViewTest):
    def setUp(self):
        ViewTest.setUp(self)
        app.config["WTF_CSRF_ENABLED"] = True

    def testCsrfGet(self):
        with mock.patch("auslib.web.admin.views.csrf.generate_csrf") as csrf:
            csrf.return_value = 111

            ret = self.client.get("/csrf_token")
            self.assertEqual(ret.status_code, 200)
            self.assertEqual(ret.headers["X-CSRF-Token"], "111")
