import unittest

from auslib.blobs.superblob_addon import SuperBlobAddon
from auslib.test.test_db import MemoryDatabaseMixin


class TestSchema1Blob(unittest.TestCase, MemoryDatabaseMixin):
    maxDiff = 2000

    def setUp(self):
        self.specialForceHosts = ('http://a.com',)
        self.whitelistedDomains = {'a.com': ('b', 'c', 'e', 'b2g', 'response-a', 'response-b', 's')}
        self.superblob_addon = SuperBlobAddon()
        self.superblob_addon.loadJSON("""
{
    "name": "fake",
    "schema_version": 6000,
    "revision": 123,
    "blobs": [
        "Hello-1.0",
        "Pocket-2.0"
    ]
}
""")

    def testGetResponseProducts(self):
        blob_names = self.superblob_addon.getResponseBlobs()
        self.assertEqual(blob_names, ['Hello-1.0', 'Pocket-2.0'])

    def testXML(self):
        updateQuery = {
            "product": "gg", "version": "3", "buildID": "1",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        headerXML = self.superblob_addon.getHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        footerXML = self.superblob_addon.getFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        expected_header = '    <addons revision=123>'
        expected_footer = '    </addons>'
        self.assertEqual(headerXML, expected_header)
        self.assertEqual(footerXML, expected_footer)
