#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os import getenv
import sentry_sdk
from datetime import datetime
from dotenv import load_dotenv

from src.sql import create_sql_client, get_data, LiquidTickers
from src.ml import predict_daily_trend_trainer
from src.utils import log

load_dotenv()

sentry_sdk.init(
    dsn=getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

if __name__ == "__main__":

    log.info("Started training models.")

    liquid_tickers = get_data(
        database_client=create_sql_client(),
        models=[LiquidTickers],
    )

    symbols = [liquid_ticker["symbol"] for liquid_ticker in liquid_tickers]

    predict_daily_trend_trainer(
        start_timestamp=datetime(2019, 9, 1),
        end_timestamp=None,
        symbols=symbols,
        diagnostic_plots_flag=False,
    )

    log.info("Completed training models.")
