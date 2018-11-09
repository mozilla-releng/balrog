import mock
import unittest
import sys

from auslib.util.cache import MaybeCacher


class TestMaybeCacher(unittest.TestCase):

    def testNoCaching(self):
        with mock.patch("auslib.util.cache.LRUCache") as lru:
            cache = MaybeCacher()
            cache.put("cache1", "foo", "bar")
            # Nothing should be in the cache, because there _isn't_ one.
            self.assertEquals(cache.get("cache1", "foo"), None)
            # And the underlying cache object should not have been touched.
            self.assertFalse(lru.put.called)
            self.assertFalse(lru.get.called)

    def testSimpleCache(self):
        cache = MaybeCacher()
        cache.make_cache("cache1", 5, 5)
        cache.put("cache1", "foo", "bar")
        self.assertEquals(cache.get("cache1", "foo"), "bar")

    def testGetDoesntCopyByDefault(self):
        cache = MaybeCacher()
        cache.make_cache("cache1", 5, 5)
        obj = [1, 2, 3]
        # We put this into the cache manually to avoid a false pass from something .put does
        # cache entry format is (pos, value, expiration)
        cache.caches["cache1"].put("foo", obj)
        cached_obj = cache.get("cache1", "foo")
        self.assertEquals(id(obj), id(cached_obj))

    def testPutDoesntCopyByDefault(self):
        cache = MaybeCacher()
        cache.make_cache("cache1", 5, 5)
        obj = [1, 2, 3]
        cache.put("cache1", "foo", obj)
        cached_obj = cache.caches["cache1"].get("foo")
        self.assertEquals(id(obj), id(cached_obj))

    def testCopyOnGet(self):
        cache = MaybeCacher()
        cache.make_cache("cache1", 5, 5)
        cache.make_copies = True
        obj = [1, 2, 3]
        cache.caches["cache1"].put("foo", obj)
        cached_obj = cache.get("cache1", "foo")
        self.assertNotEquals(id(obj), id(cached_obj))

    def testCopyOnPut(self):
        cache = MaybeCacher()
        cache.make_cache("cache1", 5, 5)
        cache.make_copies = True
        obj = [1, 2, 3]
        cache.put("cache1", "foo", obj)
        cached_obj = cache.caches["cache1"].get("foo")
        self.assertNotEquals(id(obj), id(cached_obj))

    def testMemoization(self):
        functools = 'functools' if sys.version_info[0] >= 3 else 'functools32'
        with mock.patch(functools + ".lru_cache") as lru:
            cache = MaybeCacher()
            cache.make_cache("cache1", 5, 5)
            cache.put("cache1", "foo", ['foobar'])
            self.assertTrue(lru.called)
