#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""


from src.viz import plot_history
from src.mongo import create_mongo_client
from src.utils import log


if __name__ == "__main__":

    log.info("Starting visualization.")

    mongo_client = create_mongo_client()

    plot_history(
        mongo_client,
        symbol="SHEL",
        news_flag=True,
        news_item_alignment="H",
        collection="polygon_market_data_day",
    )

    log.info("Completed visualization.")
