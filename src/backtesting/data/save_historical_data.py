#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from os.path import isfile
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical.stock import Bar
from datetime import datetime
from json import dump, JSONEncoder

from src.brokerage.alpaca.data import get_stock_bars
from src.utils import log


def save_historical_data(
    data_save_path: str,
    data_client: StockHistoricalDataClient,
    symbols: list[str],
    timeframe: TimeFrame,
    start: datetime,
    end: datetime,
    replace: bool = False,
) -> None:
    """_summary_

    Args:
        data_save_path (str): _description_
        data_client (StockHistoricalDataClient): _description_
        symbols (list[str]): _description_
        timeframe (TimeFrame): _description_
        start (datetime): _description_
        end (datetime): _description_
        replace (bool, optional): _description_. Defaults to False.

    """
    log.info("save_historical_data")

    class DateTimeEncoder(JSONEncoder):
        def default(self, o):
            if isinstance(o, Bar):
                return dict(o)
            if isinstance(o, datetime):
                return o.isoformat()
            return super().default(o)

    for symbol in symbols:
        symbol_path = data_save_path.replace(".json", f"_{symbol.lower()}.json")
        if not replace and isfile(symbol_path):
            continue
        bars = get_stock_bars(
            client=data_client,
            symbols=[symbol],
            timeframe=timeframe,
            start=start,
            end=end,
        )

        if not bars:
            continue
        with open(symbol_path, "w") as data_file:
            dump(
                bars,
                data_file,
                cls=DateTimeEncoder,
                indent=4,
            )
