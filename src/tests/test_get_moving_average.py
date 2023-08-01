#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""


from src.univariate.analysis.get_moving_average import get_moving_average


def test_get_moving_average():
    ma_data_mean, ma_data_sd = get_moving_average(
        data=[3, 5, 5, 5, 3],
        weighting="linear",
        steps=2,
    )

    assert len(ma_data_mean) == 5
