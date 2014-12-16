from repoze.lru import ExpiringLRUCache


class MaybeCacher(object):
    """MaybeCacher is a very simple wrapper to work around the fact that we
    have two consumers of the auslib library (admin app, non-admin app) that
    require different caching behaviour. The admin app should never cache
    anything, but the non-admin app should. This class is intended to be
    instantiated as a global object, and then have caches created by consumers
    through calls to make_cache.

    If the cache given to get/put/clear/invalidate doesn't exist, these methods
    are essentially no-ops. In a world where bug 1109295 is fixed, we might
    only need to handle the caching case."""
    def __init__(self):
        self.caches = {}

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

        value = self.caches[name].get(key)
        if not value and callable(value_getter):
            value = value_getter()
            self.put(name, key, value)

        return value

    def put(self, name, key, value):
        if name not in self.caches:
            return

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
