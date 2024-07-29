#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""


from src.viz import plot_history
from src.utils import log


if __name__ == "__main__":

    log.info("Starting summary calculations.")

    plot_history(
        symbol="A",
        news_flag=True,
        news_item_alignment="H",
        collection="polygon_market_data_day",
    )

    log.info("Completed summary calculations.")
