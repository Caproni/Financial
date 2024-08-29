#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from os import makedirs
from os.path import abspath, join, exists
from pickle import load, dump
from typing import Callable, Any, Dict

from src.utils import log


class PersistentCache:
    def __init__(self, cache_dir: str, cache_file: str = "cache.pkl"):
        log.function_call()
        self.cache_dir = abspath(cache_dir)
        self.cache_file = cache_file
        self.cache_path = join(cache_dir, cache_file)
        self.cache: Dict[str, Any] = {}
        self._load_cache()

    def _load_cache(self):
        log.function_call()
        if exists(self.cache_path):
            with open(self.cache_path, "rb") as f:
                self.cache = load(f)
        else:
            # Ensure the directory exists
            makedirs(self.cache_dir, exist_ok=True)

    def _save_cache(self):
        log.function_call()
        with open(self.cache_path, "wb") as f:
            dump(self.cache, f)

    def get(self, key: str) -> Any:
        log.function_call()
        return self.cache.get(key)

    def set(self, key: str, value: Any):
        log.function_call()
        self.cache[key] = value
        self._save_cache()

    def clear(self):
        log.function_call()
        self.cache = {}
        self._save_cache()

    def cache_function(self, key_func: Callable[..., str]):
        log.function_call()

        def decorator(func: Callable[..., Any]):
            def wrapper(*args, **kwargs):
                # Check for the 'use_cache' keyword argument
                use_cache = kwargs.pop("use_cache", True)

                # Generate the cache key
                key = key_func(*args, **kwargs)

                if use_cache and key in self.cache:
                    return self.cache[key]

                # Call the actual function if caching is bypassed or cache miss
                result = func(*args, **kwargs)

                if use_cache:
                    self.set(key, result)

                return result

            return wrapper

        return decorator


def generate_key(*args, **kwargs) -> str:
    models = " ".join([e.__tablename__ for e in kwargs["models"]])
    where_clause = (
        str(kwargs["where_clause"].compile(compile_kwargs={"literal_binds": True}))
        if "where_clause" in kwargs
        else "all"
    )
    return f"{models} {where_clause}"
