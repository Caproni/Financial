#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from alpaca.trading.client import TradingClient
from dotenv import load_dotenv
from os import getenv

from src.utils import log


def create_trading_client(
    paper: bool = True,
) -> TradingClient:
    log.info("Calling create_trading_client")
    load_dotenv()
    return TradingClient(
        api_key=getenv("ALPACA_PAPER_KEY") if paper else getenv("ALPACA_LIVE_KEY"),
        secret_key=getenv("ALPACA_PAPER_SECRET")
        if paper
        else getenv("ALPACA_LIVE_SECRET"),
        paper=paper,
    )
