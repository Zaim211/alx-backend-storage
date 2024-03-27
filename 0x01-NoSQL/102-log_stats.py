#!/usr/bin/env python3
"""
Improve 12-log_stats.py by adding the top 10 of the most present IPs
in the collection nginx of the database logs
"""
from pymongo import MongoClient
from collections import Counter


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

    ip_counts = Counter(doc["ip"] for doc in collection.find({}, {"ip": 1}))
    top_10_ips = ip_counts.most_common(10)
    print("IPs:")
    for ip, count in top_10_ips:
        print(f"\t{ip}: {count}")


if __name__ == "__main__":
    nginx_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    log_status(nginx_collection)
