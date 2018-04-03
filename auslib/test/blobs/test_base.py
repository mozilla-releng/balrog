from copy import deepcopy
import mock
import unittest

from hypothesis import given, assume, settings, HealthCheck
import hypothesis.strategies as st

from auslib.blobs.base import createBlob, merge_dicts, merge_lists
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
        self.assertEquals(blob, dict(schema_version=2, name="blah", has_wnp=False))

    def testLoadDict(self):
        data = dict(
            schema_version=1,
            name="foo",
            has_wnp=False
        )
        blob = createBlob(data)
        self.assertEquals(blob, data)

    def testMissingSchemaVersion(self):
        self.assertRaises(ValueError, createBlob, dict(name="foo"))

    def testBadSchemaVersion(self):
        self.assertRaises(ValueError, createBlob, dict(schema_version=666))

    def testSchemaCaching(self):
        with mock.patch("yaml.safe_load") as yaml_load:
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
                    },
                    "has_wnp": {
                        "type": "boolean"
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


# Things we consider to be useful values in testing blobs. Basically, these
# are things would actually show up in real blobs. Nesting is handled
# further down.
# Ideally we'd include st.boolean() here, but without a way to exclude
# booleans from list items (which doesn't happen in the real world), we end
# up with test failures because things like "1 in [True]" are True, which
# ends up failing tests.
useful_values = st.none() | st.floats(allow_nan=False) | st.text()


@given(st.lists(useful_values), st.lists(useful_values), st.lists(useful_values))
def test_merge_lists_unique_items_present(base, left_additional, right_additional):
    left = deepcopy(base) + left_additional
    right = deepcopy(base) + right_additional
    expected = list(set(deepcopy(base) + left_additional + right_additional))
    got = merge_lists(base, left, right)
    assert len(got) == len(expected)
    assert all([expected_item in expected + got for expected_item in expected])


@given(st.lists(useful_values), st.lists(useful_values))
def test_merge_lists_no_dupes(base, additional):
    left = deepcopy(base) + additional
    right = deepcopy(base) + additional
    expected = list(set(left))
    got = merge_lists(base, left, right)
    assert len(got) == len(expected)
    assert all([expected_item in expected + got for expected_item in expected])


def unique_items_only(i):
    """Returns a hashable value for various types to be used for testing
    uniqueness when generating test data."""
    if isinstance(i, dict):
        return tuple(i.keys())
    if isinstance(i, list):
        return tuple(i)
    return i


# Inspired by http://hypothesis.readthedocs.io/en/latest/data.html#recursive-data,
# but only generates JSON data with a dict as the top level object.
useful_dict = st.dictionaries(st.text(), useful_values | st.lists(useful_values, max_size=10, unique_by=unique_items_only), max_size=10)
useful_list = st.lists(useful_values | useful_dict, max_size=10, unique_by=unique_items_only)
json = st.dictionaries(st.text(),
                       st.recursive(useful_values,
                                    lambda x: useful_list | useful_dict,
                                    max_leaves=20),
                       max_size=10)


def test_merge_dicts_simple_additions():
    base = {
        "nothing": "nothing",
    }
    left = deepcopy(base)
    right = deepcopy(base)
    expected = deepcopy(base)
    left["foo"] = "foo"
    right["bar"] = "bar"
    got = merge_dicts(base, left, right)
    expected = {
        "foo": "foo",
        "bar": "bar",
        "nothing": "nothing",
    }
    assert got == expected


def test_merge_dicts_simple_changes():
    base = {
        "foo": "oof",
        "bar": "rab",
        "nothing": "nothing",
    }
    left = deepcopy(base)
    right = deepcopy(base)
    expected = deepcopy(base)
    left["foo"] = "foo"
    right["bar"] = "bar"
    got = merge_dicts(base, left, right)
    expected = {
        "foo": "foo",
        "bar": "bar",
        "nothing": "nothing",
    }
    assert got == expected


# too_slow health checks are repressed because tests can be slow in CI, and we
# don't want CI failures due to this.
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
@given(json)
def test_merge_dicts_join_lists(base):
    to_modify = None
    for key in base:
        if isinstance(base[key], list):
            to_modify = key
            break
    assume(to_modify is not None)

    left = deepcopy(base)
    right = deepcopy(base)
    expected = deepcopy(base)
    left[to_modify].extend(range(1, 4))
    right[to_modify].extend(range(4, 7))
    expected[to_modify].extend(range(1, 7))
    got = merge_dicts(base, left, right)
    assert got == expected


@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
@given(json)
def test_merge_dicts_raise_when_both_adding_same_key(base):
    left = deepcopy(base)
    right = deepcopy(base)
    left["foobar"] = "blah"
    right["foobar"] = "crap"
    try:
        merge_dicts(base, left, right)
    except ValueError as e:
        assert "left and right are both changing 'foobar'" in str(e)
    else:
        assert False, "ValueError not raised"


@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
@given(json)
def test_merge_dicts_raise_when_both_modifying_same_key(base):
    left = deepcopy(base)
    right = deepcopy(base)
    base["foobar"] = "foo"
    left["foobar"] = "blah"
    right["foobar"] = "crap"
    try:
        merge_dicts(base, left, right)
    except ValueError as e:
        assert "left and right are both changing" in str(e)
    else:
        assert False, "ValueError not raised"


@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
@given(json)
def test_merge_dicts_mismatched_types(base):
    assume(len(base) > 0)

    left = deepcopy(base)
    right = deepcopy(base)
    to_modify = list(base.keys())[0]
    left[to_modify] = "foo"
    right[to_modify] = [1, 2, 3]
    try:
        merge_dicts(base, left, right)
    except ValueError as e:
        assert "type mismatch" in str(e)
    else:
        assert False, "ValueError not raised"


def test_merge_dicts_unicode_and_str_are_equal():
    base = {"foo": "bar"}
    left = {"foo": "bar", "blah": "crap", "abc": "def"}
    right = {u"foo": u"bar", u"blah": u"crap", u"ghi": u"jkl"}
    expected = {"foo": "bar", "blah": "crap", "abc": "def", "ghi": "jkl"}
    got = merge_dicts(base, left, right)
    assert got == expected
