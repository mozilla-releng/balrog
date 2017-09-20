from copy import deepcopy
import mock
import unittest

from hypothesis import given
import hypothesis.strategies as st

from auslib.blobs.base import createBlob, merge_blobs
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
            blob.validate('fake', [])
            blob = createBlob(dict(
                schema_version=1,
                name="foo",
            ))
            blob.validate('fake', [])

            self.assertEquals(yaml_load.call_count, 1)


# Explicitly not using bools here because they are extremely difficult to handle correctly, and we don't need to support them.
json = st.dictionaries(st.text(), st.recursive(st.none() | st.floats(allow_nan=False) | st.text(), lambda children: st.lists(children) | st.dictionaries(st.text(), children)))


@given(json)
def test_merge_blobs(base):
    left = deepcopy(base)
    right = deepcopy(base)
    expected = deepcopy(base)
    to_modify = None
    if isinstance(base, dict):
        for key in base:
            if isinstance(base[key], list):
                to_modify = key
    if not to_modify:
        return
    left[to_modify].extend([1,2,3])
    right[to_modify].extend([4,5,6])
    expected[to_modify].extend([1,2,3,4,5,6])
    got = merge_blobs(base, left, right)
    assert got == expected
