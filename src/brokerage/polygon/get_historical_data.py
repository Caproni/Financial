#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from polygon import RESTClient
from dotenv import load_dotenv
from os import getenv

from src.utils import log


def get_historical_data(
    symbol: str,
    from_date: str,
    to_date: str,
    timeframe: str,
):
    log.info("Calling get_historical_data")
    
    load_dotenv()
    
    assert timeframe in {"day"}, "Selected timeframe is not supported."

    with RESTClient(api_key=getenv("POLYGON_API_KEY")) as client:
        response = client.stocks_equities_aggregates(
            symbol,
            1,
            timeframe,
            from_date,
            to_date,
            unadjusted=False,
        )
        return response.results
    