import unittest

from auslib.blobs.gmp import GMPBlobV1
from auslib.errors import BadDataError


class TestSchema1Blob(unittest.TestCase):
    maxDiff = 2000

    def setUp(self):
        self.specialForceHosts = ["http://a.com"]
        self.allowlistedDomains = {"a.com": ("gg",), "boring.com": ("gg",)}
        self.blob = GMPBlobV1()
        self.blob.loadJSON(
            """
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
                "t": {
                    "filesize": 21,
                    "hashValue": "22",
                    "fileUrl": "http://boring.com/qux",
                    "mirrorUrls": [
                        "http://boring.com/qux_alt",
                        "http://boring.com/qux_alt2"
                    ]
                },
                "u": {
                    "filesize": 23,
                    "hashValue": "24",
                    "fileUrl": "http://boring.com/baz",
                    "mirrorUrls": ["http://evil.com/fire"]
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
"""
        )

    def testValidateHashLength(self):
        blob = GMPBlobV1()
        blob.allowlistedDomains = {"boring.com": ("gg",)}
        blob.loadJSON(
            """
{
    "name": "validName",
    "schema_version": 1000,
    "hashFunction": "SHA512",
    "vendors": {
        "a": {
            "version": "5",
            "platforms": {
                "default": {
                    "filesize": 20,
                    "hashValue": "50",
                    "fileUrl": "http://boring.com/bar"
                }
            }
        }
    }
}
"""
        )
        self.assertRaisesRegex(
            ValueError, ("The hashValue length is different from the required length of 128 for sha512"), blob.validate, "gg", self.allowlistedDomains
        )

    def testGetVendorsForPlatform(self):
        vendors = set([v for v in self.blob.getVendorsForPlatform("q")])
        self.assertEqual(set(["c", "d"]), vendors)

    def testGetVendorsForPlatformDefault(self):
        vendors = set([v for v in self.blob.getVendorsForPlatform("q2")])
        self.assertEqual(set(["c", "d"]), vendors)

    def testGetVendorsForPlatformOnlyDefault(self):
        vendors = set([v for v in self.blob.getVendorsForPlatform("s")])
        self.assertEqual(set(["d"]), vendors)

    def testGetVendorsForPlatformOnlyInOne(self):
        vendors = set([v for v in self.blob.getVendorsForPlatform("r")])
        self.assertEqual(set(["d"]), vendors)

    def testGetResolvedPlatform(self):
        self.assertEqual("q", self.blob.getResolvedPlatform("c", "q2"))

    def testGetResolvedPlatformDefault(self):
        self.assertEqual("default", self.blob.getResolvedPlatform("d", "q2"))

    def testGetResolvedPlatformSpecificOverridesDefault(self):
        self.assertEqual("r", self.blob.getResolvedPlatform("d", "r"))

    def testGetResolvedPlatformRaisesBadDataError(self):
        self.assertRaises(BadDataError, self.blob.getResolvedPlatform, "c", "bbb")

    def testGetPlatformData(self):
        expected = {"filesize": 4, "hashValue": "5", "fileUrl": "http://boring.com/blah"}
        self.assertEqual(self.blob.getPlatformData("c", "q2"), expected)

    def testGetPlatformDataWithMirror(self):
        expected = {
            "filesize": 21,
            "hashValue": "22",
            "fileUrl": "http://boring.com/qux",
            "mirrorUrls": ["http://boring.com/qux_alt", "http://boring.com/qux_alt2"],
        }
        self.assertEqual(self.blob.getPlatformData("d", "t"), expected)

    def testGetPlatformDataRaisesBadDataError(self):
        self.assertRaises(BadDataError, self.blob.getPlatformData, "c", "f")

    def testGMPUpdate(self):
        updateQuery = {
            "product": "gg",
            "version": "3",
            "buildID": "1",
            "buildTarget": "p",
            "locale": "l",
            "channel": "a",
            "osVersion": "a",
            "distribution": "a",
            "distVersion": "a",
            "force": 0,
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = "<addons>"
        expected = [
            """
<addon id="c" URL="http://a.com/blah" hashFunction="SHA512" hashValue="3" size="2" version="1"/>
""",
            """
<addon id="d" URL="http://boring.com/bar" hashFunction="SHA512" hashValue="50" size="20" version="5"/>
""",
        ]
        expected = [x.strip() for x in expected]
        expected_footer = "</addons>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertCountEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testGMPUpdateWithAlias(self):
        updateQuery = {
            "product": "gg",
            "version": "3",
            "buildID": "1",
            "buildTarget": "q2",
            "locale": "l",
            "channel": "a",
            "osVersion": "a",
            "distribution": "a",
            "distVersion": "a",
            "force": 0,
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = "<addons>"
        expected = [
            """
<addon id="c" URL="http://boring.com/blah" hashFunction="SHA512" hashValue="5" size="4" version="1"/>
""",
            """
<addon id="d" URL="http://boring.com/bar" hashFunction="SHA512" hashValue="50" size="20" version="5"/>
""",
        ]
        expected = [x.strip() for x in expected]
        expected_footer = "</addons>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertCountEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testGMPUpdateWithMirror(self):
        updateQuery = {
            "product": "gg",
            "version": "3",
            "buildID": "1",
            "buildTarget": "t",
            "locale": "l",
            "channel": "a",
            "osVersion": "a",
            "distribution": "a",
            "distVersion": "a",
            "force": 0,
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = "<addons>"
        expected = [
            """
<addon id="d" URL="http://boring.com/qux" hashFunction="SHA512" hashValue="22" size="21" version="5">
""",
            '<mirror URL="http://boring.com/qux_alt"/>',
            '<mirror URL="http://boring.com/qux_alt2"/>',
            "</addon>",
        ]
        expected = [x.strip() for x in expected]
        expected_footer = "</addons>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertCountEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testGMPUpdateSingleAddons(self):
        updateQuery = {
            "product": "gg",
            "version": "3",
            "buildID": "1",
            "buildTarget": "q5",
            "locale": "l",
            "channel": "a",
            "osVersion": "a",
            "distribution": "a",
            "distVersion": "a",
            "force": 0,
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = "<addons>"
        expected = [
            """
<addon id="d" URL="http://boring.com/bar" hashFunction="SHA512" hashValue="50" size="20" version="5"/>
"""
        ]
        expected = [x.strip() for x in expected]
        expected_footer = "</addons>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertCountEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testGMPUpdateMultipleAddons(self):
        updateQuery = {
            "product": "gg",
            "version": "3",
            "buildID": "1",
            "buildTarget": "q",
            "locale": "l",
            "channel": "a",
            "osVersion": "a",
            "distribution": "a",
            "distVersion": "a",
            "force": 0,
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = "<addons>"
        expected = [
            """
<addon id="c" URL="http://boring.com/blah" hashFunction="SHA512" hashValue="5" size="4" version="1"/>
""",
            """
<addon id="d" URL="http://boring.com/foo" hashFunction="SHA512" hashValue="11" size="10" version="5"/>
""",
        ]
        expected = [x.strip() for x in expected]
        expected_footer = "</addons>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertCountEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testGMPWithForbiddenDomain(self):
        updateQuery = {
            "product": "gg",
            "version": "3",
            "buildID": "1",
            "buildTarget": "r",
            "locale": "l",
            "channel": "a",
            "osVersion": "a",
            "distribution": "a",
            "distVersion": "a",
            "force": 0,
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = "<addons>"
        expected = []
        expected = [x.strip() for x in expected]
        expected_footer = "</addons>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertCountEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testGMPWithForbiddenDomainInMirror(self):
        updateQuery = {
            "product": "gg",
            "version": "3",
            "buildID": "1",
            "buildTarget": "u",
            "locale": "l",
            "channel": "a",
            "osVersion": "a",
            "distribution": "a",
            "distVersion": "a",
            "force": 0,
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = "<addons>"
        expected = [
            """
<addon id="d" URL="http://boring.com/baz" hashFunction="SHA512" hashValue="24" size="23" version="5"/>
""",
        ]
        expected = [x.strip() for x in expected]
        expected_footer = "</addons>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertCountEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testContainsForbiddenDomain(self):
        blob = GMPBlobV1()
        blob.loadJSON(
            """
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
"""
        )
        self.assertTrue(blob.containsForbiddenDomain("gg", self.allowlistedDomains))

    def testContainsForbiddenDomainInMirror(self):
        blob = GMPBlobV1()
        blob.loadJSON(
            """
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
                    "fileUrl": "http://a.com/blah",
                    "mirrorUrls": ["http://evil.com/blah"]
                }
            }
        }
    }
}
"""
        )
        self.assertTrue(blob.containsForbiddenDomain("gg", self.allowlistedDomains))

    def testDoesNotContainForbiddenDomain(self):
        blob = GMPBlobV1()
        blob.loadJSON(
            """
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
"""
        )
        self.assertFalse(blob.containsForbiddenDomain("gg", self.allowlistedDomains))

    def testDoesNotContainForbiddenDomainWithMirror(self):
        blob = GMPBlobV1()
        blob.loadJSON(
            """
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
                    "fileUrl": "http://a.com/blah",
                    "mirrorUrls": ["http://a.com/blah2"]
                }
            }
        }
    }
}
"""
        )
        self.assertFalse(blob.containsForbiddenDomain("gg", self.allowlistedDomains))

    def testGMPLayoutEmptyVendor(self):
        # Correct layout with empty vendors

        blob = GMPBlobV1()
        blob.loadJSON(
            """
    {
        "name": "fake",
        "schema_version": 1000,
        "hashFunction": "SHA512",
        "vendors": {}
    }
    """
        )
        blob.validate("gg", self.allowlistedDomains)

    def testGMPLayoutNoVendor(self):
        # Incorrect layout with no vendors

        blob = GMPBlobV1()
        blob.loadJSON(
            """
    {
        "name": "fake",
        "schema_version": 1000,
        "hashFunction": "SHA512"
    }
    """
        )
        self.assertRaises(Exception, blob.validate, "gg", self.allowlistedDomains)

    def testGMPLayoutTwoPlatforms(self):
        # Correct layout with one vendor and two platforms

        blob = GMPBlobV1()
        blob.loadJSON(
            """
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
                        "hashValue": "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcda\
bcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd",
                        "fileUrl": "http://boring.com/blah"
                    }
                }
            }
        }
    }
    """
        )
        blob.validate("gg", self.allowlistedDomains)

    def testGMPLayoutMissingVersion(self):
        # Incorrect layout with missing version for an vendor name

        blob = GMPBlobV1()
        blob.loadJSON(
            """
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
                        "hashValue": "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcda\
bcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd",
                        "fileUrl": "http://boring.com/blah"
                    }
                }
            }
        }
    }
    """
        )
        self.assertRaises(Exception, blob.validate, "gg", self.allowlistedDomains)

    def testGMPLayoutEmptyPlatforms(self):
        # Correct layout with empty platforms

        blob = GMPBlobV1()
        blob.loadJSON(
            """
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
    """
        )
        blob.validate("gg", self.allowlistedDomains)

    def testGMPLayoutEmptyPlatformName(self):
        # Incorrect layout with empty platform name

        blob = GMPBlobV1()
        blob.loadJSON(
            """
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
                        "hashValue": "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcda\
bcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd",
                        "fileUrl": "http://boring.com/blah"
                    }
                }
            }
        }
    }
    """
        )
        self.assertRaises(Exception, blob.validate, "gg", self.allowlistedDomains)

    def testGMPLayoutNoFilesize(self):
        # Incorrect layout with missing filesize

        blob = GMPBlobV1()
        blob.loadJSON(
            """
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
                        "hashValue": "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcda\
bcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd",
                        "fileUrl": "http://boring.com/blah"
                    }
                }
            }
        }
    }
    """
        )
        self.assertRaises(Exception, blob.validate, "gg", self.allowlistedDomains)
