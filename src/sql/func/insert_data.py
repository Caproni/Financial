#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert as pg_insert

from ..client import DatabaseClient
from src.utils import log


def insert_data(
    sql_client: DatabaseClient,
    documents: list[Any],
    allow_partial_inserts: bool = False,
    upsert: bool = False,
) -> bool:
    """
    Bulk inserts data into the database.

    Args:
        documents (list): A list of Data Transfer Objects (DTOs) to be inserted.
        allow_partial_inserts (bool): If True, allows for partial insertion of documents that do not violate constraints.
        upsert (bool): If True, performs an upsert operation (insert or update).
    """
    log.function_call()

    with sql_client.get_db() as db:
        if allow_partial_inserts or upsert:
            success = True
            for document in documents:
                try:
                    if upsert:
                        # Assuming the document is a SQLAlchemy model instance
                        # Use the `merge` method for upsert
                        db.merge(document)
                    else:
                        db.add(document)
                    db.commit()
                except IntegrityError as e:
                    db.rollback()  # Rollback only this document's transaction
                    log.warning(f"Error processing document {document}. Error: {e}")
                    success = False
            return success
        else:
            try:
                db.bulk_save_objects(documents)
                db.commit()
                return True
            except Exception as e:
                db.rollback()
                log.error(f"Error inserting data. Error: {e}")
                return False
