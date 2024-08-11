#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from sqlalchemy.sql.elements import BooleanClauseList

from ..client import DatabaseClient
from src.utils import log


def delete_data(
    sql_client: DatabaseClient,
    model: Any,
    where_clause: BooleanClauseList | None = None,
) -> bool:
    log.function_call()

    with sql_client.get_db() as db:
        try:
            query = db.query(model)
            
            # Apply all conditions to filter which rows to delete
            if where_clause is not None:
                query = query.filter(where_clause)
            
            query.delete(synchronize_session=False)
            db.commit()
            return True
        except Exception as e:
            log.error(f"Error deleting data. Error: {e}")
            db.rollback()

        return False
