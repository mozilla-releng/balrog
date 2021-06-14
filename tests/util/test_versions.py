import unittest

from auslib.errors import BadDataError
from auslib.util.versions import MozillaVersion


class TestMozillaVersions(unittest.TestCase):
    # This tests the new behaviour we've added for suffixes

    def test_special_version(self):
        version = MozillaVersion("3.6.3plugin1")
        self.assertEqual(version.version, (3, 6, 3))
        self.assertEqual(version.prerelease, ("p", 1))
        self.assertEqual(str(version), "3.6.3p1")

    # This tests the new behaviour for number of sub-versions
    def test_long_version(self):
        version = MozillaVersion("1.5.0.12")
        self.assertEqual(version.version, (1, 5, 12))
        self.assertEqual(version.prerelease, None)
        self.assertEqual(str(version), "1.5.12")

    # The remaining tests are lifted from upstream:
    # http://hg.python.org/cpython/file/v2.7.3/Lib/distutils/tests/test_version.py
    def test_prerelease(self):
        version = MozillaVersion("1.2.3a1")
        self.assertEqual(version.version, (1, 2, 3))
        self.assertEqual(version.prerelease, ("a", 1))
        self.assertEqual(str(version), "1.2.3a1")

        version = MozillaVersion("1.2.0")
        self.assertEqual(str(version), "1.2")

    def test_cmp_strict(self):
        versions = (
            ("1.5.1", "1.5.2b2", -1),
            ("161", "3.10a", BadDataError),
            ("8.02", "8.02", 0),
            ("3.4j", "1996.07.12", BadDataError),
            ("3.2.pl0", "3.1.1.6", BadDataError),
            ("2g6", "11g", BadDataError),
            ("0.9", "2.2", -1),
            ("1.2.1", "1.2", 1),
            ("1.1", "1.2.2", -1),
            ("1.2", "1.1", 1),
            ("1.2.1", "1.2.2", -1),
            ("1.2.2", "1.2", 1),
            ("1.2", "1.2.2", -1),
            ("0.4.0", "0.4", 0),
            ("1.13++", "5.5.kw", BadDataError),
        )

        def cmp(x, y):
            return (x > y) - (x < y)

        for v1, v2, wanted in versions:
            try:
                res = cmp(MozillaVersion(v1), MozillaVersion(v2))
            except BadDataError:
                if wanted is BadDataError:
                    continue
                else:
                    raise AssertionError(("cmp(%s, %s) " "shouldn't raise BadDataError") % (v1, v2))
            self.assertEqual(res, wanted, "cmp(%s, %s) should be %s, got %s" % (v1, v2, wanted, res))

    def test_glob(self):
        version = MozillaVersion("78.8.*")
        self.assertEqual(version.version, (78, 8, 12))
        self.assertEqual(version.version, (78, 8, 0))
        self.assertEqual(MozillaVersion("78.8.1").version, version.version)
        self.assertEqual(MozillaVersion("78.8.0").version, version.version)
        self.assertEqual(version.version, MozillaVersion("78.8.1").version)
        self.assertEqual(version.version, MozillaVersion("78.8.0").version)
        self.assertNotEqual(MozillaVersion("78.80.1").version, version.version)
        self.assertNotEqual(MozillaVersion("78.80.0").version, version.version)
        self.assertNotEqual(version.version, MozillaVersion("78.80.1").version)
        self.assertNotEqual(version.version, MozillaVersion("78.80.0").version)
        self.assertEqual(version.prerelease, None)
        self.assertEqual(str(version), "78.8.*")
        version2 = MozillaVersion("78.*")
        self.assertEqual(version2.version, MozillaVersion("78.0a1").version)
