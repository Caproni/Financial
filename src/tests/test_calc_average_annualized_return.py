#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from datetime import datetime, timedelta

from src.univariate.analysis.calc_average_annualized_return import calc_average_annualized_return


def test_calc_average_annualized_return():
    
    data = [234.56, 234.56, 234.76, 234.66, 234.56, 234.46, 234.66, 234.76]
    ts = [datetime(2019, 1, 1) + timedelta(days=40 * step) for step in range(8)]

    assert round(calc_average_annualized_return(
        start_value=data[0],
        end_value=data[-1],
        start_time=ts[0],
        end_time=ts[-1],
    ), 2) == 26.09

