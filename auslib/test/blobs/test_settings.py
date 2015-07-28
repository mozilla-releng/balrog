import unittest
from xml.dom import minidom

from auslib.blobs.settings import SettingsBlob


_DATA = """\
{
    "name": "fake",
    "schema_version": 1001,
    "settings": {
        "preloaded-sts-pkp": {
            "version": "1",
            "last_modified": 1438097376
            }
    }
}
"""


class TestSchemaSettings(unittest.TestCase):

    def test_basic_blob(self):
        self.blob = SettingsBlob()
        self.blob.loadJSON(_DATA)

        update_query = {
            "product": "gg", "version": "3", "buildID": "1",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }

        special_force_hosts = ["http://a.com"]
        whitelisted_domains = ["a.com", "boring.com"]

        # make sure we generate a proper XML
        res = self.blob.createXML(update_query, "minor", whitelisted_domains,
                                  special_force_hosts)

        xml = minidom.parseString(res)
        setting = xml.getElementsByTagName('setting')[0]
        self.assertEqual(setting.getAttribute('id'), 'preloaded-sts-pkp')
        self.assertEqual(setting.getAttribute('lastModified'), '1438097376')
