import unittest

from auslib.blobs.gmp import GMPBlobV1
from auslib.errors import BadDataError


class TestSchema1Blob(unittest.TestCase):
    maxDiff = 2000

    def setUp(self):
        self.specialForceHosts = ["http://a.com"]
        self.whitelistedDomains = {"a.com": ('gg',), 'boring.com': ('gg',)}
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
                },
                "default": {
                    "filesize": 20,
                    "hashValue": "50",
                    "fileUrl": "http://boring.com/bar"
                }
            }
        }
    }
}
""")

    def testGetVendorsForPlatform(self):
        vendors = set([v for v in self.blob.getVendorsForPlatform("q")])
        self.assertEquals(set(["c", "d"]), vendors)

    def testGetVendorsForPlatformDefault(self):
        vendors = set([v for v in self.blob.getVendorsForPlatform("q2")])
        self.assertEquals(set(["c", "d"]), vendors)

    def testGetVendorsForPlatformOnlyDefault(self):
        vendors = set([v for v in self.blob.getVendorsForPlatform("s")])
        self.assertEquals(set(["d"]), vendors)

    def testGetVendorsForPlatformOnlyInOne(self):
        vendors = set([v for v in self.blob.getVendorsForPlatform("r")])
        self.assertEquals(set(["d"]), vendors)

    def testGetResolvedPlatform(self):
        self.assertEquals("q", self.blob.getResolvedPlatform("c", "q2"))

    def testGetResolvedPlatformDefault(self):
        self.assertEquals("default", self.blob.getResolvedPlatform("d", "q2"))

    def testGetResolvedPlatformSpecificOverridesDefault(self):
        self.assertEquals("r", self.blob.getResolvedPlatform("d", "r"))

    def testGetResolvedPlatformRaisesBadDataError(self):
        self.assertRaises(BadDataError, self.blob.getResolvedPlatform, "c", "bbb")

    def testGetPlatformData(self):
        expected = {
            "filesize": 4,
            "hashValue": "5",
            "fileUrl": "http://boring.com/blah",
        }
        self.assertEquals(self.blob.getPlatformData("c", "q2"), expected)

    def testGetPlatformDataRaisesBadDataError(self):
        self.assertRaises(BadDataError, self.blob.getPlatformData, "c", "f")

    def testGMPUpdate(self):
        updateQuery = {
            "product": "gg", "version": "3", "buildID": "1",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = "<addons>"
        expected = ["""
<addon id="c" URL="http://a.com/blah" hashFunction="SHA512" hashValue="3" size="2" version="1"/>
""", """
<addon id="d" URL="http://boring.com/bar" hashFunction="SHA512" hashValue="50" size="20" version="5"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</addons>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testGMPUpdateWithAlias(self):
        updateQuery = {
            "product": "gg", "version": "3", "buildID": "1",
            "buildTarget": "q2", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = "<addons>"
        expected = ["""
<addon id="c" URL="http://boring.com/blah" hashFunction="SHA512" hashValue="5" size="4" version="1"/>
""", """
<addon id="d" URL="http://boring.com/bar" hashFunction="SHA512" hashValue="50" size="20" version="5"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</addons>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testGMPUpdateSingleAddons(self):
        updateQuery = {
            "product": "gg", "version": "3", "buildID": "1",
            "buildTarget": "q5", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = "<addons>"
        expected = ["""
<addon id="d" URL="http://boring.com/bar" hashFunction="SHA512" hashValue="50" size="20" version="5"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</addons>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testGMPUpdateMultipleAddons(self):
        updateQuery = {
            "product": "gg", "version": "3", "buildID": "1",
            "buildTarget": "q", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = "<addons>"
        expected = ["""
<addon id="c" URL="http://boring.com/blah" hashFunction="SHA512" hashValue="5" size="4" version="1"/>
""", """
<addon id="d" URL="http://boring.com/foo" hashFunction="SHA512" hashValue="11" size="10" version="5"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</addons>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testGMPWithForbiddenDomain(self):
        updateQuery = {
            "product": "gg", "version": "3", "buildID": "1",
            "buildTarget": "r", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = "<addons>"
        expected = []
        expected = [x.strip() for x in expected]
        expected_footer = "</addons>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testContainsForbiddenDomain(self):
        blob = GMPBlobV1()
        blob.loadJSON("""
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
                    "fileUrl": "http://evil.com/blah"
                }
            }
        }
    }
}
""")
        self.assertTrue(blob.containsForbiddenDomain('gg',
                                                     self.whitelistedDomains))

    def testDoesNotContainForbiddenDomain(self):
        blob = GMPBlobV1()
        blob.loadJSON("""
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
                }
            }
        }
    }
}
""")
        self.assertFalse(blob.containsForbiddenDomain('gg',
                                                      self.whitelistedDomains))

    def testGMPLayoutEmptyVendor(self):

        # Correct layout with empty vendors

        blob = GMPBlobV1()
        blob.loadJSON("""
    {
        "name": "fake",
        "schema_version": 1000,
        "hashFunction": "SHA512",
        "vendors": {}
    }
    """)
        blob.validate('gg', self.whitelistedDomains)

    def testGMPLayoutNoVendor(self):

        # Incorrect layout with no vendors

        blob = GMPBlobV1()
        blob.loadJSON("""
    {
        "name": "fake",
        "schema_version": 1000,
        "hashFunction": "SHA512"
    }
    """)
        self.assertRaises(Exception, blob.validate, 'gg', self.whitelistedDomains)

    def testGMPLayoutTwoPlatforms(self):

        # Correct layout with one vendor and two platforms

        blob = GMPBlobV1()
        blob.loadJSON("""
    {
        "name": "fake",
        "schema_version": 1000,
        "hashFunction": "SHA512",
        "vendors": {
            "c": {
                "version": "1",
                "platforms": {
                    "p": {
                        "alias": "q"
                    },
                    "q": {
                        "filesize": 2,
                        "hashValue": "3",
                        "fileUrl": "http://boring.com/blah"
                    }
                }
            }
        }
    }
    """)
        blob.validate('gg', self.whitelistedDomains)

    def testGMPLayoutMissingVersion(self):

        # Incorrect layout with missing version for an vendor name

        blob = GMPBlobV1()
        blob.loadJSON("""
    {
        "name": "fake",
        "schema_version": 1000,
        "hashFunction": "SHA512",
        "vendors": {
            "c": {
                "platforms": {
                    "p": {
                        "alias": "q"
                    },
                    "q": {
                        "filesize": 2,
                        "hashValue": "3",
                        "fileUrl": "http://boring.com/blah"
                    }
                }
            }
        }
    }
    """)
        self.assertRaises(Exception, blob.validate, 'gg', self.whitelistedDomains)

    def testGMPLayoutEmptyPlatforms(self):

        # Correct layout with empty platforms

        blob = GMPBlobV1()
        blob.loadJSON("""
    {
        "name": "fake",
        "schema_version": 1000,
        "hashFunction": "SHA512",
        "vendors": {
            "c": {
                "version": "1",
                "platforms": {}
            }
        }
    }
    """)
        blob.validate('gg', self.whitelistedDomains)

    def testGMPLayoutEmptyPlatformName(self):

        # Incorrect layout with empty platform name

        blob = GMPBlobV1()
        blob.loadJSON("""
    {
        "name": "fake",
        "schema_version": 1000,
        "hashFunction": "SHA512",
        "vendors": {
            "c": {
                "version": "1",
                "platforms": {
                    "p": {},
                    "q": {
                        "filesize": 2,
                        "hashValue": "3",
                        "fileUrl": "http://boring.com/blah"
                    }
                }
            }
        }
    }
    """)
        self.assertRaises(Exception, blob.validate, 'gg', self.whitelistedDomains)

    def testGMPLayoutNoFilesize(self):

        # Incorrect layout with missing filesize

        blob = GMPBlobV1()
        blob.loadJSON("""
    {
        "name": "fake",
        "schema_version": 1000,
        "hashFunction": "SHA512",
        "vendors": {
            "c": {
                "version": "1",
                "platforms": {
                    "p": {
                        "alias": "q"
                    },
                    "q": {
                        "hashValue": "3",
                        "fileUrl": "http://boring.com/blah"
                    }
                }
            }
        }
    }
    """)
        self.assertRaises(Exception, blob.validate, 'gg', self.whitelistedDomains)
