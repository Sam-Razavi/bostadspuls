"""Regional comparison endpoints: /regions and /regions/{code}"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..bigquery import marts_table, query

router = APIRouter()


class RegionSummary(BaseModel):
    county: str
    region_code: str | None
    total_sales: int
    avg_sold_price_sek: float | None
    avg_price_per_sqm: float | None
    median_sold_price_sek: float | None
    avg_living_area_sqm: float | None
    price_per_sqm_rank: int
    sales_volume_rank: int


@router.get("", response_model=list[RegionSummary])
def get_regions() -> list[RegionSummary]:
    sql = f"""
        SELECT
            county,
            region_code,
            total_sales,
            avg_sold_price_sek,
            avg_price_per_sqm,
            median_sold_price_sek,
            avg_living_area_sqm,
            price_per_sqm_rank,
            sales_volume_rank
        FROM {marts_table('mart_regional_comparison')}
        ORDER BY price_per_sqm_rank
    """
    rows = query(sql)
    return [RegionSummary(**r) for r in rows]


@router.get("/{region_code}", response_model=RegionSummary)
def get_region(region_code: str) -> RegionSummary:
    safe_code = region_code.replace("'", "''")
    sql = f"""
        SELECT
            county,
            region_code,
            total_sales,
            avg_sold_price_sek,
            avg_price_per_sqm,
            median_sold_price_sek,
            avg_living_area_sqm,
            price_per_sqm_rank,
            sales_volume_rank
        FROM {marts_table('mart_regional_comparison')}
        WHERE region_code = '{safe_code}'
        LIMIT 1
    """
    rows = query(sql)
    if not rows:
        raise HTTPException(status_code=404, detail=f"Region '{region_code}' not found")
    return RegionSummary(**rows[0])
