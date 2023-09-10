#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.vector_ar.vecm import coint_johansen

from ..utils.logger import logger as log


def calc_johansen_test(
    v1: list[float | int],
    v2: list[float | int],
    lag: int = 0,
):
    log.info("Calling calc_johansen_test")
    
    df = pd.DataFrame(
        {
            "v1": v1,
            "v2": v2,
        }
    )
    r = coint_johansen(df, det_order=0, k_ar_diff=lag)
    return r