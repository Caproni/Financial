#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from datetime import datetime
from sqlalchemy import text

from src.sql.client import create_sql_client
from src.sql import MaterializedViews, update_data
from src.utils import log


if __name__ == "__main__":

    log.info("Starting refresh of database materialized views.")

    database_client = create_sql_client()

    materialized_views = [
        "liquid_tickers",
        "polygon_market_data_day_summary",
        "polygon_market_data_hour_summary",
    ]

    with database_client.engine.connect() as connection:

        for materialized_view in materialized_views:
            log.info(f"Refreshing: {materialized_view}")
            connection.execute(text(f"REFRESH MATERIALIZED VIEW {materialized_view}"))
            success = update_data(
                database_client,
                rows_to_update=[
                    MaterializedViews(
                        materialized_view_name=materialized_view,
                        last_refreshed=datetime.now(),
                    )
                ],
            )

            if not success:
                log.warning(
                    "Could not update materialized_views table with latest refresh timestamp."
                )

    log.info("Completed refresh of database materialized views.")
