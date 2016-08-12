import os
import simplejson as json
from tempfile import mkstemp
import unittest

from auslib.global_state import dbo, cache
from auslib.admin.base import app


class ViewTest(unittest.TestCase):
    """Base class for all view tests. Sets up some sample data, and provides
       some helper methods."""

    def setUp(self):
        self.version_fd, self.version_file = mkstemp()
        cache.reset()
        cache.make_copies = True
        app.config["SECRET_KEY"] = 'abc123'
        app.config['DEBUG'] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config['WHITELISTED_DOMAINS'] = {'good.com': ('a', 'b', 'c', 'd')}
        app.config["VERSION_FILE"] = self.version_file
        with open(self.version_file, "w+") as f:
            f.write("""
{
  "source":"https://github.com/mozilla/balrog",
  "version":"1.0",
  "commit":"abcdef123456"
}
""")
        dbo.setDb('sqlite:///:memory:')
        dbo.setDomainWhitelist({'good.com': ('a', 'b', 'c', 'd')})
        dbo.create()
        dbo.permissions.t.insert().execute(permission='admin', username='bill', data_version=1)
        dbo.permissions.t.insert().execute(permission='permission', username='bob', data_version=1)
        dbo.permissions.t.insert().execute(permission='release', username='bob',
                                           options=json.dumps(dict(products=['fake', 'b'], actions=["create", "modify"])), data_version=1)
        dbo.permissions.t.insert().execute(permission='release_read_only', username='bob', options=json.dumps(dict(actions=["set"])), data_version=1)
        dbo.permissions.t.insert().execute(permission='rule', username='bob', options=json.dumps(dict(actions=["modify"], products=['fake'])), data_version=1)
        dbo.permissions.t.insert().execute(permission='build', username='ashanti', options=json.dumps(dict(actions=["modify"], products=['a'])), data_version=1)
        dbo.permissions.t.insert().execute(permission="scheduled_change", username="mary", options=json.dumps(dict(actions=["enact"])), data_version=1)
        dbo.permissions.t.insert().execute(permission='release_locale', username='ashanti',
                                           options=json.dumps(dict(actions=["modify"], products=['a'])), data_version=1)
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
        dbo.rules.t.insert().execute(
            rule_id=1, priority=100, version='3.5', buildTarget='d', backgroundRate=100, mapping='c', update_type='minor', data_version=1
        )
        dbo.rules.t.insert().execute(
            rule_id=2, alias="frodo", priority=100, version='3.3', buildTarget='d', backgroundRate=100, mapping='b', update_type='minor',
            data_version=1
        )
        dbo.rules.t.insert().execute(
            rule_id=3, priority=100, version='3.5', buildTarget='a', backgroundRate=100, mapping='a', update_type='minor', data_version=1
        )
        dbo.rules.t.insert().execute(
            rule_id=4, product='fake', priority=80, buildTarget='d', backgroundRate=100, mapping='a', update_type='minor', data_version=1
        )
        dbo.rules.t.insert().execute(
            rule_id=5, priority=80, buildTarget='d', version='3.3', backgroundRate=0, mapping='c', update_type='minor', data_version=1
        )
        self.client = app.test_client()

    def tearDown(self):
        dbo.reset()
        os.close(self.version_fd)
        os.remove(self.version_file)

    def _getBadAuth(self):
        return {'REMOTE_USER': 'NotAuth!'}

    def _getHttpRemoteUserAuth(self, username):
        return {"HTTP_REMOTE_USER": username}

    def _getAuth(self, username):
        return {'REMOTE_USER': username}

    def _get(self, url, qs={}):
        headers = {
            "Accept-Encoding": "application/json",
            "Accept": "application/json"
        }
        if "format" not in qs:
            qs["format"] = "json"
        ret = self.client.get(url, query_string=qs, headers=headers)
        return ret

    def _post(self, url, data={}, username='bill', **kwargs):
        return self.client.post(url, data=json.dumps(data), content_type="application/json", environ_base=self._getAuth(username), **kwargs)

    def _httpRemoteUserPost(self, url, username="bill", data={}):
        return self.client.post(url, data=json.dumps(data), content_type="application/json", environ_base=self._getHttpRemoteUserAuth(username))

    def _badAuthPost(self, url, data={}):
        return self.client.post(url, data=json.dumps(data), content_type="application/json", environ_base=self._getBadAuth())

    def _put(self, url, data={}, username='bill'):
        return self.client.put(url, data=json.dumps(data), content_type="application/json", environ_base=self._getAuth(username))

    def _delete(self, url, qs={}, username='bill'):
        return self.client.delete(url, query_string=qs, environ_base=self._getAuth(username))

    def assertStatusCode(self, response, expected):
        self.assertEquals(response.status_code, expected, '%d - %s' % (response.status_code, response.data))
