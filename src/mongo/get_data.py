#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from pymongo import MongoClient

from src.utils import log


def get_data(
    client: MongoClient,
    database: str,
    collection: str,
    pipeline: None | list[dict[str, Any]] = None,
) -> list[dict[str, Any]]:
    """Gets data from a specified collection according to the pipeline defined according to: https://www.mongodb.com/docs/manual/core/aggregation-pipeline/

    Args:
        client (MongoClient): A Mongo client.
        database (str): Database from which to retrieve data.
        collection (str): Collection from which to retrieve data.
        pipeline (None | list[dict[str, Any]], optional): An aggregation pipeline. Defaults to None.
            Example:
                pipeline = [
                    {"$match": {"status": "A"}},
                    {"$group": {"_id": "$cust_id", "total": {"$sum": "$amount"}}}
                ]

    Returns:
        list[dict[str, Any]]: A list of documents
    """
    log.function_call()
    db = client[database]
    collection = db[collection]

    if pipeline is None:
        pipeline = []

    return list(
        collection.aggregate(
            pipeline,
            allowDiskUse=True,
        )
    )
