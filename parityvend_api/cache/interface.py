import abc


class CacheInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __contains__(self, key):
        raise NotImplementedError

    @abc.abstractmethod
    def __setitem__(self, key, value):
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, key):
        raise NotImplementedError

    @abc.abstractmethod
    def __delitem__(self, key):
        raise NotImplementedError
