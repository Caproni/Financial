#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from pymongo.results import InsertManyResult

from src.brokerage.polygon import (
    create_client,
    list_ticker_news,
)
from src.mongo import insert_data, get_data, delete_data, create_mongo_client
from src.utils import log


def populate_database_ticker_news() -> list[InsertManyResult]:
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

    delete_data(
        mongo_client,
        database="financial",
        collection="ticker_news",
        document_filter=None,
    )

    results: list[InsertManyResult] = []
    for i, ticker in enumerate(tickers):
        log.info(f"Processing ticker: {i + 1} of {N}")
        log.info(f"Processing: {ticker['ticker']}")
        news = list_ticker_news(
            client=polygon_client,
            ticker=ticker["ticker"],
            published_utc_gte=None,
            published_utc_lte=None,
        )

        result = insert_data(
            mongo_client,
            database="financial",
            collection="ticker_news",
            documents=news,
        )
        results.append(result)

    return results
