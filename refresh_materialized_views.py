#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os import getenv
from datetime import datetime
import sentry_sdk
from sqlalchemy import text
from dotenv import load_dotenv

from src.sql.client import create_sql_client
from src.sql import MaterializedViews, insert_data
from src.utils import log

load_dotenv()

sentry_sdk.init(
    dsn=getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

if __name__ == "__main__":

    log.info("Starting refresh of database materialized views.")

    database_client = create_sql_client()

    materialized_views = [
        "liquid_tickers",
        "model_profit_analysis",
        "polygon_market_data_day_summary",
        "polygon_market_data_hour_summary",
    ]

    with database_client.engine.connect() as connection:

        for materialized_view in materialized_views:
            log.info(f"Refreshing: {materialized_view}")
            connection.execute(text(f"REFRESH MATERIALIZED VIEW {materialized_view}"))
            success = insert_data(
                database_client,
                documents=[
                    MaterializedViews(
                        materialized_view_name=materialized_view,
                        last_refreshed=datetime.now(),
                    )
                ],
                upsert=True,
            )

            if not success:
                log.warning(
                    "Could not update materialized_views table with latest refresh timestamp."
                )

    log.info("Completed refresh of database materialized views.")
