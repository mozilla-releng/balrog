import unittest

from auslib.blobs.systemaddons import SystemAddonsBlob


class TestSchema1Blob(unittest.TestCase):
    maxDiff = 2000

    def setUp(self):
        self.specialForceHosts = ["http://a.com"]
        self.allowlistedDomains = {"a.com": ("gg",), "boring.com": ("gg",)}
        self.blob1 = SystemAddonsBlob()
        self.blob1.loadJSON(
            """
{
    "name": "fake",
    "schema_version": 5000,
    "hashFunction": "SHA512",
    "addons": {
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
"""
        )
        self.blob2 = SystemAddonsBlob()
        self.blob2.loadJSON(
            """
{
    "name": "fake",
    "schema_version": 5000,
    "hashFunction": "SHA512",
    "uninstall": true
}
"""
        )
        self.blob3 = SystemAddonsBlob()
        self.blob3.loadJSON(
            """
{
    "name": "fake",
    "schema_version": 5000,
    "hashFunction": "SHA512",
    "uninstall": false
}
"""
        )
        self.empty_blob = SystemAddonsBlob()
        self.empty_blob.loadJSON(
            """
{
    "name": "fake",
    "schema_version": 5000,
    "hashFunction": "SHA512",
    "addons": {}
}
"""
        )

    def testXML(self):
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
        returned_header = self.blob1.getInnerHeaderXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = self.blob1.getInnerXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned_footer = self.blob1.getInnerFooterXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = "    <addons>"
        expected = [
            """
<addon id="c" URL="http://a.com/blah" hashFunction="SHA512" hashValue="3" size="2" version="1"/>
""",
            """
<addon id="d" URL="http://boring.com/bar" hashFunction="SHA512" hashValue="50" size="20" version="5"/>
""",
        ]
        expected = [x.strip() for x in expected]
        expected_footer = "    </addons>"
        self.assertEqual(returned_header, expected_header)
        self.assertCountEqual(returned, expected)
        self.assertEqual(returned_footer, expected_footer)

    def testXMLWhenEmptyAndNotUninstall(self):
        updateQuery = {
            "product": "gg",
            "version": "3",
            "buildID": "1",
            "buildTarget": "t",
            "locale": "l",
            "channel": "a",
            "osVersion": "z",
            "distribution": "a",
            "distVersion": "a",
            "force": 0,
        }
        returned_header = self.empty_blob.getInnerHeaderXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = self.empty_blob.getInnerXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned_footer = self.empty_blob.getInnerFooterXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = ""
        expected = []
        expected = [x.strip() for x in expected]
        expected_footer = ""
        self.assertEqual(returned_header, expected_header)
        self.assertCountEqual(returned, expected)
        self.assertEqual(returned_footer, expected_footer)

    def testXMLWhenUninstall(self):
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
        returned_header = self.blob2.getInnerHeaderXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = self.blob2.getInnerXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned_footer = self.blob2.getInnerFooterXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = "    <addons>"
        expected = []
        expected = [x.strip() for x in expected]
        expected_footer = "    </addons>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertCountEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())
        self.assertEqual(returned_footer, expected_footer)

    def testXMLNoAddonsNoUninstallBlob(self):
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
        returned_header = self.blob3.getInnerHeaderXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = self.blob3.getInnerXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned_footer = self.blob3.getInnerFooterXML(updateQuery, "minor", self.allowlistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = ""
        expected = []
        expected = [x.strip() for x in expected]
        expected_footer = ""
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertCountEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())
        self.assertEqual(returned_footer, expected_footer)

    def testContainsForbiddenDomain(self):
        blob = SystemAddonsBlob()
        blob.loadJSON(
            """
{
    "name": "fake",
    "schema_version": 1000,
    "hashFunction": "SHA512",
    "addons": {
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

    def testDoesNotContainForbiddenDomain(self):
        blob = SystemAddonsBlob()
        blob.loadJSON(
            """
{
    "name": "fake",
    "schema_version": 1000,
    "hashFunction": "SHA512",
    "addons": {
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

    def testAddonLayoutEmptyAddons(self):
        # Correct layout with empty addons

        blob = SystemAddonsBlob()
        blob.loadJSON(
            """
    {
        "name": "fake",
        "schema_version": 5000,
        "hashFunction": "SHA512",
        "addons": {}
    }
    """
        )
        blob.validate("gg", self.allowlistedDomains)

    def testAddonLayoutWithUninstall(self):
        # Correct layout with no addons, and with uninstall

        blob = SystemAddonsBlob()
        blob.loadJSON(
            """
    {
        "name": "fake",
        "schema_version": 5000,
        "hashFunction": "SHA512",
        "uninstall": false
    }
    """
        )
        blob.validate("gg", self.allowlistedDomains)

    def testAddonLayoutNoAddonsNoUninstall(self):
        # Incorrect layout with no addons and no uninstall

        blob = SystemAddonsBlob()
        blob.loadJSON(
            """
    {
        "name": "fake",
        "schema_version": 5000,
        "hashFunction": "SHA512"
    }
    """
        )
        self.assertRaises(Exception, blob.validate, "gg", self.allowlistedDomains)

    def testAddonLayoutTwoPlatforms(self):
        # Correct layout with one addon and two platforms

        blob = SystemAddonsBlob()
        blob.loadJSON(
            """
    {
        "name": "fake",
        "schema_version": 5000,
        "hashFunction": "SHA512",
        "addons": {
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
    """
        )
        blob.validate("gg", self.allowlistedDomains)

    def testAddonLayoutNoVersion(self):
        # Incorrect layout with missing version for an addon name

        blob = SystemAddonsBlob()
        blob.loadJSON(
            """
    {
        "name": "fake",
        "schema_version": 5000,
        "hashFunction": "SHA512",
        "addons": {
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
    """
        )
        self.assertRaises(Exception, blob.validate, "gg", self.allowlistedDomains)

    def testAddonLayoutEmptyPlatforms(self):
        # Correct layout with empty platforms

        blob = SystemAddonsBlob()
        blob.loadJSON(
            """
    {
        "name": "fake",
        "schema_version": 5000,
        "hashFunction": "SHA512",
        "addons": {
            "c": {
                "version": "1",
                "platforms": {}
            }
        }
    }
    """
        )
        blob.validate("gg", self.allowlistedDomains)

    def testAddonLayoutEmptyPlatformName(self):
        # Incorrect layout with empty platform name

        blob = SystemAddonsBlob()
        blob.loadJSON(
            """
    {
        "name": "fake",
        "schema_version": 5000,
        "hashFunction": "SHA512",
        "addons": {
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
    """
        )
        self.assertRaises(Exception, blob.validate, "gg", self.allowlistedDomains)

    def testAddonLayoutNoFilesize(self):
        # Incorrect layout with missing filesize

        blob = SystemAddonsBlob()
        blob.loadJSON(
            """
    {
        "name": "fake",
        "schema_version": 5000,
        "hashFunction": "SHA512",
        "addons": {
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
    """
        )
        self.assertRaises(Exception, blob.validate, "gg", self.allowlistedDomains)
