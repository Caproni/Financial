#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import pandas as pd
import src.ml.predict_daily_trend as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from src.utils import log


def predict_daily_trend(
    data: pd.DataFrame,
):
    log.function_call()

    data.set_index("datetime", inplace=True)
    data = data.sort_index()

    data["date"] = data.index.date
    first_price_daily = data.groupby("date")[
        "close"
    ].first()  # need at least one bar from current trading day

    data["first_price"] = data["date"].map(first_price_daily)
    data["price_rise"] = (data["close"] > data["first_price"]).astype(int)
    data["target"] = data["price_rise"].shift(-1)

    data.dropna(subset=["target"], inplace=True)

    data["hour"] = data.index.hour
    data["day_of_week"] = data.index.dayofweek
    data["moving_avg_5"] = data["close"].rolling(window=5).mean()
    data["moving_avg_10"] = data["close"].rolling(window=10).mean()

    data.dropna(inplace=True)

    features = [
        "hour",
        "day_of_week",
        "moving_avg_5",
        "moving_avg_10",
        "open",
        "high",
        "low",
        "volume",
    ]
    X = data[features]
    y = data["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False, random_state=42
    )

    model = xgb.XGBClassifier(objective="binary:logistic", eval_metric="logloss")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred)

    return model, conf_matrix, class_report, accuracy
