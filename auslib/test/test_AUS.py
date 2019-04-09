import logging
import unittest

import mock
import pytest

from auslib.AUS import AUS, FAIL, SUCCEED
from auslib.blobs.base import createBlob
from auslib.global_state import dbo

ENTIRE_RANGE = range(0, 100)


def setUpModule():
    # Silence SQLAlchemy-Migrate's debugging logger
    logging.getLogger('migrate').setLevel(logging.CRITICAL)


@pytest.mark.usefixtures("current_db_schema")
class TestAUSThrottlingWithoutFallback(unittest.TestCase):

    def setUp(self):
        dbo.setDb('sqlite:///:memory:')
        self.metadata.create_all(dbo.engine)
        dbo.releases.t.insert().execute(
            name='b', product='b', data_version=1,
            data=createBlob({"name": "b", "extv": "1.0", "schema_version": 1, "platforms": {"a": {"buildID": "1", "locales": {"a": {}}}}}))

        dbo.releases.t.insert().execute(
            name='fallback', product='c', data_version=1,
            data=createBlob({"name": "fallback", "extv": "1.0", "schema_version": 1, "platforms": {"a": {"buildID": "1", "locales": {"a": {}}}}}))

    def tearDown(self):
        dbo.reset()

    def random_aus_test(self, background_rate, force=None, fallback=False):
        mapping = 'b'
        with mock.patch('auslib.db.Rules.getRulesMatchingQuery') as m:
            fallback = fallback and 'fallback'  # convert True to string
            m.return_value = [dict(backgroundRate=background_rate, priority=1, mapping=mapping, update_type='minor',
                                   fallbackMapping=fallback)]

            results = list(ENTIRE_RANGE)
            resultsLength = len(results)

            def se(*args, **kwargs):
                return results.pop()

            aus = AUS()
            aus.rand = mock.Mock(side_effect=se)
            served_mapping = 0
            served_fallback = 0
            tested = 0
            while len(results) > 0:
                updateQuery = dict(
                    channel='foo', force=force, buildTarget='a', buildID='0',
                    locale='a', version='1.0', product='bar'
                )
                r, _ = aus.evaluateRules(updateQuery)
                tested += 1
                if r and r['name'] == mapping:
                    served_mapping += 1
                elif fallback and r['name'] == fallback:
                    served_fallback += 1
                # bail out if we're not asking for any randint's
                if resultsLength == len(results):
                    break
            return (served_mapping, served_fallback, tested)

    def testThrottling100(self):
        (served, _, tested) = self.random_aus_test(background_rate=100)

        self.assertEqual(served, 1)
        self.assertEqual(tested, 1)

    def testThrottling50(self):
        (served, _, tested) = self.random_aus_test(background_rate=50)

        self.assertEqual(served, 50)
        self.assertEqual(tested, 100)

    def testThrottling25(self):
        (served, _, tested) = self.random_aus_test(background_rate=25)

        self.assertEqual(served, 25)
        self.assertEqual(tested, 100)

    def testThrottlingZero(self):
        (served, _, tested) = self.random_aus_test(background_rate=0)
        self.assertEqual(served, 0)
        self.assertEqual(tested, 100)

    def testThrottling25WithForcing(self):
        (served, _, tested) = self.random_aus_test(background_rate=25, force=SUCCEED)

        self.assertEqual(served, 1)
        self.assertEqual(tested, 1)

    def testThrottling25WithForcingFailure(self):
        (served, fallback, tested) = self.random_aus_test(background_rate=25, force=FAIL)

        self.assertEqual(served, 0)
        self.assertEqual(fallback, 0)
        self.assertEqual(tested, 1)

    def testThrottling100WithFallback(self):
        (served_mapping, served_fallback, tested) = self.random_aus_test(background_rate=100,
                                                                         fallback=True)

        self.assertEqual(served_mapping, 1)
        self.assertEqual(served_fallback, 0)
        self.assertEqual(tested, 1)

    def testThrottling50WithFallback(self):
        (served_mapping, served_fallback, tested) = self.random_aus_test(background_rate=50,
                                                                         fallback=True)

        self.assertEqual(served_mapping, 50)
        self.assertEqual(served_fallback, 50)
        self.assertEqual(tested, 100)

    def testThrottling25WithFallback(self):
        (served_mapping, served_fallback, tested) = self.random_aus_test(background_rate=25,
                                                                         fallback=True)

        self.assertEqual(served_mapping, 25)
        self.assertEqual(served_fallback, 75)
        self.assertEqual(tested, 100)

    def testThrottlingZeroWithFallback(self):
        (served_mapping, served_fallback, tested) = self.random_aus_test(background_rate=0,
                                                                         fallback=True)

        self.assertEqual(served_mapping, 0)
        self.assertEqual(served_fallback, 100)
        self.assertEqual(tested, 100)

    def testThrottling25WithForcingAndFallback(self):
        (served_mapping, served_fallback, tested) = self.random_aus_test(background_rate=25,
                                                                         force=SUCCEED,
                                                                         fallback=True)

        self.assertEqual(served_mapping, 1)
        self.assertEqual(served_fallback, 0)
        self.assertEqual(tested, 1)

    def testThrottling25WithForcingFailureAndFallback(self):
        (served, fallback, tested) = self.random_aus_test(background_rate=25, force=FAIL,
                                                          fallback=True)

        self.assertEqual(served, 0)
        self.assertEqual(fallback, 1)
        self.assertEqual(tested, 1)
