#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import OrderSide, OrderSide, QueryOrderStatus
from datetime import datetime

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
