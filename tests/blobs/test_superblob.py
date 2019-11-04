import unittest

from auslib.blobs.superblob import SuperBlob


class TestSchema1Blob(unittest.TestCase):
    maxDiff = 2000

    def setUp(self):
        self.specialForceHosts = ("http://a.com",)
        self.whitelistedDomains = {"a.com": ("b", "c", "e", "b2g", "response-a", "response-b", "s")}
        self.superblob_gmp = SuperBlob()
        self.superblob_gmp.loadJSON(
            """
{
    "name": "GMPSuperblob",
    "schema_version": 1000,
    "products": [
        "c",
        "d"
    ]
}
"""
        )
        self.superblob_addon = SuperBlob()
        self.superblob_addon.loadJSON(
            """
{
    "name": "SystemAddOnsSuperblob",
    "schema_version": 1000,
    "blobs": [
        "Hello-1.0",
        "Pocket-2.0"
    ]
}
"""
        )

    def testGetResponseBlobs(self):
        blob_names_addon = self.superblob_addon.getResponseBlobs()
        blob_names_gmp = self.superblob_gmp.getResponseBlobs()
        self.assertEqual(blob_names_addon, ["Hello-1.0", "Pocket-2.0"])
        self.assertIsNone(blob_names_gmp)

    def testGetResponseProducts(self):
        products_gmp = self.superblob_gmp.getResponseProducts()
        products_addon = self.superblob_addon.getResponseProducts()
        self.assertEqual(products_gmp, ["c", "d"])
        self.assertIsNone(products_addon)

    def testInnerHeaderXML(self):
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
        headerXML_gmp = self.superblob_gmp.getInnerHeaderXML(
            updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts
        )
        headerXML_addon = self.superblob_addon.getInnerHeaderXML(
            updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts
        )

        expected_header_gmp = "    <addons>"
        expected_header_addon = "    <addons>"

        self.assertEqual(headerXML_gmp, expected_header_gmp)
        self.assertEqual(headerXML_addon, expected_header_addon)

    def testInnerFooterXML(self):
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
        footerXML_gmp = self.superblob_gmp.getInnerFooterXML(
            updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts
        )
        footerXML_addon = self.superblob_addon.getInnerFooterXML(
            updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts
        )
        expected_footer_gmp = "    </addons>"
        expected_footer_addon = "    </addons>"
        self.assertEqual(footerXML_gmp, expected_footer_gmp)
        self.assertEqual(footerXML_addon, expected_footer_addon)
