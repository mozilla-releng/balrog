import mock
import os
from tempfile import mkstemp
import unittest
from xml.dom import minidom

import auslib.log
from auslib.global_state import dbo
from auslib.web.base import app
from auslib.web.views.client import ClientRequestView


class ClientTest(unittest.TestCase):
    maxDiff = 2000

    @classmethod
    def setUpClass(cls):
        # Error handlers are removed in order to give us better debug messages
        cls.error_spec = app.error_handler_spec
        # Ripped from https://github.com/mitsuhiko/flask/blob/1f5927eee2288b4aaf508af5dc1f148aa2140d91/flask/app.py#L394
        app.error_handler_spec = {None: {}}

    @classmethod
    def tearDownClass(cls):
        app.error_handler_spec = cls.error_spec

    def setUp(self):
        self.cef_fd, self.cef_file = mkstemp()
        app.config['DEBUG'] = True
        app.config['SPECIAL_FORCE_HOSTS'] = ('http://a.com',)
        app.config['WHITELISTED_DOMAINS'] = ('a.com', 'boring.com')
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        dbo.setDomainWhitelist(('a.com', 'boring.com'))
        self.client = app.test_client()
        self.view = ClientRequestView()
        auslib.log.cef_config = auslib.log.get_cef_config(self.cef_file)
        dbo.rules.t.insert().execute(backgroundRate=100, mapping='b', update_type='minor', product='b', data_version=1)
        dbo.releases.t.insert().execute(name='b', product='b', version='1.0', data_version=1, data="""
{
    "name": "b",
    "schema_version": 1,
    "appv": "1.0",
    "extv": "1.0",
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
                        "fileUrl": "http://a.com/z"
                    }
                },
                "xh": {
                    "complete": {
                        "filesize": "5",
                        "from": "*",
                        "hashValue": "6",
                        "fileUrl": "http://a.com/x"
                    }
                }
            }
        }
    }
}
""")
        dbo.rules.t.insert().execute(backgroundRate=100, mapping='c', update_type='minor', product='c',
                                     distribution='default', data_version=1)
        dbo.releases.t.insert().execute(name='c', product='c', version='10.0', data_version=1, data="""
{
    "name": "c",
    "schema_version": 1,
    "appv": "10.0",
    "extv": "10.0",
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
                        "fileUrl": "http://a.com/y"
                    }
                }
            }
        }
    }
}
""")
        dbo.rules.t.insert().execute(backgroundRate=100, mapping='d', update_type='minor', product='d', data_version=1)
        dbo.releases.t.insert().execute(name='d', product='d', version='20.0', data_version=1, data="""
{
    "name": "d",
    "schema_version": 1,
    "appv": "20.0",
    "extv": "20.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "21",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 22,
                        "from": "*",
                        "hashValue": "23",
                        "fileUrl": "http://evil.com/y"
                    }
                }
            }
        }
    }
}
""")

        dbo.rules.t.insert().execute(backgroundRate=100, mapping='e', update_type='minor', product='e', data_version=1)
        dbo.releases.t.insert().execute(name='e', product='e', version='22.0', data_version=1, data="""
{
    "name": "e",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "25",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 22,
                        "from": "*",
                        "hashValue": "23",
                        "fileUrl": "http://a.com/y"
                    }
                }
            }
        }
    }
}
""")

    def tearDown(self):
        os.close(self.cef_fd)
        os.remove(self.cef_file)

    def testGetHeaderArchitectureWindows(self):
        self.assertEqual(self.view.getHeaderArchitecture('WINNT_x86-msvc', 'Firefox Intel Windows'), 'Intel')

    def testGetHeaderArchitectureMacIntel(self):
        self.assertEqual(self.view.getHeaderArchitecture('Darwin_x86-gcc3-u-ppc-i386', 'Firefox Intel Mac'), 'Intel')

    def testGetHeaderArchitectureMacPPC(self):
        self.assertEqual(self.view.getHeaderArchitecture('Darwin_ppc-gcc3-u-ppc-i386', 'Firefox PPC Mac'), 'PPC')

    def testDontUpdateToYourself(self):
        ret = self.client.get('/update/3/b/1.0/2/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testDontUpdateBackwards(self):
        ret = self.client.get('/update/3/b/1.0/5/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testDontDecreaseVersion(self):
        ret = self.client.get('/update/3/c/15.0/1/p/l/a/a/default/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testVersion1Get(self):
        ret = self.client.get("/update/1/b/1.0/1/p/l/a/update.xml")
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testVersion2Get(self):
        ret = self.client.get('/update/2/b/1.0/0/p/l/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testVersion2GetIgnoresRuleWithDistribution(self):
        ret = self.client.get('/update/2/c/10.0/1/p/l/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testVersion3Get(self):
        ret = self.client.get('/update/3/a/1.0/1/a/a/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # An empty update contains an <updates> tag with a newline, which is what we're expecting here
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testVersion3GetWithUpdate(self):
        ret = self.client.get('/update/3/b/1.0/1/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testVersion4Get(self):
        ret = self.client.get('/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testGetURLNotInWhitelist(self):
        ret = self.client.get('/update/3/d/20.0/1/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testEmptySnippetMissingExtv(self):
        ret = self.client.get('/update/3/e/20.0/1/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testRobotsExists(self):
        ret = self.client.get('/robots.txt')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/plain')
        self.assertTrue('User-agent' in ret.data)

    def testBadAvastURLsFromBug1125231(self):
        # Some versions of Avast have a bug in them that prepends "x86 "
        # to the locale. We need to make sure we handle this case correctly
        # so that these people can keep up to date.
        ret = self.client.get('/update/4/b/1.0/1/p/x86 l/a/a/a/a/1/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # Compare the Avast-style URL to the non-messed up equivalent. They
        # should get the same update XML.
        ret2 = self.client.get('/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml')
        self.assertEqual(ret2.status_code, 200)
        self.assertEqual(ret2.mimetype, 'text/xml')
        self.assertEqual(ret.data, ret2.data)

    def testFixForBug1125231DoesntBreakXhLocale(self):
        ret = self.client.get('/update/4/b/1.0/1/p/xh/a/a/a/a/1/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/x" hashFunction="sha512" hashValue="6" size="5"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testAvastURLsWithBadQueryArgs(self):
        ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml?force=1%3Favast=1")
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        ret2 = self.client.get('/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml?force=1')
        self.assertEqual(ret2.status_code, 200)
        self.assertEqual(ret2.mimetype, 'text/xml')
        self.assertEqual(ret.data, ret2.data)

    def testAvastURLsWithUnescapedBadQueryArgs(self):
        ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml?force=1?avast=1")
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        ret2 = self.client.get('/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml?force=1')
        self.assertEqual(ret2.status_code, 200)
        self.assertEqual(ret2.mimetype, 'text/xml')
        self.assertEqual(ret.data, ret2.data)

    def testAvastURLsWithGoodQueryArgs(self):
        ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml?force=1&avast=1")
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z?force=1" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testDeprecatedEsrVersionStyleGetsUpdates(self):
        ret = self.client.get('/update/3/b/1.0esrpre/1/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())


class ClientTestWithErrorHandlers(unittest.TestCase):
    """Most of the tests are run without the error handler because it gives more
       useful output when things break. However, we still need to test that our
       error handlers works!"""

    def setUp(self):
        app.config['DEBUG'] = True
        app.config['WHITELISTED_DOMAINS'] = ('a.com',)
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        self.client = app.test_client()
        self.view = ClientRequestView()

    def testEmptySnippetOn404(self):
        ret = self.client.get('/whizzybang')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testEmptySnippetOn500(self):
        with mock.patch('auslib.web.views.client.ClientRequestView.get') as m:
            m.side_effect = Exception('I break!')
            ret = self.client.get('/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml')
            self.assertEqual(ret.status_code, 200)
            self.assertEqual(ret.mimetype, 'text/xml')
            self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')
