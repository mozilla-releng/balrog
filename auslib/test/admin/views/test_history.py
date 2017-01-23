import json

from auslib.global_state import dbo
from auslib.test.admin.views.base import ViewTest


class TestHistoryView(ViewTest):

    def testFieldViewBadValuesBadTable(self):
        url = '/history/view/notatable/1/whatever'
        ret = self.client.get(url)
        self.assertStatusCode(ret, 400)
        self.assertTrue('Bad table' in ret.data)

    def testFieldViewBadValuesBadChangeId(self):
        url = '/history/view/permission/9999/whatever'
        ret = self.client.get(url)
        self.assertStatusCode(ret, 404)
        self.assertTrue('Bad change_id' in ret.data)

    def testFieldViewCheckIntegerValue(self):
        data = json.dumps(dict(detailsUrl='InbhalInt', fakePartials=True, schema_version=1, name="d", hashFunction="sha512"))
        ret = self._post(
            '/releases/d',
            data=dict(data=data, product='d', data_version=1)
        )
        self.assertStatusCode(ret, 200)

        table = dbo.releases.history
        query = table.t.count()
        count, = query.execute().first()
        self.assertEqual(count, 1)

        row, = table.select()
        change_id = row['change_id']

        url = '/history/view/release/%d/data_version' % change_id
        ret = self.client.get(url)
        self.assertStatusCode(ret, 200)

    def testFieldViewBadValuesBadField(self):
        ret = self._put('/users/bob/permissions/admin', data=dict(options=json.dumps(dict(products=["a"]))))
        self.assertStatusCode(ret, 201)

        table = dbo.permissions.history
        row, = table.select(order_by=[table.change_id.desc()], limit=1)
        change_id = row['change_id']

        url = '/history/view/permission/%d/notafield' % change_id
        ret = self.client.get(url)
        self.assertStatusCode(ret, 400)
        self.assertTrue('Bad field' in ret.data)

    def testFieldViewRelease(self):
        # add a release
        data = json.dumps(dict(detailsUrl='blah', fakePartials=True, schema_version=1, name="d", hashFunction="sha512"))
        ret = self._post(
            '/releases/d',
            data=dict(data=data, product='d', data_version=1)
        )
        self.assertStatusCode(ret, 200)

        table = dbo.releases.history
        query = table.t.count()
        count, = query.execute().first()
        self.assertEqual(count, 1)

        row, = table.select()
        change_id = row['change_id']

        url = '/history/view/release/%d/data' % change_id
        ret = self.client.get(url)
        self.assertStatusCode(ret, 200)
        self.assertEqual(json.loads(ret.data), json.loads("""
{
    "name": "d",
    "schema_version": 1,
    "detailsUrl": "blah",
    "fakePartials": true,
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
"""))

        data = json.dumps(dict(detailsUrl='blah', fakePartials=False, schema_version=1, name="d", hashFunction="sha512"))
        ret = self._post(
            '/releases/d',
            data=dict(data=data, product='d', data_version=2)
        )
        self.assertStatusCode(ret, 200)

        table = dbo.releases.history
        row, = table.select(order_by=[table.change_id.desc()], limit=1)
        change_id = row['change_id']

        url = '/history/diff/release/%d/data' % change_id
        ret = self.client.get(url)
        self.assertStatusCode(ret, 200)
        self.assertTrue('"fakePartials": true' in ret.data)
        self.assertTrue('"fakePartials": false' in ret.data)

    def testFieldViewDiffRelease(self):

        # Add release history for d
        data = json.dumps(dict(detailsUrl='blahblah', fakePartials=False, schema_version=1, name="d", hashFunction="sha512"))
        ret = self._post(
            '/releases/d',
            data=dict(data=data, product='d', data_version=1)
        )
        self.assertStatusCode(ret, 200)

        # Let's add a separate release say for b(already present in the setUp)
        data = json.dumps(dict(detailsUrl='blahagain', fakePartials=True, schema_version=1, name="b", hashFunction="sha512"))
        ret = self._post(
            '/releases/b',
            data=dict(data=data, product='b', data_version=1)
        )
        self.assertStatusCode(ret, 200)

        # Let's add another release history for d
        data = json.dumps(dict(detailsUrl='blahblahblah', fakePartials=True, schema_version=1, name="d", hashFunction="sha512"))
        ret = self._post(
            '/releases/d',
            data=dict(data=data, product='d', data_version=2)
        )
        self.assertStatusCode(ret, 200)

        table = dbo.releases.history
        row, = table.select(order_by=[table.change_id.desc()], limit=1)
        change_id = row['change_id']

        url = '/history/diff/release/%d/data' % change_id
        ret = self.client.get(url)
        self.assertStatusCode(ret, 200)

        # Checks should give diff for versions of d
        self.assertTrue('"detailsUrl": "blahblahblah"' in ret.data)
        self.assertTrue('"detailsUrl": "blahblah"' in ret.data)
        self.assertFalse('"detailsUrl": "blahagain"' in ret.data)
        self.assertTrue('"fakePartials": true' in ret.data)
        self.assertTrue('"fakePartials": false' in ret.data)

        # Add another version for b
        data = json.dumps(dict(detailsUrl='blahagainblahagain', fakePartials=False, schema_version=1, name="b", hashFunction="sha512"))
        ret = self._post(
            '/releases/b',
            data=dict(data=data, product='b', data_version=2)
        )
        self.assertStatusCode(ret, 200)

        table = dbo.releases.history
        row, = table.select(order_by=[table.change_id.desc()], limit=1)
        change_id = row['change_id']

        url = '/history/diff/release/%d/data' % change_id
        ret = self.client.get(url)
        self.assertStatusCode(ret, 200)

        # Checks should now give diff for versions of b
        self.assertTrue('"detailsUrl": "blahagainblahagain"' in ret.data)
        self.assertTrue('"detailsUrl": "blahagain"' in ret.data)
        self.assertFalse('"detailsUrl": "blahblahblah"' in ret.data)
        self.assertTrue('"fakePartials": true' in ret.data)
        self.assertTrue('"fakePartials": false' in ret.data)

    def testFieldViewPermission(self):
        # Add a permission
        ret = self._put('/users/bob/permissions/admin', data=dict(options=json.dumps(dict(products=["a"]))))
        self.assertStatusCode(ret, 201)
        table = dbo.permissions.history
        row, = table.select(order_by=[table.timestamp.desc()], limit=1)
        change_id = row['change_id']

        url = '/history/view/permission/%d/options' % change_id
        ret = self.client.get(url)
        self.assertStatusCode(ret, 200)
        self.assertEqual(json.loads(ret.data), {"products": ["a"]})
