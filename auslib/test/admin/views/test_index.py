import time
from xml.etree import ElementTree as ET
import unittest
from auslib.test.admin.views.base import ViewTest
from auslib.admin.views.index import getTimeAgo


class TestIndexPage(ViewTest):

    def testLandingPage(self):
        ret = self.client.get('/')
        self.assertStatusCode(ret, 200)
        # know thy fixtures
        self.assertTrue('5 rules' in ret.data)
        self.assertTrue('5 releases' in ret.data)
        self.assertTrue('2 users' in ret.data)

    def testRecentChangesTable(self):
        url = '/recent_changes_table.html'
        ret = self.client.get(url)
        self.assertStatusCode(ret, 200)
        rows = self._parseRows(ret.data)
        self.assertEqual(rows, [])

        # Add a permission
        ret = self._put('/users/bob/permissions/admin')
        self.assertStatusCode(ret, 201)
        ret = self.client.get(url)
        self.assertStatusCode(ret, 200)
        rows = self._parseRows(ret.data)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], 'permission')  # what
        self.assertEqual(rows[0][1], 'bill')  # who
        self.assertEqual(rows[0][-1], 'insert')  # change

        # Edit a permission
        ret = self._post('/users/bill/permissions/admin',
                         data=dict(options="", data_version=1))
        self.assertStatusCode(ret, 200)
        ret = self.client.get(url)
        rows = self._parseRows(ret.data)
        self.assertEqual(rows[0][0], 'permission')
        self.assertEqual(rows[0][1], 'bill')
        self.assertEqual(rows[0][-1], 'update')

        # Delete a permission
        ret = self._delete(
            '/users/bob/permissions/users/:id/permissions/:permission',
            qs=dict(data_version=1)
        )
        self.assertStatusCode(ret, 200)
        ret = self.client.get(url)
        rows = self._parseRows(ret.data)
        self.assertEqual(rows[0][0], 'permission')
        self.assertEqual(rows[0][1], 'bill')
        self.assertEqual(rows[0][-1], 'delete')

    def _parseRows(self, table_html):
        tree = ET.fromstring(table_html)
        tbody = tree.find('tbody')
        rows = []
        for tr in tbody.getchildren():
            row = []
            for td in tr.getchildren():
                a = td.find('a')
                if a is not None:
                    row.append(a.text.strip())
                else:
                    row.append(td.text.strip())
            rows.append(row)
        return rows


class TestTimeAgo(unittest.TestCase):
    """tests the getTimeAgo function"""

    def test_getTimeAgo(self):
        # getTimeAgo expects the timestamp in milliseconds
        ts = 1000 * (time.time() - 60)
        self.assertEqual(getTimeAgo(ts), '1 minute ago')

        ts = 1000 * (time.time() - 3)
        self.assertEqual(getTimeAgo(ts), 'seconds ago')

        ts = 1000 * (time.time() - 3600)
        self.assertEqual(getTimeAgo(ts), '1 hour ago')

        ts = 1000 * (time.time() - 3600 * 24)
        self.assertEqual(getTimeAgo(ts), '1 day ago')

        ts = 1000 * (time.time() - 3600 * 24 * 7)
        self.assertEqual(getTimeAgo(ts), '1 week ago')
