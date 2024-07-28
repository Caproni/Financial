#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from polygon import RESTClient

from src.utils import log


def get_related_companies(
    client: RESTClient,
    ticker: str,
) -> list[dict[str, Any]]:
    """Gets related company data from Polygon.io.

    Args:
        client (RESTClient): A Polygon client.
        ticker (str): A specific ticker / symbol.

    Returns:
        dict[str, Any]: A dictionary of related companies.
    """
    log.info("Calling get_related_companies")

    try:
        response = client.get_related_companies(
            ticker=ticker,
            params={},
            raw=False,
        )
    except Exception as e:
        log.error(f"Error: {e}")
        raise e

    return {
        "symbol": ticker,
        "tickers": [e.ticker for e in response]
    }
