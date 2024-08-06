#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from datetime import datetime
from sqlalchemy import and_

from src.sql import create_sql_client, get_data, PolygonMarketDataDay
from src.multivariate import calc_johansen_test
from src.utils import log


if __name__ == "__main__":

    log.info("Starting multivariate analysis.")

    database_client = create_sql_client()

    start_date = datetime(2024, 1, 1)

    kmi_data = get_data(
        database_client,
        models=[PolygonMarketDataDay],
        where_clause=and_(
            PolygonMarketDataDay.symbol == "KMI",
            PolygonMarketDataDay.timestamp >= start_date,
        ),
    )

    tce_data = get_data(
        database_client,
        models=[PolygonMarketDataDay],
        where_clause=and_(
            PolygonMarketDataDay.symbol == "TRP",
            PolygonMarketDataDay.timestamp >= start_date,
        ),
    )

    result = calc_johansen_test(
        v1=[e["close"] for e in kmi_data],
        v2=[e["close"] for e in tce_data],
        lag=1,
    )

    log.info("Completing multivariate analysis.")
