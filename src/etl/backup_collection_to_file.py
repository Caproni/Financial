#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from src.sql import DatabaseClient
from src.utils import log, save_json_to_file


def backup_collection_to_file(
    database_client: DatabaseClient,
    database: str,
    collection: str,
    path_to_file: str,
) -> None:
    """Obtains all data from a collection and saves it to a file.

    Args:
        database_client (DatabaseClient): A database client.
        database (str): A database from which to obtain the data.
        collection (str): A collection from which to obtain the data.
        path_to_file (str): A filepath to which to save the data.
    """
    log.function_call()

    data = get_data(
        client=database_client,
        database=database,
        collection=collection,
        pipeline=None,
    )

    save_json_to_file(
        data_payload=data,
        path_to_file=path_to_file,
    )
