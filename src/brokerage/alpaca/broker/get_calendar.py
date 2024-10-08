#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.broker.client import BrokerClient
from alpaca.trading.models import Calendar

from src.utils import log


def get_calendar(
    client: BrokerClient,
) -> list[Calendar]:
    """Gets an Alpaca calendar

    Args:
        client (BrokerClient): An Alpaca broker client

    Returns:
        list[Calendar]: A list of Calendar objects
    """
    log.function_call()

    return client.get_calendar()
