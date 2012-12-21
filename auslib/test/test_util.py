import unittest
from auslib.util import PrinterFriendlyDict, getPagination


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

class TestGetPagination(unittest.TestCase):

    def test_basic_pagination(self):
        page = 1
        total_count = 99
        page_size = 10
        max_range_length = 10

        pagination = getPagination(
            page,
            total_count,
            page_size,
            max_range_length=max_range_length
        )
        self.assertEqual(pagination['range'], range(1, 11))
        self.assertEqual(pagination['current_page'], 1)
        self.assertEqual(pagination['next'], 2)
        self.assertTrue('prev' not in pagination)

        page = 2
        pagination = getPagination(
            page,
            total_count,
            page_size,
            max_range_length=max_range_length
        )
        self.assertEqual(pagination['range'], range(1, 11))
        self.assertEqual(pagination['current_page'], 2)
        self.assertEqual(pagination['next'], 3)
        self.assertEqual(pagination['prev'], 1)

        page = 10
        pagination = getPagination(
            page,
            total_count,
            page_size,
            max_range_length=max_range_length
        )
        self.assertEqual(pagination['range'], range(1, 11))
        self.assertEqual(pagination['current_page'], 10)
        self.assertTrue('next' not in pagination)
        self.assertEqual(pagination['prev'], 9)
