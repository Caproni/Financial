#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from typing import Any
from pickle import dump, HIGHEST_PROTOCOL
from gzip import open as open_zip

from src.utils import log


def save_json_to_file(
    data_payload: list[dict[str, Any]],
    path_to_file: str,
) -> None:
    """Saves data to a file. Expects data compatible with a Mongodb collection.

    Args:
        data_payload (list[dict[str, Any]]): Data to save to file.
        path_to_file (str): The path to which to save the data.

    Raises:
        e: If save is not successful.
    """
    log.function_call()

    try:
        with open_zip(path_to_file, "wb") as f:
            dump(data_payload, f, protocol=HIGHEST_PROTOCOL)
    except Exception as e:
        log.error("Error saving file. Error: {e}")
        raise e
