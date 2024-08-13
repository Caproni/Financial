#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any

from src.sql.client import DatabaseClient
from src.utils import log


def delete_data(
    sql_client: DatabaseClient, rows_to_delete: list[Any]  # A list of ORM instances
) -> bool:
    """
    Deletes rows from the database.

    Args:
        sql_client: DatabaseClient - The database client to use for deleting rows.
        rows_to_delete: list[Any] - A list of ORM instances to delete.

    Returns:
        bool - True if rows are deleted successfully, False otherwise.

    Raises:
        Any exceptions that occur during the deletion process.
    """
    log.function_call()

    with sql_client.get_db() as db:  # Assuming db is a Session instance
        try:
            for row in rows_to_delete:
                db.delete(row)  # Deletes each row individually

            db.commit()
            return True
        except Exception as e:
            log.error(f"Error deleting rows. Error: {e}")
            db.rollback()
            return False
