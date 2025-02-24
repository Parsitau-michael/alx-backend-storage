#!/usr/bin/env python3
"""
a Python script that provides some stats about Nginx logs stored in MongoDB
"""


from pymongo import MongoClient


def log_stats():
    """
    Fetch and display statistics from the 'nginx' collection
    in the 'logs' database.
    """
    client = MongoClient()
    collection = client.logs.nginx

    print("{} logs".format(collection.count_documents({})))
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))

    stats = collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status_count))


if __name__ == "__main__":
    log_stats()
