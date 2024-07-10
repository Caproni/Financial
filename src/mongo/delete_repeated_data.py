#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from pymongo import MongoClient

from src.mongo import delete_data
from src.mongo.get_data import get_data
from src.utils import log


def delete_repeated_data(
    mongo_client: MongoClient,
    collection: str,
    field: str,
):
    """
    Deletes repeated data entries based on a specified field in a MongoDB collection.

    Args:
        mongo_client: MongoClient instance for database connection.
        collection: Name of the collection in the database.
        field: Field used to identify repeated data entries.

    Returns:
        None
    """

    log.info("Calling delete_repeated_data")

    repeated_articles = get_data(
        mongo_client,
        database="financial",
        collection=collection,
        pipeline=[
            {
                "$group": {
                    "_id": f"${field}",
                    "count": {"$sum": 1},
                    "ids": {"$push": "$_id"},
                }
            },
            {"$match": {"count": {"$gt": 1}}},
        ],
    )

    for repeated_articles in repeated_articles:
        ids_to_delete = repeated_articles["ids"][1:]
        delete_data(
            mongo_client,
            database="financial",
            collection=collection,
            document_filter={"_id": {"$in": ids_to_delete}},
        )
