#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from requests.exceptions import ConnectionError

from src.utils.logger import logger as log


def submit_order(
    client: TradingClient,
    symbol: str,
    quantity: float,
    side: OrderSide,
    order_type: OrderType,
    time_in_force: TimeInForce,
):
    """_summary_

    Args:
        client (TradingClient): _description_
        symbol (str): _description_
        quantity (float): _description_
        side (OrderSide): _description_
        order_type (OrderType): _description_
        time_in_force (TimeInForce): _description_

    Raises:
        e: _description_

    Returns:
        _type_: _description_
    """
    log.info("Calling submit_order")

    try:
        return client.submit_order(
            order_data=MarketOrderRequest(
                symbol=symbol,
                qty=quantity,
                side=side,
                type=order_type,
                time_in_force=time_in_force,
            )
        )
    except Exception as e:
        log.critical(f"{e}")
        raise e
