#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from src.univariate.analysis.calc_hurst_exponent import calc_hurst_exponent


def test_calc_hurst_exponent():
    assert (
        calc_hurst_exponent(
            data=[
                0.25,
                0.30,
                0.35,
                0.40,
                0.45,
                0.6,
                0.7,
                0.8,
                0.9,
                1.0,
                1.1,
                1.2,
                1.2,
                1.4,
            ]
        )
        == 0.562999401363607
    )
    
    assert (
        calc_hurst_exponent(
            data=[
                0.25,
                0.30,
                0.25,
                0.20,
                0.25,
                0.30,
                0.25,
                0.20,
                0.25,
                0.30,
                0.25,
                0.20,
                0.25,
                0.30,
            ]
        )
        == 0.7881991619090498
    )
