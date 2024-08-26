#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import sentry_sdk
from datetime import datetime, timedelta
from sqlalchemy import and_

from src.sql import create_sql_client, get_data, Models
from src.utils import log

sentry_sdk.init(
    dsn="https://8cd12a857607d331985d59a77ea0828e@o4507797009334272.ingest.de.sentry.io/4507797017133136",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

if __name__ == "__main__":

    log.info("Started running models.")

    now = datetime.now()
    
    log.info(f"Obtaining metadata for models trained since: {now - timedelta(days=1)}")

    predictive_models = get_data(
        database_client=create_sql_client(),
        models=[Models],
        where=and_(
            Models.created_at >= now - timedelta(days=1),
            Models.accuracy > 0.5,
            Models.balanced_accuracy > 0.5,
        ),
    )
    
    log.info("Obtaining model files from object storage.")
    model_files = []
    for predictive_model in predictive_models:
        

    # get symbols related to each model
    

    log.info("Completed running models.")
