#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from src.univariate.analysis.calc_ulcer_index import calc_ulcer_index


def test_calc_ulcer_index():
    assert (
        round(
            calc_ulcer_index(
                data=[234.56, 234.56, 234.76, 234.66, 214.56, 234.46, 234.66, 234.76],
            ),
            2,
        )
        == 4.97
    )
