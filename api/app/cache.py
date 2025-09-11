"""Simple in-memory TTL cache for API responses."""

from __future__ import annotations

import time
from typing import Any, Callable


class TTLCache:
    def __init__(self, ttl_seconds: int = 300) -> None:
        self._ttl = ttl_seconds
        self._store: dict[str, tuple[float, Any]] = {}

    def get(self, key: str) -> Any | None:
        if key not in self._store:
            return None
        ts, value = self._store[key]
        if time.monotonic() - ts > self._ttl:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any) -> None:
        self._store[key] = (time.monotonic(), value)

    def cached(self, key_fn: Callable[..., str]):
        """Decorator: cache the return value of a function using key_fn(*args, **kwargs)."""
        def decorator(fn: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                key = key_fn(*args, **kwargs)
                cached_val = self.get(key)
                if cached_val is not None:
                    return cached_val
                result = fn(*args, **kwargs)
                self.set(key, result)
                return result
            return wrapper
        return decorator


response_cache = TTLCache(ttl_seconds=300)
