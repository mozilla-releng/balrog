import unittest


from .. import changes


class TestIsReady(unittest.TestCase):
    def testUptakeReady(self):
        change = {
            "telemetry_uptake": 5000,
            "when": None,
            "sc_id": 1,
        }
        self.assertTrue(changes.is_ready(change, current_uptake=6000))

    def testUptakeReadyExact(self):
        change = {
            "telemetry_uptake": 5000,
            "when": None,
            "sc_id": 1,
        }
        self.assertTrue(changes.is_ready(change, current_uptake=5000))

    def testUptakeAlmostReady(self):
        change = {
            "telemetry_uptake": 5000,
            "when": None,
            "sc_id": 1,
        }
        self.assertFalse(changes.is_ready(change, current_uptake=4999))

    def testUptakeNotReady(self):
        change = {
            "telemetry_uptake": 5000,
            "when": None,
            "sc_id": 1,
        }
        self.assertFalse(changes.is_ready(change, current_uptake=0))

    def testTimeBasedReady(self):
        change = {
            "telemetry_uptake": None,
            "when": 300,
            "sc_id": 1,
        }
        self.assertTrue(changes.is_ready(change, now=500))

    def testTimeBasedReadyExact(self):
        change = {
            "telemetry_uptake": None,
            "when": 300,
            "sc_id": 1,
        }
        self.assertTrue(changes.is_ready(change, now=300))

    def testTimeBasedNotReady(self):
        change = {
            "telemetry_uptake": None,
            "when": 300,
            "sc_id": 1,
        }
        self.assertFalse(changes.is_ready(change, now=200))

    def testTimeBasedAlmostReady(self):
        change = {
            "telemetry_uptake": None,
            "when": 499,
            "sc_id": 1,
        }
        self.assertFalse(changes.is_ready(change, now=498))

#    def testUnknownChangeType(self):
#    def testCantDetectType(self):
