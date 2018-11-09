import sys
from copy import deepcopy
from collections import namedtuple

if sys.version_info[0] >= 3:
    import functools
else:
    import functools32 as functools


class _Equals:
    def __init__(self, obj):
        self.obj = obj

    def __eq__(self, other):
        # if current value is truthy
        if self.obj is not None:
            return True
        return False

    def __hash__(self):
        return 0


def lru_cache(*args, **kwargs):
    lru_decorator = functools.lru_cache(*args, **kwargs)

    def decorator(f):
        @lru_decorator
        def _memoize(key, ret=None):
            if ret is not None:
                ret = ret.obj
            return f(key, ret)

        @functools.wraps(f)
        def function(key, ret=None):
            value, info = _Equals(ret), _memoize.cache_info()._asdict()
            if ret:
                info['hits'] -= 1
            return _memoize(key, value), info

        return function

    return decorator


class LRUCache:
    def __init__(self, maxsize=None):
        self.__maxsize = maxsize
        self.cache = self._cache()

    @property
    def info(self):
        return namedtuple(
            'CacheInfo', self._info.keys())(**self._info)

    def _cache(self):
        @lru_cache(maxsize=self.__maxsize)
        def function(key, ret=None):
            if callable(ret):
                return ret()
            return ret
        return function

    def put(self, key, value):
        _, self._info = self.cache(key, value)

    def get(self, key):
        value, self._info = self.cache(key)
        return value


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
        self.caches[name] = LRUCache(maxsize)

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
        # "if value is None" is important here (instead of "if not value")
        # because it allows us to cache results of potentially expensive
        # calls that may end up returning nothing.
        if value is None and callable(value_getter):
            value = value_getter()
            self.put(name, key, value)

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
