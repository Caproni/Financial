#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from pymongo import MongoClient

from src.univariate.analysis import calc_linear_moving_average
from src.mongo import get_data, insert_data
from src.utils import log


def populate_database_statistical_data(  # TODO: implement me or delete
    client: MongoClient,
    database: str,
    input_collection_name: str,
    output_collection_name: str,
    weighting: str,
    steps: list[int],
    tickers: list[str] | None = None,
) -> list[int | None]:
    """
    Populates the database with statistical data based on market data for specified tickers.

    Args:
        client: A MongoClient instance for database connection.
        database: A string representing the database name.
        input_collection_name: A string specifying the input collection name.
        output_collection_name: A string specifying the output collection name.
        weighting: A string specifying the weighting method for calculations.
        steps: A list of integers representing the steps for moving averages.
        tickers: An optional list of strings representing ticker symbols (default is None).

    Returns:
        A list of integers or None indicating the results of data population for each ticker.
    """
    log.function_call()

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
            ma_data_mean, ma_data_sd = calc_linear_moving_average(
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
