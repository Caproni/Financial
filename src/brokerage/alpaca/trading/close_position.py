#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.trading.client import TradingClient

from src.utils.logger import logger as log


def close_position(
    client: TradingClient,
    symbol: str,
):
    """Closes all open positions. Can be used at end of day.

    Args:
        client (TradingClient): A trading client
        symbol (str): A symbol. All open positions related to this symbol are closed.
    """
    log.info("Calling close_position")
    client.close_position(
        symbol_or_asset_id=symbol,
    )
