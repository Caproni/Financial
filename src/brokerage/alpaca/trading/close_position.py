#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.trading.client import TradingClient
from requests.exceptions import ConnectionError

from src.utils import log


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
    try:
        client.close_position(
            symbol_or_asset_id=symbol,
        )
    except ConnectionError as e:
        log.warning(f"Connection Error: {e}")
        try:
            client.close_position(
                symbol_or_asset_id=symbol,
            )
        except ConnectionError as e:
            log.error(f"Second Connection Error: {e}")
