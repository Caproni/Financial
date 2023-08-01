#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from src.utils.logger import logger as log


def get_assets(
    status: str = None,
    asset_class: str = None,
    exchange: str = None,
    attributes: str = None,
):
    log.info("Calling get_assets")
