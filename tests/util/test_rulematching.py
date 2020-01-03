import unittest

from auslib.util.rulematching import matchMemory


class TestMatchMemory(unittest.TestCase):
    def test_empty_string(self):
        self.assertTrue(matchMemory(">2048", ""))

    def test_none(self):
        self.assertTrue(matchMemory(">2048", None))

    def test_int(self):
        self.assertTrue(matchMemory(">2048", 10000))

    def test_parsable_string(self):
        self.assertTrue(matchMemory(">2048", "10000"))

    def test_unparsable_string(self):
        self.assertTrue(matchMemory(">2048", "trash"))

    def test_int_false(self):
        self.assertFalse(matchMemory(">2048", 10))

    def test_parsable_string_false(self):
        self.assertFalse(matchMemory(">2048", "10"))
