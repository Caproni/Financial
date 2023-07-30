#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from src.univariate.analysis.get_drawdowns import (
    get_drawdowns,
)


def test_calc_maximum_drawdown_value():
    assert [
        round(e, 4)
        for e in get_drawdowns(
            data=[234.76, 234.56, 234.76, 234.66, 234.56, 234.46, 234.86]
        )
    ] == [round(0.20 / 234.76 * 100, 4), round(0.30 / 234.76 * 100, 4)]
