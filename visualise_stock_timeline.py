#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import sentry_sdk

from src.viz import plot_history
from src.mongo import create_mongo_client
from src.utils import log

sentry_sdk.init(
    dsn="https://8cd12a857607d331985d59a77ea0828e@o4507797009334272.ingest.de.sentry.io/4507797017133136",
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
