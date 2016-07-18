import logging

from auslib.log import configure_logging, JsonLogFormatter
from auslib.test.admin.views.base import ViewTest


class TestJsonLogFormatter(ViewTest):

    def setUp(self):
        self.logger = logging.getLogger()
        self.orig_handlers = self.logger.handlers
        self.logger.handlers = []
        self.level = self.logger.level

    def tearDown(self):
        self.logger.handlers = self.orig_handlers
        self.logger.level = self.level

    def testConfigureLogging(self):
        configure_logging()
        self.assertTrue(isinstance(self.logger.handlers[0].formatter, JsonLogFormatter))
