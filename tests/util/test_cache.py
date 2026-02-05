import unittest

import mock
import orjson

from auslib.blobs.base import Blob, createBlob
from auslib.util.cache import MaybeCacher, RedisCache, TwoLayerCache


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


def test_two_layer_cache_get_with_none_default(fake_redis):
    """Test that get() works correctly when default is None"""
    cache = TwoLayerCache(fake_redis, "test", 5, 30)

    result = cache.get("missing_key")  # No default provided

    assert result is None
    assert cache.lookups == 1
    assert cache.misses == 1
    assert cache.hits == 0
    # Check underlying cache statistics
    assert cache._lru_cache.lookups == 1
    assert cache._lru_cache.misses == 1
    assert cache._lru_cache.hits == 0
    assert cache._redis_cache.lookups == 1
    assert cache._redis_cache.misses == 1
    assert cache._redis_cache.hits == 0


def test_two_layer_cache_redis_hit_populates_lru(fake_redis):
    """Test that Redis hits populate the LRU cache for subsequent access"""
    cache = TwoLayerCache(fake_redis, "test", 5, 30)

    # Pre-populate Redis with a value
    fake_redis.setex("v2-test-test_key", 30, orjson.dumps("redis_value"))

    # First access should hit Redis
    result1 = cache.get("test_key", "default")
    assert result1 == "redis_value"
    assert cache.lookups == 1
    assert cache.hits == 1
    # Check underlying cache statistics after first access
    assert cache._lru_cache.lookups == 1
    assert cache._lru_cache.misses == 1
    assert cache._lru_cache.hits == 0
    assert cache._redis_cache.lookups == 1
    assert cache._redis_cache.hits == 1
    assert cache._redis_cache.misses == 0

    # Second access should hit LRU cache (not Redis again)
    result2 = cache.get("test_key", "default")
    assert result2 == "redis_value"
    assert cache.lookups == 2
    assert cache.hits == 2
    # Check underlying cache statistics after second access
    assert cache._lru_cache.lookups == 2
    assert cache._lru_cache.misses == 1
    assert cache._lru_cache.hits == 1
    assert cache._redis_cache.lookups == 1  # Redis not accessed again
    assert cache._redis_cache.hits == 1
    assert cache._redis_cache.misses == 0


def test_two_layer_cache_hit_fetches_from_in_memory(fake_redis):
    cache = TwoLayerCache(fake_redis, "test", 5, 30)

    # Put a value in the cache
    cache.put("test_key", "test_value")

    # Get the value - should come from in-memory cache
    result = cache.get("test_key", "default_value")

    assert result == "test_value"
    assert cache.lookups == 1
    assert cache.hits == 1
    assert cache.misses == 0
    # Check underlying cache statistics
    assert cache._lru_cache.lookups == 1
    assert cache._lru_cache.hits == 1
    assert cache._lru_cache.misses == 0
    assert cache._redis_cache.lookups == 0  # Redis not accessed
    assert cache._redis_cache.hits == 0
    assert cache._redis_cache.misses == 0


def test_two_layer_cache_expired_fetches_from_redis(fake_redis):
    cache = TwoLayerCache(fake_redis, "test", 5, 30)

    # Put a value in the cache first
    cache.put("test_key", "lru_value")

    # Clear the LRU cache to simulate expiration
    cache._lru_cache.clear()

    # Put a different value in Redis to test that it's fetched when LRU is empty
    fake_redis.setex("v2-test-test_key", 30, orjson.dumps("redis_value"))

    result = cache.get("test_key", "default_value")

    assert result == "redis_value"
    assert cache.lookups == 1
    assert cache.hits == 1  # Redis hit
    assert cache.misses == 0
    # Check underlying cache statistics
    assert cache._lru_cache.lookups == 1
    assert cache._lru_cache.misses == 1  # LRU miss due to clear
    assert cache._lru_cache.hits == 0
    assert cache._redis_cache.lookups == 1
    assert cache._redis_cache.hits == 1  # Redis hit
    assert cache._redis_cache.misses == 0

    # Ensure the next fetch comes from the LRU cache and contains the correct
    # value.
    result = cache.get("test_key", "default_value")

    assert result == "redis_value"
    assert cache.lookups == 2
    assert cache.hits == 2
    assert cache.misses == 0
    # Check underlying cache statistics
    assert cache._lru_cache.lookups == 2
    assert cache._lru_cache.misses == 1
    assert cache._lru_cache.hits == 1
    assert cache._redis_cache.lookups == 1
    assert cache._redis_cache.hits == 1
    assert cache._redis_cache.misses == 0


def test_two_layer_cache_both_expired_at_same_time(fake_redis):
    cache = TwoLayerCache(fake_redis, "test", 5, 30)

    # Simulate both caches being expired
    with mock.patch("time.time") as time_mock:
        time_mock.return_value = 100
        cache.put("test_key", "original_value")
        time_mock.return_value = 200  # Much later, both should be expired

        result = cache.get("test_key", "default_value")

        assert result == "default_value"
        assert cache.lookups == 1
        assert cache.hits == 0
        assert cache.misses == 1
        # Check underlying cache statistics
        assert cache._lru_cache.lookups == 1
        assert cache._lru_cache.misses == 1
        assert cache._lru_cache.hits == 0
        assert cache._redis_cache.lookups == 1
        assert cache._redis_cache.misses == 1
        assert cache._redis_cache.hits == 0


def test_two_layer_cache_in_memory_expires_at_same_time_after_reset(fake_redis):
    """Test that LRU cache expiration time matches Redis when repopulated"""
    cache = TwoLayerCache(fake_redis, "test", 5, 30)

    with mock.patch("time.time") as time_mock:
        # Start at time 100
        time_mock.return_value = 100

        # Put value in both caches at time 100
        cache.put("test_key", "original_value")

        # Verify initial state - LRU hit, no Redis access needed
        result1 = cache.get("test_key", "default_value")
        assert result1 == "original_value"
        assert cache.lookups == 1
        assert cache.hits == 1
        assert cache.misses == 0
        # Check underlying cache statistics after initial get
        assert cache._lru_cache.lookups == 1
        assert cache._lru_cache.hits == 1
        assert cache._lru_cache.misses == 0
        assert cache._redis_cache.lookups == 0  # Redis not accessed
        assert cache._redis_cache.hits == 0
        assert cache._redis_cache.misses == 0

        # Remove the key from the lru cache to simulate it being reset/evicted
        # or eg: a new pod spinning up that has nothing cached.
        cache._lru_cache.invalidate("test_key")

        # Move to time 110 (still within 30-second window from time 100)
        time_mock.return_value = 110

        # Get should fetch from Redis and repopulate LRU with same expiration
        result2 = cache.get("test_key", "default_value")
        assert result2 == "original_value"
        assert cache.lookups == 2
        assert cache.hits == 2  # Still cached in redis
        assert cache.misses == 0
        # Check underlying cache statistics after Redis fetch
        assert cache._lru_cache.lookups == 2
        assert cache._lru_cache.hits == 1
        assert cache._lru_cache.misses == 1  # Missed due to manual invalidation
        assert cache._redis_cache.lookups == 1
        assert cache._redis_cache.hits == 1  # Redis hit
        assert cache._redis_cache.misses == 0

        # Move to a later time, but still prior to expiration
        time_mock.return_value = 120
        result3 = cache.get("test_key", "default_value")
        assert result3 == "original_value"
        assert cache.lookups == 3
        assert cache.hits == 3
        assert cache.misses == 0
        # Check underlying cache statistics after expiration
        assert cache._lru_cache.lookups == 3
        assert cache._lru_cache.hits == 2  # Recached after previous .get()
        assert cache._lru_cache.misses == 1
        assert cache._redis_cache.lookups == 1
        assert cache._redis_cache.hits == 1
        assert cache._redis_cache.misses == 0

        # Move to time 130 (30 seconds from initial put at time 100, should be expired)
        # but only 20 seconds from LRU repopulation at time 110
        time_mock.return_value = 130

        result3 = cache.get("test_key", "default_value")
        assert result3 == "default_value"
        assert cache.lookups == 4
        assert cache.hits == 3
        assert cache.misses == 1
        # Check underlying cache statistics after expiration
        assert cache._lru_cache.lookups == 4
        assert cache._lru_cache.hits == 2
        assert cache._lru_cache.misses == 2  # Expired
        assert cache._redis_cache.lookups == 2
        assert cache._redis_cache.hits == 1
        assert cache._redis_cache.misses == 1  # Expired


def test_redis_cache_default_loads(fake_redis):
    cache = RedisCache(fake_redis, "test", 30, None)

    cache.put("key", {"foo": "bar", "n": 42})
    result = cache.get("key")
    assert result == {"foo": "bar", "n": 42}


def test_redis_cache_custom_loads(fake_redis, firefox_100_0_build1):
    def load_blob(s):
        data = orjson.loads(s)
        data["blob"] = createBlob(data["blob"])
        return data

    cache = RedisCache(fake_redis, "test", 30, load_blob)

    blob = createBlob(firefox_100_0_build1)
    cache.put("testblob", {"data_version": 42, "blob": blob})
    result = cache.get("testblob")
    assert result["data_version"] == 42
    assert isinstance(result["blob"], Blob)
    assert result["blob"] == blob
