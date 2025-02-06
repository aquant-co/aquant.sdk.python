import functools
import weakref


def weak_lru(maxsize=128, typed=False):
    """LRU Cache decorator that holds a weak reference to self."""

    def decorator(func):
        @functools.lru_cache(maxsize=maxsize, typed=typed)
        def _cached(_self, *args, **kwargs):
            return func(_self(), *args, **kwargs)

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            return _cached(weakref.ref(self), *args, **kwargs)

        return wrapper

    return decorator
