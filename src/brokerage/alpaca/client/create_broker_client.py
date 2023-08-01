#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.broker.client import BrokerClient
from dotenv import load_dotenv
from os import getenv

from src.utils.logger import logger as log


def create_broker_client(
    sandbox: bool = True,
) -> BrokerClient:
    log.info("Calling create_broker_client")
    load_dotenv()
    return BrokerClient(
        api_key=getenv("ALPACA_PAPER_KEY") if sandbox else getenv("ALPACA_LIVE_KEY"),
        secret_key=getenv("ALPACA_PAPER_SECRET")
        if sandbox
        else getenv("ALPACA_LIVE_SECRET"),
        sandbox=sandbox,
    )
