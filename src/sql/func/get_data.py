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
    group_by: list = None,
    having_clause: BooleanClauseList | None = None,
    as_dict: bool = True,
):
    """
    Retrieves data from the database based on specified models, joins, and conditions.

    Args:
        database_client: A DatabaseClient instance for database connection.
        models: An optional list of model objects representing database tables.
        joins: An optional list of tuples specifying table joins.
        where_clause: An optional BooleanClauseList representing query conditions.
        entities: An optional list of entities to query.
        group_by: An optional list of columns to group results by.
        as_dict: A boolean indicating whether to return results as dictionaries (default is True).

    Returns:
        A list of dictionaries or model objects based on the query results.
    Raises:
        Exception: If an error occurs during data retrieval.
    """
    log.function_call()

    with database_client.get_db() as db:
        try:
            query = db.query(*entities) if entities else db.query(*models)

            if where_clause is not None:
                query = query.filter(where_clause)

            if joins:
                for join in joins:
                    query = query.join(*join)

            if group_by is not None:
                query = query.group_by(*group_by)

            if having_clause is not None:
                query = query.having(having_clause)

            results = query.all()

            if as_dict:
                results_as_dicts = []
                for result in results:
                    if result is not None:
                        if not hasattr(result, "__table__"):
                            result_dict = {}
                            for entity, value in zip(entities, tuple(result)):
                                if hasattr(entity, "name"):
                                    result_dict[entity.name] = value
                                else:
                                    result_dict[str(entity)] = value
                        else:
                            result_dict = {
                                column.name: getattr(result, column.name)
                                for column in result.__table__.columns
                            }
                        results_as_dicts.append(result_dict)
                return results_as_dicts

            return results

        except Exception as e:
            log.error(f"Error getting data. Error: {e}")
