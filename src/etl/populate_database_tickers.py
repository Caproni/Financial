#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from src.brokerage.polygon import (
    list_tickers,
    create_polygon_client,
)
from src.sql import create_sql_client, unpack_simple_table, insert_data, Tickers
from src.utils import log


def populate_database_tickers() -> bool:
    """
    Populates the database with ticker information.

    Returns:
        A boolean value indicating the success of data population for tickers.
    """
    log.function_call()

    polygon_client = create_polygon_client()
    database_client = create_sql_client()

    tickers = list_tickers(
        polygon_client,
        market=None,
        active=None,
    )

    log.info(f"Obtained: {len(tickers)} tickers.")

    documents = unpack_simple_table(
        collection=Tickers,
        data=tickers,
    )

    return insert_data(
        database_client,
        documents=documents,
    )
