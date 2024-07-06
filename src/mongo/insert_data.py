#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from pymongo import MongoClient
from pymongo.results import InsertManyResult

from src.utils import log


def insert_data(
    client: MongoClient,
    database: str,
    collection: str,
    documents: list[dict[str, Any]],
) -> InsertManyResult:
    """
    Insert data into Mongo database.

    Parameters:
    client (MongoClient): A pymongo client instance.
    database (str): A database name.
    collection (str): A collection name.
    documents (list): A list of dictionaries, each representing a daily bar.
        Each dictionary should have the following structure:
        {
            "symbol": "OXLCO"
            "timestamp": 2024-07-01T04:00:00.000+00:00
            "open": 22.41
            "high": 22.42
            "low": 22.34
            "close": 22.34
            "volume": 1907
            "trade_count": 19
            "vwap": 22.38822
        }
    Returns:
        InsertManyResult
    """
    log.info("Calling insert_data")
    db = client[database]
    collection = db[collection]

    result = collection.insert_many(documents)
    log.info(f"Inserted {len(result.inserted_ids)} documents into the collection.")
    return result
