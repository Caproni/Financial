#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from datetime import datetime, timedelta

from src.univariate.metrics.calc_maximum_drawdown_duration import calc_maximum_drawdown_duration


def test_calc_maximum_drawdown_duration():
    
    start_time = datetime(2019, 1, 1)
    ts = [start_time + timedelta(days=step) for step in range(7)]
   
    result = calc_maximum_drawdown_duration(
        data=[234.56, 234.56, 234.76, 234.66, 234.56, 234.46, 234.66],
        ts=ts,
    )
    assert result["maximum_drawdown_duration"] == timedelta(days=3)
