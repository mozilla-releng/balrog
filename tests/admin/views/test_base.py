import logging

from auslib.log import JsonLogFormatter, configure_logging

from .base import ViewTest


class TestJsonLogFormatter(ViewTest):
    def setUp(self):
        self.logger = logging.getLogger()
        self.orig_handlers = self.logger.handlers
        self.logger.handlers = []
        self.level = self.logger.level
        super(TestJsonLogFormatter, self).setUp()

    def tearDown(self):
        self.logger.handlers = self.orig_handlers
        self.logger.level = self.level

    def testConfigureLogging(self):
        configure_logging()
        self.assertTrue(isinstance(self.logger.handlers[0].formatter, JsonLogFormatter))

    def testStrictTransportSecurityIsSet(self):
        ret = self.client.get("/rules")
        self.assertEqual(ret.headers.get("Strict-Transport-Security"), "max-age=31536000;")

    def testContentSecurityPolicyIsSet(self):
        ret = self.client.get("/rules")
        self.assertEqual(ret.headers.get("Content-Security-Policy"), "default-src 'none'; frame-ancestors 'none'")

    def testCORSIsSet(self):
        ret = self.client.get("/rules")
        self.assertEqual(ret.headers.get("Access-Control-Allow-Headers"), "Authorization, Content-Type")
        self.assertEqual(ret.headers.get("Access-Control-Allow-Origin"), "*")
        self.assertEqual(ret.headers.get("Access-Control-Allow-Methods"), "OPTIONS, GET, POST, PUT, DELETE")
