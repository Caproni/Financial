#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os.path import abspath, join, dirname
from os import remove
from uuid import uuid4
from json import dumps
from sqlalchemy import and_
import pandas as pd
from datetime import datetime

from src.ml.models import predict_binary_daily_trend
from src.minio import create_minio_client, upload_file
from src.sql import (
    create_sql_client,
    get_data,
    insert_data,
    PolygonMarketDataDay,
    Models,
)
from src.cache import PersistentCache, generate_key
from src.utils import log, save_object_as_pickle


def predict_daily_trend_trainer(
    symbols: list[str],
    start_timestamp: datetime | None = None,
    end_timestamp: datetime | None = None,
) -> None:
    """
    Wrapper function to train the Predict Daily Trend predictive model and save the results.
    """
    log.function_call()
    
    database_client = create_sql_client()

    minio_client = create_minio_client()

    cache = PersistentCache(cache_dir="staging")

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

    performance_info = predict_binary_daily_trend(
        daily_data=pd.DataFrame(daily_data),
        serving_set_size=40,
        threshold_percentage=0.0,
    )

    theoretical_max_profits = []
    for info in performance_info:
        accuracy = info["accuracy"]
        balanced_accuracy = info["balanced_accuracy"]
        log.info(
            f"Accuracy / balanced accuracy for symbol: {info['symbols']} is {accuracy} / {balanced_accuracy}"
        )
        long_positions, long_profits, short_positions, short_profits = [], [], [], []
        if accuracy > 0.6 and balanced_accuracy > 0.6:
            log.info("The model indicates a purchase here.")
            if (
                info["serving_set_indicated_exit_prices"] is not None
                and info["serving_set_indicated_entry_prices"] is not None
            ):
                for a, b, go_long in zip(
                    info["serving_set_indicated_exit_prices"],
                    info["serving_set_indicated_entry_prices"],
                    info["y_serve_pred"],
                ):
                    if go_long:
                        long_positions.append(b)
                        long_profits.append(a - b)
                    else:
                        short_positions.append(b)
                        short_profits.append(b - a)

        theoretical_max_profits = long_profits + short_profits

    log.info(
        f"Including: {len(long_positions)} long positions with a total value of: {sum(long_positions)}"
    )
    log.info(
        f"Including: {len(short_positions)} short positions with a total value of: {sum(short_positions)}"
    )
    log.info(
        f"Summed profits from: {len(theoretical_max_profits)} positions assuming equal weighting of shares: {sum(theoretical_max_profits)}"
    )
    log.info(f"Profits from long positions: {sum(long_profits)}")
    log.info(f"Profits from short positions: {sum(short_profits)}")

    output_save_path = abspath(join(dirname(__file__), "../../../staging"))

    parts = {
        "all",
        "model",
        "training_data",
        "training_targets",
        "test_data",
        "test_targets",
        "serving_data",
        "serving_targets",
    }

    models = []
    for info in performance_info:
        log.info("Saving model components to object store.")

        for part in parts:
            partial_filename = f"binary_daily_trend_performance_info_{info['symbols'][0]}_{info['timestamp'].isoformat().replace(":", "")}"
            filename = f"{partial_filename}_{part}.pkl.gz"
            local_save_path = join(output_save_path, filename)

            if part == "all":
                save_object_as_pickle(info, local_save_path)
            else:
                save_object_as_pickle(info[part], local_save_path)

            upload_file(
                minio_client=minio_client,
                bucket_name="models",
                object_name=filename,
                file_path=local_save_path,
            )

            remove(local_save_path)

        log.info("Saving model metadata.")

        models.append(
            Models(
                model_id=uuid4(),
                model_url=f"{partial_filename}_model.pkl.gz",
                symbols=dumps(info["symbols"]),
                features=dumps(info["features"]),
                confusion_matrix=str(info["confusion_matrix"]),
                classification_report=str(info["classification_report"]),
                training_set_rows=info["training_set_rows"],
                training_data_url=f"{partial_filename}_training_data.pkl.gz",
                training_targets_url=f"{partial_filename}_training_targets.pkl.gz",
                test_set_rows=info["test_set_rows"],
                test_data_url=f"{partial_filename}_test_data.pkl.gz",
                test_targets_url=f"{partial_filename}_test_targets.pkl.gz",
                serving_set_rows=info["serving_set_rows"],
                serving_data_url=f"{partial_filename}_serving_data.pkl.gz",
                serving_targets_url=f"{partial_filename}_serving_targets.pkl.gz",
                accuracy=info["accuracy"],
                balanced_accuracy=info["balanced_accuracy"],
                precision=info["precision"],
                y_serve=dumps(info["y_serve"]),
                y_serve_pred=dumps(info["y_serve_pred"]),
                serving_set_indicated_entry_prices=dumps(
                    info["serving_set_indicated_entry_prices"]
                ),
                serving_set_indicated_exit_prices=dumps(
                    info["serving_set_indicated_exit_prices"]
                ),
                last_modified_at=info["timestamp"],
                created_at=info["timestamp"],
            )
        )

    success = insert_data(
        database_client=database_client,
        documents=models,
    )

    log.info(f"Metadata database insertion success: {success}")

    log.info(f"Results: {performance_info}")
