import unittest
import operator
from auslib.util import PrinterFriendlyDict, getPagination
from auslib.util.versions import MozillaVersion
from auslib.util.comparison import get_op, string_compare, version_compare


class TestPrinterFriendlyDict(unittest.TestCase):

    def test_keys(self):
        pdf = PrinterFriendlyDict({
            'b': 'B',
            'a': 'A'
        })
        self.assertEqual(pdf.keys(), ['a', 'b'])

    def test_items(self):
        pdf = PrinterFriendlyDict({
            'b': 'B',
            'a': 'A'
        })
        self.assertEqual(
            pdf.items(),
            [('a', u'A'), ('b', u'B')]
        )

class TestGetPagination(unittest.TestCase):

    def test_basic_pagination(self):
        page = 1
        total_count = 99
        page_size = 10
        max_range_length = 10

        pagination = getPagination(
            page,
            total_count,
            page_size,
            max_range_length=max_range_length
        )
        self.assertEqual(pagination['range'], range(1, 11))
        self.assertEqual(pagination['current_page'], 1)
        self.assertEqual(pagination['next'], 2)
        self.assertTrue('prev' not in pagination)

        page = 2
        pagination = getPagination(
            page,
            total_count,
            page_size,
            max_range_length=max_range_length
        )
        self.assertEqual(pagination['range'], range(1, 11))
        self.assertEqual(pagination['current_page'], 2)
        self.assertEqual(pagination['next'], 3)
        self.assertEqual(pagination['prev'], 1)

        page = 10
        pagination = getPagination(
            page,
            total_count,
            page_size,
            max_range_length=max_range_length
        )
        self.assertEqual(pagination['range'], range(1, 11))
        self.assertEqual(pagination['current_page'], 10)
        self.assertTrue('next' not in pagination)
        self.assertEqual(pagination['prev'], 9)


class TestMozillaVersions(unittest.TestCase):
    # This tests the new behaviour we've added.
    def test_special_version(self):
        version = MozillaVersion('3.6.3plugin1')
        self.assertEqual(version.version, (3, 6, 3))
        self.assertEqual(version.prerelease, ('p', 1))
        self.assertEqual(str(version), '3.6.3p1')

    # The remaining tests are lifted from upstream:
    # http://hg.python.org/cpython/file/v2.7.3/Lib/distutils/tests/test_version.py
    def test_prerelease(self):
        version = MozillaVersion('1.2.3a1')
        self.assertEqual(version.version, (1, 2, 3))
        self.assertEqual(version.prerelease, ('a', 1))
        self.assertEqual(str(version), '1.2.3a1')

        version = MozillaVersion('1.2.0')
        self.assertEqual(str(version), '1.2')

    def test_cmp_strict(self):
        versions = (('1.5.1', '1.5.2b2', -1),
                    ('161', '3.10a', ValueError),
                    ('8.02', '8.02', 0),
                    ('3.4j', '1996.07.12', ValueError),
                    ('3.2.pl0', '3.1.1.6', ValueError),
                    ('2g6', '11g', ValueError),
                    ('0.9', '2.2', -1),
                    ('1.2.1', '1.2', 1),
                    ('1.1', '1.2.2', -1),
                    ('1.2', '1.1', 1),
                    ('1.2.1', '1.2.2', -1),
                    ('1.2.2', '1.2', 1),
                    ('1.2', '1.2.2', -1),
                    ('0.4.0', '0.4', 0),
                    ('1.13++', '5.5.kw', ValueError))

        for v1, v2, wanted in versions:
            try:
                res = MozillaVersion(v1).__cmp__(MozillaVersion(v2))
            except ValueError:
                if wanted is ValueError:
                    continue
                else:
                    raise AssertionError(("cmp(%s, %s) "
                                          "shouldn't raise ValueError")
                                            % (v1, v2))
            self.assertEqual(res, wanted,
                             'cmp(%s, %s) should be %s, got %s' %
                             (v1, v2, wanted, res))


class testGetOp(unittest.TestCase):

    def test_equality(self):
        self.assertEqual((operator.eq, '20150314092653'), get_op('20150314092653'))
        self.assertEqual((operator.eq, '30.0b1'), get_op('30.0b1'))
        self.assertEqual((operator.eq, '30.0.1'), get_op('30.0.1'))

    def test_greater_or_equal(self):
        self.assertEqual((operator.ge, '20150314092653'), get_op('>=20150314092653'))
        self.assertEqual((operator.ge, '30.0b1'), get_op('>=30.0b1'))
        self.assertEqual((operator.ge, '30.0.1'), get_op('>=30.0.1'))

    def test_greater_than(self):
        self.assertEqual((operator.gt, '20150314092653'), get_op('>20150314092653'))
        self.assertEqual((operator.gt, '30.0b1'), get_op('>30.0b1'))
        self.assertEqual((operator.gt, '30.0.1'), get_op('>30.0.1'))

    def test_less_than(self):
        self.assertEqual((operator.lt, '20150314092653'), get_op('<20150314092653'))
        self.assertEqual((operator.lt, '30.0b1'), get_op('<30.0b1'))
        self.assertEqual((operator.lt, '30.0.1'), get_op('<30.0.1'))

    def test_lesser_or_equal(self):
        self.assertEqual((operator.le, '20150314092653'), get_op('<=20150314092653'))
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
