import unittest
from unittest import mock


from .. import cmd


class TestIsReady(unittest.TestCase):
    def testUptakeReady(self):
        change = {
            "telemetry_uptake": 5000,
            "when": None,
        }
        self.assertTrue(cmd.is_ready(change, 6000))

    def testUptakeReadyExact(self):
        change = {
            "telemetry_uptake": 5000,
            "when": None,
        }
        self.assertTrue(cmd.is_ready(change, 5000))

    def testUptakeAlmostReady(self):
        change = {
            "telemetry_uptake": 5000,
            "when": None,
        }
        self.assertFalse(cmd.is_ready(change, 4999))

    def testUptakeNotReady(self):
        change = {
            "telemetry_uptake": 5000,
            "when": None,
        }
        self.assertFalse(cmd.is_ready(change, 0))

    def testTimeBasedReady(self):
        change = {
            "telemetry_uptake": None,
            "when": 300,
        }
        with mock.patch("time.time") as t:
            t.return_value = 500
            self.assertTrue(cmd.is_ready(change))

    def testTimeBasedReadyExact(self):
        change = {
            "telemetry_uptake": None,
            "when": 300,
        }
        with mock.patch("time.time") as t:
            t.return_value = 300
            self.assertTrue(cmd.is_ready(change))

    def testTimeBasedNotReady(self):
        change = {
            "telemetry_uptake": None,
            "when": 300,
        }
        with mock.patch("time.time") as t:
            t.return_value = 200
            self.assertFalse(cmd.is_ready(change))

    def testTimeBasedAlmostReady(self):
        change = {
            "telemetry_uptake": None,
            "when": 499,
        }
        with mock.patch("time.time") as t:
            t.return_value = 498
            self.assertFalse(cmd.is_ready(change))

#    def testUnknownChangeType(self):
#    def testCantDetectType(self):
