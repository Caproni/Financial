#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from datetime import datetime, timedelta
from alpaca.broker.client import BrokerClient

from src.brokerage.alpaca.broker import get_calendar
from src.utils import log


def get_timestamp_information(
    client: BrokerClient,
    timestamps: list[datetime],
) -> list[dict[str, Any]]:
    """
    Retrieve timestamp information based on provided timestamps and a broker client.
    Timestamps must not be timezone aware but must be in ET.

    This function checks the timezone information of each timestamp, retrieves the trading calendar
    from the broker client, and constructs a list of dictionaries containing details about each timestamp,
    including trading hours and whether the market is open.

    Args:
        client (BrokerClient): The broker client used to access trading calendar information.
        timestamps (list[datetime]): A list of datetime objects for which to retrieve trading information. Timestamps must not be timezone aware but must be in ET.

    Returns:
        list[dict[str, Any]]: A list of dictionaries, each containing information about the corresponding
        timestamp, including day of the week, open and close times, and market status.

    Raises:
        AssertionError: If any timestamp has timezone information.
    """
    log.function_call()

    for timestamp in timestamps:
        assert (
            timestamp.tzinfo is None
        ), f"Timestamp: {timestamp} must be timezone agnostic."

    calendar = get_calendar(client)

    information: list[dict[str, Any]] = []
    for timestamp in timestamps:
        payload = {
            "timestamp": timestamp,
            "day_of_week": timestamp.weekday(),  # 0 = Monday, 6 = Sunday
            "open": None,
            "close": None,
            "is_open": None,
            "first_hour": None,
            "last_hour": None,
            "previous_trading_date": None,
        }

        index = None
        if calendar_dates := [e for e in calendar if e.date == timestamp.date()]:
            dt = calendar_dates[0]
            payload["date"] = dt.date
            payload["open"] = dt.open
            payload["close"] = dt.close
            payload["is_open"] = timestamp >= dt.open and timestamp <= dt.close
            payload["first_hour"] = payload[
                "is_open"
            ] and timestamp <= dt.open + timedelta(hours=1)
            payload["last_hour"] = (
                payload["is_open"] and timestamp + timedelta(hours=1) >= dt.close
            )
            index = next(
                (i for i, e in enumerate(calendar) if e.date == timestamp.date()), None
            )

        if index is not None:
            payload["previous_trading_date"] = calendar[index - 1].date

        information.append(payload)

    return information
