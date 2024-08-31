#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os import getenv
import sentry_sdk
from dotenv import load_dotenv

from src.viz import plot_history
from src.mongo import create_mongo_client
from src.utils import log

load_dotenv()

sentry_sdk.init(
    dsn=getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

if __name__ == "__main__":

    log.info("Starting visualization.")

    mongo_client = create_mongo_client()

    plot_history(
        mongo_client,
        symbol="SHEL",
        news_flag=True,
        news_item_alignment="h",
        collection="polygon_market_data_day",
    )

    log.info("Completed visualization.")
