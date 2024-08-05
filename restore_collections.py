#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os.path import abspath, join, dirname

from src.etl import restore_collection_from_file
from src.sql import (
    create_sql_client,
    Tickers,
    TickerNews,
    RelatedCompanies,
    Exchanges,
    PolygonMarketDataDay,
)
from src.utils import log


if __name__ == "__main__":

    log.info("Starting restore for financial database.")

    path_to_staging = abspath(join(dirname(__file__), "staging"))

    database_client = create_sql_client()

    collections = {
        "exchanges": None,
        "tickers": None,
        "related_companies": None,
        "ticker_news": None,
        "polygon_market_data_day": PolygonMarketDataDay,
        "polygon_market_data_hour": None,
    }

    for name, collection in collections.items():

        if collection is None:
            log.info(f"Skipping collection: {name}")
            continue

        log.info(f"Restoring {name} collection.")

        result = restore_collection_from_file(
            database_client=database_client,
            collection_name=name,
            collection=collection,
            path_to_file=join(path_to_staging, f"{name}.pkl.gz"),
        )

        log.info(f"Result: {result}")

    log.info("Completed restore for financial database.")
