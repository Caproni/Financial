#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from pymongo.results import InsertManyResult
from datetime import datetime, timedelta

from src.brokerage.polygon import (
    get_market_data,
    create_client,
)
from src.mongo import insert_data, get_data, create_mongo_client
from src.utils import log


def populate_database_market_data() -> list[InsertManyResult]:
    log.info("Calling populate_database_market_data")

    polygon_client = create_client()
    mongo_client = create_mongo_client()

    tickers = get_data(
        mongo_client,
        database="financial",
        collection="tickers",
        pipeline=None,
    )

    now = datetime.now()
    results: list[InsertManyResult] = []
    while True:
        try:
            s = next(tickers)
        except StopIteration as e:
            log.info("Reached end of generated tickers.")
            break

        log.info(f"Processing: {s.ticker}")
        historical_stock_bars = get_market_data(
            polygon_client,
            ticker=s.ticker,
            timespan="day",
            from_=now - timedelta(days=12 * 365),
            to=now - timedelta(days=1),
        )

        N = len(historical_stock_bars)
        if N:
            log.info(f"Data obtained for symbol: {s.ticker}")
            log.info(f"Number of documents obtained: {N}")
            result = insert_data(
                client=mongo_client,
                database="financial",
                collection="polygon_daily_historical_market_data",
                documents=historical_stock_bars,
            )
            results.append(result)

    return results
