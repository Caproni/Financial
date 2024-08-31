#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os import getenv
from asyncio import run
from datetime import datetime
import sentry_sdk
from dotenv import load_dotenv

from src.sql import create_sql_client, get_data, delete_repeated_data, Tickers
from src.etl import (
    populate_database_ticker_news,
)
from src.utils import log

load_dotenv()

sentry_sdk.init(
    dsn=getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

if __name__ == "__main__":

    log.info("Starting database population for ticker news.")

    database_client = create_sql_client()

    tickers = get_data(
        database_client,
        models=[Tickers],
    )

    N = len(tickers)

    for i, ticker in enumerate(tickers):
        log.info(f"Processing ticker: {i + 1} of {N}")
        log.info(f"Processing: {ticker['ticker']}")
        run(
            populate_database_ticker_news(
                start_time=datetime(2015, 1, 1),
                finish_time=datetime.now(),
                tickers=[ticker["ticker"]],
            )
        )

    log.info("Deleting repeated ticker news data.")

    delete_repeated_data(
        mongo_client=database_client,
        collection="ticker_news",
        field="polygon_id",
    )

    log.info("Completed database population for ticker news.")
