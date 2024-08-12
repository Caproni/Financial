#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import and_, func

from src.sql import create_sql_client, PolygonMarketDataHour, get_data, delete_data
from src.utils import log


def delete_repeated_polygon_market_data():
    log.function_call()

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

    with database_client.get_db() as db:
        try:
            for duplicate_row in duplicate_rows:
                symbol = duplicate_row['symbol']
                timestamp = duplicate_row['timestamp']
                
                rows_to_delete = get_data(
                    database_client=database_client,
                    models=[collection],
                    where_clause=and_(
                        collection.symbol == symbol,
                        collection.timestamp == timestamp
                    ),
                )
                
                # Keep the first row and delete the rest
                data_ids: list[str] = []
                for row in rows_to_delete[1:]:
                    data_ids.append(row.data_id)

                delete_data(
                    database_client,
                    model=[collection],
                    where_clause=and_(collection.data_id.in_(data_ids))
                )

            log.info("Successfully deleted duplicate rows.")
        except Exception as e:
            db.rollback()
            log.error(f"Error deleting duplicate rows. Error: {e}")
    
    for duplicate_row in duplicate_rows:
        ...
