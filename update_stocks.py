#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import func
from datetime import timedelta

from src.etl import populate_database_latest_market_data
from src.sql import (
    create_sql_client,
    get_data,
    PolygonMarketDataDay,
    PolygonMarketDataHour,
)
from src.utils import log


if __name__ == "__main__":

    log.info("Starting database update.")

    database_client = create_sql_client()

    timespans = [
        "day",
        "hour",
    ]

    for timespan in timespans:
        collection_name = f"polygon_market_data_{timespan}"
        log.info(f"Populating: {collection_name}")

        if collection_name == "polygon_market_data_day":
            collection = PolygonMarketDataDay
        elif collection_name == "polygon_market_data_hour":
            collection = PolygonMarketDataHour

        latest_market_data_timestamps = get_data(
            database_client,
            models=[collection],
            entities=[
                collection.symbol,
                func.max(collection.timestamp).label("timestamp"),
            ],
            group_by=[collection.symbol],
        )

        for latest_market_data_timestamp in latest_market_data_timestamps:
            populate_database_latest_market_data(
                timespan=timespan,
                collection=collection,
                ticker=latest_market_data_timestamp["symbol"],
                from_=latest_market_data_timestamp["timestamp"] + timedelta(days=1),
            )

    log.info("Completed database update.")
