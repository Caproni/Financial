#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from requests.exceptions import ConnectionError

from src.utils.logger import logger as log


def get_assets(
    client: TradingClient,
    status: str = None,
    asset_class: str = None,
    exchange: str = None,
):
    """Gets a list of tradable assets

    Args:
        client (TradingClient): An Alpaca trading client
        status (str, optional): _description_. Defaults to None.
        asset_class (str, optional): _description_. Defaults to None.
        exchange (str, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    log.info("Calling get_assets")
    return client.get_all_assets(
        filter=GetAssetsRequest(
            status=status,
            asset_class=asset_class,
            exchange=exchange,
        )
    )
