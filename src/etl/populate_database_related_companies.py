#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any

from src.brokerage.polygon import create_client, get_related_companies
from src.mongo import get_data, insert_data, create_mongo_client
from src.utils import log


def populate_database_related_companies(
    tickers: list[str] | None = None,
) -> int | None:
    """Populate database with related company data.

    Args:
        tickers (list[str] | None, optional): Tickers for which to populate the database. Defaults to None in which case all tickers are processed.

    Returns:
        int | None: Number of inserted documents or None if a failure occurred.
    """
    log.info("Calling populate_database_related_companies")

    polygon_client = create_client()
    mongo_client = create_mongo_client()

    if tickers is None:
        tickers = get_data(
            client=mongo_client,
            database="financial",
            collection="tickers",
            pipeline=None,
        )
        tickers = [ticker["ticker"] for ticker in tickers]

    N = len(tickers)

    results: list[dict[str, Any]] = []
    for i, ticker in enumerate(tickers):
        log.info(f"Processing ticker: {i + 1} of {N}")
        log.info(f"Processing: {ticker}")
        related_companies = get_related_companies(
            client=polygon_client,
            ticker=ticker,
        )
        results.append(related_companies)

    return insert_data(
        client=mongo_client,
        database="financial",
        collection="related_companies",
        documents=results,
    )