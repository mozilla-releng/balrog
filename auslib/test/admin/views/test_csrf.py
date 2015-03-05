import flask_wtf.form

from auslib.admin.base import app
from auslib.test.admin.views.base import ViewTest

class TestCSRFEndpoint(ViewTest):
    def setUp(self):
        ViewTest.setUp(self)
        app.config['WTF_CSRF_ENABLED'] = True
        # Normally we'd just use mock.patch to do this, but it's not working
        # with this class for some reason....
        def g(self, x):
            return 111
        self.old_generate_csrf_token = flask_wtf.form.Form.generate_csrf_token
        flask_wtf.form.Form.generate_csrf_token = g

    def tearDown(self):
        flask_wtf.form.Form.generate_csrf_token = self.old_generate_csrf_token
        ViewTest.tearDown(self)

    def testCsrfGet(self):
        ret = self.client.get('/csrf_token')
        self.assertEquals(ret.status_code, 200)
        self.assertEquals(ret.headers['X-CSRF-Token'], '111')
