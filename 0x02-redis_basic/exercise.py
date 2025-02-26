#!/usr/bin/env python3
"""
This module creates and initializes a cache class
"""

import uuid
import redis
from typing import Union


class Cache:
    """Cache class using Redis."""
    def __init__(self):
        """Initialize Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with a randomly generated key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
