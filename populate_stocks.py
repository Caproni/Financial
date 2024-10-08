#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os import getenv
import sentry_sdk
from dotenv import load_dotenv

from src.etl import populate_database_market_data
from src.sql import PolygonMarketDataDay, PolygonMarketDataHour
from src.utils import log

load_dotenv()

sentry_sdk.init(
    dsn=getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

if __name__ == "__main__":

    log.info("Starting database population.")

    timespan = "hour"
    collection_name = f"polygon_market_data_{timespan}"

    if collection_name == "polygon_market_data_day":
        collection = PolygonMarketDataDay
    elif collection_name == "polygon_market_data_hour":
        collection = PolygonMarketDataHour

    populate_database_market_data(
        timespan=timespan,
        collection=collection,
    )

    log.info("Completed database population.")
