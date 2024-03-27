#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ count how many times methods of the Cache class are called """
    key = method.__qualname__

    def wrapper(*args, **kwds):
        """  increments the count for that key every time the method
        is called and returns the value returned
        by the original method. """
        self._redis.INCR(key)
        return method(self, *args, **kwds)
    return wrapper

class Cache:
    """ Declare a cache redis class """
    def __init__(self):
        """
        store an instance of the Redis client
        """
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """  takes a data argument and returns a string """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
                fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ convert the data back to the desired format. """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, kye: str) -> str:
        """ parametrize Cache.get with the correct conversion function. """
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """ parametrize Cache.get with the correct conversion function. """
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
