import logging
import unittest

import mock
import pytest

from auslib.AUS import AUS, FORCE_FALLBACK_MAPPING, FORCE_MAIN_MAPPING, isForbiddenUrl
from auslib.blobs.base import createBlob
from auslib.global_state import dbo

ENTIRE_RANGE = range(0, 100)


def setUpModule():
    # Silence SQLAlchemy-Migrate's debugging logger
    logging.getLogger("migrate").setLevel(logging.CRITICAL)


@pytest.mark.usefixtures("current_db_schema")
class TestAUSThrottlingWithoutFallback(unittest.TestCase):
    def setUp(self):
        dbo.setDb("sqlite:///:memory:")
        self.metadata.create_all(dbo.engine)
        dbo.releases.t.insert().execute(
            name="b",
            product="b",
            data_version=1,
            data=createBlob({"name": "b", "extv": "2.0", "schema_version": 1, "platforms": {"a": {"buildID": "1", "locales": {"a": {}}}}}),
        )

        dbo.releases.t.insert().execute(
            name="fallback",
            product="c",
            data_version=1,
            data=createBlob({"name": "fallback", "extv": "2.0", "schema_version": 1, "platforms": {"a": {"buildID": "1", "locales": {"a": {}}}}}),
        )

        dbo.releases.t.insert().execute(
            name="pinned",
            product="c",
            data_version=1,
            data=createBlob({"name": "pinned", "extv": "1.0", "schema_version": 1, "platforms": {"a": {"buildID": "1", "locales": {"a": {}}}}}),
        )

        dbo.pinnable_releases.t.insert().execute(
            product="bar",
            version="1.",
            channel="foo",
            mapping="pinned",
            data_version=1,
        )

    def tearDown(self):
        dbo.reset()

    def random_aus_test(self, background_rate, force=None, fallback=False, pin=False):
        mapping = "b"
        pin_mapping = "pinned"
        with mock.patch("auslib.db.Rules.getRulesMatchingQuery") as m:
            fallback = fallback and "fallback"  # convert True to string
            m.return_value = [
                dict(rule_id=1, data_version=1, backgroundRate=background_rate, priority=1, mapping=mapping, update_type="minor", fallbackMapping=fallback)
            ]

            results = list(ENTIRE_RANGE)
            resultsLength = len(results)

            def se(*args, **kwargs):
                return results.pop()

            aus = AUS()
            aus.rand = mock.Mock(side_effect=se)
            served_mapping = 0
            served_fallback = 0
            served_pinned = 0
            tested = 0
            while len(results) > 0:
                updateQuery = dict(channel="foo", force=force, buildTarget="a", buildID="0", locale="a", version="1.0", product="bar")
                if pin:
                    updateQuery["pin"] = "1."
                r, _, _ = aus.evaluateRules(updateQuery)
                tested += 1
                if r:
                    if r["name"] == mapping:
                        served_mapping += 1
                    elif fallback and r["name"] == fallback:
                        served_fallback += 1
                    elif r["name"] == pin_mapping:
                        served_pinned += 1
                # bail out if we're not asking for any randint's
                if resultsLength == len(results):
                    break
            return (served_mapping, served_fallback, served_pinned, tested)

    def testThrottling100(self):
        (served, _, _, tested) = self.random_aus_test(background_rate=100)

        self.assertEqual(served, 1)
        self.assertEqual(tested, 1)

    def testThrottling50(self):
        (served, _, _, tested) = self.random_aus_test(background_rate=50)

        self.assertEqual(served, 50)
        self.assertEqual(tested, 100)

    def testThrottling25(self):
        (served, _, _, tested) = self.random_aus_test(background_rate=25)

        self.assertEqual(served, 25)
        self.assertEqual(tested, 100)

    def testThrottlingZero(self):
        (served, _, _, tested) = self.random_aus_test(background_rate=0)
        self.assertEqual(served, 0)
        self.assertEqual(tested, 100)

    def testThrottling25WithForcing(self):
        (served, _, _, tested) = self.random_aus_test(background_rate=25, force=FORCE_MAIN_MAPPING)

        self.assertEqual(served, 1)
        self.assertEqual(tested, 1)

    def testThrottling25WithForcingFailure(self):
        (served, fallback, _, tested) = self.random_aus_test(background_rate=25, force=FORCE_FALLBACK_MAPPING)

        self.assertEqual(served, 0)
        self.assertEqual(fallback, 0)
        self.assertEqual(tested, 1)

    def testThrottling100WithFallback(self):
        (served_mapping, served_fallback, _, tested) = self.random_aus_test(background_rate=100, fallback=True)

        self.assertEqual(served_mapping, 1)
        self.assertEqual(served_fallback, 0)
        self.assertEqual(tested, 1)

    def testThrottling50WithFallback(self):
        (served_mapping, served_fallback, _, tested) = self.random_aus_test(background_rate=50, fallback=True)

        self.assertEqual(served_mapping, 50)
        self.assertEqual(served_fallback, 50)
        self.assertEqual(tested, 100)

    def testThrottling25WithFallback(self):
        (served_mapping, served_fallback, _, tested) = self.random_aus_test(background_rate=25, fallback=True)

        self.assertEqual(served_mapping, 25)
        self.assertEqual(served_fallback, 75)
        self.assertEqual(tested, 100)

    def testThrottlingZeroWithFallback(self):
        (served_mapping, served_fallback, _, tested) = self.random_aus_test(background_rate=0, fallback=True)

        self.assertEqual(served_mapping, 0)
        self.assertEqual(served_fallback, 100)
        self.assertEqual(tested, 100)

    def testThrottling25WithForcingAndFallback(self):
        (served_mapping, served_fallback, _, tested) = self.random_aus_test(background_rate=25, force=FORCE_MAIN_MAPPING, fallback=True)

        self.assertEqual(served_mapping, 1)
        self.assertEqual(served_fallback, 0)
        self.assertEqual(tested, 1)

    def testThrottling25WithForcingFailureAndFallback(self):
        (served, fallback, _, tested) = self.random_aus_test(background_rate=25, force=FORCE_FALLBACK_MAPPING, fallback=True)

        self.assertEqual(served, 0)
        self.assertEqual(fallback, 1)
        self.assertEqual(tested, 1)

    def testPinningWithThrottling100(self):
        (_, _, served_pinned, tested) = self.random_aus_test(background_rate=100, pin=True)

        self.assertEqual(served_pinned, 1)
        self.assertEqual(tested, 1)

    def testPinningWithThrottling25WithForcing(self):
        (_, _, served_pinned, tested) = self.random_aus_test(background_rate=25, force=FORCE_MAIN_MAPPING, pin=True)

        self.assertEqual(served_pinned, 1)
        self.assertEqual(tested, 1)

    def testPinningWithThrottling100WithFallback(self):
        (_, _, served_pinned, tested) = self.random_aus_test(background_rate=100, fallback=True, pin=True)

        self.assertEqual(served_pinned, 1)
        self.assertEqual(tested, 1)

    def testPinningWithThrottling25WithFallback(self):
        (_, _, served_pinned, tested) = self.random_aus_test(background_rate=25, fallback=True, pin=True)

        self.assertEqual(served_pinned, 100)
        self.assertEqual(tested, 100)

    def testPinningWithThrottlingZeroWithFallback(self):
        (_, _, served_pinned, tested) = self.random_aus_test(background_rate=0, fallback=True, pin=True)

        self.assertEqual(served_pinned, 100)
        self.assertEqual(tested, 100)

    def testPinningWithThrottling25WithForcingAndFallback(self):
        (_, _, served_pinned, tested) = self.random_aus_test(background_rate=25, force=FORCE_MAIN_MAPPING, fallback=True, pin=True)

        self.assertEqual(served_pinned, 1)
        self.assertEqual(tested, 1)

    def testPinningWithThrottling25WithForcingFailureAndFallback(self):
        (_, _, served_pinned, tested) = self.random_aus_test(background_rate=25, force=FORCE_FALLBACK_MAPPING, fallback=True, pin=True)

        self.assertEqual(served_pinned, 1)
        self.assertEqual(tested, 1)


class TestForbiddenUrl(unittest.TestCase):
    def test_urls(self):
        allowlist = {
            "ignore.net": ("c", "d"),
            "b.org": ("e", "f"),
            "a.com": {
                "/path/[\\w\\.]+/[\\w\\.]+\\.bin": (
                    "a",
                    "b",
                ),
            },
        }

        # Unmatched domain
        self.assertTrue(isForbiddenUrl("https://b.com/path/foo/bar.bin", "c", allowlist))

        # Matches domain without path but not product
        self.assertTrue(isForbiddenUrl("https://b.org/anything/I/want.exe", "d", allowlist))

        # Matches domain and product without path
        self.assertFalse(isForbiddenUrl("https://b.org/anything/I/want.exe", "e", allowlist))

        # Matches domain but path doesn't match regex
        self.assertTrue(isForbiddenUrl("https://a.com/not/allowed.bin", "a", allowlist))
        self.assertTrue(isForbiddenUrl("https://a.com/path/not/allowed+.bin", "b", allowlist))

        # Matches domain and path, but not product
        self.assertTrue(isForbiddenUrl("https://a.com/path/foo/bar.bin", "c", allowlist))

        # Matches domain, path and product
        self.assertFalse(isForbiddenUrl("https://a.com/path/foo/bar.bin", "b", allowlist))
