import unittest

import mock

from auslib.util.cache import MaybeCacher


class TestMaybeCacher(unittest.TestCase):
    def testNoCaching(self):
        with mock.patch("auslib.util.cache.ExpiringLRUCache") as lru:
            cache = MaybeCacher()
            cache.put("cache1", "foo", "bar")
            # Nothing should be in the cache, because there _isn't_ one.
            self.assertEqual(cache.get("cache1", "foo"), None)
            # And the underlying cache object should not have been touched.
            self.assertFalse(lru.put.called)
            self.assertFalse(lru.get.called)

    def testSimpleCache(self):
        cache = MaybeCacher()
        cache.make_cache("cache1", 5, 5)
        cache.put("cache1", "foo", "bar")
        self.assertEqual(cache.get("cache1", "foo"), "bar")

    def testCacheExpired(self):
        cache = MaybeCacher()
        cache.make_cache("cache1", 5, 5)
        # In order to avoid tests failing due to clock skew or other
        # issues with system clocks we can mock time.time() and make sure
        # it always returns a difference large enough to force a cache expiry
        with mock.patch("time.time") as t:
            t.return_value = 100
            cache.put("cache1", "foo", "bar")
            t.return_value = 200
            self.assertEqual(cache.get("cache1", "foo"), None)

    def testGetDoesntCopyByDefault(self):
        cache = MaybeCacher()
        cache.make_cache("cache1", 5, 5)
        obj = [1, 2, 3]
        # We put this into the cache manually to avoid a false pass from something .put does
        # cache entry format is (pos, value, expiration)
        cache.caches["cache1"].data["foo"] = (0, obj, 9999999999999999)
        cached_obj = cache.get("cache1", "foo")
        self.assertEqual(id(obj), id(cached_obj))

    def testPutDoesntCopyByDefault(self):
        cache = MaybeCacher()
        cache.make_cache("cache1", 5, 5)
        obj = [1, 2, 3]
        # We put this into the cache manually to avoid a false pass from something .get does
        cache.put("cache1", "foo", obj)
        cached_obj = cache.caches["cache1"].data["foo"][1]
        self.assertEqual(id(obj), id(cached_obj))

    def testCopyOnGet(self):
        cache = MaybeCacher()
        cache.make_cache("cache1", 5, 5)
        cache.make_copies = True
        obj = [1, 2, 3]
        # We put this into the cache manually to avoid a false pass from something .put does
        cache.caches["cache1"].data["foo"] = obj
        cached_obj = cache.get("cache1", "foo")
        self.assertNotEqual(id(obj), id(cached_obj))

    def testCopyOnPut(self):
        cache = MaybeCacher()
        cache.make_cache("cache1", 5, 5)
        cache.make_copies = True
        obj = [1, 2, 3]
        # We put this into the cache manually to avoid a false pass from something .get does
        cache.put("cache1", "foo", obj)
        cached_obj = cache.caches["cache1"].data["foo"]
        self.assertNotEqual(id(obj), id(cached_obj))
