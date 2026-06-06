"""SCB (Statistics Sweden) PxWeb API client.

Fetches housing price index and sales volume data by region/municipality.
API docs: https://www.scb.se/en/services/statistical-programs-for-px-files/px-web/
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import polars as pl
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from .config import SCB_BASE_URL
from .regions import add_region_code

# SCB table paths for housing statistics
SCB_TABLES = {
    "price_index": "BO/BO0501/BO0501A/FastpiPSRegionKv",
    "sales_volume": "BO/BO0501/BO0501C/ForsBidrKv",
}


class SCBClient:
    """Async HTTP client for the SCB PxWeb API."""

    def __init__(self, base_url: str = SCB_BASE_URL, timeout: float = 30.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    @retry(
        retry=retry_if_exception_type((httpx.TransportError, httpx.HTTPStatusError)),
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        reraise=True,
    )
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


def parse_price_index(data: dict[str, Any]) -> pl.DataFrame:
    """Parse a price-index PxWeb response into a typed Polars DataFrame.

    Returns columns: Region, quarter (YYYY-Qn), region_code, price_index (Float64).
    """
    df = parse_scb_response(data)
    if df.is_empty():
        return df

    value_col = next((c for c in df.columns if c not in ("Region", "Tid", "region_code")), None)
    if value_col is None:
        return df

    return (
        df.rename({"Tid": "quarter", value_col: "price_index"})
        .with_columns(pl.col("price_index").cast(pl.Float64))
        .select(["Region", "quarter", "region_code", "price_index"])
    )


def parse_sales_volume(data: dict[str, Any]) -> pl.DataFrame:
    """Parse a sales-volume PxWeb response into a typed Polars DataFrame.

    Returns columns: Region, quarter (YYYY-Qn), region_code, sales_count (Int64).
    """
    df = parse_scb_response(data)
    if df.is_empty():
        return df

    value_col = next((c for c in df.columns if c not in ("Region", "Tid", "region_code")), None)
    if value_col is None:
        return df

    return (
        df.rename({"Tid": "quarter", value_col: "sales_count"})
        .with_columns(pl.col("sales_count").cast(pl.Float64).cast(pl.Int64, strict=False))
        .select(["Region", "quarter", "region_code", "sales_count"])
    )


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

    df = pl.DataFrame(records, schema_overrides={"Region": pl.String})
    return add_region_code(df, region_col="Region")
