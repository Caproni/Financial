#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from datetime import datetime, timedelta

from src.univariate.analysis.calc_calmar_ratio import calc_calmar_ratio


def test_calc_calmar_ratio():
    data = [234.56, 234.56, 234.76, 234.66, 214.56, 234.46, 234.66, 234.76]
    ts = [datetime(2019, 1, 1) + timedelta(days=40 * step) for step in range(8)]

    assert (
        round(
            calc_calmar_ratio(
                data=data,
                ts=ts,
            ),
            2,
        )
        == 3.03
    )
