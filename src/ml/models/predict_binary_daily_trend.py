#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from src.univariate.analysis import calc_macd
from src.utils import log


def predict_binary_daily_trend(
    data: pd.DataFrame,
):
    """
    Predicts the daily trend of stock prices based on historical data.

    This function analyzes stock price data to determine whether the price will rise or fall by the end of the trading day. It employs machine learning techniques to train a model for each stock symbol using various features derived from the data.

    Args:
        data (pd.DataFrame): A DataFrame containing stock price data with columns including 'timestamp', 'symbol', 'close', 'open', 'high', 'low', and 'volume'.

    Returns:
        tuple: A tuple containing:
            - final_model: The last trained machine learning model.
            - performance_info: A list of dictionaries containing performance metrics for each prediction.
            - predictions_df: A DataFrame with prediction results including actual and predicted values, accuracy, confusion matrix, and classification report.

    Examples:
        >>> predictions = predict_daily_trend(data)
    """
    log.function_call()

    data.set_index("timestamp", inplace=True)
    data = data.sort_index()

    data["date"] = data.index.date

    # Initialize a DataFrame to store prediction results and a list for performance
    predictions_df = pd.DataFrame(
        columns=[
            "symbol",
            "date",
            "actual",
            "predicted",
            "accuracy",
            "confusion_matrix",
            "classification_report",
        ]
    )
    performance_info = []

    final_model = None

    for symbol, symbol_data in data.groupby("symbol"):
        symbol_data = symbol_data.copy()

        first_price_daily = symbol_data.groupby("date")["close"].first()
        symbol_data["first_price"] = symbol_data["date"].map(first_price_daily)
        symbol_data["price_rise"] = (
            symbol_data["close"] > symbol_data["first_price"]
        ).astype(int)
        symbol_data["target"] = symbol_data["price_rise"].shift(-1)

        symbol_data.dropna(subset=["target"], inplace=True)

        symbol_data["hour"] = symbol_data.index.hour
        symbol_data["day_of_week"] = symbol_data.index.dayofweek
        _, _, macd_histogram, macd_first_derivative = calc_macd(
            data=symbol_data["close"].to_list(),
        )
        symbol_data["macd_histogram"] = macd_histogram
        symbol_data["macd_first_derivative"] = macd_first_derivative

        features = [
            "hour",
            "day_of_week",
            "open",
            "high",
            "low",
            "volume",
            "macd_histogram",
            "macd_first_derivative",
            "first_price",  # Include the first hourly close price as a feature
        ]

        for date, daily_data in symbol_data.groupby("date"):
            daily_data = daily_data.copy()

            # Use data before the current date for training
            training_data = symbol_data[symbol_data["date"] < date]
            if training_data.empty:
                log.info(
                    f"No training data available for the selected date: {date} and symbol: {symbol}"
                )
                continue

            # Extract the first hourly close price for the current day
            first_hourly_closes = daily_data[daily_data["hour"] == 9]["close"]

            if first_hourly_closes.empty:
                log.info(
                    f"No first close date for selected date: {date} and symbol: {symbol}"
                )
                continue

            first_hourly_close = first_hourly_closes.iloc[0]

            # Create a single-row DataFrame for prediction
            prediction_data = pd.DataFrame(
                {
                    "hour": [9],  # Using the hour of the first hourly close
                    "day_of_week": [daily_data["day_of_week"].iloc[0]],
                    "open": [daily_data["open"].iloc[0]],
                    "high": [daily_data["high"].iloc[0]],
                    "low": [daily_data["low"].iloc[0]],
                    "volume": [daily_data["volume"].iloc[0]],
                    "macd_histogram": [
                        macd_histogram[0]
                    ],  # Using the MACD histogram of the first hour
                    "macd_first_derivative": [
                        macd_first_derivative[0]
                    ],  # Using the MACD derivative of the first hour
                    "first_price": [
                        first_hourly_close
                    ],  # Use the first hourly close as a feature
                }
            )

            # Train the model with the historical data
            X_train = training_data[features]
            y_train = training_data["target"]

            model = xgb.XGBClassifier(
                objective="binary:logistic", eval_metric="logloss"
            )
            model.fit(X_train, y_train)

            # Save the final model (this will be the last model trained)
            final_model = model

            # Predict the end-of-day trend using the first hourly close price
            y_pred = model.predict(prediction_data)
            actual = daily_data["target"].iloc[
                -1
            ]  # The actual value for the end of the day
            accuracy = accuracy_score([actual], y_pred)
            conf_matrix = confusion_matrix([actual], y_pred)
            class_report = classification_report([actual], y_pred, output_dict=False)

            # Record performance information
            performance_info.append(
                {
                    "symbol": symbol,
                    "date": date,
                    "accuracy": accuracy,
                    "confusion_matrix": conf_matrix,
                    "classification_report": class_report,
                }
            )

            # Create a single row of results for this day's prediction
            daily_results = pd.DataFrame(
                {
                    "symbol": [symbol],
                    "date": [date],
                    "actual": [actual],
                    "predicted": y_pred,
                    "accuracy": [accuracy],
                    "confusion_matrix": [conf_matrix],
                    "classification_report": [class_report],
                }
            )

            # Append to the predictions DataFrame
            predictions_df = pd.concat(
                [predictions_df, daily_results], ignore_index=True
            )

    # Return the final model, performance information, and predictions DataFrame
    return final_model, performance_info, predictions_df
