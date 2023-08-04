#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from src.univariate.analysis.get_drawups import (
    get_drawups,
)


def test_calc_maximum_drawdown_value():
    assert [
        round(e, 4)
        for e in get_drawups(
            data=[234.76, 234.86, 234.96, 231.66, 231.56, 231.46, 231.86]
        )
    ] == [round(0.20 / 234.76 * 100, 4), round(0.40 / 231.46 * 100, 4)]
