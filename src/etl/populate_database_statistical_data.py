#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from pymongo import MongoClient

from src.univariate.analysis import get_moving_average
from src.mongo import get_data, insert_data
from src.utils import log


def populate_database_statistical_data(
    client: MongoClient,
    database: str,
    input_collection_name: str,
    output_collection_name: str,
    weighting: str,
    steps: list[int],
    tickers: list[str] | None = None,
) -> list[int | None]:
    log.info("Calling populate_database_statistical_data")

    if tickers is None:
        tickers = get_data(
            client=client,
            database=database,
            collection="tickers",
            pipeline=None,
        )
        tickers = [ticker["ticker"] for ticker in tickers]

    N = len(tickers)

    results: list[int | None] = []
    for i, ticker in enumerate(tickers):
        log.info(f"Processing ticker: {i + 1} of {N}")
        log.info(f"Processing: {ticker}")
        market_data = get_data(
            client=client,
            database=database,
            collection=input_collection_name,
            pipeline=[
                {
                    "$match": {
                        "symbol": ticker["ticker"],
                    }
                },
            ],
        )

        for step in steps:
            ma_data_mean, ma_data_sd = get_moving_average(
                data=market_data,
                weighting=weighting,
                steps=step,
            )

        results = insert_data(
            client=client,
            database=database,
            collection=output_collection_name,
            documents=...,
        )

    return
