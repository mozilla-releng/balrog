import unittest

from auslib.blobs.whitelist import WhitelistBlobV1


_DATA = """\
{
  "name": "b2g-whitelist",
  "schema_version": 3000,
  "whitelist": [
    { "imei": "000000000000000" },
    { "imei": "000000000000001" },
    { "imei": "000000000000002" }
  ]
}
"""


class TestWhitelist(unittest.TestCase):

    def test_whitelist_blob(self):
        self.blob = WhitelistBlobV1()
        self.blob.loadJSON(_DATA)
        self.blob.validate('fake', [])

        update_query = {
            "product": "b2g", "version": "2.5", "buildID": "1",
            "buildTarget": "a", "locale": "a", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0, "IMEI": "999999999999999"
        }

        # not whitelisted, shouldn't serve update
        self.assertFalse(self.blob.shouldServeUpdate(update_query))

        # whitelisted, should serve update
        update_query["IMEI"] = "000000000000002"
        self.assertTrue(self.blob.shouldServeUpdate(update_query))
