#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from os.path import abspath, join, dirname
from json import dumps, loads
from sqlalchemy import and_, text
import pandas as pd
from datetime import datetime
from uuid import UUID

from src.minio import create_minio_client
from src.ml.models import predict_binary_daily_trend
from src.sql import (
    create_sql_client,
    get_data,
    PolygonMarketDataDay,
    Models,
)
from src.cache import PersistentCache, generate_key
from src.utils import log


def predict_daily_trend_trainer(
    symbols: list[str],
    start_timestamp: datetime | None = None,
    end_timestamp: datetime | None = None,
    diagnostic_plots_flag: bool = False,
) -> list[dict[str, Any]]:
    """
    Wrapper function to train the Predict Daily Trend predictive model and save the results.
    """
    log.function_call()
    
    input_model_list: str | None = "generated_models_2024-09-22T195501.581838.json"

    database_client = create_sql_client()
    minio_client = create_minio_client()

    cache = PersistentCache(cache_dir="staging")

    output_save_path = abspath(join(dirname(__file__), "../../../staging"))

    where_clause_daily = and_(
        PolygonMarketDataDay.timestamp >= start_timestamp,
        PolygonMarketDataDay.symbol.in_(symbols),
    )

    if end_timestamp is not None:
        where_clause_daily = and_(
            PolygonMarketDataDay.timestamp <= end_timestamp,
            where_clause_daily,
        )

    daily_data = cache.get(
        generate_key(
            database_client,
            models=[PolygonMarketDataDay],
            where_clause=where_clause_daily,
        )
    )
    if daily_data is None:
        daily_data = get_data(
            database_client,
            models=[PolygonMarketDataDay],
            where_clause=where_clause_daily,
        )
    
    now = datetime.now()
    
    if input_model_list is None:
        log.info("Started training models.")
        model_ids = predict_binary_daily_trend(
            minio_client=minio_client,
            database_client=database_client,
            daily_data=pd.DataFrame(daily_data),
            serving_set_size=40,
            threshold_percentage=0.50,
            diagnostic_plots_flag=diagnostic_plots_flag,
        )
        log.info("Completed training models.")
        
        input_model_list = f"generated_models_{now.isoformat().replace(':', '')}.json"

        log.info(f"Saving model ids to: {join(output_save_path, input_model_list)}")

        with open(join(output_save_path, f"generated_models_{now.isoformat().replace(":", "")}.json"), "w") as f:
            f.writelines(dumps(model_ids))

    log.info("Loading model ids.")
    
    with open(join(output_save_path, input_model_list), "r") as f:
        model_ids = [UUID(e) for e in loads(f.read())]
    
    log.info("Get model metadata.")

    models = get_data(
        database_client=database_client,
        models=[Models],
        where_clause=and_(
            Models.model_id.in_(model_ids),
            Models.precision > 0.6,
            Models.training_set_rows > 200,
            text("cast(serving_set_indicated_entry_prices::json->>0 AS Float) >= 0.01")
        ),
        as_dict=True,
    )
    
    log.info("Split models according to threshold percentage.")
    
    standard_models, positive_threshold_models, negative_threshold_models = [], [], []
    for model in models:
        log.info(f"Model: {model["model_id"]}")
        if model["threshold_percentage"] == 0.0:
            standard_models.append(model)
        elif model["threshold_percentage"] > 0.0:
            positive_threshold_models.append(model)
        elif model["threshold_percentage"] < 0.0:
            negative_threshold_models.append(model)

    combined_profits: list[dict[str, Any]] = []
    for standard_model in standard_models:
        accuracy = standard_model["accuracy"]
        balanced_accuracy = standard_model["balanced_accuracy"]
        precision = standard_model["precision"]
        training_set_rows = standard_model["training_set_rows"]
        log.info(
            f"Accuracy / balanced accuracy / precision for symbol: {standard_model['symbols']} is {accuracy} / {balanced_accuracy} / {precision}"
        )
        log.info(f"Number of training set rows is: {training_set_rows}")
        long_positions, long_profits, short_positions, short_profits = [], [], [], []
        log.info("Model usage criteria met. Evaluating model.")
        positive_threshold_model = [e for e in positive_threshold_models if e["symbols"] == standard_model["symbols"]]
        negative_threshold_model = [e for e in negative_threshold_models if e["symbols"] == standard_model["symbols"]]
        
        if not positive_threshold_model and not negative_threshold_model:
            log.info("No threshold models found.")
            continue

        if (
            loads(standard_model["serving_set_indicated_exit_prices"]) is not None
            and loads(standard_model["serving_set_indicated_entry_prices"]) is not None
        ):
            for i, (a, b, go_long) in enumerate(
                zip(
                    loads(standard_model["serving_set_indicated_exit_prices"]),
                    loads(standard_model["serving_set_indicated_entry_prices"]),
                    loads(standard_model["y_serve_pred"]),
                )
            ):
                if go_long and positive_threshold_model and loads(positive_threshold_model[0]["y_serve_pred"])[i] == 1:
                    long_positions.append(b)
                    long_profits.append(a - b)
                elif not go_long and negative_threshold_model and loads(negative_threshold_model[0]["y_serve_pred"])[i] == 1:
                    short_positions.append(b)
                    short_profits.append(b - a)

        combined_profits.append(
            {
                "symbols": standard_model["symbols"],
                "number_long_positions": len(long_positions),
                "number_short_positions": len(short_positions),
                "long_positions": long_positions,
                "long_profits": long_profits,
                "short_positions": short_positions,
                "short_profits": short_profits,
            }
        )

    return combined_profits
