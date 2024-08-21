#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from pickle import load
from gzip import open as open_zip

from src.utils.logger import logger as log


def load_json_from_file(
    path_to_file: str,
) -> list[dict[str, Any]]:
    """Loads data from a file. Expects a payload compatible with a Mongodb collection.

    Args:
        path_to_file (str): Path to file from which to load data.

    Raises:
        e: If load is not successful.

    Returns:
        list[dict[str, Any]]: Data payload.
    """
    log.function_call()

    try:
        with open_zip(path_to_file, "rb") as f:
            return load(f)
    except Exception as e:
        log.error(f"Error loading file. Error: {e}")
        raise e
