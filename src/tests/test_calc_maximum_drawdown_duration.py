#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from datetime import datetime, timedelta

from src.univariate.metrics.calc_maximum_drawdown_duration import calc_maximum_drawdown_duration


def test_calc_maximum_drawdown_duration():
    
    result = calc_maximum_drawdown_duration(
        data=[234.56, 234.56, 234.76, 234.66, 234.56, 234.46, 234.66, 234.76],
        ts=[datetime(2019, 1, 1) + timedelta(days=step) for step in range(8)],
    )
    
    assert result["maximum_drawdown_duration_start_timestamp"] == datetime(2019, 1, 3, 0, 0)
    assert result["maximum_drawdown_duration_end_timestamp"] == datetime(2019, 1, 7, 0, 0)
