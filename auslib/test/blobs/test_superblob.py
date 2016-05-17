import unittest

from auslib.blobs.superblob import SuperBlob
from auslib.test.test_db import MemoryDatabaseMixin


class TestSchema1Blob(unittest.TestCase, MemoryDatabaseMixin):
    maxDiff = 2000

    def setUp(self):
        self.superblob = SuperBlob()
        self.superblob.loadJSON("""
{
    "name": "fake",
    "schema_version": 1000,
    "products": [
        "c",
        "d"
    ]
}
""")

    def testGetResponseProducts(self):
        products = self.superblob.getResponseProducts()
        self.assertEqual(products, ['c', 'd'])
