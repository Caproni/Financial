#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from datetime import datetime
from sqlalchemy import and_

from src.sql import (
    create_sql_client,
    get_data,
    PolygonMarketDataDay,
    PolygonMarketDataHour,
)
from src.univariate.analysis import calc_macd
from src.multivariate import calc_johansen_test, calc_linear_regression, calc_cadf
from src.multivariate.plots import plot_time_series
from src.univariate.plots import plot_bollinger_bands, plot_macd
from src.utils import log


if __name__ == "__main__":

    log.info("Starting multivariate analysis.")

    database_client = create_sql_client()

    start_date = datetime(2024, 4, 1)
    end_date = datetime(2024, 6, 15)

    table = PolygonMarketDataDay

    data_1 = get_data(
        database_client,
        models=[table],
        where_clause=and_(
            table.symbol == "KMI",
            table.timestamp >= start_date,
            table.timestamp <= end_date,
        ),
    )

    data_2 = get_data(
        database_client,
        models=[table],
        where_clause=and_(
            table.symbol == "TRP",
            table.timestamp >= start_date,
            table.timestamp <= end_date,
        ),
    )
    
    N1 = len(data_1)
    N2 = len(data_2)
    
    if N1 > N2:
        log.warning("Arrays not of same length. Truncating first time-series.")
        data_1 = data_1[:N2]
    elif N2 > N1:
        log.warning("Arrays not of same length. Truncating second time-series.")
        data_2 = data_2[:N1]

    close_1 = [e["close"] for e in data_1]
    timestamps_1 = [e["timestamp"] for e in data_1]
    close_2 = [e["close"] for e in data_2]
    timestamps_2 = [e["timestamp"] for e in data_2]

    plot_time_series(
        {
            "KMI": close_1,
            "TRP": close_2,
        }
    )

    plot_bollinger_bands(data=close_1)

    plot_macd(
        *calc_macd(data=close_1),
        timestamps=timestamps_1,
    )

    plot_bollinger_bands(data=close_2)

    plot_macd(
        *calc_macd(data=close_2),
        timestamps=timestamps_2,
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

    scaled_close_1 = [-e * linear_regression_results["slope"] for e in close_1]

    stationary = scaled_close_1 + close_2

    plot_time_series(
        {
            "Stationary": stationary,
        }
    )

    log.info("Completed multivariate analysis.")
