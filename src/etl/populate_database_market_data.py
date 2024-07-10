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


def populate_database_market_data(
    timespan: str,
    collection: str,
) -> list[InsertManyResult]:
    log.info("Calling populate_database_market_data")

    polygon_client = create_client()
    mongo_client = create_mongo_client()

    tickers = get_data(
        mongo_client,
        database="financial",
        collection="tickers",
        pipeline=None,
    )

    N = len(tickers)

    now = datetime.now()
    results: list[InsertManyResult] = []
    for i, s in enumerate(tickers):
        if i < 4065 or "C:" in s["ticker"]:
            continue
        log.info(f"Processing ticker {i + 1} of {N}")
        log.info(f"Processing: {s['ticker']}")
        historical_stock_bars = get_market_data(
            polygon_client,
            ticker=s["ticker"],
            timespan=timespan,
            from_=now - timedelta(days=365 * 5 + 1),
            to=now - timedelta(days=1),
        )

        number_of_bars = len(historical_stock_bars)
        if number_of_bars:
            log.info(f"Data obtained for symbol: {s['ticker']}")
            log.info(f"Number of documents obtained: {number_of_bars}")
            result = insert_data(
                client=mongo_client,
                database="financial",
                collection=collection,
                documents=historical_stock_bars,
            )
            results.append(result)

    return results
