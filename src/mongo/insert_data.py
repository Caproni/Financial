#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from pymongo import MongoClient, InsertOne, errors

from src.utils import log


def insert_data(
    client: MongoClient,
    database: str,
    collection: str,
    documents: list[dict[str, Any]],
    stop_on_key_violation: bool = True,
) -> int | None:
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
    stop_on_key_violation (bool): Sets the "ordered" parameter which defines whether a process should stop when a key violation occurs. Defaults to True in which case the process will raise an error on key violations.
    Returns:
        InsertManyResult | None
    """
    log.info("Calling insert_data")
    db = client[database]
    collection = db[collection]

    if not documents:
        log.info("No documents to insert.")
        return None

    payload: list[InsertOne] = [InsertOne(doc) for doc in documents]
    
    try:
        result = collection.bulk_write(
            payload,
            ordered=stop_on_key_violation,
        )
        insertions = result.inserted_count
        log.info(f"Inserted: {insertions} documents into the collection.")
    except errors.BulkWriteError as bwe:
        insertions = bwe.details['nInserted']
        log.info(f"Inserted: {insertions} documents into the collection.")
    except errors.ServerSelectionTimeoutError as sst:
        log.error(f"Error: {sst}")
        raise sst

    return insertions
