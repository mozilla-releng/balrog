import os
import unittest
from tempfile import mkstemp

from auslib.config import AUSConfig


class TestAUSConfig(unittest.TestCase):
    def setUp(self):
        self.config_fd, self.config_file = mkstemp()
        with open(self.config_file, "w+") as f:
            f.write(
                """
[database]
;Database to be used by AUS applications, in URI format
dburi=sqlite:///:memory:

[logging]
;Where to put the application log. No rotation is done on this file.
logfile=/foo/bar/baz

[site-specific]
domain_allowlist=a.com:c|d, boring.com:e
"""
            )
        self.cfg = AUSConfig(self.config_file)

    def tearDown(self):
        os.close(self.config_fd)
        os.remove(self.config_file)

    def testAllowlistDomains(self):
        expected = {"a.com": ("c", "d"), "boring.com": ("e",)}
        self.assertEqual(expected, self.cfg.getDomainAllowlist())
