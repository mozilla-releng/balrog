import time
from copy import deepcopy

import orjson
from repoze.lru import ExpiringLRUCache

from auslib.util.statsd import statsd

uncached_sentinel = object()


class MaybeCacher(object):
    """MaybeCacher is a very simple wrapper to work around the fact that we
    have two consumers of the auslib library (admin app, non-admin app) that
    require cache different things. Most notably, the non-admin app caches
    blobs and blob versions, while the admin app only caches blobs (because
    blob versions can change frequently). This class is intended to be
    instantiated as a global object, and then have caches created by consumers
    through calls to make_cache. Consumers that make changes (ie: the admin
    app) generally also set make_copies to True to get the cache to copy values
    on get/put to avoid the possibility of accidental cache pollution. For
    performance reasons, this should be disabled when not necessary.

    If the cache given to get/put/clear/invalidate doesn't exist, these methods
    are essentially no-ops. In a world where bug 1109295 is fixed, we might
    only need to handle the caching case."""

    def __init__(self):
        self.caches = {}
        self._make_copies = False
        # Ideally, we'd take in the cache class as an argument to this constructor.
        # Due to the way that everything in Balrog is initialized, this doesn't
        # work. We also can't use Flask in here for similar reasons, so we can't
        # pull it from application context. It's for these reasons we need to make
        # this customizable as a property. If that's all that mattered, we
        # could just set the property to a class. However, to support Redis we
        # _also_ need a Redis client passed in. The sanest way to do this is
        # to allow the caller to provide it in a closure, hence we end up
        # making this a callable instead of a simple class.
        self._factory = lambda _, maxsize, timeout, redis_loads=None: ExpiringLRUCache(maxsize, timeout)

    @property
    def factory(self):
        return self._factory

    @factory.setter
    def factory(self, value):
        if not callable(value):
            raise ValueError("factory must be callable!")
        self._factory = value

    @property
    def make_copies(self):
        return self._make_copies

    @make_copies.setter
    def make_copies(self, value):
        if value not in (True, False):
            raise TypeError("make_copies must be True or False")
        self._make_copies = value

    def make_cache(self, name, maxsize, timeout, redis_loads=None):
        if name in self.caches:
            raise Exception()

        self.caches[name] = self.factory(name, maxsize, timeout, redis_loads)

    def reset(self):
        self.caches.clear()

    def get(self, name, key, value_getter=None):
        """Returns the value of the specified key from the named cache.
        If value_getter is provided and no cache is found, or no value is
        found for the key, the return value of value_getter will be returned
        instead."""

        if name not in self.caches:
            if callable(value_getter):
                return value_getter()
            else:
                return None

        value = None
        cached_value = self.caches[name].get(key, uncached_sentinel)
        # If we got something other than a sentinel value, the key was in the cache, and we should return it
        if cached_value != uncached_sentinel:
            value = cached_value
            statsd.incr(f"cache.{name}.hits")
        else:
            # If we know how to look up the value, go do it, cache it, and return it
            if callable(value_getter):
                value = value_getter()
                self.put(name, key, value)
            statsd.incr(f"cache.{name}.misses")

        if self.make_copies:
            return deepcopy(value)
        else:
            return value

    def put(self, name, key, value):
        if name not in self.caches:
            return

        if self.make_copies:
            value = deepcopy(value)
        return self.caches[name].put(key, value)

    def clear(self, name=None):
        if name and name not in self.caches:
            return

        if not name:
            for c in self.caches.values():
                c.clear()
        else:
            self.caches[name].clear()

    def invalidate(self, name, key):
        if name not in self.caches:
            return

        self.caches[name].invalidate(key)


class RedisCache:
    """A thin wrapper around the redis client to expose a similar interface
    as ExpiringLRUCache. Unlike ExpiringLRUCache, redis does not support
    non-trivial objects, so objects are jsonified before storage and parsed
    upon retrieval.

    This cache can be used on its own, but ideally it is only used through a
    TwoLayerCache (see below).
    """

    def __init__(self, redis, name, timeout, redis_loads=None):
        self._name = name
        self._redis = redis
        self._loads = redis_loads or orjson.loads
        # redis and repoze calculate expiry slightly differently; a timeout of
        # 5 seconds with repoze ends up being 6 seconds in redis. this really
        # doesn't matter...but it's better to be consistent than not, and redis'
        # behaviour is slightly confusing, so we make this small improvement
        # since we're wrapping it anyways.
        self._timeout = timeout - 1
        self.lookups = 0
        self.hits = 0
        self.misses = 0

    def fullkey(self, key):
        return f"v2-{self._name}-{key}"

    def get(self, key, default=None):
        self.lookups += 1
        value = self._redis.get(self.fullkey(key))
        if value is not None:
            self.hits += 1
            return self._loads(value)

        self.misses += 1
        return default

    def put(self, key, value):
        self._redis.setex(self.fullkey(key), self._timeout, orjson.dumps(value, option=orjson.OPT_NON_STR_KEYS))

    def clear(self):
        self._redis.delete(*self._redis.keys(f"v2-{self._name}"))

    def invalidate(self, key):
        self._redis.delete(self.fullkey(key))

    def remaining_timeout(self, key):
        absolute_timeout = self._redis.expiretime(self.fullkey(key))
        return absolute_timeout - time.time()


class TwoLayerCache:
    """A cache that wraps both a RedisCache and ExpiringLRUCache. The
    former is treated as authoritative, while the latter is used to minimize
    unnecessary fetches from Redis. This design allows caches to be shared
    across many pods while minimizing the perf impact of having an off-machine
    cache."""

    def __init__(self, redis, name, maxsize, timeout, redis_loads=None):
        self._redis_cache = RedisCache(redis, name, timeout, redis_loads)
        self._lru_cache = ExpiringLRUCache(maxsize, timeout)
        self.lookups = 0
        self.hits = 0
        self.misses = 0

    def get(self, key, default=None):
        self.lookups += 1
        value = self._lru_cache.get(key, default)
        if value == default:
            value = self._redis_cache.get(key, default)
            # ensure the LRU cache timeout matches the one in redis
            # this is important to ensure that when new pods spin up that
            # they will not cache keys for longer than redis
            # this ensures that we don't have to wait for multiple caches
            # to expire to refresh data.
            # in practice there will be a very small difference between the
            # timeouts, because the value we pass to put here is a relative
            # timeout in seconds, which the lru cache recalculates against
            # `time.time()`. this small (probably 1s in most cases) difference
            # is unlikely to be problematic in practice.
            self._lru_cache.put(key, value, self._redis_cache.remaining_timeout(key))
            if value == default:
                self.misses += 1
            else:
                self.hits += 1
        else:
            self.hits += 1

        return value

    def put(self, key, value):
        self._redis_cache.put(key, value)
        self._lru_cache.put(key, value)

    def clear(self):
        self._redis_cache.clear()
        self._lru_cache.clear()

    def invalidate(self, key):
        self._redis_cache.invalidate(key)
        self._lru_cache.invalidate(key)
