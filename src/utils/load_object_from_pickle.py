#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import pickle
from gzip import open as open_zip, BadGzipFile

from src.utils.logger import logger as log


def load_object_from_pickle(file_path: str) -> object:
    """
    Load a Python object from a .pkl file.

    Parameters:
    file_path (str): The path to the file from which the object should be loaded.

    Returns:
    object: The loaded object.

    Example usage:
    dataframe = load_from_pickle('dataframe.pkl')
    model = load_from_pickle('model.pkl')
    list_of_dicts = load_from_pickle('data.pkl')
    """
    log.function_call()

    if file_path.endswith(".gz"):
        log.info("Attempting file decompression.")
        try:
            with open_zip(file_path, "rb") as f:
                return pickle.load(f)
        except BadGzipFile as _:
            log.info(
                "Could not decompress file. Not compressed. Trying to load file without decompression."
            )
        except Exception as e:
            log.error(f"Could not decompress file. Error: {e}")
            raise e

    with open(file_path, "rb") as f:
        return pickle.load(f)
