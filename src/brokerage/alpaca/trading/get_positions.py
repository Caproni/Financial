#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.trading.client import TradingClient
from requests.exceptions import ConnectionError

from src.utils.logger import logger as log


def get_positions(
    client: TradingClient,
):
    log.info("Calling get_positions")

    try:
        return client.get_all_positions()
    except Exception as e:
        log.critical(f"{e}")
        raise e
