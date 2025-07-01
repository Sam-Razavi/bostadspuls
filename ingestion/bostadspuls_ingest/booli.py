"""Booli API client.

Booli uses HMAC-SHA1 authentication:
  callerId  — registered caller ID
  time      — Unix timestamp (seconds)
  unique    — random 16-char alphanumeric string
  checksum  — SHA1(callerId + time + key + unique)

Docs: https://www.booli.se/api/docs
"""

from __future__ import annotations

import hashlib
import random
import string
import time
from typing import Any

import httpx
import polars as pl

from .config import BOOLI_BASE_URL, BOOLI_CALLER_ID, BOOLI_KEY


def _make_checksum(caller_id: str, key: str, ts: int, unique: str) -> str:
    raw = f"{caller_id}{ts}{key}{unique}"
    return hashlib.sha1(raw.encode()).hexdigest()


def _auth_params(caller_id: str = BOOLI_CALLER_ID, key: str = BOOLI_KEY) -> dict[str, str]:
    ts = int(time.time())
    unique = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    return {
        "callerId": caller_id,
        "time": str(ts),
        "unique": unique,
        "checksum": _make_checksum(caller_id, key, ts, unique),
    }


class BooliClient:
    """Synchronous HTTP client for the Booli sold listings API."""

    def __init__(
        self,
        caller_id: str = BOOLI_CALLER_ID,
        key: str = BOOLI_KEY,
        base_url: str = BOOLI_BASE_URL,
        timeout: float = 30.0,
    ) -> None:
        self._caller_id = caller_id
        self._key = key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        auth = _auth_params(self._caller_id, self._key)
        merged = {**(params or {}), **auth}
        with httpx.Client(timeout=self._timeout) as client:
            resp = client.get(f"{self._base_url}/{path.lstrip('/')}", params=merged)
            resp.raise_for_status()
            return resp.json()

    def fetch_sold(
        self,
        area: str | None = None,
        object_type: str | None = None,
        min_sold_date: str | None = None,
        max_sold_date: str | None = None,
        offset: int = 0,
        limit: int = 500,
    ) -> dict[str, Any]:
        """Fetch a page of sold listings."""
        params: dict[str, Any] = {"offset": offset, "limit": limit}
        if area:
            params["areaId"] = area
        if object_type:
            params["objectType"] = object_type
        if min_sold_date:
            params["minSoldDate"] = min_sold_date
        if max_sold_date:
            params["maxSoldDate"] = max_sold_date
        return self._get("sold", params)

    def fetch_sold_all_pages(
        self,
        area: str | None = None,
        object_type: str | None = None,
        min_sold_date: str | None = None,
        max_sold_date: str | None = None,
        page_size: int = 500,
    ) -> list[dict[str, Any]]:
        """Fetch all pages of sold listings, handling pagination."""
        all_listings: list[dict[str, Any]] = []
        offset = 0
        while True:
            page = self.fetch_sold(
                area=area,
                object_type=object_type,
                min_sold_date=min_sold_date,
                max_sold_date=max_sold_date,
                offset=offset,
                limit=page_size,
            )
            listings = page.get("sold", [])
            all_listings.extend(listings)
            total = page.get("totalCount", 0)
            offset += page_size
            if offset >= total or not listings:
                break
        return all_listings
