#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import OrderSide, OrderSide, QueryOrderStatus
from requests.exceptions import ConnectionError
from datetime import datetime

from src.utils.logger import logger as log


def get_orders(
    client: TradingClient,
    status: QueryOrderStatus | None = None,
    symbols: list[str] | None = None,
    side: OrderSide | None = None,
    after: datetime | None = None,
    until: datetime | None = None,
    direction: bool | None = None,
    nested: bool | None = None,
    limit: int | None = None,
):
    log.info("Calling get_orders")

    try:
        return client.get_orders(
            filter=GetOrdersRequest(
                status=status,
                limit=limit,
                after=after,
                until=until,
                direction=direction,
                nested=nested,
                side=side,
                symbols=symbols,
            )
        )
    except Exception as e:
        log.critical(f"{e}")
        raise e
