#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sqlalchemy import and_
import pandas as pd
from datetime import datetime

from src.ml.models import predict_daily_trend
from src.sql import create_sql_client, get_data, PolygonMarketDataHour
from src.utils import log


def predict_daily_trend_trainer() -> None:
    log.function_call()
    
    database_client = create_sql_client()

    data = get_data(
        database_client,
        models=[PolygonMarketDataHour],
        where_clause=and_(
            PolygonMarketDataHour.timestamp >= datetime(2024, 1, 1),
            PolygonMarketDataHour.symbol == "AAPL",
        ),
    )

    if data is None:
        log.error("Failed to obtain training data.")
        return None

    model, conf_matrix, class_report, accuracy = predict_daily_trend(
        data=pd.DataFrame(data),
    )

    log.info(f"Confusion Matrix: {conf_matrix}")
