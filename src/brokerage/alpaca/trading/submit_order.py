#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from src.utils.logger import logger as log


def submit_order(
    client: TradingClient,
    symbol: str,
    quantity: float,
    side: OrderSide,
    time_in_force: TimeInForce,
):
    log.info("Calling submit_order")

    try:
        return client.submit_order(
            order_data=MarketOrderRequest(
                symbol=symbol,
                qty=quantity,
                side=side,
                time_in_force=time_in_force,
            )
        )
    except Exception as e:
        log.critical(f"{e}")
        raise e
