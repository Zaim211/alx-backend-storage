#!/bin/usr/env python3
""" Insert a document in Python """


def insert_school(mongo_collection, **kwargs):
    """ Function that inserts a new document in a collection
    return new_id
    """
    new_doc = mongo_collection.insert_one(kwargs).inserted_id
    return new_doc
