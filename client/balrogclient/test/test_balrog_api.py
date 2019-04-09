try:
    # Python 2.6 backport with assertDictEqual()
    import unittest2 as unittest
except ImportError:
    import unittest

from balrogclient import is_csrf_token_expired


class TestCsrfTokenExpiry(unittest.TestCase):
    """
    is_csrf_token_expired expects a token
    of the form %Y%m%d%H%M%S##foo
    """

    def _generate_date_string(self, days_offset=0):
        from datetime import datetime, timedelta

        return (datetime.now() + timedelta(days=days_offset)).strftime("%Y%m%d%H%M%S")

    def test_valid_csrf_token_has_not_expired(self):
        tomorrow = self._generate_date_string(days_offset=1)
        self.assertFalse(is_csrf_token_expired(tomorrow))

    def test_valid_csrf_token_has_expired(self):
        yesterday = self._generate_date_string(days_offset=-1)
        self.assertTrue(is_csrf_token_expired(yesterday))

    def test_invalid_csrf_token(self):
        pass
