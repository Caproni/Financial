#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any

from ..client import DatabaseClient
from src.utils import log


def update_data(
    database_client: DatabaseClient,
    rows_to_update: list[Any],
) -> bool:
    log.function_call()

    with database_client.get_db() as db:
        try:
            for row in rows_to_update:
                db.add(row)
            db.commit()
            return True
        except Exception as e:
            log.error(f"Error updating rows. Error: {e}")
            db.rollback()
            return False
