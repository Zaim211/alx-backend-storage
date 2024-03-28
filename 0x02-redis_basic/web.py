#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import requests
from functools import wraps
import redit

store = redis.Redis()


def count_accessed_url(method):
    """ Decorate the count of how many
    times the URL is accessed """
    @wraps(method)
    def wrapper(url):
        key = "cache:" + url
        data = store.get(key)
        if data:
            return data.decode("utf-8")
        counter = "count:" + url
        html = method(url)
        store.incr(count_key)
        store.set(cached_key, html)
        store.expire(cached_key, 10)
        return html
    return wrapper

@count_accessed_url
def get_page(url: str) -> str:
    """ Using requests module to obtain
    HTML content of a particular URL and returns it
    """
    url = "http://slowwly.robertomurray.co.uk"
    return requests.get(url).text
