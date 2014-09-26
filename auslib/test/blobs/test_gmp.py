import mock
from tempfile import mkstemp
import unittest
from xml.dom import minidom

from auslib.blobs.gmp import GMPBlobV1
import auslib.log


class TestSchema1Blob(unittest.TestCase):
    maxDiff = 2000

    def setUp(self):
        self.cef_patcher = mock.patch("auslib.log.cef_event")
        self.cef_patcher.start()
        self.specialForceHosts = ["http://a.com"]
        self.whitelistedDomains = ["a.com", "boring.com"]
        self.blob = GMPBlobV1()
        self.blob.loadJSON("""
{
    "name": "fake",
    "schema_version": 1000,
    "hashFunction": "SHA512",
    "vendors": {
        "c": {
            "version": "1",
            "platforms": {
                "p": {
                    "filesize": 2,
                    "hashValue": "3",
                    "fileUrl": "http://a.com/blah"
                },
                "q": {
                    "filesize": 4,
                    "hashValue": "5",
                    "fileUrl": "http://boring.com/blah"
                },
                "q2": {
                    "alias": "q"
                }
            }
        },
        "d": {
            "version": "5",
            "platforms": {
                "q": {
                    "filesize": 10,
                    "hashValue": "11",
                    "fileUrl": "http://boring.com/foo"
                },
                "r": {
                    "filesize": 666,
                    "hashValue": "666",
                    "fileUrl": "http://evil.com/fire"
                }
            }
        }
    }
}
""")

    def tearDown(self):
        self.cef_patcher.stop()

    def testGetVendorsForPlatform(self):
        vendors = set([v for v in self.blob.getVendorsForPlatform("q")])
        self.assertEquals(set(["c", "d"]), vendors)

    def testGetVendorsForPlatformOnlyInOne(self):
        vendors = set([v for v in self.blob.getVendorsForPlatform("r")])
        self.assertEquals(set(["d"]), vendors)

    def testGetResolvedPlatform(self):
        self.assertEquals("q", self.blob.getResolvedPlatform("c", "q2"))

    def testGetPlatformData(self):
        expected = {
            "filesize": 4,
            "hashValue": "5",
            "fileUrl": "http://boring.com/blah",
        }
        self.assertEquals(self.blob.getPlatformData("c", "q2"), expected)

    def testGMPUpdate(self):
        updateQuery = {
            "product": "gg", "version": "3", "buildID": "1",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blob.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <addons>
        <addon id="c" URL="http://a.com/blah" hashFunction="SHA512" hashValue="3" size="2" version="1"/>
    </addons>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testGMPUpdateWithAlias(self):
        updateQuery = {
            "product": "gg", "version": "3", "buildID": "1",
            "buildTarget": "q2", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blob.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <addons>
        <addon id="c" URL="http://boring.com/blah" hashFunction="SHA512" hashValue="5" size="4" version="1"/>
    </addons>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testGMPUpdateMultipleAddons(self):
        updateQuery = {
            "product": "gg", "version": "3", "buildID": "1",
            "buildTarget": "q", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blob.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <addons>
        <addon id="c" URL="http://boring.com/blah" hashFunction="SHA512" hashValue="5" size="4" version="1"/>
        <addon id="d" URL="http://boring.com/foo" hashFunction="SHA512" hashValue="11" size="10" version="5"/>
    </addons>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testGMPWithForbiddenDomain(self):
        updateQuery = {
            "product": "gg", "version": "3", "buildID": "1",
            "buildTarget": "r", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        with mock.patch("auslib.AUS.cef_event") as c:
            returned = self.blob.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
            returned = minidom.parseString(returned)
            self.assertEqual(returned.getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')
