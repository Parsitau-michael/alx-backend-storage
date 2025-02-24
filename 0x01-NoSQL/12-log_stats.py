#!/usr/bin/env python3
"""
a Python script that provides some stats about Nginx logs stored in MongoDB
"""


from pymongo import MongoClient
client = MongoClient()
collection = client.logs.nginx
print("{} logs".format(collection.count_documents({})))
print("Methods:")
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
for method in methods:
    count = collection.count_documents({"method": method})
    print("\tmethod {}: {}".format(method, count))

status_count = collection.count_documents({"method": "GET", "path": "/status"})
print("{} status check".format(status_count))
