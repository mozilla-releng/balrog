import unittest
from xml.dom import minidom

from auslib.web.base import app, AUS
from auslib.web.views.client import ClientRequestView

class ClientTest(unittest.TestCase):
    def setUp(self):
        app.config['DEBUG'] = True
        AUS.setDb('sqlite:///:memory:')
        AUS.db.create()
        self.client = app.test_client()
        self.view = ClientRequestView()
        AUS.rules.t.insert().execute(throttle=100, mapping='b', update_type='minor', product='b', data_version=1)
        AUS.releases.t.insert().execute(name='b', product='b', version='b', data_version=1, data="""
{
    "name": "b",
    "schema_version": 1,
    "appv": "b",
    "extv": "b",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": 1,
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 1,
                        "from": "*",
                        "hashValue": "1",
                        "fileUrl": "a"
                    }
                }
            }
        }
    }
}
""")

    def testGetHeaderArchitectureWindows(self):
        self.assertEqual(self.view.getHeaderArchitecture('WINNT_x86-msvc', 'Firefox Intel Windows'), 'Intel')

    def testGetHeaderArchitectureMacIntel(self):
        self.assertEqual(self.view.getHeaderArchitecture('Darwin_x86-gcc3-u-ppc-i386', 'Firefox Intel Mac'), 'Intel')

    def testGetHeaderArchitectureMacPPC(self):
        self.assertEqual(self.view.getHeaderArchitecture('Darwin_ppc-gcc3-u-ppc-i386', 'Firefox PPC Mac'), 'PPC')

    def testGet(self):
        ret = self.client.get('/update/3/a/1/1/a/a/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # An empty update contains an <updates> tag with a newline, which is what we're expecting here
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testGetWithUpdate(self):
        ret = self.client.get('/update/3/b/b/1/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="b" extensionVersion="b" buildID="1">
        <patch type="complete" URL="a" hashFunction="sha512" hashValue="1" size="1"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())
