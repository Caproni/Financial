#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from requests.exceptions import ConnectionError
from alpaca.trading.models import Asset

from src.utils.logger import logger as log


def get_assets(
    client: TradingClient,
    status: str = None,
    asset_class: str = None,
    exchange: str = None,
) -> list[Asset]:
    """Gets a list of tradable assets

    Args:
        client (TradingClient): An Alpaca trading client
        status (str, optional): Filters on asset status. Defaults to None.
        asset_class (str, optional): Filter on asset class. "crypto" or "us_equity". Defaults to None.
        exchange (str, optional): Filter on exchange. Defaults to None.

    Returns:
        list[Asset]: A list of assets / symbols
    """
    log.info("Calling get_assets")
    try:
        return client.get_all_assets(
            filter=GetAssetsRequest(
                status=status,
                asset_class=asset_class,
                exchange=exchange,
            )
        )
    except ConnectionError as e:
        log.critical(f"Error: {e}")
        raise e
