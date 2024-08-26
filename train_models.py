#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import sentry_sdk
from datetime import datetime

from src.sql import create_sql_client, get_data, LiquidTickers
from src.ml import predict_daily_trend_trainer
from src.utils import log

sentry_sdk.init(
    dsn="https://8cd12a857607d331985d59a77ea0828e@o4507797009334272.ingest.de.sentry.io/4507797017133136",
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
        start_timestamp=datetime(2020, 4, 1),
        end_timestamp=None,
        symbols=symbols,
    )

    log.info("Completed training models.")
