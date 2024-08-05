#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from pymongo import MongoClient, DeleteMany

from src.utils import log


def delete_data(
    client: MongoClient,
    database: str,
    collection: str,
    document_filter: dict[str, Any] = None,
) -> DeleteMany:
    """
    Delete data from a specified database and collection with an optional filter.

    Parameters:
    - client (MongoClient): The MongoDB client.
    - database (str): The name of the database.
    - collection (str): The name of the collection.
    - document_filter (dict, optional): A filter to specify which documents to delete. Default is None, which deletes all documents.

    Returns:
    - DeleteMany: The result of the delete operation.
    """
    log.function_call()

    if document_filter is None:
        document_filter = {}

    db = client[database]
    collection = db[collection]

    return collection.delete_many(document_filter)
