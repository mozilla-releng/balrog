import os
import simplejson as json
from tempfile import mkstemp
import unittest

from auslib.global_state import dbo, cache
from auslib.admin.base import app
import auslib.log


class ViewTest(unittest.TestCase):
    """Base class for all view tests. Sets up some sample data, and provides
       some helper methods."""

    def setUp(self):
        self.cef_fd, self.cef_file = mkstemp()
        cache.reset()
        cache.make_copies = True
        app.config["SECRET_KEY"] = 'abc123'
        app.config['DEBUG'] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config['WHITELISTED_DOMAINS'] = ['good.com']
        auslib.log.cef_config = auslib.log.get_cef_config(self.cef_file)
        dbo.setDb('sqlite:///:memory:')
        dbo.setDomainWhitelist(['good.com'])
        dbo.create()
        dbo.permissions.t.insert().execute(permission='admin', username='bill', data_version=1)
        dbo.permissions.t.insert().execute(permission='/users/:id/permissions/:permission', username='bob', data_version=1)
        dbo.permissions.t.insert().execute(permission='/releases/:name', username='bob', options=json.dumps(dict(product=['fake'])), data_version=1)
        dbo.permissions.t.insert().execute(permission='/rules/:id', username='bob', options=json.dumps(dict(product=['fake'])), data_version=1)
        dbo.releases.t.insert().execute(
            name='a', product='a', data=json.dumps(dict(name='a', hashFunction="sha512", schema_version=1)), data_version=1)
        dbo.releases.t.insert().execute(
            name='ab', product='a', data=json.dumps(dict(name='ab', hashFunction="sha512", schema_version=1)), data_version=1)
        dbo.releases.t.insert().execute(
            name='b', product='b', data=json.dumps(dict(name='b', hashFunction="sha512", schema_version=1)), data_version=1)
        dbo.releases.t.insert().execute(
            name='c', product='c', data=json.dumps(dict(name='c', hashFunction="sha512", schema_version=1)), data_version=1)
        dbo.releases.t.insert().execute(name='d', product='d', data_version=1, data="""
{
    "name": "d",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "d": {
                    "complete": {
                        "filesize": 1234,
                        "from": "*",
                        "hashValue": "abc"
                    }
                }
            }
        }
    }
}
""")
        dbo.rules.t.insert().execute(id=1, priority=100, version='3.5', buildTarget='d', backgroundRate=100, mapping='c', update_type='minor', data_version=1)
        dbo.rules.t.insert().execute(id=2, alias="frodo", priority=100, version='3.3', buildTarget='d', backgroundRate=100, mapping='b', update_type='minor',
                                     data_version=1)
        dbo.rules.t.insert().execute(id=3, priority=100, version='3.5', buildTarget='a', backgroundRate=100, mapping='a', update_type='minor', data_version=1)
        dbo.rules.t.insert().execute(id=4, product='fake', priority=80, buildTarget='d', backgroundRate=100, mapping='a', update_type='minor', data_version=1)
        dbo.rules.t.insert().execute(id=5, priority=80, buildTarget='d', version='3.3', backgroundRate=0, mapping='c', update_type='minor', data_version=1)
        self.client = app.test_client()

    def tearDown(self):
        dbo.reset()
        os.close(self.cef_fd)
        os.remove(self.cef_file)

    def _getBadAuth(self):
        return {'REMOTE_USER': 'NotAuth!'}

    def _getAuth(self, username):
        return {'REMOTE_USER': username}

    def _post(self, url, data={}, username='bill', **kwargs):
        return self.client.post(url, data=data, environ_base=self._getAuth(username), **kwargs)

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

    def _get(self, url, qs={}):
        headers = {
            "Accept-Encoding": "application/json",
            "Accept": "application/json"
        }
        if "format" not in qs:
            qs["format"] = "json"
        ret = self.client.get(url, query_string=qs, headers=headers)
        return ret
