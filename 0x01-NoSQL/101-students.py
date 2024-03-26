#!/usr/bin/env python3
"""
Python function that returns all students sorted by average score
"""


def top_students(mongo_collection):
    """
    function return all students sorted by average
    """
    return mongo_collection.aggregate([
        {
            "$match":
            {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort":
                {
                    "averageScore": -1
                }
        }
    ])