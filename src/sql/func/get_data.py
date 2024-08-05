#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from sqlalchemy.sql.elements import BooleanClauseList

from src.sql import DatabaseClient
from src.utils import log


def get_data(
    database_client: DatabaseClient,
    models: list[Any] | None,
    joins: list[tuple[Any, ...]] = None,
    where_clause: BooleanClauseList | None = None,
    entities: list = None,
    as_dict: bool = True,
):
    log.function_call()

    with database_client.get_db() as db:
        try:
            query = db.query(*entities) if entities else db.query(*models)

            if where_clause:
                query = query.filter(where_clause)

            if joins:
                for join in joins:
                    query = query.join(*join)

            results = query.all()

            if as_dict:
                results_as_dicts = []
                for result in results:
                    if result is not None:
                        result_dict = {
                            column.name: getattr(result, column.name)
                            for column in result.__table__.columns
                        }
                        results_as_dicts.append(result_dict)
                return results_as_dicts

            return results

        except Exception as e:
            log.error(f"Error getting data. Error: {e}")
