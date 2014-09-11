import unittest
from xml.dom import minidom

from auslib import dbo
from auslib.blob import Blob, ReleaseBlobV1, ReleaseBlobV2, ReleaseBlobV3

class SimpleBlob(Blob):
    format_ = {'foo': None}

class MultiLevelBlob(Blob):
    format_ = {
        'foo': {
            'bar': {
                'baz': None
            }
        }
    }

class BlobWithWildcard(Blob):
    format_ = {
        'foo': {
            '*': None
        }
    }

class BlobWithList(Blob):
    format_ = {
        'foo': [
            {
                'bar': None
            }
        ]
    }

class TestBlob(unittest.TestCase):
    def testSimpleValid(self):
        blob = SimpleBlob(foo='bar')
        self.assertTrue(blob.isValid())

    def testSimpleInvalid(self):
        blob = SimpleBlob(bar='foo')
        self.assertFalse(blob.isValid())

    def testMultiLevelValid(self):
        blob = MultiLevelBlob(foo=dict(bar=dict(baz='abc')))
        self.assertTrue(blob.isValid())

    def testMultiLevelInvalid(self):
        blob = MultiLevelBlob(foo=dict(baz=dict(bar='abc')))
        self.assertFalse(blob.isValid())

    def testWildcardValid(self):
        blob = BlobWithWildcard(foo=dict(bar='abc', baz=123))
        self.assertTrue(blob.isValid())

    def testWildcardInvalid(self):
        blob = BlobWithWildcard(bar=dict(foo='abc'))
        self.assertFalse(blob.isValid())

    def testWildcardWrongType(self):
        blob = BlobWithWildcard(foo='abc')
        self.assertFalse(blob.isValid())

    def testGetResolvedPlatform(self):
        blob = SimpleBlob(platforms=dict(a=dict(), b=dict(alias='a')))
        self.assertEquals('a', blob.getResolvedPlatform('a'))
        self.assertEquals('a', blob.getResolvedPlatform('b'))

    def testGetPlatformData(self):
        blob = SimpleBlob(platforms=dict(a=dict(foo=1)))
        self.assertEquals(blob.getPlatformData('a'), dict(foo=1))

    def testGetLocaleOrTopLevelParamTopLevelOnly(self):
        blob = SimpleBlob(foo=5)
        self.assertEquals(5, blob.getLocaleOrTopLevelParam('a', 'b', 'foo'))

    def testGetLocaleOrTopLevelParamLocaleOnly(self):
        blob = SimpleBlob(platforms=dict(f=dict(locales=dict(g=dict(foo=6)))))
        self.assertEquals(6, blob.getLocaleOrTopLevelParam('f', 'g', 'foo'))

    def testGetLocaleOrTopLevelParamMissing(self):
        blob = ReleaseBlobV1(platforms=dict(f=dict(locales=dict(g=dict(foo=6)))))
        self.assertEquals(None, blob.getLocaleOrTopLevelParam('a', 'b', 'c'))

    def testGetBuildIDPlatformOnly(self):
        blob = SimpleBlob(platforms=dict(a=dict(buildID=1, locales=dict(b=dict()))))
        self.assertEquals(1, blob.getBuildID('a', 'b'))

    def testGetBuildIDLocaleOnly(self):
        blob = SimpleBlob(platforms=dict(c=dict(locales=dict(d=dict(buildID=9)))))
        self.assertEquals(9, blob.getBuildID('c', 'd'))

    def testGetBuildIDMissingLocale(self):
        blob = SimpleBlob(platforms=dict(c=dict(locales=dict(d=dict(buildID=9)))))
        self.assertRaises(KeyError, blob.getBuildID, 'c', 'a')

    def testGetBuildIDMissingLocaleBuildIDAtPlatform(self):
        blob = SimpleBlob(platforms=dict(c=dict(buildID=9, locales=dict(d=dict()))))
        self.assertRaises(KeyError, blob.getBuildID, 'c', 'a')
    # XXX: should we support the locale overriding the platform? this should probably be invalid

    def testBlobWithList(self):
        blob = BlobWithList(foo=[dict(bar=1)])
        self.assertTrue(blob.isValid())

    def testBlobWithEmptyList(self):
        blob = BlobWithList(foo=[])
        self.assertFalse(blob.isValid())

    def testBlobWithMissingList(self):
        blob = BlobWithList()
        self.assertTrue(blob.isValid())

    def testBlobWithInvalidSublist(self):
        blob = BlobWithList(foo=[dict(blah=2)])
        self.assertFalse(blob.isValid())

class TestReleaseBlobV1(unittest.TestCase):
    def testGetAppv(self):
        blob = ReleaseBlobV1(appv=1)
        self.assertEquals(1, blob.getAppv('p', 'l'))
        blob = ReleaseBlobV1(platforms=dict(f=dict(locales=dict(g=dict(appv=2)))))
        self.assertEquals(2, blob.getAppv('f', 'g'))

    def testGetExtv(self):
        blob = ReleaseBlobV1(extv=3)
        self.assertEquals(3, blob.getExtv('p', 'l'))
        blob = ReleaseBlobV1(platforms=dict(f=dict(locales=dict(g=dict(extv=4)))))
        self.assertEquals(4, blob.getExtv('f', 'g'))

    def testApplicationVersion(self):
        blob = ReleaseBlobV1(platforms=dict(f=dict(locales=dict(g=dict(extv=4)))))
        self.assertEquals(blob.getExtv('f', 'g'), blob.getApplicationVersion('f', 'g'))


class TestNewStyleVersionBlob(unittest.TestCase):
    def testGetAppVersion(self):
        blob = ReleaseBlobV2(appVersion=1)
        self.assertEquals(1, blob.getAppVersion('p', 'l'))
        blob = ReleaseBlobV2(platforms=dict(f=dict(locales=dict(g=dict(appVersion=2)))))
        self.assertEquals(2, blob.getAppVersion('f', 'g'))

    def testGetDisplayVersion(self):
        blob = ReleaseBlobV2(displayVersion=3)
        self.assertEquals(3, blob.getDisplayVersion('p', 'l'))
        blob = ReleaseBlobV2(platforms=dict(f=dict(locales=dict(g=dict(displayVersion=4)))))
        self.assertEquals(4, blob.getDisplayVersion('f', 'g'))

    def testGetPlatformVersion(self):
        blob = ReleaseBlobV2(platformVersion=5)
        self.assertEquals(5, blob.getPlatformVersion('p', 'l'))
        blob = ReleaseBlobV2(platforms=dict(f=dict(locales=dict(g=dict(platformVersion=6)))))
        self.assertEquals(6, blob.getPlatformVersion('f', 'g'))

    def testApplicationVersion(self):
        blob = ReleaseBlobV2(platforms=dict(f=dict(locales=dict(g=dict(appVersion=6)))))
        self.assertEquals(blob.getAppVersion('f', 'g'), blob.getApplicationVersion('f', 'g'))


class TestSpecialQueryParams(unittest.TestCase):
    def setUp(self):
        self.specialForceHosts = ["http://a.com"]
        self.whitelistedDomains = ["a.com", "boring.com"]
        self.blob = ReleaseBlobV1()
        self.blob.loadJSON("""
{
    "name": "h",
    "schema_version": 1,
    "appv": "1.0",
    "extv": "1.0",
    "hashFunction": "sha512",
    "detailsUrl": "http://example.org/details",
    "licenseUrl": "http://example.org/license",
    "platforms": {
        "p": {
            "buildID": 1,
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 1,
                        "from": "*",
                        "hashValue": "1",
                        "fileUrl": "http://a.com/?foo=a"
                    }
                },
                "m": {
                    "complete": {
                        "filesize": 1,
                        "from": "*",
                        "hashValue": "1",
                        "fileUrl": "http://boring.com/a"
                    }
                }
            }
        }
    }
}""")

    def testSpecialQueryParam(self):
        updateQuery = {
            "product": "h", "version": "0.5", "buildID": "0",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blob.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
        <patch type="complete" URL="http://a.com/?foo=a" hashFunction="sha512" hashValue="1" size="1"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testSpecialQueryParamForced(self):
        updateQuery = {
            "product": "h", "version": "0.5", "buildID": "0",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 1
        }
        returned = self.blob.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
        <patch type="complete" URL="http://a.com/?foo=a&amp;force=1" hashFunction="sha512" hashValue="1" size="1"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testNonSpecialQueryParam(self):
        updateQuery = {
            "product": "h", "version": "0.5", "buildID": "0",
            "buildTarget": "p", "locale": "m", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blob.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
        <patch type="complete" URL="http://boring.com/a" hashFunction="sha512" hashValue="1" size="1"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testNonSpecialQueryParamForced(self):
        updateQuery = {
            "product": "h", "version": "0.5", "buildID": "0",
            "buildTarget": "p", "locale": "m", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 1
        }
        returned = self.blob.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
        <patch type="complete" URL="http://boring.com/a" hashFunction="sha512" hashValue="1" size="1"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testNoSpecialDefined(self):
        updateQuery = {
            "product": "h", "version": "0.5", "buildID": "0",
            "buildTarget": "p", "locale": "m", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blob.createXML(updateQuery, "minor", self.whitelistedDomains, None)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
        <patch type="complete" URL="http://boring.com/a" hashFunction="sha512" hashValue="1" size="1"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

class TestSchema2Blob(unittest.TestCase):
    def setUp(self):
        self.specialForceHosts = ["http://a.com"]
        self.whitelistedDomains = ["a.com", "boring.com"]
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        dbo.releases.t.insert().execute(name='j1', product='j', version='39.0', data_version=1, data="""
{
    "name": "j1",
    "schema_version": 2,
    "platforms": {
        "p": {
            "buildID": "28",
            "locales": {
                "l": {}
            }
        }
    }
}
""")
        self.blobJ2 = ReleaseBlobV2()
        self.blobJ2.loadJSON("""
{
    "name": "j2",
    "schema_version": 2,
    "hashFunction": "sha512",
    "appVersion": "40.0",
    "displayVersion": "40.0",
    "platformVersion": "40.0",
    "fileUrls": {
        "c1": "http://a.com/%FILENAME%"
    },
    "ftpFilenames": {
        "partial": "j1-partial.mar",
        "complete": "complete.mar"
    },
    "platforms": {
        "p": {
            "buildID": "30",
            "OS_FTP": "o",
            "OS_BOUNCER": "o",
            "locales": {
                "l": {
                    "partial": {
                        "filesize": 6,
                        "from": "j1",
                        "hashValue": 5
                    },
                    "complete": {
                        "filesize": 38,
                        "from": "*",
                        "hashValue": "34"
                    }
                }
            }
        }
    }
}
""")
        self.blobK = ReleaseBlobV2()
        self.blobK.loadJSON("""
{
    "name": "k",
    "schema_version": 2,
    "hashFunction": "sha512",
    "appVersion": "50.0",
    "displayVersion": "50.0",
    "platformVersion": "50.0",
    "detailsUrl": "http://example.org/details/%LOCALE%",
    "licenseUrl": "http://example.org/license/%LOCALE%",
    "actions": "silent",
    "billboardURL": "http://example.org/billboard/%LOCALE%",
    "openURL": "http://example.org/url/%LOCALE%",
    "notificationURL": "http://example.org/notification/%LOCALE%",
    "alertURL": "http://example.org/alert/%LOCALE%",
    "showPrompt": "false",
    "showNeverForVersion": "true",
    "showSurvey": "false",
    "fileUrls": {
        "c1": "http://a.com/%FILENAME%"
    },
    "ftpFilenames": {
        "complete": "complete.mar"
    },
    "platforms": {
        "p": {
            "buildID": "35",
            "OS_FTP": "o",
            "OS_BOUNCER": "o",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 40,
                        "from": "*",
                        "hashValue": "35"
                    }
                },
                "l2": {
                    "isOSUpdate": true,
                    "complete": {
                        "filesize": 50,
                        "from": "*",
                        "hashValue": "45"
                    }
                }
            }
        }
    }
}
""")
    def testSchema2CompleteOnly(self):
        updateQuery = {
            "product": "j", "version": "35.0", "buildID": "4",
            "buildTarget": "p", "locale": "l", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blobJ2.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="40.0" appVersion="40.0" platformVersion="40.0" buildID="30">
        <patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="34" size="38"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testSchema2WithPartial(self):
        updateQuery = {
            "product": "j", "version": "39.0", "buildID": "28",
            "buildTarget": "p", "locale": "l", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blobJ2.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="40.0" appVersion="40.0" platformVersion="40.0" buildID="30">
        <patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="34" size="38"/>
        <patch type="partial" URL="http://a.com/j1-partial.mar" hashFunction="sha512" hashValue="5" size="6"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testSchema2WithOptionalAttributes(self):
        updateQuery = {
            "product": "k", "version": "35.0", "buildID": "4",
            "buildTarget": "p", "locale": "l", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blobK.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="50.0" appVersion="50.0" platformVersion="50.0" buildID="35" detailsURL="http://example.org/details/l" licenseURL="http://example.org/license/l" billboardURL="http://example.org/billboard/l" showPrompt="false" showNeverForVersion="true" showSurvey="false" actions="silent" openURL="http://example.org/url/l" notificationURL="http://example.org/notification/l" alertURL="http://example.org/alert/l">
        <patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="35" size="40"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testSchema2WithIsOSUpdate(self):
        updateQuery = {
            "product": "k", "version": "35.0", "buildID": "4",
            "buildTarget": "p", "locale": "l2", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blobK.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="50.0" appVersion="50.0" platformVersion="50.0" buildID="35" detailsURL="http://example.org/details/l2" licenseURL="http://example.org/license/l2" billboardURL="http://example.org/billboard/l2" showPrompt="false" showNeverForVersion="true" showSurvey="false" actions="silent" openURL="http://example.org/url/l2" notificationURL="http://example.org/notification/l2" alertURL="http://example.org/alert/l2" isOSUpdate="true">
        <patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="45" size="50"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())


class TestSchema2BlobNightlyStyle(unittest.TestCase):
    maxDiff = 2000

    def setUp(self):
        self.specialForceHosts = ["http://a.com"]
        self.whitelistedDomains = ["a.com", "boring.com"]
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        dbo.releases.t.insert().execute(name='j1', product='j', version='0.5', data_version=1, data="""
{
    "name": "j1",
    "schema_version": 2,
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "buildID": "1"
                }
            }
        }
    }
}
""")
        self.blobJ2 = ReleaseBlobV2()
        self.blobJ2.loadJSON("""
{
    "name": "j2",
    "schema_version": 2,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "buildID": "3",
                    "appVersion": "2",
                    "platformVersion": "2",
                    "displayVersion": "2",
                    "partial": {
                        "filesize": 3,
                        "from": "j1",
                        "hashValue": 4,
                        "fileUrl": "http://a.com/p"
                    },
                    "complete": {
                        "filesize": 5,
                        "from": "*",
                        "hashValue": "6",
                        "fileUrl": "http://a.com/c"
                    }
                }
            }
        }
    }
}
""")

    def testCompleteOnly(self):
        updateQuery = {
            "product": "j", "version": "0.5", "buildID": "0",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blobJ2.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="2" appVersion="2" platformVersion="2" buildID="3">
        <patch type="complete" URL="http://a.com/c" hashFunction="sha512" hashValue="6" size="5"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testCompleteAndPartial(self):
        updateQuery = {
            "product": "j", "version": "0.5", "buildID": "1",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blobJ2.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="2" appVersion="2" platformVersion="2" buildID="3">
        <patch type="complete" URL="http://a.com/c" hashFunction="sha512" hashValue="6" size="5"/>
        <patch type="partial" URL="http://a.com/p" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())


class TestSchema3Blob(unittest.TestCase):
    def setUp(self):
        self.specialForceHosts = ["http://a.com"]
        self.whitelistedDomains = ["a.com", "boring.com"]
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        dbo.releases.t.insert().execute(name='f1', product='f', version='22.0', data_version=1, data="""
{
    "name": "f1",
    "schema_version": 3,
    "platforms": {
        "p": {
            "buildID": "5",
            "locales": {
                "l": {}
            }
        }
    }
}
""")
        dbo.releases.t.insert().execute(name='f2', product='f', version='23.0', data_version=1, data="""
{
    "name": "f2",
    "schema_version": 3,
    "platforms": {
        "p": {
            "buildID": "6",
            "locales": {
                "l": {}
            }
        }
    }
}
""")
        self.blobF3 = ReleaseBlobV3()
        self.blobF3.loadJSON("""
{
    "name": "f3",
    "schema_version": 3,
    "hashFunction": "sha512",
    "appVersion": "25.0",
    "displayVersion": "25.0",
    "platformVersion": "25.0",
    "platforms": {
        "p": {
            "buildID": "29",
            "locales": {
                "l": {
                    "partials": [
                        {
                            "filesize": 2,
                            "from": "f1",
                            "hashValue": 3,
                            "fileUrl": "http://a.com/p1"
                        },
                        {
                            "filesize": 4,
                            "from": "f2",
                            "hashValue": 5,
                            "fileUrl": "http://a.com/p2"
                        }
                    ],
                    "completes": [
                        {
                            "filesize": 29,
                            "from": "f2",
                            "hashValue": 6,
                            "fileUrl": "http://a.com/c1"
                        },
                        {
                            "filesize": 30,
                            "from": "*",
                            "hashValue": "31",
                            "fileUrl": "http://a.com/c2"
                        }
                    ]
                },
                "m": {
                    "completes": [
                        {
                            "filesize": 32,
                            "from": "*",
                            "hashValue": "33",
                            "fileUrl": "http://a.com/c2m"
                        }
                    ]
                }
            }
        }
    }
}
""")
        dbo.releases.t.insert().execute(name='g1', product='g', version='23.0', data_version=1, data="""
{
    "name": "g1",
    "schema_version": 3,
    "platforms": {
        "p": {
            "buildID": "8",
            "locales": {
                "l": {}
            }
        }
    }
}
""")
        self.blobG2 = ReleaseBlobV3()
        self.blobG2.loadJSON("""
{
    "name": "g2",
    "schema_version": 3,
    "hashFunction": "sha512",
    "appVersion": "26.0",
    "displayVersion": "26.0",
    "platformVersion": "26.0",
    "fileUrls": {
        "c1": "http://a.com/%FILENAME%",
        "c2": "http://a.com/%PRODUCT%"
    },
    "ftpFilenames": {
        "partials": {
            "g1": "g1-partial.mar"
        },
        "completes": {
            "*": "complete.mar"
        }
    },
    "bouncerProducts": {
        "partials": {
            "g1": "g1-partial"
        },
        "completes": {
            "*": "complete"
        }
    },
    "platforms": {
        "p": {
            "buildID": "40",
            "OS_FTP": "o",
            "OS_BOUNCER": "o",
            "locales": {
                "l": {
                    "partials": [
                        {
                            "filesize": 4,
                            "from": "g1",
                            "hashValue": 5
                        }
                    ],
                    "completes": [
                        {
                            "filesize": 34,
                            "from": "*",
                            "hashValue": "35"
                        }
                    ]
                }
            }
        }
    }
}
""")
    def testSchema3MultipleUpdates(self):
        updateQuery = {
            "product": "f", "version": "22.0", "buildID": "5",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blobF3.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="25.0" appVersion="25.0" platformVersion="25.0" buildID="29">
        <patch type="complete" URL="http://a.com/c2" hashFunction="sha512" hashValue="31" size="30"/>
        <patch type="partial" URL="http://a.com/p1" hashFunction="sha512" hashValue="3" size="2"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

        updateQuery = {
            "product": "f", "version": "23.0", "buildID": "6",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blobF3.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="25.0" appVersion="25.0" platformVersion="25.0" buildID="29">
        <patch type="complete" URL="http://a.com/c1" hashFunction="sha512" hashValue="6" size="29"/>
        <patch type="partial" URL="http://a.com/p2" hashFunction="sha512" hashValue="5" size="4"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testSchema3NoPartial(self):
        updateQuery = {
            "product": "f", "version": "20.0", "buildID": "1",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blobF3.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="25.0" appVersion="25.0" platformVersion="25.0" buildID="29">
        <patch type="complete" URL="http://a.com/c2" hashFunction="sha512" hashValue="31" size="30"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testSchema3NoPartialBlock(self):
        updateQuery = {
            "product": "f", "version": "20.0", "buildID": "1",
            "buildTarget": "p", "locale": "m", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blobF3.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="25.0" appVersion="25.0" platformVersion="25.0" buildID="29">
        <patch type="complete" URL="http://a.com/c2m" hashFunction="sha512" hashValue="33" size="32"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testSchema3FtpSubstitutions(self):
        updateQuery = {
            "product": "g", "version": "23.0", "buildID": "8",
            "buildTarget": "p", "locale": "l", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blobG2.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="26.0" appVersion="26.0" platformVersion="26.0" buildID="40">
        <patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="35" size="34"/>
        <patch type="partial" URL="http://a.com/g1-partial.mar" hashFunction="sha512" hashValue="5" size="4"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testSchema3BouncerSubstitutions(self):
        updateQuery = {
            "product": "g", "version": "23.0", "buildID": "8",
            "buildTarget": "p", "locale": "l", "channel": "c2",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": 0
        }
        returned = self.blobG2.createXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = minidom.parseString(returned)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="26.0" appVersion="26.0" platformVersion="26.0" buildID="40">
        <patch type="complete" URL="http://a.com/complete" hashFunction="sha512" hashValue="35" size="34"/>
        <patch type="partial" URL="http://a.com/g1-partial" hashFunction="sha512" hashValue="5" size="4"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())
