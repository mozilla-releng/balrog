from base64 import b64encode
import simplejson as json
import unittest

from auslib.db import AUSDatabase
from auslib.web.base import app, db

class ViewTest(unittest.TestCase):
    """Base class for all view tests. Sets up some sample data, and provides
       some helper methods."""
    def setUp(self):
        app.config['SECRET_KEY'] = 'abc123'
        app.config['DEBUG'] = True
        db.setDburi('sqlite:///:memory:')
        db.permissions.t.insert().execute(permission='admin', username='bill', data_version=1)
        db.permissions.t.insert().execute(permission='/users/:id/permissions/:permission', username='bob', data_version=1)
        db.permissions.t.insert().execute(permission='/releases/:name', username='bob', options=json.dumps(dict(product='fake')), data_version=1)
        db.releases.t.insert().execute(name='a', product='a', version='a', data=json.dumps(dict(one=1)), data_version=1)
        db.releases.t.insert().execute(name='ab', product='a', version='a', data=json.dumps(dict(one=1)), data_version=1)
        db.releases.t.insert().execute(name='b', product='b', version='b', data=json.dumps(dict(two=2)), data_version=1)
        db.releases.t.insert().execute(name='c', product='c', version='c', data=json.dumps(dict(three=3)), data_version=1)
        db.rules.t.insert().execute(id=1, priority=100, version='3.5', buildTarget='d', throttle=100, mapping='c', update_type='minor', data_version=1)
        db.rules.t.insert().execute(id=2, priority=100, version='3.3', buildTarget='d', throttle=100, mapping='b', update_type='minor', data_version=1)
        db.rules.t.insert().execute(id=3, priority=100, version='3.5', buildTarget='a', throttle=100, mapping='a', update_type='minor', data_version=1)
        db.rules.t.insert().execute(id=4, priority=80, buildTarget='d', throttle=100, mapping='a', update_type='minor', data_version=1)
        db.rules.t.insert().execute(id=5, priority=80, buildTarget='d', version='3.3', throttle=0, mapping='c', update_type='minor', data_version=1)
        self.client = app.test_client()

    def tearDown(self):
        db.reset()

    def _getAuth(self, username='bill'):
        return {'REMOTE_USER': 'bill'}

    def _post(self, url, data={}):
        return self.client.post(url, data=data, environ_base=self._getAuth())

    def _put(self, url, data={}):
        return self.client.put(url, data=data, environ_base=self._getAuth())

    def _delete(self, url, qs={}):
        return self.client.delete(url, query_string=qs, environ_base=self._getAuth())

    def assertStatusCode(self, response, expected):
        self.assertEquals(response.status_code, expected, '%d - %s' % (response.status_code, response.data))

class JSONTestMixin(object):
    """Provides a _get method that always asks for format='json', and checks
       the returned MIME type."""
    def _get(self, url):
        ret = self.client.get(url, query_string=dict(format='json'))
        self.assertEquals(ret.mimetype, 'application/json')
        return ret

class HTMLTestMixin(object):
    """Provides a _get method that always asks for format='html', and checks
       the returned MIME type."""
    def _get(self, url, query_string=dict()):
        qs = query_string.copy()
        qs['format'] = 'html'
        ret = self.client.get(url, query_string=qs)
        self.assertEquals(ret.mimetype, 'text/html')
        return ret
