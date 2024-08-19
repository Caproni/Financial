#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from src.utils import log
import sentry_sdk

sentry_sdk.init(
    dsn="https://8cd12a857607d331985d59a77ea0828e@o4507797009334272.ingest.de.sentry.io/4507797017133136",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

if __name__ == "__main__":

    log.info("Test CronJob run completed.")
