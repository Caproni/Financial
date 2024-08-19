#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from datetime import datetime
from sqlalchemy import and_
import sentry_sdk

from src.sql import (
    create_sql_client,
    get_data,
    PolygonMarketDataDay,
    PolygonMarketDataHour,
)
from src.univariate.analysis import calc_macd
from src.multivariate import calc_johansen_test, calc_linear_regression, calc_cadf
from src.multivariate.plots import plot_time_series, plot_vertical_bars
from src.univariate.plots import plot_bollinger_bands, plot_macd
from src.utils import log, align_time_series

sentry_sdk.init(
    dsn="https://8cd12a857607d331985d59a77ea0828e@o4507797009334272.ingest.de.sentry.io/4507797017133136",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

if __name__ == "__main__":

    log.info("Starting multivariate analysis.")

    database_client = create_sql_client()

    start_date = datetime(2024, 6, 1)
    end_date = datetime(2024, 7, 15)

    table = PolygonMarketDataHour
    symbol_1 = "GOOG"
    symbol_2 = "GOOGL"

    data_1 = get_data(
        database_client,
        models=[table],
        where_clause=and_(
            table.symbol == symbol_1,
            table.timestamp >= start_date,
            table.timestamp <= end_date,
        ),
    )

    data_2 = get_data(
        database_client,
        models=[table],
        where_clause=and_(
            table.symbol == symbol_2,
            table.timestamp >= start_date,
            table.timestamp <= end_date,
        ),
    )

    close_1 = [e["close"] for e in data_1]
    timestamps_1 = [e["timestamp"] for e in data_1]
    close_2 = [e["close"] for e in data_2]
    timestamps_2 = [e["timestamp"] for e in data_2]

    timestamps, close_1, close_2 = align_time_series(
        datetime1=timestamps_1,
        values1=close_1,
        datetime2=timestamps_2,
        values2=close_2,
    )

    plot_time_series(
        {
            symbol_1: (timestamps_1, close_1),
            symbol_2: (timestamps_2, close_2),
        },
        title=f"Time-series of {symbol_1} and {symbol_2}",
    )

    plot_bollinger_bands(
        data=close_1,
        timestamps=timestamps_1,
        title=f"Bollinger Bands {symbol_1}",
    )

    plot_macd(
        *calc_macd(data=close_1),
        timestamps=timestamps_1,
        title=f"MACD {symbol_1}",
    )

    plot_bollinger_bands(
        data=close_2,
        timestamps=timestamps_2,
        title=f"Bollinger Bands {symbol_2}",
    )

    plot_macd(
        *calc_macd(data=close_2),
        timestamps=timestamps_2,
        title=f"MACD {symbol_2}",
    )

    johansen_test_result = calc_johansen_test(
        v1=close_1,
        v2=close_2,
        lag=0,
    )

    cadf_test_result = calc_cadf(
        data_1=close_1,
        data_2=close_2,
    )

    linear_regression_results = calc_linear_regression(
        data_1=close_1,
        data_2=close_2,
    )

    stationary = [
        linear_regression_results["slope"] * x - y for x, y in zip(close_1, close_2)
    ]

    plot_vertical_bars(
        {
            "Stationary": stationary,
        },
        timestamps=timestamps_1,
        title=f"Stationary time-series of {symbol_1} and {symbol_2}",
    )

    log.info("Completed multivariate analysis.")
