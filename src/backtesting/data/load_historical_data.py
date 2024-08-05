#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2023
"""

from collections.abc import Callable
from os.path import split, getsize
from typing import Any
from json import load, JSONDecoder
from datetime import datetime


from src.utils.get_files_recursively import FileManipulation
from src.utils import log


def load_historical_data(
    directory: str,
    prefix: str,
) -> dict[str, list[Any]]:
    """Loads historical stock data saved in JSON format from multiple files in a directory

    Args:
        directory (str): A directory from which to load data
        prefix (str): A prefix present in the name of the file. Assumes that each filename follows the convention: prefix_aapl.json

    Returns:
        dict[str, list[Any]]: Stock data retrieved from multiple files with the provided prefix
    """
    log.function_call()

    class DateTimeDecoder(JSONDecoder):
        def __init__(
            self,
            *,
            parse_float: Callable[[str], Any] | None = None,
            parse_int: Callable[[str], Any] | None = None,
            parse_constant: Callable[[str], Any] | None = None,
            strict: bool = True,
            object_pairs_hook: Callable[[list[tuple[str, Any]]], Any] | None = None,
        ) -> None:
            super().__init__(
                object_hook=self.object_hook,
                parse_float=parse_float,
                parse_int=parse_int,
                parse_constant=parse_constant,
                strict=strict,
                object_pairs_hook=object_pairs_hook,
            )

        def object_hook(self, obj):
            for k, v in obj.items():
                try:
                    obj[k] = datetime.fromisoformat(v)
                except (ValueError, TypeError):
                    pass
            return obj

    files = FileManipulation.get_files_recursively(
        directory,
        file_extension_allow_list=["json"],
    )

    stock_data: dict[str, list[Any]] = {}
    for data_file in files:
        _, filename = split(data_file)
        symbol = filename.replace(f"{prefix}_", "").replace(".json", "").upper()
        if getsize(data_file) > 0:
            with open(data_file, "r") as f:
                data = load(
                    f,
                    cls=DateTimeDecoder,
                )
                stock_data.update(data)

    return stock_data
