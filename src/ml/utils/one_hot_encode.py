#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
import pandas as pd

from src.utils import log


def one_hot_encode(
    df: pd.DataFrame, column: str, value_mapping: dict[Any, str] | None = None
) -> pd.DataFrame:
    """
    One-hot encodes a specified categorical column in a pandas DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    column (str): The column name to one-hot encode.
    value_mapping (dict[Any, str]). An optional dictionary to map the values in the column to strings.

    Returns:
    pd.DataFrame: A DataFrame with the one-hot encoded column.
    """
    log.function_call()

    if value_mapping is not None:
        df[column] = df[column].map(value_mapping)

    return pd.get_dummies(df, columns=[column], prefix=column)
