#!/usr/bin/env python3
"""
A Python function that lists all documents in a collection
"""


def list_all(mongo_collection):
    """Python function that lists all documents in a collection"""
    return mongo_collection.find()
