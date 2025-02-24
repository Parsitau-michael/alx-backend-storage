#!/usr/bin/env python3
"""
Improve 12-log_stats.py by adding the top 10 of the most present
IPs in the collection nginx of the database logs
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
    print("{} status check".format(stats))

    print("IPs:")
    res = collection.aggregate([
        {
            "$group": {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        },
        {
            "$limit": 10
        }
    ])

    for doc in res:
        print("\t{}: {}".format(doc.get("_id"), doc.get("count")))


if __name__ == "__main__":
    log_stats()
