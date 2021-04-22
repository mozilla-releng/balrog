import unittest

from auslib.util.rulematching import matchMemory, matchVersion


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


class TestMatchVersion(unittest.TestCase):
    def test_glob(self):
        self.assertTrue(matchVersion("78.8.*", "78.8.0"))
        self.assertTrue(matchVersion("78.8.*", "78.8.1"))
        self.assertFalse(matchVersion("78.8.*", "78.9.0"))
        self.assertTrue(matchVersion("78.*", "78.8.0"))
        self.assertTrue(matchVersion("78.*", "78.9.0"))
        self.assertFalse(matchVersion("79.*", "78.9.0"))
