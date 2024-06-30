#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from pymongo import MongoClient
from pymongo.results import InsertManyResult
from src.utils import log


def insert_daily_bars(
    client: MongoClient,
    database: str,
    collection: str,
    daily_bars: list[dict[str, Any]],
) -> InsertManyResult:
    """
    Insert daily bars into Mongo database.

    Parameters:
    client (MongoClient): A pymongo client instance.
    database (str): A database name.
    collection (str): A collection name.
    daily_bars (list): A list of dictionaries, each representing a daily bar.
                       Each dictionary should have the following structure:
                       {
                           'date': datetime,
                           'open': float,
                           'high': float,
                           'low': float,
                           'close': float,
                           'volume': int
                       }
    Returns:
        InsertManyResult
    """
    log.info("Calling insert_daily_bars")
    db = client[database]
    collection = db[collection]

    result = collection.insert_many(daily_bars)
    log.info(f'Inserted {len(result.inserted_ids)} documents into the collection.')
    return result
