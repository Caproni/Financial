import os
import pickle
from typing import Callable, Any, Dict

from src.utils import log


class PersistentCache:
    def __init__(self, cache_dir: str, cache_file: str = "cache.pkl"):
        log.function_call()
        self.cache_dir = cache_dir
        self.cache_file = cache_file
        self.cache_path = os.path.join(cache_dir, cache_file)
        self.cache: Dict[str, Any] = {}
        self._load_cache()

    def _load_cache(self):
        log.function_call()
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "rb") as f:
                self.cache = pickle.load(f)
        else:
            # Ensure the directory exists
            os.makedirs(self.cache_dir, exist_ok=True)

    def _save_cache(self):
        log.function_call()
        with open(self.cache_path, "wb") as f:
            pickle.dump(self.cache, f)

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
                key = key_func(*args, **kwargs)
                if key in self.cache:
                    return self.cache[key]
                result = func(*args, **kwargs)
                self.set(key, result)
                return result

            return wrapper

        return decorator


def generate_key(*args, **kwargs) -> str:
    return str(args) + str(kwargs)
