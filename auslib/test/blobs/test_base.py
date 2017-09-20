from copy import deepcopy
import mock
import unittest

from hypothesis import given, assume
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
json = st.dictionaries(st.text(),
                       st.recursive(st.none() | st.floats(allow_nan=False) | st.text(),
                                    lambda children: st.lists(children, max_size=10) | st.dictionaries(st.text(), children, max_size=10),
                                    max_leaves=20),
                       max_size=10)


@given(json)
def test_merge_blobs_join_lists(base):
    left = deepcopy(base)
    right = deepcopy(base)
    expected = deepcopy(base)
    to_modify = None
    for key in base:
        if isinstance(base[key], list):
            to_modify = key
            break
    assume(to_modify is not None)
    left[to_modify].extend(range(1, 4))
    right[to_modify].extend(range(4, 7))
    expected[to_modify].extend(range(1, 7))
    got = merge_blobs(base, left, right)
    assert got == expected


@given(json)
def test_merge_blobs_raise_when_both_adding_same_key(base):
    left = deepcopy(base)
    right = deepcopy(base)
    left["foobar"] = "blah"
    right["foobar"] = "crap"
    try:
        merge_blobs(base, left, right)
    except ValueError as e:
        assert "left and right are both changing 'foobar'" in e.message
    else:
        assert False, "ValueError not raised"


@given(json)
def test_merge_blobs_raise_when_both_modifying_same_key(base):
    left = deepcopy(base)
    right = deepcopy(base)
    base["foobar"] = "foo"
    left["foobar"] = "blah"
    right["foobar"] = "crap"
    try:
        merge_blobs(base, left, right)
    except ValueError as e:
        assert "left and right are both changing" in e.message
    else:
        assert False, "ValueError not raised"


@given(json)
def test_merge_blobs_mismatched_types(base):
    left = deepcopy(base)
    right = deepcopy(base)
    assume(len(base) > 0)
    to_modify = base.keys()[0]
    left[to_modify] = "foo"
    right[to_modify] = [1, 2, 3]
    try:
        merge_blobs(base, left, right)
    except ValueError as e:
        assert "type mismatch" in e.message
    else:
        assert False, "ValueError not raised"
