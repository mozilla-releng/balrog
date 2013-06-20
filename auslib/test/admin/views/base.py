import simplejson as json
import unittest

from flask import Response

from auslib.admin.base import app, db

# When running tests, there's no web server to convert uncaught exceptions to
# 500 errors, so we need to do it here. Maybe we should just do it globally
# anyways?
@app.errorhandler(Exception)
def uncaughtexceptions(error):
    return Response(response=error, status=500)

class ViewTest(unittest.TestCase):
    """Base class for all view tests. Sets up some sample data, and provides
       some helper methods."""
    def setUp(self):
        app.config['SECRET_KEY'] = 'abc123'
        app.config['DEBUG'] = True
        app.config['CSRF_ENABLED'] = False
        db.setDburi('sqlite:///:memory:')
        db.create()
        db.permissions.t.insert().execute(permission='admin', username='bill', data_version=1)
        db.permissions.t.insert().execute(permission='/users/:id/permissions/:permission', username='bob', data_version=1)
        db.permissions.t.insert().execute(permission='/releases/:name', username='bob', options=json.dumps(dict(product='fake')), data_version=1)
        db.releases.t.insert().execute(name='a', product='a', version='a', data=json.dumps(dict(name='a')), data_version=1)
        db.releases.t.insert().execute(name='ab', product='a', version='a', data=json.dumps(dict(name='ab')), data_version=1)
        db.releases.t.insert().execute(name='b', product='b', version='b', data=json.dumps(dict(name='b')), data_version=1)
        db.releases.t.insert().execute(name='c', product='c', version='c', data=json.dumps(dict(name='c')), data_version=1)
        db.releases.t.insert().execute(name='d', product='d', version='d', data_version=1, data="""
{
    "name": "d",
    "platforms": {
        "p": {
            "locales": {
                "d": {
                    "complete": {
                        "filesize": "1234"
                    }
                }
            }
        }
    }
}
""")
        db.rules.t.insert().execute(id=1, priority=100, version='3.5', buildTarget='d', throttle=100, mapping='c', update_type='minor', data_version=1)
        db.rules.t.insert().execute(id=2, priority=100, version='3.3', buildTarget='d', throttle=100, mapping='b', update_type='minor', data_version=1)
        db.rules.t.insert().execute(id=3, priority=100, version='3.5', buildTarget='a', throttle=100, mapping='a', update_type='minor', data_version=1)
        db.rules.t.insert().execute(id=4, priority=80, buildTarget='d', throttle=100, mapping='a', update_type='minor', data_version=1)
        db.rules.t.insert().execute(id=5, priority=80, buildTarget='d', version='3.3', throttle=0, mapping='c', update_type='minor', data_version=1)
        self.client = app.test_client()

    def tearDown(self):
        db.reset()

    
    def _getBadAuth(self):
        return {'REMOTE_USER': 'NotAuth!'}

    def _getAuth(self, username):
        return {'REMOTE_USER': username}

    def _post(self, url, data={}, username='bill'):
        return self.client.post(url, data=data, environ_base=self._getAuth(username))

    def _badAuthPost(self, url, data={}):
        return self.client.post(url, data=data, environ_base=self._getBadAuth())

    def _put(self, url, data={}, username='bill'):
        return self.client.put(url, data=data, environ_base=self._getAuth(username))

    def _delete(self, url, qs={}, username='bill'):
        return self.client.delete(url, query_string=qs, environ_base=self._getAuth(username))

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
