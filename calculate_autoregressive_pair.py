#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from datetime import datetime

from src.mongo import create_mongo_client, get_data
from src.multivariate import calc_johansen_test
from src.utils import log


if __name__ == "__main__":
    
    log.info("Starting multivariate analysis.")
    
    mongo_client = create_mongo_client()
    
    start_date = datetime(2024, 1, 1)
    
    kmi_data = get_data(
        mongo_client,
        database="financial",
        collection="polygon_market_data_day",
        pipeline=[
            {
                "$match": {"symbol": "KMI", "timestamp": {"$gt": start_date}},
            },
        ]
    )
    
    tce_data = get_data(
        mongo_client,
        database="financial",
        collection="polygon_market_data_day",
        pipeline=[
            {
                "$match": {"symbol": "TRP", "timestamp": {"$gt": start_date}},
            },
        ]
    )
    
    result = calc_johansen_test(
        v1=[e["close"] for e in kmi_data],
        v2=[e["close"] for e in tce_data],
        lag=1,
    )
    
    log.info("Completing multivariate analysis.")
