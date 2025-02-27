#!/usr/bin/env python3
"""This module is of a function get_page, that uses the requests
module to obtain the HTML content of a particular URL and returns it.
"""


import redis
import requests
from functools import wraps
from typing import Callable


r = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """Decorator to count the number of times a url was accessed"""
    @wraps(method)
    def wrapper(url: str):
        r.incr(f"count:{url}")
        cached_content = r.get(f"cache:{url}")

        if cached_content:
            return cached_content.decode("utf-8")

        response = method(url)
        r.setex(f"cache:{url}", 10, response.encode("utf-8"))
        return response
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """track how many times a particular URL was accessed in the key
    "count:{url}" and cache the result with an expiration time of 10 seconds.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    print(get_page("http://google.com"))
    print(get_page("http://slowwly.robertomurray.co.uk"))
