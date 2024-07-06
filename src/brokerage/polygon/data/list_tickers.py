#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from polygon import RESTClient

from src.utils import log


def list_tickers(
    client: RESTClient,
    market: str,
    active: bool,
):
    log.info("Calling list_tickers")

    try:
        return client.list_tickers(
            market=market,
            active=active,
        )
    except Exception as e:
        log.error("Could not retrieve list of tickers from polygon")
        raise e
