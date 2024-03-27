#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
from uuid import uuid4
from typing import Union


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
