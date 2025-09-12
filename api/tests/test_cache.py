"""Tests for the TTL cache."""

import time

from app.cache import TTLCache


def test_cache_miss_returns_none():
    cache = TTLCache(ttl_seconds=60)
    assert cache.get("missing") is None


def test_cache_set_and_get():
    cache = TTLCache(ttl_seconds=60)
    cache.set("key", {"value": 42})
    assert cache.get("key") == {"value": 42}


def test_cache_expires():
    cache = TTLCache(ttl_seconds=0)
    cache.set("key", "data")
    time.sleep(0.01)
    assert cache.get("key") is None


def test_cache_overwrite():
    cache = TTLCache(ttl_seconds=60)
    cache.set("key", "first")
    cache.set("key", "second")
    assert cache.get("key") == "second"
