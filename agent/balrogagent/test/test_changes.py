import unittest


from .. import changes


class TestIsReady(unittest.TestCase):
    def testUptakeReady(self):
        change = {
            "telemetry_uptake": 5000,
            "when": None,
            "sc_id": 1,
        }
        self.assertTrue(changes.telemetry_is_ready(change, 6000))

    def testUptakeReadyExact(self):
        change = {
            "telemetry_uptake": 5000,
            "when": None,
            "sc_id": 1,
        }
        self.assertTrue(changes.telemetry_is_ready(change, 5000))

    def testUptakeAlmostReady(self):
        change = {
            "telemetry_uptake": 5000,
            "when": None,
            "sc_id": 1,
        }
        self.assertFalse(changes.telemetry_is_ready(change, 4999))

    def testUptakeNotReady(self):
        change = {
            "telemetry_uptake": 5000,
            "when": None,
            "sc_id": 1,
        }
        self.assertFalse(changes.telemetry_is_ready(change, 0))

    def testTimeBasedReady(self):
        change = {
            "telemetry_uptake": None,
            "when": 300,
            "sc_id": 1,
        }
        self.assertTrue(changes.time_is_ready(change, 500))

    def testTimeBasedReadyExact(self):
        change = {
            "telemetry_uptake": None,
            "when": 300,
            "sc_id": 1,
        }
        self.assertTrue(changes.time_is_ready(change, 300))

    def testTimeBasedNotReady(self):
        change = {
            "telemetry_uptake": None,
            "when": 300,
            "sc_id": 1,
        }
        self.assertFalse(changes.time_is_ready(change, 200))

    def testTimeBasedAlmostReady(self):
        change = {
            "telemetry_uptake": None,
            "when": 499,
            "sc_id": 1,
        }
        self.assertFalse(changes.time_is_ready(change, 498))

#    def testUnknownChangeType(self):
#    def testCantDetectType(self):
