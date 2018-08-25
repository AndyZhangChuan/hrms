# -*- coding: utf-8 -*-

import hashlib
import threading
from functools import wraps
try:
    import cPickle as pickle
except ImportError:
    import pickle

local_context = threading.local()


def _make_key(func, args, kwargs):
    """
    Serialize the param to hash value.
    :param func:
    :param args:
    :param kwargs:
    :return:
    """
    key = pickle.dumps((func.__name__, args, kwargs))

    return hashlib.md5(key).hexdigest()


def local_cache(name=None):
    """
    Decorate function to cache result in local_context.
    :param name: cache key name.
    """
    def _local_cache(func):
        @wraps(func)
        def _cache(*args, **kwargs):
            local_name = name
            if local_name is None:
                local_name = _make_key(func, args, kwargs)
            data = getattr(local_context, local_name, None)
            if data is None:
                data = func(*args, **kwargs)
                setattr(local_context, local_name, data)

            return data

        return _cache

    return _local_cache
