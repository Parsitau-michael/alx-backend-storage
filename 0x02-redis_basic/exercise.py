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


def call_history(method: Callable) -> Callable:
    """Defining a decorator to store the history of inputs
    and outputs for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(method.__qualname__ + ":inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(method.__qualname__ + ":outputs", str(output))
        return output
    return wrapper


def replay(method: Callable):
    """Function to display the history of calls of a particular function.
    """
    redis_instance = method.__self__._redis
    method_name = method.__qualname__

    inputs = redis_instance.lrange(method_name + ":inputs", 0,  -1)
    outputs = redis_instance.lrange(method_name + ":outputs", 0, -1)

    print("{} was called {} times:".format(method_name, len(inputs)))

    for input_, output in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(method_name, input_.decode('utf-8'),
                                      output.decode('utf-8')))


class Cache:
    """Cache class using Redis."""
    def __init__(self):
        """Initialize Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
