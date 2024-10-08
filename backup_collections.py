#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os import getenv
from os.path import abspath, join, dirname
import sentry_sdk
from dotenv import load_dotenv

from src.etl import backup_collection_to_file
from src.mongo import create_mongo_client
from src.utils import log

load_dotenv()

sentry_sdk.init(
    dsn=getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

if __name__ == "__main__":

    log.info("Starting backup for financial database.")

    database = "financial"

    path_to_staging = abspath(join(dirname(__file__), "staging"))

    mongo_client = create_mongo_client()

    collections = [
        "exchanges",
        "tickers",
        "ticker_news",
        "related_companies",
        "polygon_market_data_day",
    ]

    for collection in collections:

        log.info(f"Backing up {collection} collection.")

        result = backup_collection_to_file(
            database_client=mongo_client,
            database=database,
            collection=collection,
            path_to_file=join(path_to_staging, f"{collection}.pkl.gz"),
        )

        log.info(f"Result: {result}")

    log.info("Completed backup for financial database.")
