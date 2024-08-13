#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import and_, func

from src.sql import create_sql_client, PolygonMarketDataHour, get_data, delete_data
from src.utils import log


if __name__ == "__main__":

    log.info("Starting deleting duplicate rows.")

    database_client = create_sql_client()

    collection = PolygonMarketDataHour

    duplicate_rows = get_data(
        database_client=database_client,
        models=[collection],
        group_by=[
            collection.symbol,
            collection.timestamp,
        ],
        having_clause=and_(
            func.count(collection.timestamp) > 1,
        ),
        entities=[
            collection.symbol,
            collection.timestamp,
        ],
    )

    for duplicate_row in duplicate_rows:
        symbol = duplicate_row["symbol"]
        timestamp = duplicate_row["timestamp"]
        log.info(f"Processing symbol: {symbol} at timestamp: {timestamp}")

        rows_to_delete = get_data(
            database_client=database_client,
            models=[collection],
            where_clause=and_(
                collection.symbol == symbol,
                collection.timestamp == timestamp,
            ),
        )

        rows_to_delete.pop(0)

        if rows_to_delete:
            log.info(f"Deleting: {len(rows_to_delete)} rows.")
            delete_data(
                database_client,
                rows_to_delete=rows_to_delete,
            )

    log.info("Completed deleting duplicate rows.")
