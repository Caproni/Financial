#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from pymongo.results import InsertManyResult
from datetime import datetime

from src.brokerage.polygon import (
    create_client,
    list_ticker_news,
)
from src.mongo import insert_data, get_data, create_mongo_client
from src.utils import log


def populate_database_ticker_news(
    published_utc_gte: datetime,
    published_utc_lte: datetime,
) -> list[InsertManyResult]:
    log.info("Calling populate_database_ticker_news")

    polygon_client = create_client()
    mongo_client = create_mongo_client()

    tickers = get_data(
        mongo_client,
        database="financial",
        collection="tickers",
        pipeline=None,
    )

    N = len(tickers)

    log.info(f"Retrieved: {N} tickers.")

    results: list[InsertManyResult] = []
    for i, ticker in enumerate(tickers):
        log.info(f"Processing ticker: {i + 1} of {N}")
        log.info(f"Processing: {ticker['ticker']}")
        
        news = list_ticker_news(
            client=polygon_client,
            ticker=ticker["ticker"],
            published_utc_gte=published_utc_gte,
            published_utc_lte=published_utc_lte,
        )

        result = insert_data(
            mongo_client,
            database="financial",
            collection="ticker_news",
            documents=news,
            stop_on_key_violation=False,
        )
        results.append(result)

    return results
