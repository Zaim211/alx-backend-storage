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

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """  increments the count for that key every time the method
        is called and returns the value returned
        by the original method. """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """ store the history of inputs and outputs for a particular function """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrap decorated function """
        input = str(args)
        self._redis.rpush(method.__qualname__ + ':inputs', input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ':outputs', output)
        return output
    return wrapper

def replay(fn: Callable):
    """ function to display the history of calls of a particular function. """
    r = redis.Redis()
    p_function = fn.__qualname__
    call = r.get(p_function)
    try:
        call = int(call.decode("utf-8"))
    except Exception:
        call = 0
    print("{} was called {} times:".format(p_function, call))
    inputs = r.lrange("{}:inputs".format(p_function), 0, -1)
    outputs = r.lrange("{}:outputs".format(p_function), 0, -1)
    for i, o in zip(inputs, outputs):
        try:
            i = i.decode("utf-8")
        except Exception:
            i = ""
        try:
            o = o.decode("utf-8")
        except Exception:
            o = ""
        print("{}(*{}) -> {}".format(p_function, i, o))


class Cache:
    """ Declare a cache redis class """
    def __init__(self):
        """
        store an instance of the Redis client
        """
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """  takes a data argument and returns a string """
        r_key = str(uuid4())
        self._redis.set(r_key, data)
        return r_key

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
