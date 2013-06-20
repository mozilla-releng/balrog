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
        AUS.releases.t.insert().execute(name='b', product='b', version='1', data_version=1, data="""
{
    "name": "b",
    "schema_version": 1,
    "appv": "1",
    "extv": "1",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "2",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "3",
                        "from": "*",
                        "hashValue": "4",
                        "fileUrl": "z"
                    }
                }
            }
        }
    }
}
""")
        AUS.rules.t.insert().execute(throttle=100, mapping='c', update_type='minor', product='c',
                                     distribution='default', data_version=1)
        AUS.releases.t.insert().execute(name='c', product='c', version='10', data_version=1, data="""
{
    "name": "c",
    "schema_version": 1,
    "appv": "10",
    "extv": "10",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "11",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "12",
                        "from": "*",
                        "hashValue": "13",
                        "fileUrl": "y"
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

    def testDontUpdateToYourself(self):
        ret = self.client.get('/update/3/b/1/2/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testVersion3Get(self):
        ret = self.client.get('/update/3/a/1/1/a/a/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # An empty update contains an <updates> tag with a newline, which is what we're expecting here
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testVersion3GetWithUpdate(self):
        ret = self.client.get('/update/3/b/1/1/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1" extensionVersion="1" buildID="2">
        <patch type="complete" URL="z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testVersion2Get(self):
        ret = self.client.get('/update/2/b/1/0/p/l/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1" extensionVersion="1" buildID="2">
        <patch type="complete" URL="z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testVersion2GetIgnoresRuleWithDistribution(self):
        ret = self.client.get('/update/2/c/10/1/p/l/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testVersion4Get(self):
        ret = self.client.get('/update/4/b/1/1/p/l/a/a/a/a/1/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1" extensionVersion="1" buildID="2">
        <patch type="complete" URL="z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())
