#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from typing import Any
from polygon import RESTClient
from datetime import datetime

from src.utils import log


def list_tickers(
    client: RESTClient,
    market: str | None = None,
    active: bool | None = None,
) -> list[dict[str, Any]]:
    log.info("Calling list_tickers")

    try:
        response = client.list_tickers(
            market=market,
            active=active,
        )
    except Exception as e:
        log.error("Could not retrieve list of tickers from polygon")
        log.info(f"Error: {e}")
        return None

    return [
        {
            "active": e.active,
            "base_currency_name": e.base_currency_name,
            "base_currency_symbol": e.base_currency_symbol,
            "cik": e.cik,
            "composite_figi": e.composite_figi,
            "currency_name": e.currency_name,
            "currency_symbol": e.currency_symbol,
            "delisted_utc": (
                datetime.fromisoformat(e.delisted_utc)
                if e.delisted_utc is not None
                else None
            ),
            "last_updated_utc": (
                datetime.fromisoformat(e.last_updated_utc)
                if e.last_updated_utc is not None
                else None
            ),
            "locale": e.locale,
            "market": e.market,
            "name": e.name,
            "primary_exchange": e.primary_exchange,
            "share_class_figi": e.share_class_figi,
            "source_feed": e.source_feed,
            "ticker": e.ticker,
            "type": e.type,
        }
        for e in response
    ]
