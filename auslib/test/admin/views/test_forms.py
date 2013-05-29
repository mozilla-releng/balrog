import json
import cgi
import flask
from auslib.test.admin.views.base import ViewTest
from auslib.admin.views.forms import PermissionForm


class TestFormsWithJSONFields(ViewTest):

    def testRenderPermissionForm(self):
        """Rendering the Permission form with a dict for the options field
        should serialize it when preparing it as the input tag value in HTML"""
        app = flask.Flask(__name__)
        app.config['SECRET_KEY'] = 'abc123'
        app.config['CSRF_ENABLED'] = False
        with app.test_request_context('/'):
            struct = {'foo': u'\xe3'}
            form = PermissionForm(options=struct)
            assert not form.is_submitted()
            output = form.options()
            expected = 'value="%s"' % cgi.escape(json.dumps(struct), True)
            self.assertTrue(expected in output, expected)

        struct = {'bar': u'\xe3'}
        data = {
            'options': json.dumps(struct),
            'data_version': 1,
        }
        with app.test_request_context('/', method='POST', data=data):
            app.preprocess_request()
            form = PermissionForm()
            self.assertEqual(form.options.data, struct)
