#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

import numpy as np

from ..multivariate.calc_johansen_test import calc_johansen_test


def test_calc_johansen_test():
    np.random.seed(42)

    result = calc_johansen_test(
        v1=np.cumsum(np.random.randn(100)),
        v2=np.cumsum(np.random.randn(100)),
        lag=0,
    )

    assert result.lr1.size == 2
    assert result.cvm.size == 6
