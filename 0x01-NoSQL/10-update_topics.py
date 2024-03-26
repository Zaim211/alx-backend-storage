#!/bin/usr/env python3
"""
Python function that changes all topics of a school document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """" Change all topic of document """
    return mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
