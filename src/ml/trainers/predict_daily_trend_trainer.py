#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os.path import abspath, join, dirname
from sqlalchemy import and_
import pandas as pd
from datetime import datetime

from src.ml.models import predict_binary_daily_trend
from src.sql import create_sql_client, get_data, PolygonMarketDataHour
from src.utils import log, save_object_as_pickle


def predict_daily_trend_trainer() -> None:
    """
    Wrapper function to train the Predict Daily Trend predictive model and save the results.
    """
    log.function_call()

    database_client = create_sql_client()

    data = get_data(
        database_client,
        models=[PolygonMarketDataHour],
        where_clause=and_(
            PolygonMarketDataHour.timestamp >= datetime(2024, 4, 1),
            PolygonMarketDataHour.symbol == "AAPL",
        ),
    )

    if data is None:
        log.error("Failed to obtain training data.")
        return None

    final_model, performance_info, predictions_df = predict_binary_daily_trend(
        data=pd.DataFrame(data),
    )

    output_save_path = abspath(join(dirname(__file__), "../../../staging"))

    save_object_as_pickle(
        final_model,
        join(output_save_path, "binary_daily_trend_model.pkl"),
    )

    save_object_as_pickle(
        performance_info,
        join(output_save_path, "binary_daily_trend_performance_info.pkl"),
    )

    save_object_as_pickle(
        predictions_df,
        join(output_save_path, "binary_daily_trend_predictions_df.pkl"),
    )

    log.info(f"Results: {predictions_df}")
