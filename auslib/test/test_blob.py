import unittest

from auslib.blob import Blob

class SimpleBlob(Blob):
    format = {'foo': None}

class MultiLevelBlob(Blob):
    format = {
        'foo': {
            'bar': {
                'baz': None
            }
        }
    }

class BlobWithWildcard(Blob):
    format = {
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
