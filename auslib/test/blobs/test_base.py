import unittest

from auslib.blobs.base import Blob, createBlob


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


class TestCreateBlob(unittest.TestCase):

    def testLoadString(self):
        data = """{
"schema_version": 2,
"name": "blah"}"""
        blob = createBlob(data)
        self.assertEquals(blob, dict(schema_version=2, name="blah"))

    def testLoadDict(self):
        data = dict(
            schema_version=1,
            name="foo"
        )
        blob = createBlob(data)
        self.assertEquals(blob, data)

    def testMissingSchemaVersion(self):
        self.assertRaises(ValueError, createBlob, dict(name="foo"))

    def testBadSchemaVersion(self):
        self.assertRaises(ValueError, createBlob, dict(schema_version=666))
