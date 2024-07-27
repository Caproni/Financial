#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from pymongo.results import InsertManyResult

from src.brokerage.polygon import (
    list_tickers,
    create_client,
)
from src.mongo import insert_data, create_mongo_client
from src.utils import log


def populate_database_tickers() -> InsertManyResult:
    log.info("Calling populate_database_tickers")

    polygon_client = create_client()
    mongo_client = create_mongo_client()

    tickers = list_tickers(
        polygon_client,
        market=None,
        active=None,
    )
    
    log.info(f"Obtained: {len(tickers)} tickers.")

    return insert_data(
        mongo_client,
        database="financial",
        collection="tickers",
        documents=tickers,
    )
