#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import pandas as pd

from src.utils import log


def calc_macd(
    data: list[int | float],
    short_window: int = 12,
    long_window: int = 26,
    signal_window: int = 9,
) -> tuple[list[float], list[float], list[float]]:
    """
    Calculates the Moving Average Convergence Divergence (MACD) for the given data.

    Args:
        data: A list of integers or floats representing the price data.
        short_window: An integer specifying the short EMA window (default is 12).
        long_window: An integer specifying the long EMA window (default is 26).
        signal_window: An integer specifying the signal line window (default is 9).

    Returns:
        tuple[list[float], list[float], list[float]]: A tuple of lists containing the MACD, Signal Line, and MACD Histogram.
    """
    log.function_call()

    df = pd.DataFrame({"Price": data})

    df["EMA_short"] = df["Price"].ewm(span=short_window, adjust=False).mean()
    df["EMA_long"] = df["Price"].ewm(span=long_window, adjust=False).mean()

    df["MACD"] = df["EMA_short"] - df["EMA_long"]
    df["Signal_Line"] = df["MACD"].ewm(span=signal_window, adjust=False).mean()
    df["MACD_Histogram"] = df["MACD"] - df["Signal_Line"]

    df = df.drop(columns=["EMA_short", "EMA_long", "Price"])

    return (
        df["MACD"].to_list(),
        df["Signal_Line"].to_list(),
        df["MACD_Histogram"].to_list(),
    )
