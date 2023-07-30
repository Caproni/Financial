#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from src.univariate.analysis.calc_average_drawdown import calc_average_drawdown


def test_calc_average_drawdown():
    assert (
        round(
            calc_average_drawdown(
                data=[234.56, 234.56, 234.76, 234.66, 214.56, 234.46, 234.66, 234.76],
            ),
            2,
        )
        == 2.87
    )
