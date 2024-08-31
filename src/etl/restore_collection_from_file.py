#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any

from src.sql import (
    DatabaseClient,
    insert_data,
    unpack_related_companies,
    unpack_simple_table,
)
from src.utils import log, load_json_from_file


def restore_collection_from_file(
    database_client: DatabaseClient,
    collection_name: str,
    collection: Any,
    path_to_file: str,
) -> int | None:
    """Restores collection from file backup.

    Args:
        database_client (DatabaseClient): A database client.
        collection (Any): A collection DTO into which to restore the data.
        path_to_file (str): Path to a file to restore into the indicated collection.

    Returns:
        int | None: Number of rows inserted, or None.
    """
    log.function_call()

    data = load_json_from_file(
        path_to_file=path_to_file,
    )

    log.info(f"Obtained: {len(data)} documents.")

    if collection_name == "related_companies":
        documents = unpack_related_companies(
            data=data,
        )
    else:
        documents = unpack_simple_table(
            collection=collection,
            data=data,
        )

    return insert_data(
        database_client=database_client,
        documents=documents,
    )
