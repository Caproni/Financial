#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from src.univariate.metrics.calc_maximum_drawdown_value import calc_maximum_drawdown_value


def test_calc_maximum_drawdown_value():
    result = calc_maximum_drawdown_value(
        data=[234.56, 234.56, 234.76, 234.66, 234.56, 234.46, 234.66]
    )
    assert result["high_water_mark"] == 234.76
    assert round(result["maximum_drawdown_value"], 2) == 0.30