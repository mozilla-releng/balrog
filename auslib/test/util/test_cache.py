import mock
import unittest

from auslib.util.cache import MaybeCacher


class TestMaybeCacher(unittest.TestCase):
    def testNoCaching(self):
        with mock.patch("auslib.util.cache.ExpiringLRUCache") as lru:
            cache = MaybeCacher(maxsize=0, timeout=0)
            cache.put("cache1", "foo", "bar")
            # Nothing should be in the cache, because there _isn't_ one.
            self.assertEquals(cache.get("cache1", "foo"), None)
            # And the underlying cache object should not have been touched.
            self.assertFalse(lru.put.called)
            self.assertFalse(lru.get.called)

    def testSimpleCache(self):
        cache = MaybeCacher(maxsize=5, timeout=5)
        cache.put("cache1", "foo", "bar")
        self.assertEquals(cache.get("cache1", "foo"), "bar")

    def testCacheExpired(self):
        cache = MaybeCacher(maxsize=5, timeout=5)
        # In order to avoid tests failing due to clock skew or other
        # issues with system clocks we can mock time.time() and make sure
        # it always returns a difference large enough to force a cache expiry
        with mock.patch("time.time") as t:
            t.return_value = 100
            cache.put("cache1", "foo", "bar")
            t.return_value = 200
            self.assertEquals(cache.get("cache1", "foo"), None)
