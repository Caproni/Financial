#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

import pandas as pd


def load_base_rate_data(path_to_data: str):
    data = pd.read_csv(
        path_to_data,
        parse_dates=["Date Changed"],
        date_format="%d %b %y",
    )
    return data.sort_values(by="Date Changed")
