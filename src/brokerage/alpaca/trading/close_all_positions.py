#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.trading.client import TradingClient
from requests.exceptions import ConnectionError

from src.utils.logger import logger as log


def close_all_positions(
    client: TradingClient,
    cancel_orders: bool = True,
):
    """Closes all open positions. Can be used at end of day.

    Args:
        client (TradingClient): A trading client
        cancel_orders (bool, optional): Whether to also cancel open orders. Defaults to True.
    """
    log.info("Calling close_all_positions")
    client.close_all_positions(
        cancel_orders=cancel_orders,
    )
