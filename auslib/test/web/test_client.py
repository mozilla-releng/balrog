import mock
import os
from tempfile import mkstemp
import unittest
from xml.dom import minidom

from auslib.blobs.base import createBlob
from auslib.global_state import dbo
from auslib.web.base import app
from auslib.web.views.client import ClientRequestView
from auslib.errors import BadDataError


class ClientTestCommon(unittest.TestCase):
    def assertHttpResponse(self, http_reponse):
        self.assertEqual(http_reponse.status_code, 200)
        self.assertEqual(http_reponse.mimetype, 'text/xml')

    def assertUpdatesAreEmpty(self, http_reponse):
        self.assertHttpResponse(http_reponse)
        # An empty update contains an <updates> tag with a newline, which is what we're expecting here
        self.assertEqual(
            minidom.parseString(http_reponse.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n'
        )

    def assertUpdateEqual(self, http_reponse, expected_xml_string):
        self.assertHttpResponse(http_reponse)
        returned = minidom.parseString(http_reponse.data)
        expected = minidom.parseString(expected_xml_string)
        self.assertEqual(returned.toxml(), expected.toxml())


class ClientTestBase(ClientTestCommon):
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
        self.version_fd, self.version_file = mkstemp()
        app.config['DEBUG'] = True
        app.config['SPECIAL_FORCE_HOSTS'] = ('http://a.com',)
        app.config['WHITELISTED_DOMAINS'] = {'a.com': ('b', 'c', 'e', 'b2g', 'response-a', 'response-b', 's', 'responseblob-a',
                                                       'responseblob-b', 'q', 'fallback')}
        app.config["VERSION_FILE"] = self.version_file
        with open(self.version_file, "w+") as f:
            f.write("""
{
  "source":"https://github.com/mozilla/balrog",
  "version":"1.0",
  "commit":"abcdef123456"
}
""")
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        dbo.setDomainWhitelist({'a.com': ('b', 'c', 'e', 'b2g')})
        self.client = app.test_client()
        self.view = ClientRequestView()
        dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping='b', update_type='minor', product='b',
                                     data_version=1)
        dbo.releases.t.insert().execute(name='b', product='b', data_version=1, data=createBlob("""
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
"""))

        dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping='s', update_type='minor', product='s',
                                     systemCapabilities="SSE", data_version=1)
        dbo.releases.t.insert().execute(name='s', product='s', data_version=1, data=createBlob("""
{
    "name": "s",
    "schema_version": 1,
    "appv": "1.0",
    "extv": "1.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "5",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "5",
                        "from": "*",
                        "hashValue": "5",
                        "fileUrl": "http://a.com/s"
                    }
                }
            }
        }
    }
}
"""))
        dbo.rules.t.insert().execute(priority=90, backgroundRate=0, mapping='q', update_type='minor', product='q',
                                     fallbackMapping='fallback', data_version=1)
        dbo.releases.t.insert().execute(name='q', product='q', data_version=1, data=createBlob("""
{
    "name": "q",
    "schema_version": 1,
    "appv": "1.0",
    "extv": "1.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "5",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "5",
                        "from": "*",
                        "hashValue": "5",
                        "fileUrl": "http://a.com/q"
                    }
                }
            }
        }
    }
}
"""))
        dbo.releases.t.insert().execute(name='fallback', product='q', data_version=1, data=createBlob("""
{
    "name": "fallback",
    "schema_version": 1,
    "appv": "1.0",
    "extv": "1.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "5",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "5",
                        "from": "*",
                        "hashValue": "5",
                        "fileUrl": "http://a.com/fallback"
                    }
                }
            }
        }
    }
}
"""))

        dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping='c', update_type='minor', product='c',
                                     distribution='default', data_version=1)
        dbo.releases.t.insert().execute(name='c', product='c', data_version=1, data=createBlob("""
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
"""))
        dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping='d', update_type='minor', product='d', data_version=1)
        dbo.releases.t.insert().execute(name='d', product='d', data_version=1, data=createBlob("""
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
"""))

        dbo.rules.t.insert().execute(priority=90, backgroundRate=0, mapping='e', update_type='minor', product='e', data_version=1)
        dbo.releases.t.insert().execute(name='e', product='e', data_version=1, data=createBlob("""
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
"""))

        dbo.rules.t.insert().execute(priority=100, backgroundRate=100, mapping='foxfood-whitelisted', update_type='minor', product='b2g',
                                     whitelist='b2g-whitelist', data_version=1)
        dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping='foxfood-whitelisted', update_type='minor', product='b2g',
                                     channel="foxfood", whitelist='b2g-whitelist', data_version=1)
        dbo.rules.t.insert().execute(priority=80, backgroundRate=100, mapping='foxfood-fallback', update_type='minor', product='b2g', data_version=1)
        dbo.releases.t.insert().execute(name='b2g-whitelist', product='b2g', data_version=1, data=createBlob("""
{
  "name": "b2g-whitelist",
  "schema_version": 3000,
  "whitelist": [
    { "imei": "000000000000000" },
    { "imei": "000000000000001" },
    { "imei": "000000000000002" }
  ]
}
"""))

        dbo.releases.t.insert().execute(name='foxfood-whitelisted', product='b2g', data_version=1, data=createBlob("""
{
    "name": "foxfood-whitelisted",
    "schema_version": 1,
    "extv": "2.5",
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
                        "fileUrl": "http://a.com/secrets"
                    }
                }
            }
        }
    }
}
"""))
        dbo.releases.t.insert().execute(name='foxfood-fallback', product='b2g', data_version=1, data=createBlob("""
{
    "name": "foxfood-fallback",
    "schema_version": 1,
    "extv": "2.5",
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
                        "fileUrl": "http://a.com/public"
                    }
                }
            }
        }
    }
}
"""))
        dbo.rules.t.insert().execute(priority=200, backgroundRate=100,
                                     mapping='gmp', update_type='minor',
                                     product='gmp',
                                     data_version=1)
        dbo.rules.t.insert().execute(priority=200, backgroundRate=100,
                                     mapping='gmp-with-one-response-product', update_type='minor',
                                     product='gmp-with-one-response-product',
                                     data_version=1)
        dbo.rules.t.insert().execute(priority=190, backgroundRate=100,
                                     mapping='response-a', update_type='minor',
                                     product='response-a',
                                     data_version=1)
        dbo.rules.t.insert().execute(priority=180, backgroundRate=100,
                                     mapping='response-b', update_type='minor',
                                     product='response-b', data_version=1)
        dbo.releases.t.insert().execute(name='gmp-with-one-response-product',
                                        product='gmp-with-one-response-product', data_version=1, data=createBlob("""
{
    "name": "superblob",
    "schema_version": 4000,
    "products": ["response-a"]
}
"""))
        dbo.releases.t.insert().execute(name='gmp', product='gmp', data_version=1, data=createBlob("""
{
    "name": "superblob",
    "schema_version": 4000,
    "products": ["response-a", "response-b"]
}
"""))
        dbo.releases.t.insert().execute(name='response-a', product='response-a', data_version=1, data=createBlob("""
{
    "name": "response-a",
    "schema_version": 1,
    "extv": "2.5",
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
                        "fileUrl": "http://a.com/public"
                    }
                }
            }
        },
        "q": {
            "buildID": "25",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 22,
                        "from": "*",
                        "hashValue": "23",
                        "fileUrl": "http://a.com/public-q"
                    }
                }
            }
        }
    }
}
"""))
        dbo.releases.t.insert().execute(name='response-b', product='response-b', data_version=1, data=createBlob("""
{
    "name": "response-b",
    "schema_version": 1,
    "extv": "2.5",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "25",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 27777777,
                        "from": "*",
                        "hashValue": "23",
                        "fileUrl": "http://a.com/b"
                    }
                }
            }
        }
    }
}
"""))
        dbo.rules.t.insert().execute(priority=180, backgroundRate=100,
                                     mapping='systemaddons-uninstall', update_type='minor',
                                     product='systemaddons-uninstall', data_version=1)
        dbo.releases.t.insert().execute(name='systemaddons-uninstall',
                                        product='systemaddons-uninstall', data_version=1, data=createBlob("""
{
    "name": "fake",
    "schema_version": 5000,
    "hashFunction": "SHA512",
    "uninstall": true
}
"""))
        dbo.rules.t.insert().execute(priority=180, backgroundRate=100,
                                     mapping='systemaddons', update_type='minor',
                                     product='systemaddons', data_version=1)
        dbo.releases.t.insert().execute(name='systemaddons',
                                        product='systemaddons', data_version=1, data=createBlob("""
{
    "name": "fake",
    "schema_version": 5000,
    "hashFunction": "SHA512",
    "uninstall": false,
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
"""))

        dbo.rules.t.insert().execute(priority=1000, backgroundRate=0, mapping='product_that_should_not_be_updated-1.1',
                                     update_type='minor', product='product_that_should_not_be_updated',
                                     data_version=1)
        dbo.releases.t.insert().execute(name='product_that_should_not_be_updated-1.1', product='product_that_should_not_be_updated', data_version=1, data=createBlob("""
{
    "name": "product_that_should_not_be_updated-1.1",
    "schema_version": 1,
    "appv": "1.1",
    "extv": "1.1",
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
                }
            }
        }
    }
}
"""))

        dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping='product_that_should_not_be_updated-2.0',
                                     update_type='minor', product='product_that_should_not_be_updated',
                                     data_version=1)
        dbo.releases.t.insert().execute(name='product_that_should_not_be_updated-2.0', product='product_that_should_not_be_updated', data_version=1, data=createBlob("""
{
    "name": "product_that_should_not_be_updated-2.0",
    "schema_version": 1,
    "appv": "2.0",
    "extv": "2.0",
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
                }
            }
        }
    }
}
"""))
        dbo.rules.t.insert().execute(priority=200, backgroundRate=100,
                                     mapping='superblobaddon-with-multiple-response-blob', update_type='minor',
                                     product='superblobaddon-with-multiple-response-blob',
                                     data_version=1)
        dbo.rules.t.insert().execute(priority=200, backgroundRate=100,
                                     mapping='superblobaddon-with-one-response-blob', update_type='minor',
                                     product='superblobaddon-with-one-response-blob',
                                     data_version=1)
        dbo.releases.t.insert().execute(name='superblobaddon-with-one-response-blob',
                                        product='superblobaddon-with-one-response-blob', data_version=1, data=createBlob("""
{
    "name": "superblobaddon",
    "schema_version": 4000,
    "revision": 123,
    "blobs": ["responseblob-a"]
}
"""))
        dbo.releases.t.insert().execute(name='superblobaddon-with-multiple-response-blob',
                                        product='superblobaddon-with-multiple-response-blob', data_version=1, data=createBlob("""
{
    "name": "superblobaddon",
    "schema_version": 4000,
    "revision": 124,
    "blobs": ["responseblob-a", "responseblob-b"]
}
"""))
        dbo.releases.t.insert().execute(name='responseblob-a', product='responseblob-a', data_version=1, data=createBlob("""
{
    "name": "responseblob-a",
    "schema_version": 5000,
    "hashFunction": "SHA512",
    "addons": {
        "c": {
            "version": "1",
            "platforms": {
                "p": {
                    "filesize": 2,
                    "hashValue": "3",
                    "fileUrl": "http://a.com/e"
                },
                "q": {
                    "filesize": 4,
                    "hashValue": "5",
                    "fileUrl": "http://a.com/e"
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
                    "fileUrl": "http://a.com/c"
                },
                "default": {
                    "filesize": 20,
                    "hashValue": "50",
                    "fileUrl": "http://a.com/c"
                }
            }
        }
    }
}
"""))
        dbo.releases.t.insert().execute(name='responseblob-b', product='responseblob-b', data_version=1, data=createBlob("""
{
    "name": "responseblob-b",
    "schema_version": 5000,
    "hashFunction": "sha512",
    "uninstall": false,
    "addons": {
        "b": {
            "version": "1",
            "platforms": {
                "p": {
                        "filesize": 27,
                        "hashValue": "23",
                        "fileUrl": "http://a.com/b"

                }
            }
        }
    }
}
"""))

    def tearDown(self):
        os.close(self.version_fd)
        os.remove(self.version_file)


class ClientTest(ClientTestBase):

    def testGetHeaderArchitectureWindows(self):
        self.assertEqual(self.view.getHeaderArchitecture('WINNT_x86-msvc', 'Firefox Intel Windows'), 'Intel')

    def testGetHeaderArchitectureMacIntel(self):
        self.assertEqual(self.view.getHeaderArchitecture('Darwin_x86-gcc3-u-ppc-i386', 'Firefox Intel Mac'), 'Intel')

    def testGetHeaderArchitectureMacPPC(self):
        self.assertEqual(self.view.getHeaderArchitecture('Darwin_ppc-gcc3-u-ppc-i386', 'Firefox PPC Mac'), 'PPC')

    def testDontUpdateToYourself(self):
        ret = self.client.get('/update/3/b/1.0/2/p/l/a/a/a/a/update.xml')
        self.assertUpdatesAreEmpty(ret)

    def testDontUpdateBackwards(self):
        ret = self.client.get('/update/3/b/1.0/5/p/l/a/a/a/a/update.xml')
        self.assertUpdatesAreEmpty(ret)

    def testDontDecreaseVersion(self):
        ret = self.client.get('/update/3/c/15.0/1/p/l/a/a/default/a/update.xml')
        self.assertUpdatesAreEmpty(ret)

    def testVersion1Get(self):
        ret = self.client.get("/update/1/b/1.0/1/p/l/a/update.xml")
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")

    def testVersion2Get(self):
        ret = self.client.get('/update/2/b/1.0/0/p/l/a/a/update.xml')
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")

    def testVersion2GetIgnoresRuleWithDistribution(self):
        ret = self.client.get('/update/2/c/10.0/1/p/l/a/a/update.xml')
        self.assertUpdatesAreEmpty(ret)

    def testVersion3Get(self):
        ret = self.client.get('/update/3/a/1.0/1/a/a/a/a/a/a/update.xml')
        self.assertUpdatesAreEmpty(ret)

    def testVersion3GetWithUpdate(self):
        ret = self.client.get('/update/3/b/1.0/1/p/l/a/a/a/a/update.xml')
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")

    def testVersion4Get(self):
        ret = self.client.get('/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml')
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")

    def testVersion5GetWhitelistedOneLevel(self):
        ret = self.client.get('/update/5/b2g/1.0/1/p/l/foxfood/a/a/a/000000000000001/update.xml')
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <update type="minor" version="None" extensionVersion="2.5" buildID="25">
        <patch type="complete" URL="http://a.com/secrets" hashFunction="sha512" hashValue="23" size="22"/>
    </update>
</updates>
""")

    def testVersion5GetNotWhitelistedOneLevel(self):
        ret = self.client.get('/update/5/b2g/1.0/1/p/l/a/a/a/a/000000000000009/update.xml')
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <update type="minor" version="None" extensionVersion="2.5" buildID="25">
        <patch type="complete" URL="http://a.com/public" hashFunction="sha512" hashValue="23" size="22"/>
    </update>
</updates>
""")

    def testVersion5GetNotWhitelistedMultiLevel(self):
        ret = self.client.get('/update/5/b2g/1.0/1/p/l/foxfood/a/a/a/000000000000009/update.xml')
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <update type="minor" version="None" extensionVersion="2.5" buildID="25">
        <patch type="complete" URL="http://a.com/public" hashFunction="sha512" hashValue="23" size="22"/>
    </update>
</updates>
""")

    def testVersion6GetWithSystemCapabilitiesMatch(self):
        ret = self.client.get('/update/6/s/1.0/1/p/l/a/a/SSE/a/a/update.xml')
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="5">
        <patch type="complete" URL="http://a.com/s" hashFunction="sha512" hashValue="5" size="5"/>
    </update>
</updates>
""")

    def testVersion6GetWithFallbackMapping(self):
        ret = self.client.get('/update/6/q/1.0/1/p/l/a/a/a/a/1/update.xml')
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="5">
        <patch type="complete" URL="http://a.com/fallback" hashFunction="sha512" hashValue="5" size="5"/>
    </update>
</updates>
""")

    def testVersion6GetWithoutSystemCapabilitiesMatch(self):
        ret = self.client.get('/update/6/s/1.0/1/p/l/a/a/SSE2/a/a/update.xml')
        self.assertUpdatesAreEmpty(ret)

    def testGetURLNotInWhitelist(self):
        ret = self.client.get('/update/3/d/20.0/1/p/l/a/a/a/a/update.xml')
        self.assertHttpResponse(ret)
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue,
                         '\n    ')

    def testEmptySnippetMissingExtv(self):
        ret = self.client.get('/update/3/e/20.0/1/p/l/a/a/a/a/update.xml')
        self.assertUpdatesAreEmpty(ret)

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
        self.assertHttpResponse(ret)
        # Compare the Avast-style URL to the non-messed up equivalent. They
        # should get the same update XML.
        ret2 = self.client.get('/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml')
        self.assertHttpResponse(ret2)
        self.assertEqual(ret.data, ret2.data)

    def testFixForBug1125231DoesntBreakXhLocale(self):
        ret = self.client.get('/update/4/b/1.0/1/p/xh/a/a/a/a/1/update.xml')
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/x" hashFunction="sha512" hashValue="6" size="5"/>
    </update>
</updates>
""")

    def testAvastURLsWithBadQueryArgs(self):
        ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml?force=1%3Favast=1")
        self.assertHttpResponse(ret)
        ret2 = self.client.get('/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml?force=1')
        self.assertHttpResponse(ret2)
        self.assertEqual(ret.data, ret2.data)

    def testAvastURLsWithUnescapedBadQueryArgs(self):
        ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml?force=1?avast=1")
        self.assertHttpResponse(ret)
        ret2 = self.client.get('/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml?force=1')
        self.assertHttpResponse(ret2)
        self.assertEqual(ret.data, ret2.data)

    def testAvastURLsWithGoodQueryArgs(self):
        ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml?force=1&avast=1")
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z?force=1" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")

    def testDeprecatedEsrVersionStyleGetsUpdates(self):
        ret = self.client.get('/update/3/b/1.0esrpre/1/p/l/a/a/a/a/update.xml')
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")

    def testGetWithResponseProducts(self):
        ret = self.client.get('/update/4/gmp/1.0/1/p/l/a/a/a/a/1/update.xml')
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <addons>
        <patch type="complete" URL="http://a.com/public" hashFunction="sha512" hashValue="23" size="22"/>
        <patch type="complete" URL="http://a.com/b" hashFunction="sha512" hashValue="23" size="27777777"/>
    </addons>
</updates>
""")

    def testGetWithResponseProductsWithAbsentRule(self):
        ret = self.client.get('/update/4/gmp/1.0/1/q/l/a/a/a/a/1/update.xml')
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <addons>
        <patch type="complete" URL="http://a.com/public-q" hashFunction="sha512" hashValue="23" size="22"/>
    </addons>
</updates>
""")

    def testGetWithResponseProductsWithOneRule(self):
        ret = self.client.get('/update/4/gmp-with-one-response-product/1.0/1/q/l/a/a/a/a/1/update.xml')
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <addons>
        <patch type="complete" URL="http://a.com/public-q" hashFunction="sha512" hashValue="23" size="22"/>
    </addons>
</updates>
""")

    def testSystemAddonsBlobWithUninstall(self):
        ret = self.client.get('/update/4/systemaddons-uninstall/1.0/1/z/p/a/b/c/d/1/update.xml')
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <addons>
    </addons>
</updates>
""")

    def testSystemAddonsBlobWithoutUninstall(self):
        ret = self.client.get('/update/4/systemaddons/1.0/1/z/p/a/b/c/d/1/update.xml')
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>


</updates>
""")

    def testSuperBlobAddOnMultipleUpdates(self):
        ret = self.client.get('/update/3/superblobaddon-with-multiple-response-blob/1.0/1/p/l/a/a/a/a/update.xml')
        # update / 3 / gg / 3 / 1 / p / l / a / a / a / a / update.xml?force = 0
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <addons revision="124">
        <addon id="c" URL="http://a.com/e" hashFunction="SHA512" hashValue="3" size="2" version="1"/>
        <addon id="d" URL="http://a.com/c" hashFunction="SHA512" hashValue="50" size="20" version="5"/>
        <addon id="b" URL="http://a.com/b" hashFunction="sha512" hashValue="23" size="27" version="1"/>
    </addons>
</updates>
""")

    def testSuperBlobAddOnOneUpdates(self):
        ret = self.client.get('/update/3/superblobaddon-with-one-response-blob/1.0/1/p/l/a/a/a/a/update.xml')
        # update / 3 / gg / 3 / 1 / p / l / a / a / a / a / update.xml?force = 0
        self.assertUpdateEqual(ret, """<?xml version="1.0"?>
<updates>
    <addons revision="123">
        <addon id="c" URL="http://a.com/e" hashFunction="SHA512" hashValue="3" size="2" version="1"/>
        <addon id="d" URL="http://a.com/c" hashFunction="SHA512" hashValue="50" size="20" version="5"/>
    </addons>
</updates>
""")

    def testUpdateBackgroundRateSetTo0(self):
        ret = self.client.get('/update/3/product_that_should_not_be_updated/1.0/1/p/l/a/a/a/a/update.xml')
        self.assertUpdatesAreEmpty(ret)

    def testNonSubstitutedUrlVariablesReturn404(self):
        request1 = '/update/1/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/update.xml'
        request2 = '/update/2/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/update.xml'
        request3 = '/update/3/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/' \
            'update.xml'
        request4 = '/update/4/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/' \
            '%MOZ_VERSION%/update.xml'
        request5 = '/update/5/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/' \
            '%IMEI%/update.xml'
        request6 = '/update/6/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%SYSTEM_CAPABILITIES%/%DISTRIBUTION%/' \
            '%DISTRIBUTION_VERSION%/update.xml'

        with mock.patch('auslib.web.views.client.ClientRequestView') as mock_cr_view:
            for request in [request1, request2, request3, request4, request5, request6]:
                ret = self.client.get(request)
                self.assertEqual(ret.status_code, 404)
                self.assertFalse(mock_cr_view.called)


class ClientTestWithErrorHandlers(ClientTestCommon):
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

    def testCacheControlIsSet(self):
        ret = self.client.get('/update/3/c/15.0/1/p/l/a/a/default/a/update.xml')
        self.assertEqual(ret.headers.get("Cache-Control"), "public, max-age=90")

    def testCacheControlIsNotSetFor404(self):
        ret = self.client.get('/whizzybang')
        self.assertEqual(ret.headers.get("Cache-Control"), None)

    def testEmptySnippetOn404(self):
        ret = self.client.get('/whizzybang')
        self.assertUpdatesAreEmpty(ret)

    def testErrorMessageOn500(self):
        with mock.patch('auslib.web.views.client.ClientRequestView.get') as m:
            m.side_effect = Exception('I break!')
            ret = self.client.get('/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml')
            self.assertEqual(ret.status_code, 500)
            self.assertEqual(ret.mimetype, "text/plain")
            self.assertEqual('I break!', ret.data)

    def testEscapedOutputOn500(self):
        with mock.patch('auslib.web.views.client.ClientRequestView.get') as m:
            m.side_effect = Exception('50.1.0zibj5<img src%3da onerror%3dalert(document.domain)>')
            ret = self.client.get('/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml')
            self.assertEqual(ret.status_code, 500)
            self.assertEqual(ret.mimetype, "text/plain")
            self.assertEqual('50.1.0zibj5&lt;img src%3da onerror%3dalert(document.domain)&gt;', ret.data)

    def testEscapedOutputOn400(self):
        with mock.patch("auslib.web.views.client.ClientRequestView.get") as m:
            m.side_effect = BadDataError('Version number 50.1.0zibj5<img src%3da onerror%3dalert(document.domain)> is invalid.')
            ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
            self.assertEqual(ret.status_code, 400, ret.data)
            self.assertEqual(ret.mimetype, "text/plain")
            self.assertEqual("Version number 50.1.0zibj5&lt;img src%3da onerror%3dalert(document.domain)&gt; is invalid.", ret.data)

    def testSentryBadDataError(self):
        with mock.patch("auslib.web.views.client.ClientRequestView.get") as m, mock.patch("auslib.web.base.sentry") as sentry:
            m.side_effect = BadDataError("exterminate!")
            ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
            self.assertFalse(sentry.captureException.called)
            self.assertEqual(ret.status_code, 400, ret.data)
            self.assertEqual(ret.mimetype, "text/plain")

    def testSentryRealError(self):
        with mock.patch("auslib.web.views.client.ClientRequestView.get") as m, mock.patch("auslib.web.base.sentry") as sentry:
            m.side_effect = Exception("exterminate!")
            ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
            self.assertEqual(ret.status_code, 500)
            self.assertEqual(ret.mimetype, "text/plain")
            self.assertTrue(sentry.captureException.called)
            self.assertEqual('exterminate!', ret.data)

    def testNonSubstitutedUrlVariablesReturnEmptyUpdate(self):
        request1 = '/update/1/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/update.xml'
        request2 = '/update/2/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/update.xml'
        request3 = '/update/3/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/' \
            'update.xml'
        request4 = '/update/4/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/' \
            '%MOZ_VERSION%/update.xml'
        request5 = '/update/5/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/' \
            '%IMEI%/update.xml'
        request6 = '/update/6/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%SYSTEM_CAPABILITIES%/%DISTRIBUTION%/' \
            '%DISTRIBUTION_VERSION%/update.xml'

        with mock.patch('auslib.web.views.client.ClientRequestView') as mock_cr_view:
            for request in [request1, request2, request3, request4, request5, request6]:
                ret = self.client.get(request)
                self.assertUpdatesAreEmpty(ret)
                self.assertFalse(mock_cr_view.called)
