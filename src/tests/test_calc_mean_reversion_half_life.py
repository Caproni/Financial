#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

import numpy as np

from src.univariate.analysis.calc_mean_reversion_half_life import (
    calc_mean_reversion_half_life,
)


def test_calc_mean_reversion_half_life():
    np.random.seed(42)
    t = np.linspace(0, 10*np.pi, 2000)
    data = list(np.sin(t) + np.random.normal(scale=0.05, size=len(t)))
    half_life = calc_mean_reversion_half_life(data)
    assert half_life > 0
