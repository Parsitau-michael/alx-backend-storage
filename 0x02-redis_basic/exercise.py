#!/usr/bin/env python3
"""
This module creates and initializes a cache class
"""

import uuid
import redis
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Defining a decorator to count how many times
    methods of the Cache class are called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """Cache class using Redis."""
    def __init__(self):
        """Initialize Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with a randomly generated key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[[bytes], any]]
            = None) -> Optional[any]:
        """Retrieve data from Redis and optionally apply a conversion function.
        """
        response = self._redis.get(key)
        if response is None:
            return None
        return fn(response) if fn else response

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve value as a string."""
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve value as an integer."""
        return self.get(key, int)
