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
