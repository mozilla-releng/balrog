import operator
import unittest

from auslib.util.comparison import get_op, string_compare, version_compare


class testGetOp(unittest.TestCase):

    def test_equality(self):
        self.assertEqual((operator.eq, '20150314092653'),
                         get_op('20150314092653'))
        self.assertEqual((operator.eq, '30.0b1'), get_op('30.0b1'))
        self.assertEqual((operator.eq, '30.0.1'), get_op('30.0.1'))

    def test_greater_or_equal(self):
        self.assertEqual((operator.ge, '20150314092653'),
                         get_op('>=20150314092653'))
        self.assertEqual((operator.ge, '30.0b1'), get_op('>=30.0b1'))
        self.assertEqual((operator.ge, '30.0.1'), get_op('>=30.0.1'))

    def test_greater_than(self):
        self.assertEqual((operator.gt, '20150314092653'),
                         get_op('>20150314092653'))
        self.assertEqual((operator.gt, '30.0b1'), get_op('>30.0b1'))
        self.assertEqual((operator.gt, '30.0.1'), get_op('>30.0.1'))

    def test_less_than(self):
        self.assertEqual((operator.lt, '20150314092653'),
                         get_op('<20150314092653'))
        self.assertEqual((operator.lt, '30.0b1'), get_op('<30.0b1'))
        self.assertEqual((operator.lt, '30.0.1'), get_op('<30.0.1'))

    def test_lesser_or_equal(self):
        self.assertEqual((operator.le, '20150314092653'),
                         get_op('<=20150314092653'))
        self.assertEqual((operator.le, '30.0b1'), get_op('<=30.0b1'))
        self.assertEqual((operator.le, '30.0.1'), get_op('<=30.0.1'))


class testStringCompare(unittest.TestCase):

    def test_equality(self):
        self.assertTrue(string_compare('20150314092653', '20150314092653'))
        self.assertFalse(string_compare('20010100000000', '20150314092653'))

    def test_greater_or_equal(self):
        self.assertFalse(string_compare('20150314092652', '>=20150314092653'))
        self.assertTrue(string_compare('20150314092653', '>=20150314092653'))
        self.assertTrue(string_compare('20150314092654', '>=20150314092653'))

    def test_greater_than(self):
        self.assertFalse(string_compare('20150314092652', '>20150314092653'))
        self.assertFalse(string_compare('20150314092653', '>20150314092653'))
        self.assertTrue(string_compare('20150314092654', '>20150314092653'))

    def test_less_than(self):
        self.assertTrue(string_compare('20150314092652', '<20150314092653'))
        self.assertFalse(string_compare('20150314092653', '<20150314092653'))
        self.assertFalse(string_compare('20150314092654', '<20150314092653'))

    def test_lesser_or_equal(self):
        self.assertTrue(string_compare('20150314092652', '<=20150314092653'))
        self.assertTrue(string_compare('20150314092653', '<=20150314092653'))
        self.assertFalse(string_compare('20150314092654', '<=20150314092653'))


class testVersionCompare(unittest.TestCase):

    def test_equality(self):
        # this isn't exhaustive, no need to redo all the MozillaVersion tests
        self.assertTrue(version_compare('30.0', '30.0'))
        self.assertTrue(version_compare('30.0.1', '30.0.1'))
        self.assertFalse(version_compare('30.0', '30.0.1'))
        self.assertFalse(version_compare('30.0.1', '30.0'))

    def test_greater_or_equal(self):
        self.assertFalse(version_compare('29.0', '>=30.0'))
        self.assertTrue(version_compare('30.0', '>=30.0'))
        self.assertTrue(version_compare('30.0.1', '>=30.0'))

    def test_greater_than(self):
        self.assertFalse(version_compare('29.0', '>30.0'))
        self.assertFalse(version_compare('30.0', '>30.0'))
        self.assertTrue(version_compare('30.0.1', '>30.0'))

    def test_less_than(self):
        self.assertTrue(version_compare('29.0', '<30.0'))
        self.assertFalse(version_compare('30.0', '<30.0'))
        self.assertFalse(version_compare('30.0.1', '<30.0'))

    def test_less_or_equal(self):
        self.assertTrue(version_compare('29.0', '<=30.0'))
        self.assertTrue(version_compare('30.0', '<=30.0'))
        self.assertFalse(version_compare('30.0.1', '<=30.0'))
