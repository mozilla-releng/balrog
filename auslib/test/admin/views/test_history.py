import json
from auslib.admin.base import db
from auslib.test.admin.views.base import ViewTest


class TestHistoryView(ViewTest):

    def testFieldViewBadValues(self):
        url = '/view/notatable/1/whatever'
        ret = self.client.get(url)
        self.assertStatusCode(ret, 400)
        self.assertTrue('Bad table' in ret.data)

        url = '/view/permission/9999/whatever'
        ret = self.client.get(url)
        self.assertStatusCode(ret, 404)
        self.assertTrue('Bad change_id' in ret.data)

        ret = self._put('/users/bob/permissions/admin')
        self.assertStatusCode(ret, 201)

        query = db.permissions.history.t.select()
        row = query.execute().first()
        change_id = row[0]
        url = '/view/permission/%d/notafield' % change_id
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

        query = db.releases.history.t.count()
        count, = query.execute().first()
        self.assertEqual(count, 1)

        query = db.releases.history.t.select()
        row = query.execute().first()
        change_id = row[0]
        url = '/view/release/%d/data' % change_id
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
                        "filesize": 1234
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

        query = db.releases.history.t.select(
            order_by=[db.releases.history.change_id.desc()]
        )
        row = query.execute().first()
        change_id = row[0]

        url = '/diff/release/%d/data' % change_id
        ret = self.client.get(url)
        self.assertStatusCode(ret, 200)
        self.assertTrue('"fakePartials": true' in ret.data)
        self.assertTrue('"fakePartials": false' in ret.data)

    def testFieldViewPermission(self):
        # Add a permission
        ret = self._put('/users/bob/permissions/admin')
        self.assertStatusCode(ret, 201)
        query = db.permissions.history.t.select()
        row = query.execute().first()
        change_id = row[0]
        url = '/view/permission/%d/options' % change_id
        ret = self.client.get(url)
        self.assertStatusCode(ret, 200)
        self.assertEqual(ret.data, 'NULL')
