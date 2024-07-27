#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from pymongo import MongoClient

from src.univariate.analysis import get_moving_average
from src.mongo import get_data, insert_data
from src.utils import log


def save_statistical_data(
    client: MongoClient,
    database: str,
    input_collection_name: str,
    output_collection_name: str,
) -> list[int | None]:
    log.info("Calling save_statistical_data")
    
    tickers = get_data(
        client=client,
        database=database,
        collection="tickers",
        pipeline=None,
    )
    
    results: list[int | None] = []
    for ticker in tickers:
        market_data = get_data(
            client=client,
            database=database,
            collection=input_collection_name,
            pipeline= [
                {
                    "$match": {
                        "symbol": ticker["ticker"],
                    }
                },
            ],
        )
        
        results = insert_data(
            client=client,
            database=database,
            collection=output_collection_name,
            documents=...,
        )
        
    return
