#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import pandas as pd
import xgboost as xgb
from datetime import timedelta
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
from sklearn.model_selection import train_test_split
import numpy as np
from datetime import datetime

from src.ml.viz import plot_pca_results
from src.ml.utils import one_hot_encode
from src.univariate.analysis import calc_macd
from src.utils import log


np.random.seed(1729)


def predict_binary_daily_trend(
    daily_data: pd.DataFrame,
    serving_set_size: int,
    threshold_percentage: float = 0.0,
    diagnostic_plots_flag: bool = False,
):
    """
    Predicts the daily trend of stock prices based on historical data.

    This function analyzes stock price data to determine whether the price will rise or fall by the end of the trading day. It employs machine learning techniques to train a model for each stock symbol using various features derived from the data.

    Args:
        daily_data (pd.DataFrame): A DataFrame containing stock price data with columns including 'timestamp', 'symbol', 'close', 'open', 'high', 'low', and 'volume'.
        serving_set_size (int): The number of rows to be included in a serving set.
        threshold_percentage (float): Percentage added to the entry price. A prediction of 1 indicates that the exit price will have moved by at least this percentage. 
        diagnostic_plots_flag (bool): Whether to produce diagnostic plots. Defaults to False.

    Returns:
        performance_info: A list of dictionaries containing performance metrics for each prediction.

    Examples:
        >>> predictions = predict_daily_trend(data)
    """
    log.function_call()

    threshold_percentage = abs(threshold_percentage)

    daily_data = daily_data.set_index("timestamp")
    daily_data = daily_data.sort_index()

    daily_data["date"] = daily_data.index.date
    daily_data["timestamp"] = daily_data.index.date
    daily_data["daily_hour"] = daily_data.index.hour
    daily_data["weekday"] = daily_data.index.dayofweek
    daily_data = one_hot_encode(
        daily_data,
        column="weekday",
        value_mapping={
            0: "monday",
            1: "tuesday",
            2: "wednesday",
            3: "thursday",
            4: "friday",
        },
    )
    daily_data = daily_data.drop(labels=["data_id", "otc", "high", "low"], axis=1)
    daily_data = daily_data.rename(
        columns={
            "open": "daily_open",
            "close": "daily_close",
            "volume": "daily_volume",
            "transactions": "daily_transactions",
            "vwap": "daily_vwap",
        }
    )

    performance_info = []

    features = [
        "daily_open",  # care should be taken here - daily_open and daily_close are first used to calculate the target variable and then shifted
        "daily_close",
        "daily_macd_histogram",
        # "daily_macd_first_derivative",  # PCA indicates that these are not useful
        # "weekday_monday",
        # "weekday_tuesday",
        # "weekday_wednesday",
        # "weekday_thursday",
        # "weekday_friday",
        "target_date_daily_open",  # this is the open price on the market data for which a prediction is required
    ]

    targets = [
        "target",
        "positive_threshold_target",
        "negative_threshold_target",
    ]

    for symbol, daily_symbol_data in daily_data.groupby("symbol"):
        if daily_symbol_data.empty:
            log.info(f"No daily data available for the selected symbol: {symbol}")
            continue

        daily_symbol_data["price_change"] = (
            daily_symbol_data["daily_close"]
            > daily_symbol_data["daily_open"]
        ).astype(int)

        daily_symbol_data["positive_threshold_price_change"] = (
            daily_symbol_data["daily_close"]
            > daily_symbol_data["daily_open"] * (1 + (threshold_percentage / 100))
        ).astype(int)

        daily_symbol_data["negative_threshold_price_change"] = (
            daily_symbol_data["daily_close"]
            < daily_symbol_data["daily_open"] * (1 + (-threshold_percentage / 100))
        ).astype(int)

        daily_symbol_data["target"] = daily_symbol_data["price_change"].shift(-1)
        daily_symbol_data["positive_threshold_target"] = daily_symbol_data["positive_threshold_price_change"].shift(-1)
        daily_symbol_data["negative_threshold_target"] = daily_symbol_data["negative_threshold_price_change"].shift(-1)

        daily_symbol_data = daily_symbol_data.dropna(
            subset=["target", "positive_threshold_target", "negative_threshold_target"],
        )
        daily_symbol_data["target"] = daily_symbol_data["target"].astype(int)
        daily_symbol_data["positive_threshold_target"] = daily_symbol_data["positive_threshold_target"].astype(int)
        daily_symbol_data["negative_threshold_target"] = daily_symbol_data["negative_threshold_target"].astype(int)

        _, _, daily_macd_histogram, daily_macd_first_derivative = calc_macd(
            data=daily_symbol_data["daily_close"].to_list(),
        )
        daily_symbol_data["daily_macd_histogram"] = daily_macd_histogram
        daily_symbol_data["daily_macd_first_derivative"] = daily_macd_first_derivative

        serving_set: None | pd.DataFrame = None
        prediction_inputs: None | pd.DataFrame = None
        for date, _ in daily_symbol_data.iterrows():

            if date.weekday() in [5, 6]:
                log.info("Date is on the weekend.")
                continue

            days_prior = 1
            if date.weekday() == 0:  # Monday
                days_prior = 3  # previous Friday

            # Use data from trading date before the current date for training
            daily_training_data = daily_symbol_data[
                daily_symbol_data["date"] == date.date() - timedelta(days=days_prior)
            ]

            daily_training_data = daily_training_data.dropna()

            if daily_training_data.empty:
                log.info(
                    f"No daily data available for the selected date: {date} and symbol: {symbol}"
                )
                continue

            # Check that the markets opened that morning
            daily_open = daily_symbol_data[
                daily_symbol_data["date"] == date.date()
            ].copy()
            daily_open = daily_open.dropna()

            if daily_open.empty:
                log.warning("No available open data for this day.")
                continue

            daily_open = daily_open.rename(
                columns={
                    "daily_open": "target_date_daily_open",
                    "daily_close": "target_date_daily_close",
                }
            )

            prediction_input = daily_training_data.copy()
            prediction_input["target_date_daily_open"] = daily_open[
                "target_date_daily_open"
            ].to_list()  # the model will be ran after market open so this will be known
            prediction_input["target_date_daily_close"] = daily_open[
                "target_date_daily_close"
            ].to_list()  # this will not be known at the time the model is ran and should not be used in the training set

            if prediction_inputs is None:
                prediction_inputs = prediction_input
            else:
                prediction_inputs = pd.concat(
                    [prediction_inputs, prediction_input],
                    axis=0,
                )

        if prediction_inputs is None:
            log.warning(
                f"Insufficient data available for model training for symbol: {symbol}"
            )
            continue

        prediction_inputs = prediction_inputs.dropna(subset=targets)

        if len(prediction_inputs) < 20:
            log.warning(
                f"Insufficient data available for model training for symbol: {symbol}"
            )
            continue

        serving_set = prediction_inputs.sample(
            n=min(len(prediction_inputs) // 10, serving_set_size)
        )

        X = prediction_inputs[features]
        y = prediction_inputs[targets]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=1729,
        )

        model = xgb.XGBClassifier(
            objective="binary:logistic",
            eval_metric="logloss",
        )
        model.fit(X_train, y_train["target"])

        model_positive_threshold = xgb.XGBClassifier(
            objective="binary:logistic",
            eval_metric="logloss",
        )
        model_positive_threshold.fit(X_train, y_train["positive_threshold_target"])

        model_negative_threshold = xgb.XGBClassifier(
            objective="binary:logistic",
            eval_metric="logloss",
        )
        model_negative_threshold.fit(X_train, y_train["negative_threshold_target"])

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test["target"], y_pred)
        balanced_accuracy = balanced_accuracy_score(y_test["target"], y_pred)
        precision = precision_score(y_test["target"], y_pred)
        f1 = f1_score(y_test["target"], y_pred)
        conf_matrix = confusion_matrix(y_test["target"], y_pred)
        class_report = classification_report(y_test["target"], y_pred, output_dict=False)

        y_pred_positive_threshold = model_positive_threshold.predict(X_test)
        accuracy_positive_threshold = accuracy_score(y_test["positive_threshold_target"], y_pred_positive_threshold)
        balanced_accuracy_positive_threshold = balanced_accuracy_score(y_test["positive_threshold_target"], y_pred_positive_threshold)
        precision_positive_threshold = precision_score(y_test["positive_threshold_target"], y_pred_positive_threshold)
        f1_positive_threshold = f1_score(y_test["positive_threshold_target"], y_pred_positive_threshold)
        conf_matrix_positive_threshold = confusion_matrix(y_test["positive_threshold_target"], y_pred_positive_threshold)
        class_report_positive_threshold = classification_report(y_test["positive_threshold_target"], y_pred_positive_threshold, output_dict=False)

        y_pred_negative_threshold = model_negative_threshold.predict(X_test)
        accuracy_negative_threshold = accuracy_score(y_test["negative_threshold_target"], y_pred_negative_threshold)
        balanced_accuracy_negative_threshold = balanced_accuracy_score(y_test["negative_threshold_target"], y_pred_negative_threshold)
        precision_negative_threshold = precision_score(y_test["negative_threshold_target"], y_pred_negative_threshold)
        f1_negative_threshold = f1_score(y_test["negative_threshold_target"], y_pred_negative_threshold)
        conf_matrix_negative_threshold = confusion_matrix(y_test["negative_threshold_target"], y_pred_negative_threshold)
        class_report_negative_threshold = classification_report(y_test["negative_threshold_target"], y_pred_negative_threshold, output_dict=False)

        X_serve, y_serve, y_serve_pred = None, None, None
        if serving_set is not None:
            X_serve = serving_set[features]
            y_serve = serving_set["target"]
            y_serve_positive_threshold = serving_set["positive_threshold_target"]
            y_serve_negative_threshold = serving_set["negative_threshold_target"]
            y_serve_pred = model.predict(X_serve)
            y_serve_pred_positive_threshold = model_positive_threshold.predict(X_serve)
            y_serve_pred_negative_threshold = model_negative_threshold.predict(X_serve)

        log.info("Training model on all data.")

        full_model = xgb.XGBClassifier(
            objective="binary:logistic",
            eval_metric="logloss",
        )
        full_model.fit(X, y["target"])

        full_model_positive_threshold = xgb.XGBClassifier(
            objective="binary:logistic",
            eval_metric="logloss",
        )
        full_model_positive_threshold.fit(X, y["positive_threshold_target"])

        full_model_negative_threshold = xgb.XGBClassifier(
            objective="binary:logistic",
            eval_metric="logloss",
        )
        full_model_negative_threshold.fit(X, y["negative_threshold_target"])

        if diagnostic_plots_flag:
            plot_pca_results(X)

        log.info("Recording performance information.")

        performance_info.extend(
            (
                {
                    "threshold_percentage": 0.0,
                    "timestamp": datetime.now(),
                    "symbols": [symbol],
                    "accuracy": float(accuracy),
                    "balanced_accuracy": float(balanced_accuracy),
                    "precision": float(precision),
                    "f1": float(f1),
                    "confusion_matrix": conf_matrix,
                    "features": features,
                    "classification_report": class_report,
                    "validated_model": model,
                    "model": full_model,
                    "model_positive_threshold": full_model_positive_threshold,
                    "model_negative_threshold": full_model_negative_threshold,
                    "training_set_rows": len(y_train),
                    "training_data": X_train,
                    "training_targets": y_train["target"],
                    "test_set_rows": len(y_test),
                    "test_data": X_test,
                    "test_targets": y_test["target"],
                    "serving_set_rows": len(serving_set),
                    "serving_data": X_serve,
                    "serving_targets": y_serve,
                    "y_serve": (
                        y_serve.tolist() if y_serve is not None else None
                    ),
                    "y_serve_pred": (
                        y_serve_pred.tolist()
                        if y_serve_pred is not None
                        else None
                    ),
                    "serving_set_indicated_entry_prices": (
                        serving_set["target_date_daily_open"].tolist()
                        if serving_set is not None
                        else None
                    ),
                    "serving_set_indicated_exit_prices": (
                        serving_set["target_date_daily_close"].tolist()
                        if serving_set is not None
                        else None
                    ),
                },
                {
                    "threshold_percentage": threshold_percentage,
                    "timestamp": datetime.now(),
                    "symbols": [symbol],
                    "accuracy": float(accuracy_positive_threshold),
                    "balanced_accuracy": float(
                        balanced_accuracy_positive_threshold
                    ),
                    "precision": float(precision_positive_threshold),
                    "f1": float(f1_positive_threshold),
                    "confusion_matrix": conf_matrix_positive_threshold,
                    "features": features,
                    "classification_report": class_report_positive_threshold,
                    "validated_model": model_positive_threshold,
                    "model": full_model_positive_threshold,
                    "training_set_rows": len(y_train),
                    "training_data": X_train,
                    "training_targets": y_train["positive_threshold_target"],
                    "test_set_rows": len(y_test),
                    "test_data": X_test,
                    "test_targets": y_test["positive_threshold_target"],
                    "serving_set_rows": len(serving_set),
                    "serving_data": X_serve,
                    "serving_targets": y_serve_positive_threshold,
                    "y_serve": (
                        y_serve_positive_threshold.tolist()
                        if y_serve_positive_threshold is not None
                        else None
                    ),
                    "y_serve_pred": (
                        y_serve_pred_positive_threshold.tolist()
                        if y_serve_pred_positive_threshold is not None
                        else None
                    ),
                    "serving_set_indicated_entry_prices": (
                        serving_set["target_date_daily_open"].tolist()
                        if serving_set is not None
                        else None
                    ),
                    "serving_set_indicated_exit_prices": (
                        serving_set["target_date_daily_close"].tolist()
                        if serving_set is not None
                        else None
                    ),
                },
                {
                    "threshold_percentage": -threshold_percentage,
                    "timestamp": datetime.now(),
                    "symbols": [symbol],
                    "accuracy": float(accuracy_negative_threshold),
                    "balanced_accuracy": float(
                        balanced_accuracy_negative_threshold
                    ),
                    "precision": float(precision_negative_threshold),
                    "f1": float(f1_negative_threshold),
                    "confusion_matrix": conf_matrix_negative_threshold,
                    "features": features,
                    "classification_report": class_report_negative_threshold,
                    "validated_model": model_negative_threshold,
                    "model": full_model_negative_threshold,
                    "training_set_rows": len(y_train),
                    "training_data": X_train,
                    "training_targets": y_train["negative_threshold_target"],
                    "test_set_rows": len(y_test),
                    "test_data": X_test,
                    "test_targets": y_test["negative_threshold_target"],
                    "serving_set_rows": len(serving_set),
                    "serving_data": X_serve,
                    "serving_targets": y_serve_negative_threshold,
                    "y_serve": (
                        y_serve_negative_threshold.tolist()
                        if y_serve_negative_threshold is not None
                        else None
                    ),
                    "y_serve_pred": (
                        y_serve_pred_negative_threshold.tolist()
                        if y_serve_pred_negative_threshold is not None
                        else None
                    ),
                    "serving_set_indicated_entry_prices": (
                        serving_set["target_date_daily_open"].tolist()
                        if serving_set is not None
                        else None
                    ),
                    "serving_set_indicated_exit_prices": (
                        serving_set["target_date_daily_close"].tolist()
                        if serving_set is not None
                        else None
                    ),
                },
            )
        )
    return performance_info
