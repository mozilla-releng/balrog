import unittest

from auslib.blobs.superblob import SuperBlob
from auslib.test.test_db import MemoryDatabaseMixin


class TestSchema1Blob(unittest.TestCase, MemoryDatabaseMixin):
    maxDiff = 2000

    def setUp(self):
        self.specialForceHosts = ('http://a.com',)
        self.whitelistedDomains = {'a.com': ('b', 'c', 'e', 'b2g', 'response-a', 'response-b', 's')}
        self.superblob = SuperBlob()
        self.superblob.loadJSON("""
{
    "name": "fake",
    "schema_version": 1000,
    "products": [
        "c",
        "d"
    ]
}
""")

    def testGetResponseProducts(self):
        products = self.superblob.getResponseProducts()
        self.assertEqual(products, ['c', 'd'])

    def testXML(self):
        updateQuery = {
            "product": "gg", "version": "3", "buildID": "1",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        headerXML = self.superblob.getHeaderXML(updateQuery, "minor", self.whitelistedDomains,
                                                self.specialForceHosts)
        footerXML = self.superblob.getFooterXML(updateQuery, "minor", self.whitelistedDomains,
                                                self.specialForceHosts)
        expected_header = '    <addons>'
        expected_footer = '    </addons>'
        self.assertEqual(headerXML, expected_header)
        self.assertEqual(footerXML, expected_footer)
