import cachetools

from .interface import CacheInterface


class DefaultCache(CacheInterface):
    def __init__(self, **cache_options):
        self.cache = cachetools.TTLCache(**cache_options)

    def __contains__(self, key):
        return self.cache.__contains__(key)

    def __setitem__(self, key, value):
        return self.cache.__setitem__(key, value)

    def __getitem__(self, key):
        return self.cache.__getitem__(key)

    def __delitem__(self, key):
        return self.cache.__delitem__(key)
