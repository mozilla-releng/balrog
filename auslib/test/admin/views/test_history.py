import json
from auslib.admin.base import db
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

    def testFieldViewBadValuesBadField(self):
        ret = self._put('/users/bob/permissions/admin')
        self.assertStatusCode(ret, 201)

        table = db.permissions.history
        row, = table.select(order_by=[table.change_id.desc()], limit=1)
        change_id = row['change_id']

        url = '/history/view/permission/%d/notafield' % change_id
        ret = self.client.get(url)
        self.assertStatusCode(ret, 400)
        self.assertTrue('Bad field' in ret.data)

    def testFieldViewRelease(self):
        # add a release
        data = json.dumps(dict(detailsUrl='blah', fakePartials=True))
        ret = self._post(
            '/releases/d',
            data=dict(data=data, product='d', version='d', data_version=1)
        )
        self.assertStatusCode(ret, 200)

        table = db.releases.history
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
    "detailsUrl": "blah",
    "fakePartials": true,
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
"""))

        data = json.dumps(dict(detailsUrl='blah', fakePartials=False))
        ret = self._post(
            '/releases/d',
            data=dict(data=data, product='d', version='d', data_version=2)
        )
        self.assertStatusCode(ret, 200)

        table = db.releases.history
        row, = table.select(order_by=[table.change_id.desc()], limit=1)
        change_id = row['change_id']

        url = '/history/diff/release/%d/data' % change_id
        ret = self.client.get(url)
        self.assertStatusCode(ret, 200)
        self.assertTrue('"fakePartials": true' in ret.data)
        self.assertTrue('"fakePartials": false' in ret.data)

    def testFieldViewPermission(self):
        # Add a permission
        ret = self._put('/users/bob/permissions/admin')
        self.assertStatusCode(ret, 201)
        table = db.permissions.history
        row, = table.select(order_by=[table.timestamp.desc()], limit=1)
        change_id = row['change_id']

        url = '/history/view/permission/%d/options' % change_id
        ret = self.client.get(url)
        self.assertStatusCode(ret, 200)
        self.assertEqual(ret.data, 'NULL')
