import unittest

from auslib.blob import Blob, ReleaseBlobV1

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

class TestReleaseBlobV1(unittest.TestCase):
    def testGetResolvedPlatform(self):
        blob = ReleaseBlobV1(platforms=dict(a=dict(), b=dict(alias='a')))
        self.assertEquals('a', blob.getResolvedPlatform('a'))
        self.assertEquals('a', blob.getResolvedPlatform('b'))

    def testGetPlatformData(self):
        blob = ReleaseBlobV1(platforms=dict(a=dict(foo=1)))
        self.assertEquals(blob.getPlatformData('a'), dict(foo=1))

    def testGetLocaleOrTopLevelParamTopLevelOnly(self):
        blob = ReleaseBlobV1(foo=5)
        self.assertEquals(5, blob.getLocaleOrTopLevelParam('a', 'b', 'foo'))

    def testGetLocaleOrTopLevelParamLocaleOnly(self):
        blob = ReleaseBlobV1(platforms=dict(f=dict(locales=dict(g=dict(foo=6)))))
        self.assertEquals(6, blob.getLocaleOrTopLevelParam('f', 'g', 'foo'))

    def testGetBuildIDPlatformOnly(self):
        blob = ReleaseBlobV1(platforms=dict(a=dict(buildID=1, locales=dict(b=dict()))))
        self.assertEquals(1, blob.getBuildID('a', 'b'))

    def testGetBuildIDLocaleOnly(self):
        blob = ReleaseBlobV1(platforms=dict(c=dict(locales=dict(d=dict(buildID=9)))))
        self.assertEquals(9, blob.getBuildID('c', 'd'))
    # XXX: should we support the locale overriding the platform? this should probably be invalid
