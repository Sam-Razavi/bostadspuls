"""Year-over-year comparison endpoint: /compare"""

from __future__ import annotations

from fastapi import APIRouter, Query
from pydantic import BaseModel

from ..bigquery import marts_table, query

router = APIRouter()


class YoYPoint(BaseModel):
    county: str
    region_code: str | None
    period_start: str
    period_type: str
    sales_count: int
    avg_price_per_sqm: float | None
    prior_year_avg_price_per_sqm: float | None
    yoy_pct_change: float | None


@router.get("", response_model=list[YoYPoint])
def get_compare(
    county: str | None = Query(None, description="Filter by county name"),
    period_type: str = Query("month", description="'month' or 'quarter'"),
    limit: int = Query(120, ge=1, le=1000),
) -> list[YoYPoint]:
    where_clauses = [f"period_type = '{period_type}'"]
    if county:
        safe_county = county.replace("'", "''")
        where_clauses.append(f"county = '{safe_county}'")

    where = " AND ".join(where_clauses)
    sql = f"""
        SELECT
            county,
            region_code,
            cast(period_start as string) as period_start,
            period_type,
            sales_count,
            avg_price_per_sqm,
            prior_year_avg_price_per_sqm,
            yoy_pct_change
        FROM {marts_table('mart_yoy_comparison')}
        WHERE {where}
        ORDER BY period_start DESC, county
        LIMIT {limit}
    """
    rows = query(sql)
    return [YoYPoint(**r) for r in rows]
