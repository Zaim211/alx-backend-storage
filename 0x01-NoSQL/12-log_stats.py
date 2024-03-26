#!/usr/bin/env python3
"""
Python script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def log_status(collection, option=None):
    """
     that provides some stats about Nginx logs
     stored in MongoDB
    """
    results = {}
    if option:
        value = collection.count_documents(
            {"method": {"$regex": option}})
        print(f"\tmethod {option}: {value}")
        return

    result = collection.count_documents(results)
    print(f"{result} logs")
    print("Methods:")
    for method in METHODS:
        log_status(nginx_collection, method)
    status_check = collection.count_documents({"path": "/status"})
    print(f"{status_check} status check")


if __name__ == "__main__":
    nginx_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    log_status(nginx_collection)
