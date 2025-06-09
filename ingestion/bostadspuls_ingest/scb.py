"""SCB (Statistics Sweden) PxWeb API client.

Fetches housing price index and sales volume data by region/municipality.
API docs: https://www.scb.se/en/services/statistical-programs-for-px-files/px-web/
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import polars as pl

from .config import SCB_BASE_URL

# SCB table paths for housing statistics
SCB_TABLES = {
    "price_index": "BO/BO0501/BO0501A/FastpiPSRegionKv",
    "sales_volume": "BO/BO0501/BO0501C/ForsBidrKv",
}

# Mapping from SCB region code prefixes to ISO-3166-2 style codes
_REGION_PREFIX_MAP: dict[str, str] = {
    "01": "SE-AB",
    "03": "SE-C",
    "04": "SE-D",
    "05": "SE-E",
    "06": "SE-F",
    "07": "SE-G",
    "08": "SE-H",
    "09": "SE-I",
    "10": "SE-K",
    "12": "SE-M",
    "13": "SE-N",
    "14": "SE-O",
    "17": "SE-S",
    "18": "SE-T",
    "19": "SE-U",
    "20": "SE-W",
    "21": "SE-X",
    "22": "SE-Y",
    "23": "SE-Z",
    "24": "SE-AC",
    "25": "SE-BD",
}


class SCBClient:
    """Async HTTP client for the SCB PxWeb API."""

    def __init__(self, base_url: str = SCB_BASE_URL, timeout: float = 30.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    async def fetch_table(
        self,
        table_path: str,
        query: dict[str, Any],
    ) -> dict[str, Any]:
        """POST a PxWeb query and return the JSON response."""
        url = f"{self._base_url}/{table_path}"
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.post(
                url,
                content=json.dumps(query),
                headers={"Content-Type": "application/json"},
            )
            resp.raise_for_status()
            return resp.json()

    async def fetch_price_index(
        self,
        regions: list[str] | None = None,
        quarters: list[str] | None = None,
    ) -> dict[str, Any]:
        """Fetch quarterly housing price index data."""
        query = _build_query(
            variables={
                "Region": regions or ["*"],
                "ContentsCode": ["FastpiPSRegionKv"],
                "Tid": quarters or ["*"],
            }
        )
        return await self.fetch_table(SCB_TABLES["price_index"], query)

    async def fetch_sales_volume(
        self,
        regions: list[str] | None = None,
        quarters: list[str] | None = None,
    ) -> dict[str, Any]:
        """Fetch quarterly residential sales volume data."""
        query = _build_query(
            variables={
                "Region": regions or ["*"],
                "ContentsCode": ["ForsBidrKv"],
                "Tid": quarters or ["*"],
            }
        )
        return await self.fetch_table(SCB_TABLES["sales_volume"], query)


def _build_query(variables: dict[str, list[str]]) -> dict[str, Any]:
    """Build a PxWeb selection query payload."""
    return {
        "query": [
            {
                "code": code,
                "selection": {
                    "filter": "all" if values == ["*"] else "item",
                    "values": values if values != ["*"] else ["*"],
                },
            }
            for code, values in variables.items()
        ],
        "response": {"format": "json"},
    }


def parse_scb_response(data: dict[str, Any]) -> pl.DataFrame:
    """Parse a PxWeb JSON response into a Polars DataFrame.

    PxWeb returns data in a column-store format:
      data[].key   — dimension values (list)
      data[].values — metric values (list of strings)
    columns[] — column metadata with code and text labels.
    """
    columns_meta: list[dict[str, Any]] = data.get("columns", [])
    rows: list[dict[str, Any]] = data.get("data", [])

    if not rows:
        return pl.DataFrame()

    dim_cols = [c["code"] for c in columns_meta if c.get("type") != "d"]
    val_cols = [c["code"] for c in columns_meta if c.get("type") == "d"]

    n_dims = len(dim_cols)

    records: list[dict[str, Any]] = []
    for row in rows:
        keys: list[str] = row.get("key", [])
        values: list[str] = row.get("values", [])
        record: dict[str, Any] = dict(zip(dim_cols, keys[:n_dims]))
        for col, val in zip(val_cols, values):
            try:
                record[col] = float(val) if val not in (".", "..", "...") else None
            except ValueError:
                record[col] = None
        records.append(record)

    df = pl.DataFrame(records)
    return normalize_region_codes(df)


def normalize_region_codes(df: pl.DataFrame) -> pl.DataFrame:
    """Add a standardized `region_code` column derived from the SCB Region code."""
    if "Region" not in df.columns:
        return df

    mapping_df = pl.DataFrame(
        {
            "prefix": list(_REGION_PREFIX_MAP.keys()),
            "region_code": list(_REGION_PREFIX_MAP.values()),
        }
    )

    result = (
        df.with_columns(pl.col("Region").str.slice(0, 2).alias("prefix"))
        .join(mapping_df, on="prefix", how="left")
        .drop("prefix")
    )
    return result
