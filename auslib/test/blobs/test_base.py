import mock
import unittest

from auslib.blobs.base import createBlob
from auslib.global_state import cache


class TestCreateBlob(unittest.TestCase):

    def setUp(self):
        cache.reset()
        cache.make_cache("blob_schema", 50, 10000)

    def tearDown(self):
        cache.reset()

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

    def testSchemaCaching(self):
        with mock.patch("yaml.load") as yaml_load:
            yaml_load.return_value = {
                "title": "Test",
                "type": "object",
                "required": ["schema_version", "name"],
                "additionalProperties": False,
                "properties": {
                    "schema_version": {
                        "type": "number"
                    },
                    "name": {
                        "type": "string"
                    }
                }
            }
            blob = createBlob(dict(
                schema_version=1,
                name="foo",
            ))
            blob.validate()
            blob = createBlob(dict(
                schema_version=1,
                name="foo",
            ))
            blob.validate()

            self.assertEquals(yaml_load.call_count, 1)
