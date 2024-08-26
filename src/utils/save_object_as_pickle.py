#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import pickle

from src.utils.logger import logger as log


def save_object_as_pickle(
    obj: object,
    file_path: str,
    compress: bool = True,
):
    """
    Save a Python object.

    Parameters:
    obj (object): The object to be saved.
    file_path (str): The path to the file where the object should be saved.

    Example usage:
    save_object(obj, 'model.pkl')
    """
    log.function_call()

    with open(file_path, "wb") as f:
        if compress:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            pickle.dump(obj, f)

    log.info(f"Object saved to {file_path}")
