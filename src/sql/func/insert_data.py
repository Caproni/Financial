#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any

from ..client import DatabaseClient
from src.utils import log


def insert_data(
    sql_client: DatabaseClient,
    documents: list[Any],
) -> bool:
    """
    Bulk inserts ticker records into the database.

    Args:
        documents (list): A list of DTOs to be inserted.
    """
    log.function_call()

    with sql_client.get_db() as db:
        try:
            db.bulk_save_objects(documents)
            db.commit()
            return True
        except Exception as e:
            log.error(f"Error inserting data. Error: {e}")

        return False
