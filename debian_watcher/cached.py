
class Cached(object):
    _cache_enabled = False
    _cache = {}

    def _cache_result(func):
        def wrapper(self, *args, **kwargs):
            key = (func.__name__, args, *list(kwargs.keys()))
            if self._cache.get(key):
                return self._cache.get(key)
            result = func(self, *args, **kwargs)
            if self._cache_enabled:
                self._cache[key] = result
            return result
        return wrapper
