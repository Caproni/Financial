#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, StopOrderRequest, TrailingStopOrderRequest, StopLimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType, OrderClass
from alpaca.trading.models import Order
from requests.exceptions import ConnectionError, RequestException

from src.utils.logger import logger as log


def submit_order(
    client: TradingClient,
    symbol: str,
    quantity: float,
    side: OrderSide,
    order_type: OrderType,
    time_in_force: TimeInForce,
    limit_price: float = None,
    stop_price: float = None,
    trail_percent: float = None,
) -> Order:
    """Submits an order according to the specified inputs.

    Args:
        client (TradingClient): An Alpaca trading client
        symbol (str): A ticker / symbol to trade on
        quantity (float): A quantity of shares to trade
        side (OrderSide): Buy or sell
        order_type (OrderType): A type of order to submit
        time_in_force (TimeInForce): Lifetime of the submitted order
        limit_price (float): Only for limit orders. The worst fill price for a limit or stop limit order. Defaults to None.
        stop_price (float): Only for stop orders. The price at which the stop order is converted to a market order or a stop limit
            order is converted to a limit order. Defaults to None.
        trail_percent (float): Only for trailing stop orders. The percent price difference by which the trailing stop will trail. Defaults to None.

    Returns:
        Order: A submitted order.
    """
    log.info("Calling submit_order")
    
    # create order
    
    if order_type == OrderType.MARKET:
        log.debug("Order is a Market Order")
        order = MarketOrderRequest(
            symbol=symbol,
            qty=quantity,
            side=side,
            type=order_type,
            time_in_force=time_in_force,
            extended_hours=None,
            client_order_id=None,
            order_class=OrderClass.SIMPLE,
            take_profit=None,
            stop_loss=None,
        )
    elif order_type == OrderType.LIMIT:
        log.debug("Order is a Limit Order")
        if limit_price is None:
            log.critical("Limit Order attempted but limit_price parameter is None")
            raise RequestException("Limit Order attempted but limit_price parameter is None")
        order = LimitOrderRequest(
            symbol=symbol,
            qty=quantity,
            side=side,
            type=order_type,
            time_in_force=time_in_force,
            extended_hours=None,
            client_order_id=None,
            order_class=OrderClass.SIMPLE,
            take_profit=None,
            stop_loss=None,
            limit_price=limit_price,
        )
    elif order_type == OrderType.STOP:
        log.debug("Order is a Stop Order")
        if stop_price is None:
            log.critical("Limit Order attempted but stop_price parameter is None")
            raise RequestException("Limit Order attempted but stop_price parameter is None")
        order = StopOrderRequest(
            symbol=symbol,
            qty=quantity,
            side=side,
            type=order_type,
            time_in_force=time_in_force,
            extended_hours=None,
            client_order_id=None,
            order_class=OrderClass.SIMPLE,
            take_profit=None,
            stop_loss=None,
            stop_price=stop_price,
        )
    elif order_type == OrderType.TRAILING_STOP:
        log.debug("Order is a Trailing Stop Order")
        order = TrailingStopOrderRequest(
            symbol=symbol,
            qty=quantity,
            side=side,
            type=order_type,
            time_in_force=time_in_force,
            extended_hours=None,
            client_order_id=None,
            order_class=OrderClass.SIMPLE,
            take_profit=None,
            stop_loss=None,
            trail_percent=trail_percent,
        )
    elif order_type == OrderType.STOP_LIMIT:
        log.debug("Order is a Stop Limit Order")
        order = StopLimitOrderRequest(
            symbol=symbol,
            qty=quantity,
            side=side,
            type=order_type,
            time_in_force=time_in_force,
            extended_hours=None,
            client_order_id=None,
            order_class=OrderClass.SIMPLE,
            take_profit=None,
            stop_loss=None,
            stop_price=stop_price,
            limit_price=limit_price,
        )
    else:  # order type not supported
        raise RequestException(f"Order type: {order_type} not supported")
    
    # submit order

    try:
        return client.submit_order(
            order_data=order
        )
    except ConnectionError as ce:
        log.warning(f"Connection Error: {ce}")
        try:
            client.close_position(
                symbol_or_asset_id=symbol,
            )
        except ConnectionError as ce2:
            log.error(f"Second Connection Error: {ce2}") 
    except Exception as e:
        log.error(f"{e}")
