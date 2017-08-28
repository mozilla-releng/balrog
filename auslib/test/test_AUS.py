import logging
import mock
import unittest

from auslib.global_state import dbo
from auslib.AUS import AUS, AUSRandom
from auslib.blobs.base import createBlob


def getRange(rand):
    return range(rand.min, rand.max + 1)


def setUpModule():
    # Silence SQLAlchemy-Migrate's debugging logger
    logging.getLogger('migrate').setLevel(logging.CRITICAL)


def RandomAUSTestWithoutFallback(backgroundRate, force, mapping):
    with mock.patch('auslib.db.Rules.getRulesMatchingQuery') as m:
        m.return_value = [dict(backgroundRate=backgroundRate, priority=1, mapping=mapping, update_type='minor',
                               fallbackMapping=None)]

        results = getRange(AUSRandom)
        resultsLength = len(results)

        def se(*args, **kwargs):
            return results.pop()

        aus = AUS(se)
        served = 0
        tested = 0
        while len(results) > 0:
            updateQuery = dict(
                channel='foo', force=force, buildTarget='a', buildID='0',
                locale='a', version='1.0',
            )
            r, _ = aus.evaluateRules(updateQuery)
            tested += 1
            if r:
                served += 1
            # bail out if we're not asking for any randint's
            if resultsLength == len(results):
                break
        return (served, tested)


def RandomAUSTestWithFallback(backgroundRate, force, mapping):
    with mock.patch('auslib.db.Rules.getRulesMatchingQuery') as m:
        m.return_value = [dict(backgroundRate=backgroundRate, priority=1, mapping=mapping, update_type='minor',
                               fallbackMapping='fallback')]

        results = getRange(AUSRandom)
        resultsLength = len(results)

        def se(*args, **kwargs):
            return results.pop()
        aus = AUS(se)

        served_mapping = 0
        served_fallback = 0
        tested = 0
        while len(results) > 0:
            updateQuery = dict(
                channel='foo', force=force, buildTarget='a', buildID='0',
                locale='a', version='1.0',
            )
            r, _ = aus.evaluateRules(updateQuery)
            tested += 1
            if r['name'] == mapping:
                served_mapping += 1
            elif r['name'] == "fallback":
                served_fallback += 1
            # bail out if we're not asking for any randint's
            if resultsLength == len(results):
                break
        return (served_mapping, served_fallback, tested)


class TestAUSThrottlingWithoutFallback(unittest.TestCase):

    def setUp(self):
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        dbo.releases.t.insert().execute(
            name='b', product='b', data_version=1,
            data=createBlob({"name": "b", "extv": "1.0", "schema_version": 1, "platforms": {"a": {"buildID": "1", "locales": {"a": {}}}}}))

        dbo.releases.t.insert().execute(
            name='fallback', product='c', data_version=1,
            data=createBlob({"name": "fallback", "extv": "1.0", "schema_version": 1, "platforms": {"a": {"buildID": "1", "locales": {"a": {}}}}}))

    def tearDown(self):
        dbo.reset()

    def testThrottling100(self):
        (served, tested) = RandomAUSTestWithoutFallback(backgroundRate=100, force=False, mapping='b')

        self.assertEqual(served, 1)
        self.assertEqual(tested, 1)

    def testThrottling50(self):
        (served, tested) = RandomAUSTestWithoutFallback(backgroundRate=50, force=False, mapping='b')

        self.assertEqual(served, 50)
        self.assertEqual(tested, 100)

    def testThrottling25(self):
        (served, tested) = RandomAUSTestWithoutFallback(backgroundRate=25, force=False, mapping='b')

        self.assertEqual(served, 25)
        self.assertEqual(tested, 100)

    def testThrottlingZero(self):
        (served, tested) = RandomAUSTestWithoutFallback(backgroundRate=0, force=False, mapping='b')
        self.assertEqual(served, 0)
        self.assertEqual(tested, 100)

    def testThrottling25WithForcing(self):
        (served, tested) = RandomAUSTestWithoutFallback(backgroundRate=25, force=True, mapping='b')

        self.assertEqual(served, 1)
        self.assertEqual(tested, 1)


    def testThrottling100WithFallback(self):
        (served_mapping, served_fallback, tested) = RandomAUSTestWithFallback(backgroundRate=100,
                                                                              force=False, mapping='b')

        self.assertEqual(served_mapping, 1)
        self.assertEqual(served_fallback, 0)
        self.assertEqual(tested, 1)

    def testThrottling50WithFallback(self):
        (served_mapping, served_fallback, tested) = RandomAUSTestWithFallback(backgroundRate=50,
                                                                              force=False, mapping='b')

        self.assertEqual(served_mapping, 50)
        self.assertEqual(served_fallback, 50)
        self.assertEqual(tested, 100)

    def testThrottling25WithFallback(self):
        (served_mapping, served_fallback, tested) = RandomAUSTestWithFallback(backgroundRate=25,
                                                                              force=False, mapping='b')

        self.assertEqual(served_mapping, 25)
        self.assertEqual(served_fallback, 75)
        self.assertEqual(tested, 100)

    def testThrottlingZeroWithFallback(self):
        (served_mapping, served_fallback, tested) = RandomAUSTestWithFallback(backgroundRate=0,
                                                                              force=False, mapping='b')

        self.assertEqual(served_mapping, 0)
        self.assertEqual(served_fallback, 100)
        self.assertEqual(tested, 100)

    def testThrottling25WithForcingAndFallback(self):
        (served_mapping, served_fallback, tested) = RandomAUSTestWithFallback(backgroundRate=25,
                                                                              force=True, mapping='b')

        self.assertEqual(served_mapping, 1)
        self.assertEqual(served_fallback, 0)
        self.assertEqual(tested, 1)
