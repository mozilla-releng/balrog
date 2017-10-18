try:
    from collections import OrderedDict
except ImportError:
    # so you're in python <2.7
    from ordereddict import OrderedDict

import logging
import mock
import unittest

from auslib.AUS import SUCCEED, FAIL
from auslib.global_state import dbo
from auslib.errors import BadDataError
from auslib.web.public.base import app
from auslib.blobs.base import BlobValidationError, createBlob
from auslib.blobs.apprelease import ReleaseBlobBase, ReleaseBlobV1, ReleaseBlobV2, ReleaseBlobV3, \
    ReleaseBlobV4, ReleaseBlobV5, ReleaseBlobV6, ReleaseBlobV8, DesupportBlob, \
    UnifiedFileUrlsMixin, ProofXMLMixin


def setUpModule():
    # Silence SQLAlchemy-Migrate's debugging logger
    logging.getLogger('migrate').setLevel(logging.CRITICAL)


class SimpleBlob(ReleaseBlobBase):
    format_ = {'foo': None}


class TestReleaseBlobBase(unittest.TestCase):

    def testGetResolvedPlatform(self):
        blob = SimpleBlob(platforms=dict(a=dict(), b=dict(alias='a')))
        self.assertEquals('a', blob.getResolvedPlatform('a'))
        self.assertEquals('a', blob.getResolvedPlatform('b'))

    def testGetResolvedPlatformRaisesBadDataError(self):
        blob = SimpleBlob(platforms=dict(a=dict(), b=dict(alias='a')))
        self.assertRaises(BadDataError, blob.getResolvedPlatform, "d")

    def testGetPlatformData(self):
        blob = SimpleBlob(platforms=dict(a=dict(foo=1)))
        self.assertEquals(blob.getPlatformData('a'), dict(foo=1))

    def testGetPlatformDataRaisesBadDataError(self):
        blob = SimpleBlob(platforms=dict(a=dict(foo=1)))
        self.assertRaises(BadDataError, blob.getPlatformData, "c")

    def testGetPlatformDataBadAliasRaisesBadDataError(self):
        blob = SimpleBlob(platforms=dict(b=dict(alias="c")))
        self.assertRaises(BadDataError, blob.getPlatformData, "b")

    def testGetLocaleData(self):
        blob = SimpleBlob(platforms=dict(b=dict(locales=dict(a=dict(foo=4)))))
        self.assertEquals(blob.getLocaleData("b", "a"), dict(foo=4))

    def testGetLocaleDataRaisesBadDataError(self):
        blob = SimpleBlob(platforms=dict(b=dict(locales=dict(a=dict(foo=4)))))
        self.assertRaises(BadDataError, blob.getLocaleData, "b", "c")

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
        self.assertRaises(BadDataError, blob.getBuildID, 'c', 'a')

    def testGetBuildIDMissingPlatform(self):
        blob = SimpleBlob(platforms=dict())
        self.assertRaises(BadDataError, blob.getBuildID, 'c', 'a')

    def testGetBuildIDMissingLocalesFieldInPlatform(self):
        blob = SimpleBlob(platforms=dict(c=dict()))
        self.assertRaises(BadDataError, blob.getBuildID, 'c', 'a')

    def testGetBuildIDMissingPlatformWithNoLocale(self):
        blob = SimpleBlob(platforms=dict())
        self.assertRaises(BadDataError, blob.getBuildID, 'c', None)

    def testGetBuildIDMissingBuildIDAtPlatformAndLocale(self):
        blob = SimpleBlob(platforms=dict(c=dict(locales=dict(d=dict()))))
        self.assertRaises(BadDataError, blob.getBuildID, 'c', 'a')

    def testGetBuildIDMissingLocaleBuildIDAtPlatform(self):
        blob = SimpleBlob(platforms=dict(c=dict(buildID=9, locales=dict(d=dict()))))
        self.assertRaises(BadDataError, blob.getBuildID, 'c', 'a')
    # XXX: should we support the locale overriding the platform? this should probably be invalid


class TestReleaseBlobV1(unittest.TestCase):

    def setUp(self):
        self.whitelistedDomains = {'a.com': ('a',), 'boring.com': ('b',)}
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        dbo.setDomainWhitelist(self.whitelistedDomains)
        self.sampleReleaseBlob = ReleaseBlobV1()
        self.sampleReleaseBlob.loadJSON("""
        {
            "name": "j1",
            "schema_version": 1,
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
                    "buildID": 30,
                    "OS_FTP": "o",
                    "OS_BOUNCER": "o",
                    "locales": {
                        "l": {
                            "partial": {
                                "filesize": 6,
                                "from": "samplePartial1",
                                "hashValue": "5"
                            },
                            "complete": {
                                "filesize": 38,
                                "from": "*",
                                "hashValue": "34"
                            }
                        },
                        "en-US": {
                            "partial": {
                                "filesize": 6,
                                "from": "samplePartial2",
                                "hashValue": "5"
                            },
                            "complete": {
                                "filesize": 38,
                                "from": "*",
                                "hashValue": "34"
                            }
                        }
                    }
                },
                "p2": {
                    "buildID": 31,
                    "OS_FTP": "o",
                    "OS_BOUNCER": "o",
                    "locales": {
                        "l": {
                            "partial": {
                                "filesize": 6,
                                "from": "samplePartial3",
                                "hashValue": "5"
                            },
                            "complete": {
                                "filesize": 38,
                                "from": "*",
                                "hashValue": "34"
                            }
                        },
                        "en-GB": {
                            "partial": {
                                "filesize": 6,
                                "from": "samplePartial4",
                                "hashValue": "5"
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

    def testGetPartialReleaseReferences_Happy_Case(self):
        partial_releases = self.sampleReleaseBlob.getReferencedReleases()
        self.assertTrue(4, len(partial_releases))
        self.assertEquals(sorted(partial_releases),
                          ['samplePartial1', 'samplePartial2', 'samplePartial3', 'samplePartial4']
                          )

    def testGetPartialReleaseReferences_Empty_Locales_Case(self):
        sample_release_JSON = """
        {
            "name": "Firefox-3.6.8-build1",
            "schema_version": 1,
            "extv": "3.6.8",
            "platforms": {
                "Darwin_Universal-gcc3": {
                    "buildID": "20100722150226",
                    "locales": {
                        "en-US": {
                        }
                    }
                }
            }
        }
        """
        sample_release_blob = ReleaseBlobV1()
        sample_release_blob.loadJSON(sample_release_JSON)
        partial_releases = sample_release_blob.getReferencedReleases()
        self.assertEquals(0, len(partial_releases))

    def testGetPartialReleaseReferences_No_Partial_Release_Case(self):
        sample_release_JSON = """
        {
            "name": "Firefox-3.6.8-build1",
            "schema_version": 1,
            "extv": "3.6.8",
            "platforms": {
                "Darwin_Universal-gcc3": {
                    "buildID": "20100722150226",
                    "locales": {
                        "en-US": {
                            "complete": {
                                "filesize": "19002137",
                                "from": "*",
                                "hashValue": "a9f8e5"
                            }
                        }
                    }
                }
            }
        }
        """
        sample_release_blob = ReleaseBlobV1()
        sample_release_blob.loadJSON(sample_release_JSON)
        partial_releases = sample_release_blob.getReferencedReleases()
        self.assertEquals(0, len(partial_releases))

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

    def testAllowedDomain(self):
        blob = ReleaseBlobV1(fileUrls=dict(c="http://a.com/a"))
        self.assertFalse(blob.containsForbiddenDomain("a",
                                                      self.whitelistedDomains))

    def testForbiddenDomainFileUrls(self):
        blob = ReleaseBlobV1(fileUrls=dict(c="http://evil.com/a"))
        self.assertTrue(blob.containsForbiddenDomain("a",
                                                     self.whitelistedDomains))

    def testForbiddenDomainInLocale(self):
        blob = ReleaseBlobV1(platforms=dict(f=dict(locales=dict(h=dict(partial=dict(fileUrl="http://evil.com/a"))))))
        self.assertTrue(blob.containsForbiddenDomain("a",
                                                     self.whitelistedDomains))

    def testForbiddenDomainAndAllowedDomain(self):
        updates = OrderedDict()
        updates["partial"] = dict(fileUrl="http://a.com/a")
        updates["complete"] = dict(fileUrl="http://evil.com/a")
        blob = ReleaseBlobV1(platforms=dict(f=dict(locales=dict(j=updates))))
        self.assertTrue(blob.containsForbiddenDomain("a",
                                                     self.whitelistedDomains))


class TestOldVersionSpecialCases(unittest.TestCase):

    def setUp(self):
        self.specialForceHosts = ["http://a.com"]
        self.whitelistedDomains = {'boring.com': ('h',)}
        self.blob = ReleaseBlobV1()
        self.blob.loadJSON("""
    {
    "name": "h",
    "schema_version": 1,
    "appv": "12.0",
    "extv": "12.0",
    "hashFunction": "sha512",
    "detailsUrl": "http://example.org/details",
    "oldVersionSpecialCases": true,
    "platforms": {
        "p": {
            "buildID": 1,
            "locales": {
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

    def testIsValid(self):
        # Raises on error
        self.blob.validate('h', self.whitelistedDomains)

    def test2_0(self):
        updateQuery = {
            "product": "h", "version": "2.0.0.20", "buildID": "0",
            "buildTarget": "p", "locale": "m", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.whitelistedDomains, None)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" version="2.0.0.20" buildID="1" detailsURL="http://example.org/details">
"""
        expected = ["""
<patch type="complete" URL="http://boring.com/a" hashFunction="sha512" hashValue="1" size="1"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def test3_0(self):
        updateQuery = {
            "product": "h", "version": "3.0.9", "buildID": "0",
            "buildTarget": "p", "locale": "m", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.whitelistedDomains, None)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" version="3.0.9" buildID="1" detailsURL="http://example.org/details">
"""
        expected = ["""
<patch type="complete" URL="http://boring.com/a" hashFunction="sha512" hashValue="1" size="1"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def test3_5(self):
        updateQuery = {
            "product": "h", "version": "3.5.19", "buildID": "0",
            "buildTarget": "p", "locale": "m", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.whitelistedDomains, None)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" version="12.0" buildID="1" detailsURL="http://example.org/details">
"""
        expected = ["""
<patch type="complete" URL="http://boring.com/a" hashFunction="sha512" hashValue="1" size="1"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def test3_6(self):
        updateQuery = {
            "product": "h", "version": "3.6", "buildID": "0",
            "buildTarget": "p", "locale": "m", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.whitelistedDomains, None)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" version="12.0" extensionVersion="3.6" buildID="1" detailsURL="http://example.org/details">
"""
        expected = ["""
<patch type="complete" URL="http://boring.com/a" hashFunction="sha512" hashValue="1" size="1"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())


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
        self.whitelistedDomains = {'a.com': ('h',), 'boring.com': ('h',)}
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
            "force": None,
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/?foo=a" hashFunction="sha512" hashValue="1" size="1"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testSpecialQueryParamForced(self):
        updateQuery = {
            "product": "h", "version": "0.5", "buildID": "0",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": SUCCEED,
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/?foo=a&force=1" hashFunction="sha512" hashValue="1" size="1"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testSpecialQueryParamForcedFail(self):
        updateQuery = {
            "product": "h", "version": "0.5", "buildID": "0",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": FAIL,
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/?foo=a&force=-1" hashFunction="sha512" hashValue="1" size="1"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testNonSpecialQueryParam(self):
        updateQuery = {
            "product": "h", "version": "0.5", "buildID": "0",
            "buildTarget": "p", "locale": "m", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
"""
        expected = ["""
<patch type="complete" URL="http://boring.com/a" hashFunction="sha512" hashValue="1" size="1"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testNonSpecialQueryParamForced(self):
        updateQuery = {
            "product": "h", "version": "0.5", "buildID": "0",
            "buildTarget": "p", "locale": "m", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": SUCCEED,
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
"""
        expected = ["""
<patch type="complete" URL="http://boring.com/a" hashFunction="sha512" hashValue="1" size="1"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testNoSpecialDefined(self):
        updateQuery = {
            "product": "h", "version": "0.5", "buildID": "0",
            "buildTarget": "p", "locale": "m", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
"""
        expected = ["""
<patch type="complete" URL="http://boring.com/a" hashFunction="sha512" hashValue="1" size="1"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())


class TestSchema2Blob(unittest.TestCase):

    def setUp(self):
        self.specialForceHosts = ["http://a.com"]
        self.whitelistedDomains = {'a.com': ('j', 'k')}
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        dbo.setDomainWhitelist(self.whitelistedDomains)
        dbo.releases.t.insert().execute(name='j1', product='j', version='39.0', data_version=1, data=createBlob("""
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
"""))
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
            "buildID": 30,
            "OS_FTP": "o",
            "OS_BOUNCER": "o",
            "locales": {
                "l": {
                    "partial": {
                        "filesize": 6,
                        "from": "j1",
                        "hashValue": "5"
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
    "detailsUrl": "http://example.org/details/%locale%",
    "licenseUrl": "http://example.org/license/%LOCALE%",
    "actions": "silent",
    "billboardURL": "http://example.org/billboard/%LOCALE%",
    "openURL": "http://example.org/url/%locale%",
    "notificationURL": "http://example.org/notification/%locale%",
    "alertURL": "http://example.org/alert/%LOCALE%",
    "showPrompt": false,
    "showNeverForVersion": true,
    "fileUrls": {
        "c1": "http://a.com/%filename%/%os_ftp%/%os_bouncer%"
    },
    "ftpFilenames": {
        "complete": "complete.mar"
    },
    "platforms": {
        "p": {
            "buildID": 35,
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

        self.sampleReleaseBlob = ReleaseBlobV2()
        self.sampleReleaseBlob.loadJSON("""
                {
                    "name": "SampleBlob",
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
                            "buildID": 30,
                            "OS_FTP": "o",
                            "OS_BOUNCER": "o",
                            "locales": {
                                "l": {
                                    "partial": {
                                        "filesize": 6,
                                        "from": "samplePartial1",
                                        "hashValue": "5"
                                    },
                                    "complete": {
                                        "filesize": 38,
                                        "from": "*",
                                        "hashValue": "34"
                                    }
                                },
                                "en-US": {
                                    "partial": {
                                        "filesize": 6,
                                        "from": "samplePartial2",
                                        "hashValue": "5"
                                    },
                                    "complete": {
                                        "filesize": 38,
                                        "from": "*",
                                        "hashValue": "34"
                                    }
                                }
                            }
                        },
                        "p2": {
                            "buildID": 31,
                            "OS_FTP": "o",
                            "OS_BOUNCER": "o",
                            "locales": {
                                "l": {
                                    "partial": {
                                        "filesize": 6,
                                        "from": "samplePartial3",
                                        "hashValue": "5"
                                    },
                                    "complete": {
                                        "filesize": 38,
                                        "from": "*",
                                        "hashValue": "34"
                                    }
                                },
                                "en-GB": {
                                    "partial": {
                                        "filesize": 6,
                                        "from": "samplePartial4",
                                        "hashValue": "5"
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

    def testGetPartialReleaseReferences_Happy_Case(self):
        partial_releases = self.sampleReleaseBlob.getReferencedReleases()
        self.assertTrue(4, len(partial_releases))
        self.assertEquals(sorted(partial_releases),
                          ['samplePartial1', 'samplePartial2', 'samplePartial3', 'samplePartial4']
                          )

    def testIsValid(self):
        # Raises on error
        self.blobJ2.validate('j', self.whitelistedDomains)
        self.blobK.validate('k', self.whitelistedDomains)

    def testSchema2CompleteOnly(self):
        updateQuery = {
            "product": "j", "version": "35.0", "buildID": "4",
            "buildTarget": "p", "locale": "l", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobJ2.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobJ2.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobJ2.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" displayVersion="40.0" appVersion="40.0" platformVersion="40.0" buildID="30">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="34" size="38"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testSchema2WithPartial(self):
        updateQuery = {
            "product": "j", "version": "39.0", "buildID": "28",
            "buildTarget": "p", "locale": "l", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobJ2.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobJ2.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobJ2.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" displayVersion="40.0" appVersion="40.0" platformVersion="40.0" buildID="30">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="34" size="38"/>
""", """
<patch type="partial" URL="http://a.com/j1-partial.mar" hashFunction="sha512" hashValue="5" size="6"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testSchema2WithOptionalAttributes(self):
        updateQuery = {
            "product": "k", "version": "35.0", "buildID": "4",
            "buildTarget": "p", "locale": "l", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobK.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobK.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobK.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = '<update type="minor" displayVersion="50.0" appVersion="50.0" platformVersion="50.0" ' \
            'buildID="35" detailsURL="http://example.org/details/l" licenseURL="http://example.org/license/l" ' \
            'billboardURL="http://example.org/billboard/l" showPrompt="false" showNeverForVersion="true" ' \
            'actions="silent" openURL="http://example.org/url/l" notificationURL="http://example.org/notification/l" ' \
            'alertURL="http://example.org/alert/l">'
        expected = ["""
<patch type="complete" URL="http://a.com/complete.mar/o/o" hashFunction="sha512" hashValue="35" size="40"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testSchema2WithIsOSUpdate(self):
        updateQuery = {
            "product": "k", "version": "35.0", "buildID": "4",
            "buildTarget": "p", "locale": "l2", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobK.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobK.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobK.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = '<update type="minor" displayVersion="50.0" appVersion="50.0" platformVersion="50.0" ' \
            'buildID="35" detailsURL="http://example.org/details/l2" licenseURL="http://example.org/license/l2" ' \
            'isOSUpdate="true" billboardURL="http://example.org/billboard/l2" showPrompt="false" ' \
            'showNeverForVersion="true" actions="silent" openURL="http://example.org/url/l2" ' \
            'notificationURL="http://example.org/notification/l2" alertURL="http://example.org/alert/l2">'
        expected = ["""
<patch type="complete" URL="http://a.com/complete.mar/o/o" hashFunction="sha512" hashValue="45" size="50"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testAllowedDomain(self):
        blob = ReleaseBlobV2(fileUrls=dict(c="http://a.com/a"))
        self.assertFalse(blob.containsForbiddenDomain('j',
                                                      self.whitelistedDomains))

    def testForbiddenDomainFileUrls(self):
        blob = ReleaseBlobV2(fileUrls=dict(c="http://evil.com/a"))
        self.assertTrue(blob.containsForbiddenDomain('j',
                                                     self.whitelistedDomains))


class TestSchema2BlobNightlyStyle(unittest.TestCase):
    maxDiff = 2000

    def setUp(self):
        self.specialForceHosts = ["http://a.com"]
        self.whitelistedDomains = {'a.com': ('j',)}
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        dbo.setDomainWhitelist(self.whitelistedDomains)
        dbo.releases.t.insert().execute(name='j1', product='j', version='0.5', data_version=1, data=createBlob("""
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
"""))
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
                    "buildID": 3,
                    "appVersion": "2",
                    "platformVersion": "2",
                    "displayVersion": "2",
                    "partial": {
                        "filesize": 3,
                        "from": "j1",
                        "hashValue": "4",
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

    def testIsValid(self):
        # Raises on error
        self.blobJ2.validate('j', self.whitelistedDomains)

    def testCompleteOnly(self):
        updateQuery = {
            "product": "j", "version": "0.5", "buildID": "0",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobJ2.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobJ2.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobJ2.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" displayVersion="2" appVersion="2" platformVersion="2" buildID="3">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/c" hashFunction="sha512" hashValue="6" size="5"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testCompleteAndPartial(self):
        updateQuery = {
            "product": "j", "version": "0.5", "buildID": "1",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobJ2.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobJ2.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobJ2.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" displayVersion="2" appVersion="2" platformVersion="2" buildID="3">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/c" hashFunction="sha512" hashValue="6" size="5"/>
""", """
<patch type="partial" URL="http://a.com/p" hashFunction="sha512" hashValue="4" size="3"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testForbiddenDomainInLocale(self):
        blob = ReleaseBlobV2(platforms=dict(f=dict(locales=dict(h=dict(partial=dict(fileUrl="http://evil.com/a"))))))
        self.assertTrue(blob.containsForbiddenDomain('a',
                                                     self.whitelistedDomains))

    def testForbiddenDomainAndAllowedDomain(self):
        updates = OrderedDict()
        updates["partial"] = dict(fileUrl="http://a.com/a")
        updates["complete"] = dict(fileUrl="http://evil.com/a")
        blob = ReleaseBlobV2(platforms=dict(f=dict(locales=dict(j=updates))))
        self.assertTrue(blob.containsForbiddenDomain('a',
                                                     self.whitelistedDomains))


class TestSchema3Blob(unittest.TestCase):

    def setUp(self):
        self.specialForceHosts = ["http://a.com"]
        self.whitelistedDomains = {'a.com': ('f', 'g')}
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        dbo.setDomainWhitelist(self.whitelistedDomains)
        dbo.releases.t.insert().execute(name='f1', product='f', version='22.0', data_version=1, data=createBlob("""
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
"""))
        dbo.releases.t.insert().execute(name='f2', product='f', version='23.0', data_version=1, data=createBlob("""
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
"""))
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
            "buildID": 29,
            "locales": {
                "l": {
                    "partials": [
                        {
                            "filesize": 2,
                            "from": "f1",
                            "hashValue": "3",
                            "fileUrl": "http://a.com/p1"
                        },
                        {
                            "filesize": 4,
                            "from": "f2",
                            "hashValue": "5",
                            "fileUrl": "http://a.com/p2"
                        }
                    ],
                    "completes": [
                        {
                            "filesize": 29,
                            "from": "f2",
                            "hashValue": "6",
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
        dbo.releases.t.insert().execute(name='g1', product='g', version='23.0', data_version=1, data=createBlob("""
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
"""))
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
        "c2": "http://a.com/%product%"
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
            "buildID": 40,
            "OS_FTP": "o",
            "OS_BOUNCER": "o",
            "locales": {
                "l": {
                    "partials": [
                        {
                            "filesize": 4,
                            "from": "g1",
                            "hashValue": "5"
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

        self.sampleReleaseBlobV3 = ReleaseBlobV3()
        self.sampleReleaseBlobV3.loadJSON("""
        {
            "name": "f3",
            "schema_version": 3,
            "hashFunction": "sha512",
            "appVersion": "25.0",
            "displayVersion": "25.0",
            "platformVersion": "25.0",
            "platforms": {
                "p": {
                    "buildID": 29,
                    "locales": {
                        "l": {
                            "partials": [
                                {
                                    "filesize": 2,
                                    "from": "g1",
                                    "hashValue": "3",
                                    "fileUrl": "http://a.com/p1"
                                },
                                {
                                    "filesize": 4,
                                    "from": "g1",
                                    "hashValue": "5",
                                    "fileUrl": "http://a.com/p2"
                                }
                            ],
                            "completes": [
                                {
                                    "filesize": 29,
                                    "from": "f2",
                                    "hashValue": "6",
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
                            "partials": [
                                {
                                    "filesize": 32,
                                    "from": "e3",
                                    "hashValue": "33",
                                    "fileUrl": "http://a.com/c2m"
                                },
                                {
                                    "filesize": 32,
                                    "from": "d4",
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

    def testGetPartialReleaseReferences_Happy_Case(self):
        partial_releases = self.sampleReleaseBlobV3.getReferencedReleases()
        self.assertTrue(3, len(partial_releases))
        self.assertEquals(sorted(partial_releases), ['d4', 'e3', 'g1'])

    def testGetPartialReleaseReferences_Empty_Partials(self):
        sampleReleaseDataJSON = """
        {
            "name": "f3",
            "schema_version": 3,
            "hashFunction": "sha512",
            "appVersion": "25.0",
            "displayVersion": "25.0",
            "platformVersion": "25.0",
            "platforms": {
                "p": {
                    "buildID": 29,
                    "locales": {
                        "l": {
                            "partials": [
                            ],
                            "completes": [
                                {
                                    "filesize": 29,
                                    "from": "f2",
                                    "hashValue": "6",
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
                                    "from": "e3",
                                    "hashValue": "33",
                                    "fileUrl": "http://a.com/c2m"
                                },
                                {
                                    "filesize": 32,
                                    "from": "d4",
                                    "hashValue": "33",
                                    "fileUrl": "http://a.com/c2m"
                                }
                            ]
                        }
                    }
                }
            }
        }
        """
        sampleReleaseBlobV3 = ReleaseBlobV3()
        sampleReleaseBlobV3.loadJSON(sampleReleaseDataJSON)
        partial_releases = sampleReleaseBlobV3.getReferencedReleases()
        self.assertEquals(0, len(partial_releases))

    def testIsValid(self):
        # Raises on error
        self.blobF3.validate('f', self.whitelistedDomains)
        self.blobG2.validate('g', self.whitelistedDomains)

    def testSchema3MultipleUpdates(self):
        updateQuery = {
            "product": "f", "version": "22.0", "buildID": "5",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobF3.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobF3.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobF3.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" displayVersion="25.0" appVersion="25.0" platformVersion="25.0" buildID="29">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/c2" hashFunction="sha512" hashValue="31" size="30"/>
""", """
<patch type="partial" URL="http://a.com/p1" hashFunction="sha512" hashValue="3" size="2"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

        updateQuery = {
            "product": "f", "version": "23.0", "buildID": "6",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobF3.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobF3.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobF3.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" displayVersion="25.0" appVersion="25.0" platformVersion="25.0" buildID="29">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/c1" hashFunction="sha512" hashValue="6" size="29"/>
""", """
<patch type="partial" URL="http://a.com/p2" hashFunction="sha512" hashValue="5" size="4"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testSchema3NoPartial(self):
        updateQuery = {
            "product": "f", "version": "20.0", "buildID": "1",
            "buildTarget": "p", "locale": "l", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobF3.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobF3.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobF3.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" displayVersion="25.0" appVersion="25.0" platformVersion="25.0" buildID="29">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/c2" hashFunction="sha512" hashValue="31" size="30"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testSchema3NoPartialBlock(self):
        updateQuery = {
            "product": "f", "version": "20.0", "buildID": "1",
            "buildTarget": "p", "locale": "m", "channel": "a",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobF3.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobF3.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobF3.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" displayVersion="25.0" appVersion="25.0" platformVersion="25.0" buildID="29">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/c2m" hashFunction="sha512" hashValue="33" size="32"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testSchema3FtpSubstitutions(self):
        updateQuery = {
            "product": "g", "version": "23.0", "buildID": "8",
            "buildTarget": "p", "locale": "l", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobG2.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobG2.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobG2.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" displayVersion="26.0" appVersion="26.0" platformVersion="26.0" buildID="40">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="35" size="34"/>
""", """
<patch type="partial" URL="http://a.com/g1-partial.mar" hashFunction="sha512" hashValue="5" size="4"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testSchema3BouncerSubstitutions(self):
        updateQuery = {
            "product": "g", "version": "23.0", "buildID": "8",
            "buildTarget": "p", "locale": "l", "channel": "c2",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobG2.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobG2.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobG2.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" displayVersion="26.0" appVersion="26.0" platformVersion="26.0" buildID="40">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/complete" hashFunction="sha512" hashValue="35" size="34"/>
""", """
<patch type="partial" URL="http://a.com/g1-partial" hashFunction="sha512" hashValue="5" size="4"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testAllowedDomain(self):
        blob = ReleaseBlobV3(fileUrls=dict(c="http://a.com/a"))
        self.assertFalse(blob.containsForbiddenDomain('f',
                                                      self.whitelistedDomains))

    def testForbiddenDomainFileUrls(self):
        blob = ReleaseBlobV3(fileUrls=dict(c="http://evil.com/a"))
        self.assertTrue(blob.containsForbiddenDomain('f',
                                                     self.whitelistedDomains))

    def testForbiddenDomainInLocale(self):
        blob = ReleaseBlobV3(platforms=dict(f=dict(locales=dict(h=dict(partials=[dict(fileUrl="http://evil.com/a")])))))
        self.assertTrue(blob.containsForbiddenDomain('f',
                                                     self.whitelistedDomains))

    def testForbiddenDomainAndAllowedDomain(self):
        updates = dict(partials=[dict(fileUrl="http://a.com/a"), dict(fileUrl="http://evil.com/a")])
        blob = ReleaseBlobV3(platforms=dict(f=dict(locales=dict(j=updates))))
        self.assertTrue(blob.containsForbiddenDomain('f',
                                                     self.whitelistedDomains))


class TestSchema4Blob(unittest.TestCase):

    def setUp(self):
        self.specialForceHosts = ["http://a.com"]
        self.whitelistedDomains = {'a.com': ('h', 'g',)}
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        dbo.setDomainWhitelist(self.whitelistedDomains)
        dbo.releases.t.insert().execute(name='h0', product='h', version='29.0', data_version=1, data=createBlob("""
{
    "name": "h0",
    "schema_version": 4,
    "platforms": {
        "p": {
            "buildID": "5",
            "locales": {
                "l": {}
            }
        }
    }
}
"""))
        dbo.releases.t.insert().execute(name='h1', product='h', version='30.0', data_version=1, data=createBlob("""
{
    "name": "h1",
    "schema_version": 4,
    "platforms": {
        "p": {
            "buildID": "10",
            "locales": {
                "l": {}
            }
        }
    }
}
"""))
        self.blobH2 = ReleaseBlobV4()
        self.blobH2.loadJSON("""
{
    "name": "h2",
    "schema_version": 4,
    "hashFunction": "sha512",
    "appVersion": "31.0",
    "displayVersion": "31.0",
    "platformVersion": "31.0",
    "fileUrls": {
        "c1": {
            "partials": {
                "h1": "http://a.com/h1-partial.mar",
                "h2": "http://a.com/h2-partial.mar"
            },
            "completes": {
                "*": "http://a.com/complete.mar"
            }
        },
        "c2": {
            "partials": {
                "h1": "http://a.com/h1-%LOCALE%-partial",
                "h2": "http://a.com/h2-%LOCALE%-partial"
            },
            "completes": {
                "*": "http://a.com/%LOCALE%-complete"
            }
        },
        "*": {
            "partials": {
                "h1": "http://a.com/h1-partial-catchall",
                "h2": "http://a.com/h2-partial-catchall"
            },
            "completes": {
                "*": "http://a.com/complete-catchall"
            }
        }
    },
    "platforms": {
        "p": {
            "buildID": 50,
            "OS_FTP": "p",
            "OS_BOUNCER": "p",
            "locales": {
                "l": {
                    "partials": [
                        {
                            "filesize": 6,
                            "from": "h2",
                            "hashValue": "7"
                        },
                        {
                            "filesize": 8,
                            "from": "h1",
                            "hashValue": "9"
                        }
                    ],
                    "completes": [
                        {
                            "filesize": 40,
                            "from": "*",
                            "hashValue": "41"
                        }
                    ]
                }
            }
        }
    }
}
""")
        self.blobH3 = ReleaseBlobV4()
        self.blobH3.loadJSON("""
{
    "name": "h3",
    "schema_version": 4,
    "hashFunction": "sha512",
    "appVersion": "32.0",
    "displayVersion": "32.0",
    "platformVersion": "32.0",
    "fileUrls": {
        "c1": {
            "partials": {
                "h1": "http://a.com/h1-partial.mar",
                "h2": "http://a.com/h2-partial.mar"
            },
            "completes": {
                "*": "http://a.com/complete.mar"
            }
        },
        "c2": {
            "partials": {
                "h1": "http://a.com/h1-%LOCALE%-partial",
                "h2": "http://a.com/h2-%LOCALE%-partial"
            },
            "completes": {
                "*": "http://a.com/%LOCALE%-complete"
            }
        },
        "*": {
            "partials": {
                "h0": "http://a.com/h0-partial-catchall.mar",
                "h1": "http://a.com/h1-partial-catchall",
                "h2": "http://a.com/h2-partial-catchall"
            },
            "completes": {
                "*": "http://a.com/complete-catchall"
            }
        }
    },
    "platforms": {
        "p": {
            "buildID": 500,
            "OS_FTP": "p",
            "OS_BOUNCER": "p",
            "locales": {
                "l": {
                    "partials": [
                        {
                            "filesize": 60,
                            "from": "h2",
                            "hashValue": "70"
                        },
                        {
                            "filesize": 80,
                            "from": "h1",
                            "hashValue": "90"
                        },
                        {
                            "filesize": 90,
                            "from": "h0",
                            "hashValue": "100"
                        }
                    ],
                    "completes": [
                        {
                            "filesize": 400,
                            "from": "*",
                            "hashValue": "410"
                        }
                    ]
                }
            }
        }
    }
}
""")

    def testGetPartialReleaseReferences_Happy_Case(self):
        sample_release_blob_v4 = ReleaseBlobV4()
        sample_release_blob_v4.loadJSON("""
        {
            "name": "sample",
            "schema_version": 4,
            "hashFunction": "sha512",
            "appVersion": "32.0",
            "displayVersion": "32.0",
            "platformVersion": "32.0",
            "fileUrls": {
                "c1": {
                    "partials": {
                        "h1": "http://a.com/h1-partial.mar",
                        "h2": "http://a.com/h2-partial.mar"
                    },
                    "completes": {
                        "*": "http://a.com/complete.mar"
                    }
                },
                "c2": {
                    "partials": {
                        "h3": "http://a.com/h1-%LOCALE%-partial",
                        "h2": "http://a.com/h2-%LOCALE%-partial"
                    },
                    "completes": {
                        "*": "http://a.com/%LOCALE%-complete"
                    }
                },
                "*": {
                    "partials": {
                        "h0": "http://a.com/h0-partial-catchall.mar",
                        "h1": "http://a.com/h1-partial-catchall",
                        "h2": "http://a.com/h2-partial-catchall"
                    },
                    "completes": {
                        "*": "http://a.com/complete-catchall"
                    }
                }
            },
            "platforms": {
                "p": {
                    "buildID": 500,
                    "OS_FTP": "p",
                    "OS_BOUNCER": "p",
                    "locales": {
                        "l": {
                            "partials": [
                                {
                                    "filesize": 60,
                                    "from": "h4",
                                    "hashValue": "70"
                                },
                                {
                                    "filesize": 80,
                                    "from": "h1",
                                    "hashValue": "90"
                                },
                                {
                                    "filesize": 90,
                                    "from": "h0",
                                    "hashValue": "100"
                                }
                            ],
                            "completes": [
                                {
                                    "filesize": 400,
                                    "from": "*",
                                    "hashValue": "410"
                                }
                            ]
                        }
                    }
                }
            }
        }
        """)
        partial_releases = sample_release_blob_v4.getReferencedReleases()
        self.assertTrue(5, len(partial_releases))
        self.assertEquals(sorted(partial_releases), ['h0', 'h1', 'h2', 'h3', 'h4'])

    def testGetPartialReleaseReferences_Empty_Partials_Case(self):
        sample_release_blob_v4 = ReleaseBlobV4()
        sample_release_blob_v4.loadJSON("""
            {
                "name": "h1",
                "schema_version": 4,
                "platforms": {
                    "p": {
                        "buildID": "10",
                        "locales": {
                            "l": {}
                        }
                    }
                }
            }
            """)
        partial_releases = sample_release_blob_v4.getReferencedReleases()
        self.assertEquals(0, len(partial_releases))

    def testGetPartialReleaseReferences_Empty_Locales_Case(self):
        sample_release_blob_v4 = ReleaseBlobV4()
        sample_release_blob_v4.loadJSON("""
        {
            "name": "sample",
            "schema_version": 4,
            "hashFunction": "sha512",
            "appVersion": "32.0",
            "displayVersion": "32.0",
            "platformVersion": "32.0",
            "fileUrls": {
                "c1": {
                    "partials": {
                        "h1": "http://a.com/h1-partial.mar",
                        "h2": "http://a.com/h2-partial.mar"
                    },
                    "completes": {
                        "*": "http://a.com/complete.mar"
                    }
                },
                "c2": {
                    "partials": {
                        "h3": "http://a.com/h1-%LOCALE%-partial",
                        "h2": "http://a.com/h2-%LOCALE%-partial"
                    },
                    "completes": {
                        "*": "http://a.com/%LOCALE%-complete"
                    }
                },
                "*": {
                    "partials": {
                        "h0": "http://a.com/h0-partial-catchall.mar",
                        "h1": "http://a.com/h1-partial-catchall",
                        "h2": "http://a.com/h2-partial-catchall"
                    },
                    "completes": {
                        "*": "http://a.com/complete-catchall"
                    }
                }
            },
            "platforms": {
                "p": {
                    "buildID": 500,
                    "OS_FTP": "p",
                    "OS_BOUNCER": "p",
                    "locales": {
                        "l": {
                            "partials": [
                            ],
                            "completes": [
                                {
                                    "filesize": 400,
                                    "from": "*",
                                    "hashValue": "410"
                                }
                            ]
                        }
                    }
                }
            }
        }
        """)
        partial_releases = sample_release_blob_v4.getReferencedReleases()
        self.assertTrue(4, len(partial_releases))
        self.assertEquals(sorted(partial_releases), ['h0', 'h1', 'h2', 'h3'])

    def testIsValid(self):
        # Raises on error
        self.blobH2.validate('h', self.whitelistedDomains)

    def testSchema4WithPartials(self):
        updateQuery = {
            "product": "h", "version": "30.0", "buildID": "10",
            "buildTarget": "p", "locale": "l", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobH2.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobH2.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobH2.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" displayVersion="31.0" appVersion="31.0" platformVersion="31.0" buildID="50">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="41" size="40"/>
""", """
<patch type="partial" URL="http://a.com/h1-partial.mar" hashFunction="sha512" hashValue="9" size="8"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

        updateQuery = {
            "product": "h", "version": "30.0", "buildID": "10",
            "buildTarget": "p", "locale": "l", "channel": "c2",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobH2.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobH2.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobH2.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" displayVersion="31.0" appVersion="31.0" platformVersion="31.0" buildID="50">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/l-complete" hashFunction="sha512" hashValue="41" size="40"/>
""", """
<patch type="partial" URL="http://a.com/h1-l-partial" hashFunction="sha512" hashValue="9" size="8"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

        updateQuery = {
            "product": "h", "version": "30.0", "buildID": "10",
            "buildTarget": "p", "locale": "l", "channel": "c3",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobH2.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobH2.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobH2.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" displayVersion="31.0" appVersion="31.0" platformVersion="31.0" buildID="50">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/complete-catchall" hashFunction="sha512" hashValue="41" size="40"/>
""", """
<patch type="partial" URL="http://a.com/h1-partial-catchall" hashFunction="sha512" hashValue="9" size="8"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testSchema4NoPartials(self):
        updateQuery = {
            "product": "h", "version": "25.0", "buildID": "2",
            "buildTarget": "p", "locale": "l", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobH2.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobH2.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobH2.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" displayVersion="31.0" appVersion="31.0" platformVersion="31.0" buildID="50">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="41" size="40"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

        updateQuery = {
            "product": "h", "version": "25.0", "buildID": "2",
            "buildTarget": "p", "locale": "l", "channel": "c2",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobH2.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobH2.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobH2.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" displayVersion="31.0" appVersion="31.0" platformVersion="31.0" buildID="50">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/l-complete" hashFunction="sha512" hashValue="41" size="40"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

        updateQuery = {
            "product": "h", "version": "25.0", "buildID": "2",
            "buildTarget": "p", "locale": "l", "channel": "c3",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobH2.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobH2.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobH2.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" displayVersion="31.0" appVersion="31.0" platformVersion="31.0" buildID="50">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/complete-catchall" hashFunction="sha512" hashValue="41" size="40"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testSchema4MismatchedLocalePartialsAndFileUrls(self):
        updateQuery = {
            "product": "h", "version": "29.0", "buildID": "5",
            "buildTarget": "p", "locale": "l", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobH3.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobH3.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobH3.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = """
<update type="minor" displayVersion="32.0" appVersion="32.0" platformVersion="32.0" buildID="500">
"""
        expected = ["""
<patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="410" size="400"/>
"""]
        expected_footer = "</update>"
        expected = [x.strip() for x in expected]
        self.assertEquals(returned_header.strip(), expected_header.strip())
        self.assertEquals(returned, expected)
        self.assertEquals(returned_footer.strip(), expected_footer.strip())

    def testConvertFromV3(self):
        v3Blob = ReleaseBlobV3()
        v3Blob.loadJSON("""
{
    "name": "g2",
    "schema_version": 3,
    "hashFunction": "sha512",
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
    }
}
""")

        v4Blob = ReleaseBlobV4.fromV3(v3Blob)
        # Raises on error
        v4Blob.validate('g', self.whitelistedDomains)

        expected = {
            "name": "g2",
            "schema_version": 4,
            "hashFunction": "sha512",
            "fileUrls": {
                "c1": {
                    "partials": {
                        "g1": "http://a.com/g1-partial.mar"
                    },
                    "completes": {
                        "*": "http://a.com/complete.mar"
                    }
                },
                "c2": {
                    "partials": {
                        "g1": "http://a.com/g1-partial",
                    },
                    "completes": {
                        "*": "http://a.com/complete"
                    }
                }
            }
        }

        self.assertEquals(v4Blob, expected)

    def testConvertFromV3Noop(self):
        v3Blob = ReleaseBlobV3()
        v3Blob.loadJSON("""
{
    "name": "g2",
    "schema_version": 4,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": 40,
            "OS_FTP": "o",
            "OS_BOUNCER": "o",
            "locales": {
                "l": {
                    "partials": [
                        {
                            "filesize": 4,
                            "from": "g1",
                            "hashValue": "5",
                            "fileUrl": "http://a.com/g1-partial"
                        }
                    ],
                    "completes": [
                        {
                            "filesize": 34,
                            "from": "*",
                            "hashValue": "35",
                            "fileUrl": "http://a.com/complete"
                        }
                    ]
                }
            }
        }
    }
}
""")

        v4Blob = ReleaseBlobV4.fromV3(v3Blob)
        # Raises on error
        v4Blob.validate('g', self.whitelistedDomains)

        expected = v3Blob.copy()
        expected["schema_version"] = 4

        self.assertEquals(v4Blob, expected)

    def testAllowedDomain(self):
        blob = ReleaseBlobV4(fileUrls=dict(c=dict(completes=dict(foo="http://a.com/c"))))
        self.assertFalse(blob.containsForbiddenDomain('h',
                                                      self.whitelistedDomains))

    def testAllowedDomainWrongProduct(self):
        blob = ReleaseBlobV4(fileUrls=dict(c=dict(completes=dict(foo="http://a.com/c"))))
        self.assertTrue(blob.containsForbiddenDomain('hhh',
                                                     self.whitelistedDomains))

    def testForbiddenDomainFileUrls(self):
        blob = ReleaseBlobV4(fileUrls=dict(c=dict(completes=dict(foo="http://evil.com/c"))))
        self.assertTrue(blob.containsForbiddenDomain('h',
                                                     self.whitelistedDomains))

    def testForbiddenDomainInLocale(self):
        blob = ReleaseBlobV4(platforms=dict(f=dict(locales=dict(h=dict(partials=[dict(fileUrl="http://evil.com/a")])))))
        self.assertTrue(blob.containsForbiddenDomain('h',
                                                     self.whitelistedDomains))

    def testForbiddenDomainAndAllowedDomain(self):
        updates = dict(partials=[dict(fileUrl="http://a.com/a"), dict(fileUrl="http://evil.com/a")])
        blob = ReleaseBlobV3(platforms=dict(f=dict(locales=dict(j=updates))))
        self.assertTrue(blob.containsForbiddenDomain('h',
                                                     self.whitelistedDomains))


class TestSchema5Blob(unittest.TestCase):

    def setUp(self):
        self.specialForceHosts = ["http://a.com"]
        self.whitelistedDomains = {'a.com': ('h',)}
        app.config['DEBUG'] = True
        app.config['SPECIAL_FORCE_HOSTS'] = self.specialForceHosts
        app.config['WHITELISTED_DOMAINS'] = self.whitelistedDomains
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        dbo.releases.t.insert().execute(name='h1', product='h', version='30.0', data_version=1, data=createBlob("""
{
    "name": "h1",
    "schema_version": 5,
    "platforms": {
        "p": {
            "buildID": "10",
            "locales": {
                "l": {}
            }
        }
    }
}
"""))
        self.blobH2 = ReleaseBlobV5()
        self.blobH2.loadJSON("""
{
    "name": "h2",
    "schema_version": 5,
    "hashFunction": "sha512",
    "appVersion": "31.0",
    "displayVersion": "31.0",
    "platformVersion": "31.0",
    "detailsUrl": "http://example.org/details/%LOCALE%",
    "licenseUrl": "http://example.org/license/%LOCALE%",
    "actions": "silent",
    "billboardURL": "http://example.org/billboard/%LOCALE%",
    "openURL": "http://example.org/url/%LOCALE%",
    "notificationURL": "http://example.org/notification/%LOCALE%",
    "alertURL": "http://example.org/alert/%LOCALE%",
    "showPrompt": false,
    "showNeverForVersion": true,
    "promptWaitTime": 12345,
    "fileUrls": {
        "c1": {
            "partials": {
                "h1": "http://a.com/h1-partial.mar"
            },
            "completes": {
                "*": "http://a.com/complete.mar"
            }
        },
        "*": {
            "partials": {
                "h1": "http://a.com/h1-partial-catchall"
            },
            "completes": {
                "*": "http://a.com/complete-catchall"
            }
        }
    },
    "platforms": {
        "p": {
            "buildID": 50,
            "OS_FTP": "p",
            "OS_BOUNCER": "p",
            "locales": {
                "l": {
                    "partials": [
                        {
                            "filesize": 8,
                            "from": "h1",
                            "hashValue": "9"
                        }
                    ],
                    "completes": [
                        {
                            "filesize": 40,
                            "from": "*",
                            "hashValue": "41"
                        }
                    ]
                }
            }
        }
    }
}
""")

    def testGetPartialReleaseReferences_Happy_Case(self):
        sample_release_blob_v5 = ReleaseBlobV5()
        sample_release_blob_v5.loadJSON("""
        {
            "name": "sample",
            "schema_version": 5,
            "hashFunction": "sha512",
            "appVersion": "31.0",
            "displayVersion": "31.0",
            "platformVersion": "31.0",
            "detailsUrl": "http://example.org/details/%LOCALE%",
            "licenseUrl": "http://example.org/license/%LOCALE%",
            "actions": "silent",
            "billboardURL": "http://example.org/billboard/%LOCALE%",
            "openURL": "http://example.org/url/%LOCALE%",
            "notificationURL": "http://example.org/notification/%LOCALE%",
            "alertURL": "http://example.org/alert/%LOCALE%",
            "showPrompt": false,
            "showNeverForVersion": true,
            "promptWaitTime": 12345,
            "fileUrls": {
                "c1": {
                    "partials": {
                        "h1": "http://a.com/h1-partial.mar"
                    },
                    "completes": {
                        "*": "http://a.com/complete.mar"
                    }
                },
                "*": {
                    "partials": {
                        "h1": "http://a.com/h1-partial-catchall"
                    },
                    "completes": {
                        "*": "http://a.com/complete-catchall"
                    }
                }
            },
            "platforms": {
                "p": {
                    "buildID": 50,
                    "OS_FTP": "p",
                    "OS_BOUNCER": "p",
                    "locales": {
                        "l": {
                            "partials": [
                                {
                                    "filesize": 8,
                                    "from": "h2",
                                    "hashValue": "9"
                                }
                            ],
                            "completes": [
                                {
                                    "filesize": 40,
                                    "from": "*",
                                    "hashValue": "41"
                                }
                            ]
                        }
                    }
                }
            }
        }
        """)
        partial_releases = sample_release_blob_v5.getReferencedReleases()
        self.assertTrue(2, len(partial_releases))
        self.assertEquals(sorted(partial_releases), ['h1', 'h2'])

    def testGetPartialReleaseReferences_Empty_fileUrls_Case(self):
        sample_release_blob_v5 = ReleaseBlobV5()
        sample_release_blob_v5.loadJSON("""
        {
            "name": "h2",
            "schema_version": 5,
            "hashFunction": "sha512",
            "appVersion": "31.0",
            "displayVersion": "31.0",
            "platformVersion": "31.0",
            "detailsUrl": "http://example.org/details/%LOCALE%",
            "licenseUrl": "http://example.org/license/%LOCALE%",
            "actions": "silent",
            "billboardURL": "http://example.org/billboard/%LOCALE%",
            "openURL": "http://example.org/url/%LOCALE%",
            "notificationURL": "http://example.org/notification/%LOCALE%",
            "alertURL": "http://example.org/alert/%LOCALE%",
            "showPrompt": false,
            "showNeverForVersion": true,
            "promptWaitTime": 12345,
            "fileUrls": {
                "c1": {
                    "completes": {
                        "*": "http://a.com/complete.mar"
                    }
                },
                "*": {
                    "completes": {
                        "*": "http://a.com/complete-catchall"
                    }
                }
            },
            "platforms": {
                "p": {
                    "buildID": 50,
                    "OS_FTP": "p",
                    "OS_BOUNCER": "p",
                    "locales": {
                        "l": {
                            "partials": [
                                {
                                    "filesize": 8,
                                    "from": "h1",
                                    "hashValue": "9"
                                },
                                {
                                    "filesize": 8,
                                    "from": "h2",
                                    "hashValue": "9"
                                }
                            ],
                            "completes": [
                                {
                                    "filesize": 40,
                                    "from": "*",
                                    "hashValue": "41"
                                }
                            ]
                        },
                        "g": {
                            "partials": [
                                {
                                    "filesize": 8,
                                    "from": "h3",
                                    "hashValue": "9"
                                },
                                {
                                    "filesize": 8,
                                    "from": "h2",
                                    "hashValue": "9"
                                }
                            ],
                            "completes": [
                                {
                                    "filesize": 40,
                                    "from": "*",
                                    "hashValue": "41"
                                }
                            ]
                        }
                    }
                }
            }
        }
        """)
        partial_releases = sample_release_blob_v5.getReferencedReleases()
        self.assertTrue(3, len(partial_releases))
        self.assertEquals(sorted(partial_releases), ['h1', 'h2', 'h3'])

    def testIsValid(self):
        # Raises on error
        self.blobH2.validate('h', self.whitelistedDomains)

    def testSchema5OptionalAttributes(self):
        updateQuery = {
            "product": "h", "version": "30.0", "buildID": "10",
            "buildTarget": "p", "locale": "l", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobH2.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobH2.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobH2.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = '<update type="minor" displayVersion="31.0" appVersion="31.0" platformVersion="31.0" ' \
            'buildID="50" detailsURL="http://example.org/details/l" licenseURL="http://example.org/license/l" ' \
            'billboardURL="http://example.org/billboard/l" showPrompt="false" showNeverForVersion="true" ' \
            'actions="silent" openURL="http://example.org/url/l" notificationURL="http://example.org/notification/l" ' \
            'alertURL="http://example.org/alert/l" promptWaitTime="12345">'
        expected = ["""
<patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="41" size="40"/>
""", """
<patch type="partial" URL="http://a.com/h1-partial.mar" hashFunction="sha512" hashValue="9" size="8"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())


class TestSchema6Blob(unittest.TestCase):

    def setUp(self):
        self.specialForceHosts = ["http://a.com"]
        self.whitelistedDomains = {'a.com': ('h',)}
        app.config['DEBUG'] = True
        app.config['SPECIAL_FORCE_HOSTS'] = self.specialForceHosts
        app.config['WHITELISTED_DOMAINS'] = self.whitelistedDomains
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        dbo.releases.t.insert().execute(name='h1', product='h', data_version=1, data=createBlob("""
{
    "name": "h1",
    "schema_version": 6,
    "platforms": {
        "p": {
            "buildID": "10",
            "locales": {
                "l": {}
            }
        }
    }
}
"""))
        self.blobH2 = ReleaseBlobV6()
        self.blobH2.loadJSON("""
{
    "name": "h2",
    "schema_version": 6,
    "hashFunction": "sha512",
    "appVersion": "31.0",
    "displayVersion": "31.0",
    "detailsUrl": "http://example.org/details/%LOCALE%",
    "actions": "silent",
    "openURL": "http://example.org/url/%LOCALE%",
    "notificationURL": "http://example.org/notification/%LOCALE%",
    "alertURL": "http://example.org/alert/%LOCALE%",
    "showPrompt": false,
    "showNeverForVersion": true,
    "promptWaitTime": 12345,
    "fileUrls": {
        "c1": {
            "partials": {
                "h1": "http://a.com/h1-partial.mar"
            },
            "completes": {
                "*": "http://a.com/complete.mar"
            }
        },
        "*": {
            "partials": {
                "h1": "http://a.com/h1-partial-catchall"
            },
            "completes": {
                "*": "http://a.com/complete-catchall"
            }
        }
    },
    "platforms": {
        "p": {
            "buildID": 50,
            "OS_FTP": "p",
            "OS_BOUNCER": "p",
            "locales": {
                "l": {
                    "partials": [
                        {
                            "filesize": 8,
                            "from": "h1",
                            "hashValue": "9"
                        }
                    ],
                    "completes": [
                        {
                            "filesize": 40,
                            "from": "*",
                            "hashValue": "41"
                        }
                    ]
                }
            }
        }
    }
}
""")

    def testGetPartialReleaseReferences_Happy_Case(self):
        sample_release_blob_v6 = ReleaseBlobV6()
        sample_release_blob_v6.loadJSON("""
        {
            "name": "h2",
            "schema_version": 6,
            "hashFunction": "sha512",
            "appVersion": "31.0",
            "displayVersion": "31.0",
            "detailsUrl": "http://example.org/details/%LOCALE%",
            "actions": "silent",
            "openURL": "http://example.org/url/%LOCALE%",
            "notificationURL": "http://example.org/notification/%LOCALE%",
            "alertURL": "http://example.org/alert/%LOCALE%",
            "showPrompt": false,
            "showNeverForVersion": true,
            "promptWaitTime": 12345,
            "fileUrls": {
                "c1": {
                    "partials": {
                        "h1": "http://a.com/h1-partial.mar"
                    },
                    "completes": {
                        "*": "http://a.com/complete.mar"
                    }
                },
                "*": {
                    "partials": {
                        "h1": "http://a.com/h1-partial-catchall"
                    },
                    "completes": {
                        "*": "http://a.com/complete-catchall"
                    }
                }
            },
            "platforms": {
                "p": {
                    "buildID": 50,
                    "OS_FTP": "p",
                    "OS_BOUNCER": "p",
                    "locales": {
                        "l": {
                            "partials": [
                                {
                                    "filesize": 8,
                                    "from": "h2",
                                    "hashValue": "9"
                                }
                            ],
                            "completes": [
                                {
                                    "filesize": 40,
                                    "from": "*",
                                    "hashValue": "41"
                                }
                            ]
                        }
                    }
                }
            }
        }
        """)
        partial_releases = sample_release_blob_v6.getReferencedReleases()
        self.assertTrue(2, len(partial_releases))
        self.assertEquals(sorted(partial_releases), ['h1', 'h2'])

    def testGetPartialReleaseReferences_Empty_Partials_Case(self):
        sample_release_blob_v6 = ReleaseBlobV6()
        sample_release_blob_v6.loadJSON("""{
            "name": "h1",
            "schema_version": 6,
            "platforms": {
                "p": {
                    "buildID": "10",
                    "locales": {
                        "l": {}
                    }
                }
            }
        }
        """)
        partial_releases = sample_release_blob_v6.getReferencedReleases()
        self.assertEquals(0, len(partial_releases))

    def testIsValid(self):
        # Raises on error
        self.blobH2.validate('h', self.whitelistedDomains)

    def testSchema6OptionalAttributes(self):
        updateQuery = {
            "product": "h", "buildID": "10",
            "buildTarget": "p", "locale": "l", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobH2.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobH2.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobH2.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = '<update type="minor" displayVersion="31.0" appVersion="31.0" platformVersion="None" ' \
            'buildID="50" detailsURL="http://example.org/details/l" showPrompt="false" showNeverForVersion="true" ' \
            'actions="silent" openURL="http://example.org/url/l" notificationURL="http://example.org/notification/l" ' \
            'alertURL="http://example.org/alert/l" promptWaitTime="12345">'
        expected = ["""
<patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="41" size="40"/>
""", """
<patch type="partial" URL="http://a.com/h1-partial.mar" hashFunction="sha512" hashValue="9" size="8"/>
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testCheckFailForUnsuportedAttributes(self):
        self.blobH3 = ReleaseBlobV6()
        self.blobH3.loadJSON("""
{
    "name": "h3",
    "schema_version": 5,
    "hashFunction": "sha512",
    "appVersion": "31.0",
    "displayVersion": "31.0",
    "platformVersion": "31.0",
    "detailsUrl": "http://example.org/details/%LOCALE%",
    "licenseUrl": "http://example.org/license/%LOCALE%",
    "actions": "silent",
    "billboardURL": "http://example.org/billboard/%LOCALE%",
    "openURL": "http://example.org/url/%LOCALE%",
    "notificationURL": "http://example.org/notification/%LOCALE%",
    "alertURL": "http://example.org/alert/%LOCALE%",
    "showPrompt": false,
    "showNeverForVersion": true,
    "promptWaitTime": 12345,
    "fileUrls": {
        "c1": {
            "partials": {
                "h1": "http://a.com/h1-partial.mar"
            },
            "completes": {
                "*": "http://a.com/complete.mar"
            }
        },
        "*": {
            "partials": {
                "h1": "http://a.com/h1-partial-catchall"
            },
            "completes": {
                "*": "http://a.com/complete-catchall"
            }
        }
    },
    "platforms": {
        "p": {
            "buildID": 50,
            "OS_FTP": "p",
            "OS_BOUNCER": "p",
            "locales": {
                "l": {
                    "partials": [
                        {
                            "filesize": 8,
                            "from": "h1",
                            "hashValue": "9"
                        }
                    ],
                    "completes": [
                        {
                            "filesize": 40,
                            "from": "*",
                            "hashValue": "41"
                        }
                    ]
                }
            }
        }
    }
}
""")
        self.assertRaises(BlobValidationError, self.blobH3.validate, 'h', self.whitelistedDomains)


class TestSchema8Blob(unittest.TestCase):

    def setUp(self):
        self.specialForceHosts = ["http://a.com"]
        self.whitelistedDomains = {'a.com': ('h',)}
        app.config['DEBUG'] = True
        app.config['SPECIAL_FORCE_HOSTS'] = self.specialForceHosts
        app.config['WHITELISTED_DOMAINS'] = self.whitelistedDomains
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        dbo.releases.t.insert().execute(name='h1', product='h', data_version=1, data=createBlob("""
{
    "name": "h1",
    "schema_version": 8,
    "platforms": {
        "p": {
            "buildID": "10",
            "locales": {
                "l": {}
            }
        }
    }
}
"""))
        self.blobH2 = ReleaseBlobV8()
        self.blobH2.loadJSON("""
{
    "name": "h2",
    "schema_version": 8,
    "hashFunction": "sha512",
    "appVersion": "31.0",
    "displayVersion": "31.0",
    "detailsUrl": "http://example.org/details/%LOCALE%",
    "actions": "silent",
    "openURL": "http://example.org/url/%LOCALE%",
    "notificationURL": "http://example.org/notification/%LOCALE%",
    "alertURL": "http://example.org/alert/%LOCALE%",
    "showPrompt": false,
    "showNeverForVersion": true,
    "promptWaitTime": 12345,
    "binTransMerkleRoot": "merkle_root",
    "binTransCertificate": "cert",
    "binTransSCTList": "sct_list",
    "fileUrls": {
        "c1": {
            "partials": {
                "h1": "http://a.com/h1-partial.mar"
            },
            "completes": {
                "*": "http://a.com/complete.mar"
            }
        },
        "*": {
            "partials": {
                "h1": "http://a.com/h1-partial-catchall"
            },
            "completes": {
                "*": "http://a.com/complete-catchall"
            }
        }
    },
    "platforms": {
        "p": {
            "buildID": 50,
            "OS_FTP": "p",
            "OS_BOUNCER": "p",
            "locales": {
                "l": {
                    "partials": [
                        {
                            "filesize": 8,
                            "from": "h1",
                            "hashValue": "9",
                            "binTransInclusionProof": """ + '"' + ('834charpartialsproof' * 42)[:834] + '"' + """
                        }
                    ],
                    "completes": [
                        {
                            "filesize": 40,
                            "from": "*",
                            "hashValue": "41",
                            "binTransInclusionProof": """ + '"' + ('834charcompletesproof' * 40)[:834] + '"' + """
                        }
                    ]
                }
            }
        }
    }
}
""")

    def testIsValid(self):
        # Raises on error
        self.blobH2.validate('h', self.whitelistedDomains)

    def testSchema8OptionalAttributes(self):
        updateQuery = {
            "product": "h", "buildID": "10",
            "buildTarget": "p", "locale": "l", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        returned_header = self.blobH2.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blobH2.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blobH2.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = '<update type="minor" displayVersion="31.0" appVersion="31.0" platformVersion="None" ' \
            'buildID="50" detailsURL="http://example.org/details/l" showPrompt="false" showNeverForVersion="true" ' \
            'actions="silent" openURL="http://example.org/url/l" notificationURL="http://example.org/notification/l" ' \
            'alertURL="http://example.org/alert/l" promptWaitTime="12345" ' \
            'binTransMerkleRoot="merkle_root" binTransCertificate="cert" binTransSCTList="sct_list">'
        expected = ["""
<patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="41" size="40" """ +
                    'binTransInclusionProof="' + ('834charcompletesproof' * 40)[:834] + '"/>\n',
                    """
<patch type="partial" URL="http://a.com/h1-partial.mar" hashFunction="sha512" hashValue="9" size="8" """ +
                    'binTransInclusionProof="' + ('834charpartialsproof' * 42)[:834] + '"/>\n'
                    ]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())


class TestDesupportBlob(unittest.TestCase):

    def setUp(self):
        self.specialForceHosts = ["http://a.com"]
        self.whitelistedDomains = {'a.com': ('a',), 'moo.com': ('d',)}
        app.config['DEBUG'] = True
        app.config['SPECIAL_FORCE_HOSTS'] = self.specialForceHosts
        app.config['WHITELISTED_DOMAINS'] = self.whitelistedDomains
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        self.blob = DesupportBlob()
        self.blob.loadJSON("""
{
    "name": "d1",
    "schema_version": 50,
    "detailsUrl": "http://moo.com/%locale%/cow/%version%/%os%",
    "displayVersion": "50.0"
}
""")

    def testDesupport(self):
        updateQuery = {"locale": "<locale>", "version": "<version>", "buildTarget": "Darwin_x86_64-gcc3-u-i386-x86_64"}
        returned_header = self.blob.getInnerHeaderXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = self.blob.getInnerXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned_footer = self.blob.getInnerFooterXML(updateQuery, "minor", self.whitelistedDomains, self.specialForceHosts)
        returned = [x.strip() for x in returned]
        expected_header = ""
        expected = ["""
<update type="minor" unsupported="true" detailsURL="http://moo.com/<locale>/cow/<version>/Darwin" displayVersion="50.0">
"""]
        expected = [x.strip() for x in expected]
        expected_footer = "</update>"
        self.assertEqual(returned_header.strip(), expected_header.strip())
        self.assertItemsEqual(returned, expected)
        self.assertEqual(returned_footer.strip(), expected_footer.strip())

    def testBrokenDesupport(self):
        blob = DesupportBlob(name="d2", schema_version=50, foo="bar")
        self.assertRaises(BlobValidationError, blob.validate, 'd',
                          self.whitelistedDomains)


class TestUnifiedFileUrlsMixin(unittest.TestCase):

    def setUp(self):
        fileUrls = {
            "c1": {
                "partials": {
                    "h1": "http://a.com/h1-partial.mar"
                },
                "completes": {
                    "*": "http://a.com/complete.mar"
                }
            },
            "*": {
                "partials": {
                    "h1": "http://a.com/h1-partial-catchall",
                    "h2": "http://a.com/h2-partial-catchall",
                },
                "completes": {
                    "*": "http://a.com/complete-catchall"
                }
            }
        }
        values = {'fileUrls': fileUrls, 'p': {'OS_FTP': 'os_ftp', 'OS_BOUNCER': 'os_bouncer'}}

        def side_effects(key, *args):
            return values[key]

        self.mixin_instance = UnifiedFileUrlsMixin()
        self.mixin_instance.getPlatformData = mock.Mock(side_effect=side_effects)
        self.mixin_instance.get = mock.Mock(side_effect=side_effects)
        self.mixin_instance.log = mock.MagicMock()
        self.mixin_instance.log.debug = mock.MagicMock()

    def testGetUrlGetsFromChannel(self):
        updateQuery = {
            "product": "h", "version": "30.0", "buildID": "10",
            "buildTarget": "p", "locale": "l", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        patchKey = "partials"
        patch = {"from": "h1"}
        specialForceHosts = ["http://a.com"]

        expected_url = "http://a.com/h1-partial.mar"
        url = self.mixin_instance._getUrl(updateQuery, patchKey, patch, specialForceHosts)

        self.assertEquals(expected_url, url)

    def testGetUrlDoesntFallBackToCatchAll(self):
        updateQuery = {
            "product": "h", "version": "30.0", "buildID": "10",
            "buildTarget": "p", "locale": "l", "channel": "c1",
            "osVersion": "a", "distribution": "a", "distVersion": "a",
            "force": None,
        }
        patchKey = "partials"
        patch = {"from": "h2"}
        specialForceHosts = ["http://a.com"]

        with self.assertRaises(ValueError):
            self.mixin_instance._getUrl(updateQuery, patchKey, patch, specialForceHosts)


class TestAdditionalPatchAttributesXMLMixin(unittest.TestCase):

    def setUp(self):
        self.mixin_instance = ProofXMLMixin()

    def testGetAdditionalPatchAttributesComplete(self):
        patch = {
            'hashValue': 'd456a23ff5a6b35146d9edf05ccc983b0b7b6695fdc11e8d4f44a704c63ae69a585c3429bb90fece5a34a59b06f54'
                         'b1c947178b9038ce6c83a1b6ac8a86f4274',
            'from': '*',
            'filesize': 49376124,
            'binTransInclusionProof': 'foobar'
        }

        expected_additional_patch_attributes = {'binTransInclusionProof': 'foobar'}
        additionalPatchAttributes = self.mixin_instance._getAdditionalPatchAttributes(patch)

        self.assertEquals(expected_additional_patch_attributes, additionalPatchAttributes)

    def testGetAdditionalPatchAttributesPartial(self):
        patch = {
            'hashValue': 'dffd728108a176b1aeca390a420200daa9272f246587f81fde41ad3f5c44bf6de17fb7899b4353e5cbaa8528ea389'
                         '234890221188db5bb58588ad366c2be0676',
            'from': 'Firefox-54.0b12-build1',
            'filesize': 28264739,
            'binTransInclusionProof': 'barfoo'
        }

        expected_additional_patch_attributes = {'binTransInclusionProof': 'barfoo'}
        additionalPatchAttributes = self.mixin_instance._getAdditionalPatchAttributes(patch)

        self.assertEquals(expected_additional_patch_attributes, additionalPatchAttributes)
