#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from datetime import datetime

from src.brokerage.alpaca.client import create_broker_client
from src.brokerage.alpaca.utils import get_timestamp_information


def test_get_timestamp_information():
    broker_client = create_broker_client()
    information = get_timestamp_information(
        client=broker_client,
        timestamps=[
            datetime(2024, 8, 19, 16, 0, 0),
            datetime(2024, 8, 19, 23, 0, 0),
            datetime(2024, 1, 1, 0, 0, 0),
        ],
    )

    assert len(information) == 3
    assert information[0]["open"] == datetime(2024, 8, 19, 9, 30)
