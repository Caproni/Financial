#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from datetime import timedelta
from alpaca.trading.client import TradingClient
from alpaca.broker.client import BrokerClient

from src.brokerage.alpaca.trading.get_clock import get_clock
from src.brokerage.alpaca.trading.close_all_positions import close_all_positions
from src.utils.logger import logger as log


def close_positions_conditionally(
    trading_client: TradingClient,
    broker_client: BrokerClient,
    within: timedelta,
) -> bool:
    """Closes all positions if within a specified duration of market close.

    Args:
        trading_client (TradingClient): An Alpaca trading client.
        broker_client (BrokerClient): An Alpaca trading client.
        within (timedelta): Duration condition used to check whether market positions should be closed.

    Returns:
        bool: Whether or not all positions have been closed
    """
    log.info("Calling close_positions_conditionally")
    clock = get_clock(broker_client)
    if clock < within:
        log.info("Attempting to close all positions")
        close_all_positions(trading_client)
        return True
    return False
