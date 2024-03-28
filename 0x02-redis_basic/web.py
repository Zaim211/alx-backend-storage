#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import requests
from functools import wraps
import redis


def count_accessed_url(method):
    """ Decorate the count of how many
    times the URL is accessed """
    @wraps(method)
    def wrapper(url):
        key = "cache:" + url
        data = redis.Redis().get(key)
        if data:
            return data.decode("utf-8")

        counter = "count:" + url
        html = method(url)

        redis.Redis().incr(counter)
        redis.Redis().set(key, html)
        redis.Redis().expire(key, 10)
        return html
    return wrapper


@count_accessed_url
def get_page(url: str) -> str:
    """ Using requests module to obtain
    HTML content of a particular URL and returns it
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # Test the get_page function
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
