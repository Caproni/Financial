#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os import getenv
import sentry_sdk
from dotenv import load_dotenv

from src.viz import plot_history
from src.utils import log

load_dotenv()

sentry_sdk.init(
    dsn=getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

if __name__ == "__main__":

    log.info("Starting summary calculations.")

    plot_history(
        symbol="A",
        news_flag=True,
        news_item_alignment="H",
        collection="polygon_market_data_day",
    )

    log.info("Completed summary calculations.")
