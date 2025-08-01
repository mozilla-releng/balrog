from copy import deepcopy

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

    @property
    def make_copies(self):
        return self._make_copies

    @make_copies.setter
    def make_copies(self, value):
        if value not in (True, False):
            raise TypeError("make_copies must be True or False")
        self._make_copies = value

    def make_cache(self, name, maxsize, timeout):
        if name in self.caches:
            raise Exception()
        self.caches[name] = ExpiringLRUCache(maxsize, timeout)

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
