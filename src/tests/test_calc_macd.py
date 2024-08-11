#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""


from src.univariate.analysis import calc_macd


def test_calc_macd():
    macd, macd_signal_line, macd_histogram = calc_macd(
        data=[3, 50, 35, 20, 3],
    )

    assert len(macd) == 5
