#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""


from src.univariate.analysis.calc_linear_moving_average import (
    calc_linear_moving_average,
)


def test_calc_linear_moving_average():
    ma_data_mean, ma_data_sd = calc_linear_moving_average(
        data=[3, 5, 5, 5, 3],
        steps=2,
    )

    assert len(ma_data_mean) == 5
