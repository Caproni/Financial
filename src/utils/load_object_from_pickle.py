#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import pickle

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

    with open(file_path, "rb") as f:
        return pickle.load(f)