#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from src.etl import populate_database_market_data
from src.mongo import create_mongo_client
from src.utils import log


if __name__ == "__main__":

    log.info("Starting database population.")

    mongo_client = create_mongo_client()

    # stock data

    timespan = "hour"

    populate_database_market_data(
        timespan=timespan,
        collection=f"polygon_market_data_{timespan}",
    )

    log.info("Completed database population.")
