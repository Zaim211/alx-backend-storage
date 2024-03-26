#!/usr/bin/env python3
"""
Python function that lists all documents in a collection.
Return an empty list if no document in the collection
mongo_collection will be the pymongo collection object
"""
import pymongo


def list_all(mongo_collection):
    """ Lists all documents """
    documents = mongo_collection.find()
    count = mongo_collection.count_documents({})
    if count == 0:
        return []

    return documents
