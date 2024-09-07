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
    confusion_matrix,
    classification_report,
)
from sklearn.model_selection import train_test_split
import numpy as np
from datetime import datetime

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

    # param_grid = {
    #     "n_estimators": [100, 200, 300],
    #     "max_depth": [3, 4, 5],
    #     "learning_rate": [0.01, 0.1, 0.3],
    #     "subsample": [0.7, 0.8, 1.0],
    #     "colsample_bytree": [0.7, 0.8, 1.0],
    # }

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
        "daily_macd_first_derivative",
        "weekday_monday",
        "weekday_tuesday",
        "weekday_wednesday",
        "weekday_thursday",
        "weekday_friday",
        "target_date_daily_open",  # this is the open price on the market data for which a prediction is required
    ]

    for symbol, daily_symbol_data in daily_data.groupby("symbol"):
        if daily_symbol_data.empty:
            log.info(f"No daily data available for the selected symbol: {symbol}")
            continue

        daily_symbol_data["price_rise"] = (
            daily_symbol_data["daily_close"]
            > daily_symbol_data["daily_open"] * (1 + (threshold_percentage / 100))
        ).astype(int)

        daily_symbol_data["target"] = daily_symbol_data["price_rise"].shift(-1)

        daily_symbol_data = daily_symbol_data.dropna(subset=["target"])
        daily_symbol_data["target"] = daily_symbol_data["target"].astype(int)

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

        prediction_inputs = prediction_inputs.dropna(subset=["target"])

        if len(prediction_inputs) < 20:
            log.warning(
                f"Insufficient data available for model training for symbol: {symbol}"
            )
            continue

        serving_set = prediction_inputs.sample(
            n=min(len(prediction_inputs) // 10, serving_set_size)
        )

        X = prediction_inputs[features]
        y = prediction_inputs["target"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=1729,
        )

        model = xgb.XGBClassifier(  # model_archetype
            objective="binary:logistic",
            eval_metric="logloss",
        )
        # grid_search = GridSearchCV(
        #     estimator=model_archetype,
        #     param_grid=param_grid,
        #     scoring="balanced_accuracy",
        #     cv=1,
        #     verbose=1,
        #     n_jobs=-1,
        # )
        model.fit(X_train, y_train)
        # log.info("Best parameters found: ", grid_search.best_params_)
        # log.info("Best cross-validation accuracy: ", grid_search.best_score_)
        # model = grid_search.best_estimator_

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        balanced_accuracy = balanced_accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)
        class_report = classification_report(y_test, y_pred, output_dict=False)

        X_serve, y_serve, y_serve_pred = None, None, None
        if serving_set is not None:
            X_serve = serving_set[features]
            y_serve = serving_set["target"]
            y_serve_pred = model.predict(X_serve)

        log.info("Training model on all data.")

        full_model = xgb.XGBClassifier(
            # **grid_search.best_params_,
            objective="binary:logistic",
            eval_metric="logloss",
        )
        full_model.fit(X, y)

        PCA(full_model)

        # explainer = TreeExplainer(full_model, X)
        # explanation = explainer(X)
        # beeswarm(explanation, order=explanation.abs.max(0))

        log.info("Recording performance information.")

        performance_info.append(
            {
                "timestamp": datetime.now(),
                "symbols": [symbol],
                "accuracy": float(accuracy),
                "balanced_accuracy": float(balanced_accuracy),
                "precision": float(precision),
                "confusion_matrix": conf_matrix,
                "features": features,
                "classification_report": class_report,
                "validated_model": model,
                "model": full_model,
                "training_set_rows": len(y_train),
                "training_data": X_train,
                "training_targets": y_train,
                "test_set_rows": len(y_test),
                "test_data": X_test,
                "test_targets": y_test,
                "serving_set_rows": len(serving_set),
                "serving_data": X_serve,
                "serving_targets": y_serve,
                "y_serve": y_serve.tolist() if y_serve is not None else None,
                "y_serve_pred": (
                    y_serve_pred.tolist() if y_serve_pred is not None else None
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
            }
        )

    return performance_info
