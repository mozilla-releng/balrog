import unittest
from auslib.util import PrinterFriendlyDict


class TestPrinterFriendlyDict(unittest.TestCase):

    def test_keys(self):
        pdf = PrinterFriendlyDict({
            'b': 'B',
            'a': 'A'
        })
        self.assertEqual(pdf.keys(), ['a', 'b'])

    def test_items(self):
        pdf = PrinterFriendlyDict({
            'b': 'B',
            'a': 'A'
        })
        self.assertEqual(
            pdf.items(),
            [('a', u'A'), ('b', u'B')]
        )
